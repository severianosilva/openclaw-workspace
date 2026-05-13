#!/usr/bin/env python3
"""
Script para converter e transcrever arquivos de áudio recebidos
Aceita diversos formatos de entrada e converte para WAV antes da transcrição
"""

import sys
import os
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

def converter_para_wav(caminho_entrada, caminho_saida):
    """Tenta converter arquivo de áudio para WAV usando diferentes métodos"""
    print("Convertendo arquivo de áudio para WAV...")
    
    # Primeiro tentar com PyAV (melhor qualidade)
    if converter_para_wav_pyav(caminho_entrada, caminho_saida):
        print("Conversão com PyAV bem-sucedida!")
        return True
    # Depois tentar com pydub
    elif converter_para_wav_pydub(caminho_entrada, caminho_saida):
        print("Conversão com pydub bem-sucedida!")
        return True
    # Finalmente tentar com ffmpeg
    else:
        print("Tentando conversão com ffmpeg...")
        try:
            subprocess.run([
                'ffmpeg', '-i', caminho_entrada,
                '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le',
                caminho_saida
            ], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Falha em todos os métodos de conversão.")
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
        
        # Converter para array numpy para processamento
        audio_array = np.array(audio_samples, dtype=np.int16)
        
        # Calcular volume médio
        volume_medio = np.mean(np.abs(audio_array))
        
        # Amplificar o áudio se estiver muito baixo
        if volume_medio < 100:  # Limiar para áudio muito baixo
            gain_factor = min(20.0, 1000.0 / (volume_medio + 1))  # Limitar ganho máximo
            audio_array = (audio_array.astype(np.float32) * gain_factor).astype(np.int16)
            print(f"Áudio amplificado em {gain_factor:.2f}x para melhor detecção")
        
        # Salvar como arquivo WAV
        import wave
        with wave.open(caminho_saida, 'wb') as wav_file:
            wav_file.setnchannels(target_channels)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(target_sample_rate)
            wav_file.writeframes(audio_array.tobytes())
        
        return True
    except ImportError:
        print("AVISO: PyAV ou numpy não estão instalados. Instale com: pip install av numpy")
        return False
    except Exception as e:
        print(f"AVISO: Erro ao converter áudio com PyAV: {str(e)}")
        return False

def transcrever_audio_wav(caminho_arquivo_wav):
    """Transcreve arquivo WAV usando SpeechRecognition com Google STT"""
    try:
        import speech_recognition as sr
        
        r = sr.Recognizer()
        
        # Ajustar o limiar de energia para detectar fala mais baixa
        r.energy_threshold = 400  # Valor padrão é 300, aumentar para ser mais sensível
        
        with sr.AudioFile(caminho_arquivo_wav) as source:
            audio = r.record(source)
            
            # Tentar transcrever usando o serviço gratuito do Google em português
            text = r.recognize_google(audio, language="pt-BR")
            if text.strip():
                print(f"Google STT detectou texto: '{text[:50]}...'")  # Mostrar primeiros 50 chars
            return text
            
    except ImportError:
        return "SpeechRecognition não está instalado"
    except sr.UnknownValueError:
        print("Google STT: Não foi possível entender o áudio")
        return "Não foi possível entender o áudio"
    except sr.RequestError as e:
        print(f"Google STT: Erro de requisição: {str(e)}")
        return f"Erro de requisição: {str(e)}"
    except Exception as e:
        print(f"Google STT: Erro ao transcrever: {str(e)}")
        return f"Erro ao transcrever: {str(e)}"

def transcrever_com_whisper_otimizado(caminho_arquivo_wav):
    """Tenta usar uma versão otimizada do Whisper"""
    try:
        import whisper
        import torch
        
        # Carregar modelo pequeno para processamento mais rápido
        model = whisper.load_model("tiny", device="cpu")
        result = model.transcribe(caminho_arquivo_wav, language="pt")
        
        return result["text"]
        
    except ImportError:
        return None  # Whisper não está instalado
    except Exception as e:
        print(f"Whisper falhou: {str(e)}")
        return None

def transcrever_com_whisper_tiny_quantizado(caminho_arquivo_wav):
    """Tenta usar faster-whisper com modelo quantizado"""
    try:
        from faster_whisper import WhisperModel
        
        # Usar modelo pequeno e otimizado, com configurações específicas para português
        model = WhisperModel("tiny", device="cpu", compute_type="int8")
        
        # Adicionando mais parâmetros para melhorar a transcrição em português
        segments, info = model.transcribe(
            caminho_arquivo_wav, 
            language="pt",
            beam_size=5,
            best_of=5,
            patience=2.0
        )
        
        # Concatenar todos os segmentos
        text = " ".join([segment.text for segment in segments])
        
        if text.strip():
            print(f"Faster-whisper detectou texto: '{text[:50]}...'")  # Mostrar primeiros 50 chars
            return text.strip()
        else:
            print("Faster-whisper não detectou fala clara no áudio")
            return None  # Retorna None para tentar outros métodos
        
    except ImportError:
        return None  # faster-whisper não está instalado
    except Exception as e:
        print(f"Faster-whisper falhou: {str(e)}")
        return None

def transcrever_com_vosk(caminho_arquivo_wav, modelo_path="/tmp/vosk-model-small-pt-0.3"):
    """Tenta usar o Vosk com modelo em português"""
    try:
        from vosk import Model, KaldiRecognizer
        import json
        import wave
        
        # Carregar modelo
        model = Model(modelo_path)
        
        # Abrir arquivo de áudio
        wf = wave.open(caminho_arquivo_wav, "rb")
        
        # Verificar formato do áudio
        if wf.getnchannels() != 1:
            print("AVISO: O áudio deve ser mono (canal único) para melhor reconhecimento.")
        
        # Criar reconhecedor com configurações mais sensíveis
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        # Definir nível de silêncio mais baixo para detectar fala mais baixa
        rec.SetMaxAlternatives(1)
        
        # Processar o áudio
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if 'text' in result and result['text'].strip():
                    results.append(result)
        
        # Obter resultado final
        final_result = json.loads(rec.FinalResult())
        if 'text' in final_result and final_result['text'].strip():
            results.append(final_result)
        
        # Fechar arquivo
        wf.close()
        
        # Extrair e combinar textos
        texts = []
        for res in results:
            if 'text' in res and res['text'].strip():
                texts.append(res['text'])
        
        full_text = ' '.join(texts).strip()
        
        if full_text:
            print(f"Vosk detectou texto: '{full_text[:50]}...'")  # Mostrar primeiros 50 chars
            return full_text
        else:
            print("Vosk não detectou fala clara no áudio")
            return None  # Retorna None para tentar outros métodos
        
    except ImportError:
        print("Vosk não está instalado")
        return None
    except FileNotFoundError:
        print(f"Modelo Vosk não encontrado em: {modelo_path}")
        # Tenta usar o modelo diretamente pelo nome se o caminho absoluto falhar
        try:
            from vosk import Model, KaldiRecognizer
            import json
            import wave
            
            # Tentar carregar modelo usando nome curto
            model = Model('vosk-model-small-pt-0.3')
            
            # Abrir arquivo de áudio
            wf = wave.open(caminho_arquivo_wav, "rb")
            
            # Criar reconhecedor com configurações mais sensíveis
            rec = KaldiRecognizer(model, wf.getframerate())
            rec.SetWords(True)
            rec.SetMaxAlternatives(1)
            
            # Processar o áudio
            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    if 'text' in result and result['text'].strip():
                        results.append(result)
            
            # Obter resultado final
            final_result = json.loads(rec.FinalResult())
            if 'text' in final_result and final_result['text'].strip():
                results.append(final_result)
            
            # Fechar arquivo
            wf.close()
            
            # Extrair e combinar textos
            texts = []
            for res in results:
                if 'text' in res and res['text'].strip():
                    texts.append(res['text'])
            
            full_text = ' '.join(texts).strip()
            
            if full_text:
                print(f"Vosk detectou texto: '{full_text[:50]}...'")  # Mostrar primeiros 50 chars
                return full_text
            else:
                print("Vosk não detectou fala clara no áudio")
                return None  # Retorna None para tentar outros métodos
                
        except Exception as e:
            print(f"Erro ao usar Vosk com modelo direto: {str(e)}")
            return None
    except Exception as e:
        print(f"Erro ao usar Vosk: {str(e)}")
        return None

def main(caminho_arquivo=None):
    """Função principal"""
    if caminho_arquivo is None:
        if len(sys.argv) < 2:
            print("Uso: python3 converter_e_transcrever.py <caminho_do_arquivo>")
            return
        caminho_arquivo = sys.argv[1]
    
    print(f"Processando arquivo: {caminho_arquivo}")
    
    # Verificar se o arquivo existe
    if not Path(caminho_arquivo).exists():
        print("Arquivo não encontrado!")
        return
    
    # Criar caminho para o arquivo WAV convertido
    caminho_wav = Path(caminho_arquivo).with_suffix('.converted.wav')
    
    # Converter o arquivo para WAV
    if converter_para_wav(caminho_arquivo, str(caminho_wav)):
        print(f"Arquivo convertido com sucesso: {caminho_wav}")
    else:
        print("Falha na conversão do arquivo para WAV")
        return
    
    print("Conversão concluída. Iniciando transcrição...")
    
    # Tentar transcrição com Google STT primeiro (mais confiável atualmente)
    print("Tentando transcrição com Google STT (primeira tentativa)...")
    resultado = transcrever_audio_wav(str(caminho_wav))
    
    if resultado is not None and resultado != "Não foi possível entender o áudio" and "Erro" not in resultado:
        print("Transcrição bem-sucedida com Google STT!")
    else:
        # Se Google STT falhar, tentar com Whisper
        print("Google STT falhou. Tentando com Whisper local...")
        resultado = transcrever_com_whisper_tiny_quantizado(str(caminho_wav))
        
        if resultado is not None and resultado.strip() and resultado != "Não foi possível entender o áudio":
            print("Transcrição bem-sucedida com Whisper!")
        else:
            # Se Whisper também falhar, tentar com Vosk
            print("Whisper não disponível ou falhou. Tentando com Vosk...")
            resultado = transcrever_com_vosk(str(caminho_wav))
            
            if resultado is not None and resultado != "Não foi possível entender o áudio":
                print("Transcrição bem-sucedida com Vosk!")
            else:
                # Se tudo falhar, retornar mensagem padrão
                resultado = "Não foi possível entender o áudio"
    
    # Exibir resultado
    print("\nResultado da transcrição:")
    print("=" * 40)
    print(resultado)
    print("=" * 40)
    
    # Salvar resultado em arquivo
    caminho_saida = Path(caminho_arquivo).with_suffix('.transcricao_final.txt')
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.write(f"Transcrição do arquivo: {Path(caminho_arquivo).name}\n")
        f.write(f"Método: Conversão com PyAV + Transcrição Vosk/Whisper/Google STT\n")
        f.write(f"Data: {datetime.now()}\n")
        f.write("-" * 50 + "\n")
        f.write(resultado)
    
    print(f"\nTranscrição salva em: {caminho_saida}")

if __name__ == "__main__":
    main()