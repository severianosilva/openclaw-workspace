#!/usr/bin/env python3
"""
Script para transcrição de áudio usando Vosk (modelo offline em português)
Este script oferece uma alternativa mais precisa para reconhecimento de fala em português
"""

import sys
import json
from pathlib import Path
from datetime import datetime

def transcrever_com_vosk(caminho_arquivo, modelo_path="vosk-model-small-pt-0.3"):
    """
    Transcreve áudio usando o modelo Vosk em português
    """
    try:
        from vosk import Model, KaldiRecognizer
        import json
        import wave
        
        # Carregar modelo - agora usando o nome correto do modelo instalado
        print(f"Carregando modelo Vosk em português: {modelo_path}")
        model = Model(modelo_path)
        
        # Abrir arquivo de áudio
        wf = wave.open(caminho_arquivo, "rb")
        
        # Verificar formato do áudio
        print(f"Taxa de amostragem: {wf.getframerate()}, Canais: {wf.getnchannels()}, Bits: {wf.getsampwidth()}")
        
        # Criar reconhecedor
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        
        # Processar o áudio
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = rec.Result()
                result_dict = json.loads(result)
                if 'text' in result_dict and result_dict['text'].strip():
                    results.append(result_dict)
                print(f"Segmento detectado: {result_dict}")
        
        # Obter resultado final
        final_result_str = rec.FinalResult()
        final_result = json.loads(final_result_str)
        if 'text' in final_result and final_result['text'].strip():
            results.append(final_result)
        print(f"Resultado final: {final_result}")
        
        # Fechar arquivo
        wf.close()
        
        # Extrair textos
        texts = []
        for res in results:
            if 'text' in res and res['text'].strip():
                texts.append(res['text'])
        
        # Combinar textos
        full_text = ' '.join(texts).strip()
        
        return full_text if full_text else "Não foi possível entender o áudio"
        
    except ImportError:
        return "Vosk não está instalado. Execute: pip install vosk"
    except FileNotFoundError:
        return f"Modelo Vosk não encontrado em: {modelo_path}"
    except Exception as e:
        return f"Erro ao usar Vosk: {str(e)}"

def converter_para_wav_mono(caminho_entrada, caminho_saida):
    """Converte arquivo de áudio para WAV mono usando PyAV"""
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
        
        # Salvar como arquivo WAV com configurações adequadas para Vosk
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

def transcrever_audio_vosk_otimizado(caminho_arquivo):
    """
    Função principal que converte e transcreve áudio usando Vosk
    """
    print(f"Tentando transcrição com Vosk (modelo em português): {caminho_arquivo}")
    
    # Verificar se o arquivo existe
    if not Path(caminho_arquivo).exists():
        return "Arquivo de áudio não encontrado"
    
    # Converter para WAV se necessário
    caminho_para_usar = caminho_arquivo
    if Path(caminho_arquivo).suffix.lower() != '.wav':
        caminho_temp_wav = Path(caminho_arquivo).with_suffix('.mono.wav')
        print("Convertendo para WAV mono...")
        if converter_para_wav_mono(caminho_arquivo, str(caminho_temp_wav)):
            caminho_para_usar = str(caminho_temp_wav)
        else:
            return "Falha na conversão para WAV mono"
    
    # Transcrever com Vosk
    resultado = transcrever_com_vosk(caminho_para_usar)
    
    # Remover arquivo temporário se criado
    temp_path = Path(caminho_arquivo).with_suffix('.mono.wav')
    if temp_path.exists() and caminho_para_usar == str(temp_path):
        temp_path.unlink()
    
    return resultado

def main(caminho_arquivo=None):
    """
    Função principal para uso direto do script
    """
    print("Sistema de Transcrição Vosk para Português")
    print("=" * 45)
    
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
    resultado = transcrever_audio_vosk_otimizado(caminho_arquivo)
    
    print(f"\nResultado da transcrição Vosk:")
    print("-" * 30)
    print(resultado)
    
    # Salvar resultado
    caminho_saida = Path(caminho_arquivo).with_suffix('.transcricao_vosk.txt')
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        f.write(f"Transcrição Vosk do arquivo: {Path(caminho_arquivo).name}\n")
        f.write(f"Método: Vosk modelo offline em português\n")
        f.write(f"Data: {datetime.now()}\n")
        f.write("-" * 50 + "\n")
        f.write(resultado)
    
    print(f"\nTranscrição salva em: {caminho_saida}")
    
    return resultado

if __name__ == "__main__":
    # Aceitar caminho do arquivo como argumento opcional
    caminho_arquivo = sys.argv[1] if len(sys.argv) > 1 else None
    main(caminho_arquivo)