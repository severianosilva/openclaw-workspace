#!/bin/bash

# Script de integração para processar arquivos de áudio recebidos via WhatsApp
# Este script pode ser chamado automaticamente quando um novo arquivo de áudio é recebido
# ATUALIZADO: Usa versão otimizada de transcrição de áudio com múltiplos métodos (Vosk -> Whisper -> Google STT)

CAMINHO_BASE="/home/severosa/.openclaw/media/inbound"
CAMINHO_SAIDA="/home/severosa/organizacao/captura/transcricoes"

# Criar diretório de saída se não existir
mkdir -p "$CAMINHO_SAIDA"

echo "Verificando novos arquivos de áudio em $CAMINHO_BASE..."

# Encontrar arquivos de áudio mais recentes (últimas 24 horas)
find "$CAMINHO_BASE" -type f \( -iname "*.mp3" -o -iname "*.wav" -o -iname "*.m4a" -o -iname "*.aac" -o -iname "*.ogg" -o -iname "*.flac" -o -iname "*.opus" \) -mtime -1 | while read -r arquivo_audio; do
    nome_arquivo=$(basename "$arquivo_audio")
    caminho_saida="$CAMINHO_SAIDA/${nome_arquivo%.*}.txt"
    
    echo "Processando áudio: $nome_arquivo"
    
    # Verificar se já existe transcrição para este arquivo
    if [ ! -f "$caminho_saida" ]; then
        echo "Gerando transcrição otimizada para: $nome_arquivo"
        
        # Executar o script Python com versão otimizada (usa PyAV para conversão e múltiplos métodos de transcrição)
        python3 /home/severosa/organizacao/captura/transcricao_qwen_ajudada.py "$arquivo_audio"
        
        # Após a transcrição, mover o arquivo original para pasta de processados
        mkdir -p "$CAMINHO_SAIDA/audios_processados"
        mv "$arquivo_audio" "$CAMINHO_SAIDA/audios_processados/"
    else
        echo "Transcrição já existe para: $nome_arquivo"
    fi
done

echo "Verificação de áudio concluída."