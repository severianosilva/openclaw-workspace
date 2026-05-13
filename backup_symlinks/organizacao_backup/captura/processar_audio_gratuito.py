#!/usr/bin/env python3
"""
Script alternativo para processar arquivos de áudio recebidos via WhatsApp
usando serviços de transcrição gratuitos
"""

import os
import sys
from pathlib import Path
import subprocess
from datetime import datetime

def verificar_ffmpeg():
    """Verifica se o ffmpeg está disponível"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def converter_para_wav(caminho_entrada, caminho_saida):
    """Converte arquivo de áudio para WAV usando ffmpeg"""
    try:
        subprocess.run([
            'ffmpeg', '-i', caminho_entrada, 
            '-acodec', 'pcm_s16le', 
            '-ar', '16000', 
            '-ac', '1', 
            '-y',  # Sobrescrever se necessário
            caminho_saida
        ], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def transcrever_com_google_stt_wit_ai(caminho_arquivo):
    """
    Função alternativa que utiliza o serviço Wit.ai (proprietário mas com uso gratuito limitado)
    ou Google STT offline
    """
    try:
        # Tenta usar o SpeechRecognition se estiver disponível
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        
        # Carregar o arquivo de áudio
        with sr.AudioFile(caminho_arquivo) as source:
            audio_data = recognizer.record(source)
            
            # Tentar transcrever usando o serviço gratuito do Google
            try:
                text = recognizer.recognize_google(audio_data, language="pt-BR")
                return text
            except sr.RequestError:
                # Se o serviço online falhar, retornar mensagem
                return "Serviço de transcrição online indisponível ou limite excedido"
            except sr.UnknownValueError:
                return "Não foi possível entender o áudio"
                
    except ImportError:
        # Se SpeechRecognition não estiver disponível, usar abordagem alternativa
        return "Biblioteca SpeechRecognition não disponível. Instale com: pip install SpeechRecognition"

def transcrever_audio_alternativo(caminho_arquivo):
    """
    Processa um arquivo de áudio usando métodos alternativos gratuitos
    """
    # Verificar se o arquivo existe
    if not Path(caminho_arquivo).exists():
        return "Arquivo de áudio não encontrado"
    
    # Verificar se o ffmpeg está disponível
    if not verificar_ffmpeg():
        return "FFmpeg não encontrado. Instale o ffmpeg para processar arquivos de áudio"
    
    # Converter para WAV com formato compatível
    caminho_temp = Path(caminho_arquivo).with_suffix('.temp.wav')
    
    if converter_para_wav(caminho_arquivo, str(caminho_temp)):
        # Tentar transcrever o arquivo convertido
        resultado = transcrever_com_google_stt_wit_ai(str(caminho_temp))
        
        # Remover arquivo temporário
        if caminho_temp.exists():
            caminho_temp.unlink()
        
        return resultado
    else:
        return "Falha na conversão do arquivo de áudio"

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
    Função principal para processar arquivos de áudio com métodos gratuitos
    """
    print("Processando arquivos de áudio com serviços gratuitos...")
    
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
        
        # Tentar transcrever o áudio usando métodos gratuitos
        resultado = transcrever_audio_alternativo(str(arquivo_recente))
        
        print(f"Resultado da transcrição:\n{resultado}")
        
        # Salvar transcrição em arquivo
        nome_saida = arquivo_recente.with_suffix('.txt')
        with open(nome_saida, 'w', encoding='utf-8') as f:
            f.write(f"Transcrição do áudio: {arquivo_recente.name}\n")
            f.write(f"Método: Serviço gratuito (Google STT)\n")
            f.write(f"Data: {datetime.now()}\n")
            f.write("-" * 50 + "\n")
            f.write(resultado)
        
        print(f"Transcrição salva em: {nome_saida}")

if __name__ == "__main__":
    main()