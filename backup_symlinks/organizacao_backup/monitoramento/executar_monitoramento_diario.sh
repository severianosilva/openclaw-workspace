#!/bin/bash

# Script para executar o monitoramento diário de processos
# Este script será executado diariamente pelo cron job

echo "==========================================="
echo "INICIANDO MONITORAMENTO DIÁRIO - $(date)"
echo "==========================================="

# Diretório base
BASE_DIR="$HOME/organizacao/monitoramento"
RELATORIOS_DIR="$BASE_DIR/relatorios-diarios"

# Criar diretório de relatórios se não existir
mkdir -p "$RELATORIOS_DIR"

# Data atual para nome do relatório
DATA_ATUAL=$(date +%Y-%m-%d)
ARQUIVO_RELATORIO="$RELATORIOS_DIR/relatorio_$DATA_ATUAL.txt"

# Iniciar relatório
echo "Relatório de Monitoramento - $DATA_ATUAL" > "$ARQUIVO_RELATORIO"
echo "======================================" >> "$ARQUIVO_RELATORIO"
echo "" >> "$ARQUIVO_RELATORIO"

echo "1. Verificando Diário Oficial de Minas Gerais..."
echo "- Executando verificação do Diário Oficial..." >> "$ARQUIVO_RELATORIO"
python3 "$BASE_DIR/modelo_verificar_diario_mg.py" 2>&1 | tee -a "$ARQUIVO_RELATORIO"
echo "" >> "$ARQUIVO_RELATORIO"

echo "2. Verificando e-mails relevantes (Gmail)..."
echo "- Executando verificação de e-mails..." >> "$ARQUIVO_RELATORIO"
python3 "$BASE_DIR/modelo_verificar_emails.py" 2>&1 | tee -a "$ARQUIVO_RELATORIO"
echo "" >> "$ARQUIVO_RELATORIO"

echo "3. Verificando Google Drive..."
echo "- Executando verificação do Google Drive..." >> "$ARQUIVO_RELATORIO"
python3 "$BASE_DIR/modelo_verificar_google_drive.py" 2>&1 | tee -a "$ARQUIVO_RELATORIO"
echo "" >> "$ARQUIVO_RELATORIO"

echo "4. Verificando OneDrive..."
echo "- Executando verificação do OneDrive..." >> "$ARQUIVO_RELATORIO"
python3 "$BASE_DIR/modelo_verificar_onedrive.py" 2>&1 | tee -a "$ARQUIVO_RELATORIO"
echo "" >> "$ARQUIVO_RELATORIO"

echo "5. Verificando Dropbox..."
echo "- Executando verificação do Dropbox..." >> "$ARQUIVO_RELATORIO"
python3 "$BASE_DIR/modelo_verificar_dropbox.py" 2>&1 | tee -a "$ARQUIVO_RELATORIO"
echo "" >> "$ARQUIVO_RELATORIO"

echo "6. Processando arquivos de áudio recebidos via WhatsApp..."
echo "- Executando verificação e transcrição de áudios recebidos..." >> "$ARQUIVO_RELATORIO"
bash "$HOME/organizacao/captura/integracao_audio_whatsapp.sh" 2>&1 | tee -a "$ARQUIVO_RELATORIO"
echo "" >> "$ARQUIVO_RELATORIO"

echo "7. Atualizando controles de processos..."
echo "- Verificando atualizações pendentes nos controles de processos..." >> "$ARQUIVO_RELATORIO"
echo "Nenhuma atualização automática realizada (aguardando integração completa)" >> "$ARQUIVO_RELATORIO"
echo "" >> "$ARQUIVO_RELATORIO"

echo "Monitoramento diário concluído em $(date)" >> "$ARQUIVO_RELATORIO"

echo ""
echo "Relatório salvo em: $ARQUIVO_RELATORIO"
echo "==========================================="
echo "NOTA: Este script contém modelos que precisam de credenciais para funcionar completamente."

# Atualizar os controles de processos com base nas verificações (quando implementado)
echo "Próxima etapa: Integrar dados de todas as fontes aos controles de processos individuais"

# Enviar relatório automaticamente por WhatsApp
echo "Enviando relatório por WhatsApp..."
"$BASE_DIR/enviar_relatorio_diario.sh"