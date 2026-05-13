#!/usr/bin/env python3
"""
Implementação alternativa de transcrição de áudio usando tecnologias open-source
como Whisper local ou outras alternativas gratuitas
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

def converter_para_wav_pydub(caminho_entrada, caminho_saida):
    """Converte arquivo de áudio para WAV usando pydub como fallback"""
    try:
        from pydub import AudioSegment
        import os
        
        # Determinar o formato de entrada a partir da extensão
        formato_entrada = Path(caminho_entrada).suffix.lower().lstrip('.')
        
        # Carregar o áudio com pydub
        audio = AudioSegment.from_file(caminho_entrada, format=formato_entrada)
        
        # Converter para WAV com as configurações apropriadas para SpeechRecognition
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

def converter_para_wav(caminho_entrada, caminho_saida):
    """Converte arquivo de áudio para WAV usando ffmpeg, PyAV ou pydub como fallback"""
    # Tentar primeiro com ffmpeg
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
        # Fallback para PyAV
        if converter_para_wav_pyav(caminho_entrada, caminho_saida):
            return True
        # Se PyAV falhar, tentar pydub
        return converter_para_wav_pydub(caminho_entrada, caminho_saida)

def verificar_dependencias():
    """Verifica se as dependências necessárias estão disponíveis"""
    dependencias = []
    
    # Verificar se o ffmpeg está disponível
    if verificar_ffmpeg():
        dependencias.append('ffmpeg')
    else:
        print("AVISO: ffmpeg não encontrado. Instale para melhor suporte de formatos de áudio.")
        print("Tentando usar pydub como fallback...")
    
    # Verificar se o Python tem módulos necessários
    try:
        import wave
        dependencias.append('wave')
    except ImportError:
        print("AVISO: módulo wave não disponível")
    
    try:
        import audioop
        dependencias.append('audioop')
    except ImportError:
        print("AVISO: módulo audioop não disponível")
    
    return dependencias

def transcrever_com_whisper_local(caminho_arquivo):
    """
    Tenta usar o Whisper local (se instalado) para transcrição
    """
    try:
        # Verificar se o comando whisper está disponível
        result = subprocess.run(['whisper', '--help'], capture_output=True, text=True)
        if result.returncode == 0:
            # Whisper CLI está instalado, tentar usar
            saida_temp = Path(caminho_arquivo).with_suffix('.transcricao.txt')
            subprocess.run([
                'whisper', 
                caminho_arquivo, 
                '--language', 'Portuguese',
                '--output_dir', str(Path(saida_temp).parent),
                '--output_format', 'txt'
            ])
            
            # Ler o resultado
            caminho_resultado = Path(caminho_arquivo).with_suffix('.txt')
            if caminho_resultado.exists():
                with open(caminho_resultado, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                # Remover arquivo temporário de texto gerado pelo whisper
                if caminho_resultado.exists():
                    caminho_resultado.unlink()
                return conteudo
            else:
                return "Falha ao ler o resultado do Whisper"
        else:
            return "Comando whisper não disponível"
    except FileNotFoundError:
        return "Whisper CLI não está instalado. Instale com: pip install openai-whisper"
    except Exception as e:
        return f"Erro ao usar Whisper local: {str(e)}"

def transcrever_com_vosk(caminho_arquivo):
    """
    Usa o Vosk (módulo de fala offline gratuito) para transcrição
    """
    try:
        import speech_recognition as sr
    except ImportError:
        return "Módulo speech_recognition não está instalado"
    
    try:
        # Usar o reconhecedor do Vosk
        r = sr.Recognizer()
        with sr.AudioFile(caminho_arquivo) as source:
            audio = r.record(source)
            # Tentar usar o Vosk se estiver configurado
            text = r.recognize_vosk(audio)
            import json
            result = json.loads(text)
            return result["text"]
    except sr.UnknownValueError:
        return "Vosk não pôde entender o áudio"
    except sr.RequestError as e:
        return f"Erro com Vosk: {str(e)}"
    except Exception as e:
        return f"Erro ao usar Vosk: {str(e)}"

def transcrever_audio_gratuito(caminho_arquivo):
    """
    Função principal para transcrição gratuita de áudio
    Tenta múltiplas abordagens em ordem de preferência
    """
    print(f"Tentando transcrição de: {caminho_arquivo}")
    
    # Verificar se o arquivo existe
    if not Path(caminho_arquivo).exists():
        return "Arquivo de áudio não encontrado"
    
    # Caminho para o arquivo temporário WAV
    caminho_temp_wav = Path(caminho_arquivo).with_suffix('.temp.wav')
    
    # Tentar converter o arquivo para WAV se necessário
    if not verificar_ffmpeg() and Path(caminho_arquivo).suffix.lower() != '.wav':
        print("Convertendo arquivo de áudio para WAV usando pydub...")
        if converter_para_wav_pydub(caminho_arquivo, str(caminho_temp_wav)):
            caminho_para_usar = str(caminho_temp_wav)
            print("Conversão bem-sucedida!")
        else:
            print("Falha na conversão. Tentando diretamente com o arquivo original...")
            caminho_para_usar = caminho_arquivo
    elif Path(caminho_arquivo).suffix.lower() != '.wav':
        print("Convertendo arquivo de áudio para WAV usando ffmpeg...")
        if converter_para_wav(caminho_arquivo, str(caminho_temp_wav)):
            caminho_para_usar = str(caminho_temp_wav)
            print("Conversão bem-sucedida!")
        else:
            print("Falha na conversão. Tentando diretamente com o arquivo original...")
            caminho_para_usar = caminho_arquivo
    else:
        caminho_para_usar = caminho_arquivo
    
    # Primeira tentativa: Whisper local (se disponível)
    print("Tentando com Whisper local...")
    resultado = transcrever_com_whisper_local(caminho_para_usar)
    if "não está instalado" not in resultado and "não disponível" not in resultado:
        # Remover arquivo temporário se existir
        if caminho_temp_wav.exists() and caminho_para_usar == str(caminho_temp_wav):
            caminho_temp_wav.unlink()
        return resultado
    
    # Segunda tentativa: Vosk (se configurado)
    print("Tentando com Vosk...")
    resultado = transcrever_com_vosk(caminho_para_usar)
    if "não está instalado" not in resultado and "não pôde entender" not in resultado:
        # Remover arquivo temporário se existir
        if caminho_temp_wav.exists() and caminho_para_usar == str(caminho_temp_wav):
            caminho_temp_wav.unlink()
        return resultado
    
    # Terceira tentativa: Google STT via SpeechRecognition (limite gratuito)
    print("Tentando com Google STT...")
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        
        # Usar o arquivo convertido ou original
        with sr.AudioFile(caminho_para_usar) as source:
            audio = r.record(source)
            # Limite gratuito do Google STT
            text = r.recognize_google(audio, language="pt-BR")
            
            # Remover arquivo temporário se existir
            if caminho_temp_wav.exists() and caminho_para_usar == str(caminho_temp_wav):
                caminho_temp_wav.unlink()
                
            return text
    except ImportError:
        # Remover arquivo temporário se existir
        if caminho_temp_wav.exists() and caminho_para_usar == str(caminho_temp_wav):
            caminho_temp_wav.unlink()
        return "Nenhum módulo de transcrição disponível. Instale com: pip install SpeechRecognition"
    except sr.UnknownValueError:
        # Remover arquivo temporário se existir
        if caminho_temp_wav.exists() and caminho_para_usar == str(caminho_temp_wav):
            caminho_temp_wav.unlink()
        return "Não foi possível entender o áudio com os serviços disponíveis"
    except sr.RequestError as e:
        # Remover arquivo temporário se existir
        if caminho_temp_wav.exists() and caminho_para_usar == str(caminho_temp_wav):
            caminho_temp_wav.unlink()
        return f"Erro de requisição: {str(e)}. Pode ser falta de conexão ou limite excedido."
    except Exception as e:
        # Remover arquivo temporário se existir
        if caminho_temp_wav.exists() and caminho_para_usar == str(caminho_temp_wav):
            caminho_temp_wav.unlink()
        return f"Erro geral: {str(e)}"

def main(caminho_arquivo=None):
    """
    Função principal para uso direto do script
    """
    print("Sistema de Transcrição de Áudio Gratuito")
    print("=" * 40)
    
    # Verificar dependências
    deps = verificar_dependencias()
    print(f"Dependências disponíveis: {deps}")
    
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
    resultado = transcrever_audio_gratuito(caminho_arquivo)
    
    print(f"\nResultado da transcrição:")
    print("-" * 30)
    print(resultado)
    
    # Salvar resultado
    caminho_saida = Path(caminho_arquivo).with_suffix('.transcricao_gratuita.txt')
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.write(f"Transcrição gratuita do arquivo: {Path(caminho_arquivo).name}\n")
        f.write(f"Método: Melhor serviço gratuito disponível\n")
        f.write(f"Data: {datetime.now()}\n")
        f.write("-" * 50 + "\n")
        f.write(resultado)
    
    print(f"\nTranscrição salva em: {caminho_saida}")

if __name__ == "__main__":
    # Aceitar caminho do arquivo como argumento opcional
    caminho_arquivo = sys.argv[1] if len(sys.argv) > 1 else None
    main(caminho_arquivo)