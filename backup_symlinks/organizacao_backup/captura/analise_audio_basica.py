#!/usr/bin/env python3
"""
Script para análise básica do conteúdo de áudio
"""

import av
import numpy as np
from pathlib import Path
import sys
from scipy.io import wavfile

def analisar_audio_basico(caminho_entrada):
    """Analisar basicamente o conteúdo do áudio"""
    
    print(f"Análise básica do áudio: {caminho_entrada}")
    print("=" * 60)
    
    # Obter informações básicas com PyAV
    container = av.open(caminho_entrada)
    
    audio_stream = None
    for stream in container.streams.audio:
        audio_stream = stream
        break
    
    if audio_stream is None:
        print("ERRO: Nenhum stream de áudio encontrado")
        return
    
    print(f"Codec: {audio_stream.codec.name}")
    print(f"Taxa de amostragem: {audio_stream.rate} Hz")
    print(f"Canais: {audio_stream.channels}")
    print(f"Duração: {container.duration / 1000000:.2f} segundos")
    
    # Coletar amostras de áudio
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
    
    audio_array = np.array(audio_samples)
    
    # Análise estatística
    print(f"\nAnálise Estatística:")
    print(f"- Total de amostras: {len(audio_array):,}")
    print(f"- Valor médio: {np.mean(audio_array):.2f}")
    print(f"- Desvio padrão: {np.std(audio_array):.2f}")
    print(f"- Valor mínimo: {np.min(audio_array)}")
    print(f"- Valor máximo: {np.max(audio_array)}")
    
    volume_medio = np.mean(np.abs(audio_array))
    volume_rms = np.sqrt(np.mean(audio_array**2))
    
    print(f"- Volume médio (absoluto): {volume_medio:.2f}")
    print(f"- Volume RMS: {volume_rms:.2f}")
    
    # Detectar silêncio
    threshold_silencio = 50  # Limiar para considerar como silêncio
    amostras_acima_silencio = np.sum(np.abs(audio_array) > threshold_silencio)
    percentual_ativo = (amostras_acima_silencio / len(audio_array)) * 100
    
    print(f"- Percentual de atividade (> {threshold_silencio}): {percentual_ativo:.2f}%")
    
    # Análise de possibilidade de fala
    if volume_medio < 50:
        qualidade_volume = "MUITO BAIXO"
    elif volume_medio < 200:
        qualidade_volume = "BAIXO"
    elif volume_medio < 1000:
        qualidade_volume = "ADEQUADO"
    else:
        qualidade_volume = "ALTO"
    
    print(f"- Qualidade de volume: {qualidade_volume}")
    
    # Análise de variação (indicativo de fala)
    variacao = np.std(audio_array) / (np.mean(np.abs(audio_array)) + 1)  # +1 para evitar divisão por zero
    print(f"- Índice de variação (possível fala): {variacao:.2f}")
    
    # Classificação preliminar
    print(f"\nClassificação Preliminar:")
    if percentual_ativo < 10:
        classificacao = "Possivelmente silencioso ou com muito ruído"
    elif volume_medio < 30:
        classificacao = "Volume extremamente baixo, difícil detecção de fala"
    elif variacao < 0.5:
        classificacao = "Baixa variação, possivelmente ruído constante ou tom fixo"
    else:
        classificacao = "Conteúdo com potencial para conter fala, mas análise automática não detectou"
    
    print(f"- {classificacao}")
    
    # Salvar áudio amplificado para análise manual (opcional)
    if volume_medio < 200:
        gain_factor = min(20.0, 1000.0 / (volume_medio + 1))
        audio_amplificado = (audio_array.astype(np.float32) * gain_factor).astype(np.int16)
        
        caminho_saida = Path(caminho_entrada).with_suffix('.amplificado.wav')
        wavfile.write(caminho_saida, audio_stream.rate, audio_amplificado)
        print(f"\nÁudio amplificado salvo para análise: {caminho_saida}")
        print(f"Ganho aplicado: {gain_factor:.2f}x")
    
    print("\nRecomendações:")
    if volume_medio < 50:
        print("- O áudio tem volume muito baixo para detecção automática de fala")
        print("- Considere verificar se realmente contém fala audível")
    if percentual_ativo < 20:
        print("- Grande parte do áudio pode ser silêncio ou ruído de fundo")
    print("- Se o áudio contém fala clara, pode precisar de modelos mais sensíveis")
    
    return {
        'volume_medio': volume_medio,
        'percentual_ativo': percentual_ativo,
        'variacao': variacao,
        'duracao': container.duration / 1000000
    }

def main(caminho_arquivo):
    """Função principal"""
    if not Path(caminho_arquivo).exists():
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        return
    
    stats = analisar_audio_basico(caminho_arquivo)
    return stats

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 analise_audio_basica.py <caminho_do_arquivo>")
        sys.exit(1)
    
    caminho_arquivo = sys.argv[1]
    main(caminho_arquivo)