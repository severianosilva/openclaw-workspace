#!/usr/bin/env python3
"""Transcritor padrão usando Whisper tiny - Melhor precisão/espaço"""
import sys
from pathlib import Path

def transcrever_whisper(audio_file):
    """Transcreve com Whisper tiny - Padrão recomendado"""
    import whisper
    model = whisper.load_model("tiny")
    result = model.transcribe(str(audio_file), language="pt", task="transcribe")
    return result["text"]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        audio = Path(sys.argv[1])
    else:
        # Usar último áudio recebido
        audio = sorted(Path("C:/Users/User/.openclaw/media/inbound").glob("*.wav"))[-1]
    
    print(f"Transcrevendo: {audio.name}")
    texto = transcrever_whisper(audio)
    print(f"\n=== TRANSCRIÇÃO ===\n{texto}")
    
    # Salvar
    saida = audio.with_suffix(".transcricao.txt")
    with open(saida, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"\nSalvo em: {saida}")