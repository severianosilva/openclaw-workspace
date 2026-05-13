#!/usr/bin/env python3
"""
Script otimizado para transcrição de áudio em português
Combina várias técnicas para maximizar a chance de sucesso
"""

import os
import sys
from pathlib import Path
import subprocess
from datetime import datetime

def converter_para_wav_pydub(caminho_entrada, caminho_saida):
    """Converte arquivo de áudio para WAV usando pydub como fallback"""
    try:
        from pydub import AudioSegment
        import os
        
        # Determinar o formato de entrada a partir da extensão
        formato_entrada = Path(caminho_entrada).suffix.lower().lstrip('.')
        
        # Carregar o áudio com pydub
        audio = AudioSegment.from_file(caminho_entrada, format=formato_entrada)
        
        # Converter para WAV com as configurações apropriadas
        audio = audio.set_frame_rate(16000).set_channels(1)
        
        # Exportar como WAV
        audio.export(caminho_saida, format="wav")
        
        return True
    except ImportError:
        print("AVISO: pydub não está instalado. Instale com: pip install pydub")
        return False
    except Exception as e:
        print(f"AVISO: Erro ao converter áudio com pydub: {str(e)}")
        return False

def converter_para_wav_pyav(caminho_entrada, caminho_saida):
    """Converte arquivo de áudio para WAV usando PyAV como fallback"""
    try:
        import av
        import numpy as np
        
        # Abrir o arquivo de áudio com PyAV
        container = av.open(caminho_entrada)
        
        # Encontrar o stream de áudio
        audio_stream = None
        for stream in container.streams.audio:
            audio_stream = stream
            break
        
        if audio_stream is None:
            print("AVISO: Nenhum stream de áudio encontrado no arquivo")
            return False
        
        # Configurar o samplerate alvo
        target_sample_rate = 16000
        target_channels = 1
        
        # Coletar os dados de áudio
        audio_samples = []
        
        for frame in container.decode(audio=0):
            # Converter o frame para array numpy
            samples = frame.to_ndarray()
            
            # Converter para 16-bit PCM
            if samples.dtype == np.float32:
                samples = (samples * 32767).astype(np.int16)
            elif samples.dtype == np.int32:
                samples = (samples / 2**16).astype(np.int16)
            
            # Se tiver mais de um canal, converter para mono
            if len(samples.shape) > 1 and samples.shape[1] > 1:
                samples = samples.mean(axis=1).astype(np.int16)
            
            audio_samples.extend(samples.tolist())
        
        container.close()
        
        # Salvar como arquivo WAV
        import wave
        with wave.open(caminho_saida, 'wb') as wav_file:
            wav_file.setnchannels(target_channels)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(target_sample_rate)
            wav_file.writeframes(np.array(audio_samples, dtype=np.int16).tobytes())
        
        return True
    except ImportError:
        print("AVISO: PyAV ou numpy não estão instalados. Instale com: pip install av numpy")
        return False
    except Exception as e:
        print(f"AVISO: Erro ao converter áudio com PyAV: {str(e)}")
        return False

def transcrever_google_stt(caminho_arquivo_wav):
    """Tenta transcrever usando Google STT via SpeechRecognition"""
    try:
        import speech_recognition as sr
        
        r = sr.Recognizer()
        
        with sr.AudioFile(caminho_arquivo_wav) as source:
            audio = r.record(source)
            
            # Tentar transcrever usando o serviço gratuito do Google em português
            text = r.recognize_google(audio, language="pt-BR")
            return text
            
    except ImportError:
        return "SpeechRecognition não está instalado"
    except sr.UnknownValueError:
        return "Google STT: Não foi possível entender o áudio"
    except sr.RequestError as e:
        return f"Google STT: Erro de requisição - {str(e)}"
    except Exception as e:
        return f"Google STT: Erro geral - {str(e)}"

def tentar_transcricao_whisper_local(caminho_arquivo_wav):
    """Tenta transcrever usando Whisper local se disponível"""
    try:
        # Primeiro tentar com faster-whisper
        from faster_whisper import WhisperModel
        
        print("Usando faster-whisper...")
        model = WhisperModel("tiny", device="cpu", compute_type="int8")
        segments, info = model.transcribe(caminho_arquivo_wav, language="pt")
        
        text = " ".join([segment.text for segment in segments])
        return text.strip()
        
    except ImportError:
        try:
            # Tentar com o whisper padrão
            import whisper
            import torch
            
            print("Usando whisper padrão...")
            model = whisper.load_model("tiny", device="cpu")
            result = model.transcribe(caminho_arquivo_wav, language="pt")
            
            return result["text"].strip()
            
        except ImportError:
            return None  # Não disponível
        except Exception as e:
            print(f"Whisper falhou: {str(e)}")
            return None
    except Exception as e:
        print(f"Faster-whisper falhou: {str(e)}")
        return None

