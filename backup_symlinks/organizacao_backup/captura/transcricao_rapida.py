#!/usr/bin/env python3
"""
Script rápido para transcrição de áudio usando Google STT
"""

import sys
import os
import speech_recognition as sr
from pydub import AudioSegment
import subprocess

def converter_audio(input_file, output_file):
    """Converte áudio para WAV usando ffmpeg"""
    try:
        subprocess.run([
            'ffmpeg', '-y', '-i', input_file,
            '-ar', '16000', '-ac', '1', '-sample_fmt', 's16',
            output_file
        ], check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"Erro na conversão: {e}")
        return False

def transcrever_google(audio_file):
    """Transcreve usando Google STT"""
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        
        print("Enviando para Google STT...")
        text = recognizer.recognize_google(audio, language='pt-BR')
        return text
    except sr.UnknownValueError:
        return "Não foi possível entender o áudio"
    except sr.RequestError as e:
        return f"Erro no serviço: {e}"

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 transcricao_rapida.py <arquivo_audio>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"Arquivo não encontrado: {input_file}")
        sys.exit(1)
    
    print(f"Processando: {input_file}")
    
    # Converter para WAV
    wav_file = input_file.replace('.ogg', '.wav').replace('.mp3', '.wav')
    if input_file == wav_file:
        wav_file = input_file + '.wav'
    
    print("Convertendo para WAV...")
    if not converter_audio(input_file, wav_file):
        sys.exit(1)
    
    print(f"Arquivo convertido: {wav_file}")
    
    # Verificar tamanho do arquivo
    file_size = os.path.getsize(wav_file)
    print(f"Tamanho do arquivo WAV: {file_size} bytes")
    
    if file_size < 1000:
        print("⚠️  Arquivo muito pequeno - pode não conter áudio significativo")
    
    # Transcrever
    print("\nIniciando transcrição...")
    resultado = transcrever_google(wav_file)
    
    print("\n" + "="*50)
    print("RESULTADO DA TRANSCRIÇÃO:")
    print("="*50)
    print(resultado)
    print("="*50)
    
    # Salvar resultado
    output_txt = input_file + '.transcricao.txt'
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(resultado)
    
    print(f"\nTranscrição salva em: {output_txt}")

if __name__ == '__main__':
    main()
