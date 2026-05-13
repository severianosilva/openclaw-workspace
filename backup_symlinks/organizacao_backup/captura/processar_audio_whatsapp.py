#!/usr/bin/env python3
"""
Script para processar arquivos de áudio recebidos via WhatsApp
usando a API de transcrição do OpenAI Whisper
"""

import os
import sys
import json
from pathlib import Path
import base64
from datetime import datetime

def transcrever_audio_whatsapp(caminho_arquivo, api_key=None):
    """
    Processa um arquivo de áudio recebido via WhatsApp e retorna sua transcrição
    """
    try:
        # Importar o cliente OpenAI apenas quando necessário
        from openai import OpenAI
        
        # Usar a API key do ambiente ou passada como parâmetro
        client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        
        # Abrir o arquivo de áudio
        with open(caminho_arquivo, 'rb') as audio_file:
            # Fazer a transcrição usando o modelo whisper
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        
        return transcription.text
    
    except ImportError:
        print("Erro: OpenAI SDK não encontrado. Execute 'pip install openai'")
        return None
    except Exception as e:
        print(f"Erro ao transcrever áudio: {str(e)}")
        return None

def encontrar_arquivos_audio(diretorio_base="/home/severosa/.openclaw/media/inbound"):
    """
    Encontra arquivos de áudio recentes recebidos via WhatsApp
    """
    diretorio = Path(diretorio_base)
    
    if not diretorio.exists():
        print(f"Diretório {diretorio_base} não encontrado")
        return []
    
    # Extensões comuns de áudio
    extensoes_audio = ['.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac', '.opus']
    
    arquivos_audio = []
    for ext in extensoes_audio:
        arquivos_audio.extend(list(diretorio.rglob(f"*{ext}")))
    
    # Ordenar por data de modificação (mais recentes primeiro)
    arquivos_audio.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    return arquivos_audio

def main():
    """
    Função principal para processar arquivos de áudio
    """
    print("Processando arquivos de áudio recebidos via WhatsApp...")
    
    # Obter arquivos de áudio
    arquivos_audio = encontrar_arquivos_audio()
    
    if not arquivos_audio:
        print("Nenhum arquivo de áudio encontrado.")
        return
    
    print(f"Encontrados {len(arquivos_audio)} arquivos de áudio:")
    for i, arquivo in enumerate(arquivos_audio[:5]):  # Mostrar apenas os 5 mais recentes
        print(f"{i+1}. {arquivo.name} ({datetime.fromtimestamp(arquivo.stat().st_mtime)})")
    
    # Processar o arquivo mais recente
    if arquivos_audio:
        arquivo_recente = arquivos_audio[0]
        print(f"\nProcessando: {arquivo_recente}")
        
        # Tentar transcrever o áudio
        resultado = transcrever_audio_whatsapp(str(arquivo_recente))
        
        if resultado:
            print(f"Transcrição concluída:\n{resultado}")
            
            # Salvar transcrição em arquivo
            nome_saida = arquivo_recente.with_suffix('.txt')
            with open(nome_saida, 'w', encoding='utf-8') as f:
                f.write(f"Transcrição do áudio: {arquivo_recente.name}\n")
                f.write(f"Data: {datetime.now()}\n")
                f.write("-" * 50 + "\n")
                f.write(resultado)
            
            print(f"Transcrição salva em: {nome_saida}")
        else:
            print("Falha na transcrição do áudio.")

if __name__ == "__main__":
    main()