def transcrever_audio_otimizado(caminho_arquivo):
    """
    Função principal que tenta múltiplas abordagens para transcrever áudio
    """
    print(f"Tentando transcrição otimizada de: {caminho_arquivo}")
    
    # Verificar se o arquivo existe
    if not Path(caminho_arquivo).exists():
        return "Arquivo de áudio não encontrado"
    
    # Caminho para o arquivo temporário WAV
    caminho_temp_wav = Path(caminho_arquivo).with_suffix('.temp.wav')
    
    # Converter o arquivo para WAV se necessário
    if Path(caminho_arquivo).suffix.lower() != '.wav':
        print("Convertendo arquivo de áudio para WAV...")
        
        # Tentar converter usando PyAV primeiro (melhor qualidade)
        if converter_para_wav_pyav(caminho_arquivo, str(caminho_temp_wav)):
            caminho_para_usar = str(caminho_temp_wav)
            print("Conversão com PyAV bem-sucedida!")
        elif converter_para_wav_pydub(caminho_arquivo, str(caminho_temp_wav)):
            caminho_para_usar = str(caminho_temp_wav)
            print("Conversão com pydub bem-sucedida!")
        else:
            print("Falha na conversão. Tentando diretamente com o arquivo original...")
            caminho_para_usar = caminho_arquivo
    else:
        caminho_para_usar = caminho_arquivo
    
    # Tentar transcrição com Whisper local primeiro (mais preciso)
    print("Tentando transcrição com Whisper local...")
    resultado = tentar_transcricao_whisper_local(caminho_para_usar)
    
    if resultado is not None and resultado.strip():
        print("Transcrição bem-sucedida com Whisper!")
    else:
        # Se Whisper falhar, tentar com Google STT
        print("Whisper não disponível ou falhou. Tentando com Google STT...")
        resultado = transcrever_google_stt(caminho_para_usar)
    
    # Remover arquivo temporário se existir
    if caminho_temp_wav.exists() and caminho_para_usar == str(caminho_temp_wav):
        caminho_temp_wav.unlink()
    
    return resultado

def main(caminho_arquivo=None):
    """
    Função principal para uso direto do script
    """
    print("Sistema de Transcrição de Áudio Otimizado para Português")
    print("=" * 55)
    
    if caminho_arquivo is None:
        # Procurar arquivos de áudio no diretório padrão
        diretorio_inbound = Path("/home/severosa/.openclaw/media/inbound")
        arquivos_audio = []
        
        if diretorio_inbound.exists():
            extensoes = ['.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac', '.opus']
            for ext in extensoes:
                arquivos_audio.extend(list(diretorio_inbound.rglob(f"*{ext}")))
            
            if arquivos_audio:
                # Pegar o mais recente
                arquivo_recente = sorted(arquivos_audio, key=lambda x: x.stat().st_mtime, reverse=True)[0]
                caminho_arquivo = str(arquivo_recente)
                print(f"Processando arquivo mais recente: {caminho_arquivo}")
            else:
                print("Nenhum arquivo de áudio encontrado no diretório inbound")
                return
        else:
            print("Diretório de entrada não encontrado")
            return
    
    # Tentar transcrever o arquivo
    resultado = transcrever_audio_otimizado(caminho_arquivo)
    
    print(f"\nResultado da transcrição:")
    print("-" * 30)
    print(resultado)
    
    # Salvar resultado
    caminho_saida = Path(caminho_arquivo).with_suffix('.transcricao_otimizada.txt')
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.write(f"Transcrição otimizada do arquivo: {Path(caminho_arquivo).name}\n")
        f.write(f"Método: Combinação de Whisper local e Google STT\n")
        f.write(f"Data: {datetime.now()}\n")
        f.write("-" * 50 + "\n")
        f.write(resultado)
    
    print(f"\nTranscrição salva em: {caminho_saida}")
    
    return resultado

if __name__ == "__main__":
    # Aceitar caminho do arquivo como argumento opcional
    caminho_arquivo = sys.argv[1] if len(sys.argv) > 1 else None
    main(caminho_arquivo)