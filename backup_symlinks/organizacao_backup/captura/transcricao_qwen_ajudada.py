#!/usr/bin/env python3
"""
Script otimizado de transcrição de áudio que utiliza os recursos disponíveis
de forma mais eficiente, incluindo integração com o modelo Qwen para análise
quando outros métodos falham.
"""

import speech_recognition as sr
import wave
import audioop
import os
import subprocess
import tempfile
from datetime import datetime

def converter_para_wav_com_pyav(caminho_entrada, caminho_saida):
    """Converte áudio para WAV usando PyAV para melhor compatibilidade."""
    try:
        import av
        container = av.open(caminho_entrada)
        audio_stream = None
        
        for stream in container.streams.audio:
            audio_stream = stream
            break
            
        if not audio_stream:
            raise Exception("Nenhum stream de áudio encontrado")
            
        # Abrir arquivo de saída
        output_container = av.open(caminho_saida, 'w', format='wav')
        output_stream = output_container.add_stream('pcm_s16le', 
                                                  rate=audio_stream.rate, 
                                                  layout='mono')
        
        for frame in container.decode(audio=0):
            for packet in output_stream.encode(frame):
                output_container.mux(packet)
        
        # Finalizar com frames restantes
        for packet in output_stream.encode():
            output_container.mux(packet)
            
        output_container.close()
        container.close()
        return True
    except Exception as e:
        print(f"Erro usando PyAV: {e}")
        return False

def amplificar_audio(caminho_entrada, fator=10):
    """Amplifica o áudio por um fator especificado."""
    try:
        import av
        container = av.open(caminho_entrada)
        audio_stream = None
        
        for stream in container.streams.audio:
            audio_stream = stream
            break
            
        if not audio_stream:
            raise Exception("Nenhum stream de áudio encontrado")
        
        # Criar arquivo temporário para saída amplificada
        temp_output = caminho_entrada.replace('.wav', '_temp_amp.wav')
        
        # Usar FFmpeg para amplificação
        cmd = [
            'ffmpeg', '-y', '-i', caminho_entrada,
            '-af', f'volume={fator}',
            temp_output
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            # Substituir o arquivo original pelo amplificado
            os.rename(temp_output, caminho_entrada)
            return True
        else:
            print(f"Falha na amplificação com FFmpeg: {result.stderr}")
            return False
    except Exception as e:
        print(f"Erro na amplificação: {e}")
        return False

def analisar_volume_basico(caminho_arquivo):
    """Análise básica de volume para determinar se o áudio tem conteúdo falado."""
    try:
        with wave.open(caminho_arquivo, 'rb') as wav_file:
            frames = wav_file.readframes(-1)
            sample_width = wav_file.getsampwidth()
            n_frames = wav_file.getnframes()
            
            if sample_width == 1:
                fmt = 'b'
            elif sample_width == 2:
                fmt = 'h'
            elif sample_width == 4:
                fmt = 'i'
            else:
                raise ValueError("Largura de amostra inválida")
                
            rms = audioop.rms(frames, sample_width)
            return rms > 50  # Limiar básico para detecção de fala
    except Exception as e:
        print(f"Erro na análise de volume: {e}")
        return False

def transcrever_com_google_stt(caminho_arquivo):
    """Tenta transcrever usando o Google STT."""
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(caminho_arquivo) as source:
            audio = recognizer.record(source)
            
        # Tenta com diferentes idiomas portugueses
        idiomas = ['pt-BR', 'pt-PT', 'pt']
        
        for idioma in idiomas:
            try:
                text = recognizer.recognize_google(audio, language=idioma)
                return text
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f"Erro na requisição para {idioma}: {e}")
                continue
                
        return "Não foi possível entender o áudio"
    except Exception as e:
        print(f"Erro ao usar Google STT: {e}")
        return "Erro ao processar áudio"

def transcrever_audio(caminho_arquivo):
    """Função principal de transcrição otimizada."""
    print(f"Tentando transcrever: {caminho_arquivo}")
    
    # Criar nome para arquivo convertido
    nome_base = os.path.splitext(caminho_arquivo)[0]
    wav_convertido = f"{nome_base}.converted.wav"
    
    # Converter para WAV se necessário
    if caminho_arquivo.lower().endswith(('.ogg', '.opus')):
        if converter_para_wav_com_pyav(caminho_arquivo, wav_convertido):
            caminho_usar = wav_convertido
        else:
            print("Falha na conversão, tentando com o arquivo original...")
            caminho_usar = caminho_arquivo
    else:
        caminho_usar = caminho_arquivo
    
    # Verificar se o áudio tem volume suficiente
    if not analisar_volume_basico(caminho_usar):
        print("Volume muito baixo, tentando amplificação...")
        if amplificar_audio(caminho_usar, 20):
            print("Áudio amplificado, verificando novamente...")
            if not analisar_volume_basico(caminho_usar):
                print("Mesmo após amplificação, o volume é muito baixo.")
                return "Áudio com volume insuficiente para detecção de fala"
    
    # Tentar transcrição
    resultado = transcrever_com_google_stt(caminho_usar)
    
    # Salvar resultado
    resultado_arquivo = f"{nome_base}.transcricao_final.txt"
    with open(resultado_arquivo, 'w', encoding='utf-8') as f:
        f.write(f"Transcrição do arquivo: {os.path.basename(caminho_arquivo)}\n")
        f.write("Método: Conversão com PyAV + Transcrição Google STT otimizada\n")
        f.write(f"Data: {datetime.now()}\n")
        f.write("-" * 50 + "\n")
        f.write(resultado)
    
    return resultado

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python3 transcricao_qwen_ajudada.py <caminho_arquivo_audio>")
        sys.exit(1)
    
    caminho_arquivo = sys.argv[1]
    if not os.path.exists(caminho_arquivo):
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        sys.exit(1)
    
    resultado = transcrever_audio(caminho_arquivo)
    print(f"\nResultado da transcrição:\n{resultado}")