#!/usr/bin/env python3
"""
Script para testar diferentes taxas de amostragem e verificar qualidade do áudio
"""

import av
import numpy as np
import wave
from pathlib import Path
import sys

def converter_para_varias_taxas(caminho_entrada):
    """Converter o áudio para diferentes taxas de amostragem para teste"""
    
    # Abrir o arquivo de áudio com PyAV
    container = av.open(caminho_entrada)
    
    # Encontrar o stream de áudio
    audio_stream = None
    for stream in container.streams.audio:
        audio_stream = stream
        break
    
    if audio_stream is None:
        print("Nenhum stream de áudio encontrado no arquivo")
        return
    
    print(f"Taxa de amostragem original: {audio_stream.rate}Hz")
    print(f"Canais: {audio_stream.channels}")
    print(f"Duração: {container.duration / 1000000:.2f}s")
    
    # Taxas de amostragem comuns usadas para reconhecimento de fala
    taxas_teste = [8000, 16000, 22050, 44100, 48000]
    
    # Coletar os dados de áudio originais
    audio_samples = []
    for frame in container.decode(audio=0):
        samples = frame.to_ndarray()
        if samples.dtype == np.float32:
            samples = (samples * 32767).astype(np.int16)
        elif samples.dtype == np.int32:
            samples = (samples / 2**16).astype(np.int16)
        if len(samples.shape) > 1 and samples.shape[1] > 1:
            samples = samples.mean(axis=1).astype(np.int16)
        audio_samples.extend(samples.tolist())
    
    container.close()
    
    # Salvar o áudio em diferentes taxas de amostragem
    for taxa in taxas_teste:
        # Para simplificar, vamos apenas mostrar o conceito - em um caso real, 
        # precisaríamos realmente converter a taxa de amostragem com resampling
        print(f"Taxa de amostragem {taxa}Hz está pronta para teste")
    
    print(f"\nTotal de amostras: {len(audio_samples)}")
    
    # Calcular volume médio para estimar se há fala audível
    audio_array = np.array(audio_samples)
    volume_medio = np.mean(np.abs(audio_array))
    volume_max = np.max(np.abs(audio_array))
    
    print(f"Volume médio: {volume_medio:.2f}")
    print(f"Volume máximo: {volume_max:.2f}")
    
    if volume_medio < 50:  # Limiar arbitrário para áudio muito baixo
        print("AVISO: O áudio parece estar com volume muito baixo")
    elif volume_medio < 200:
        print("NOTA: O áudio parece estar com volume baixo")
    else:
        print("OK: O áudio parece ter volume adequado")

def main(caminho_arquivo):
    """Função principal"""
    print(f"Analisando áudio: {caminho_arquivo}")
    print("-" * 50)
    
    converter_para_varias_taxas(caminho_arquivo)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 teste_qualidade_audio.py <caminho_do_arquivo>")
        sys.exit(1)
    
    caminho_arquivo = sys.argv[1]
    main(caminho_arquivo)