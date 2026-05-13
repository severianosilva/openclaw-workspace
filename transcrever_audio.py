#!/usr/bin/env python3
"""Script simples para transcrever áudio OGG usando Vosk"""
import sys
import json
import wave
from pathlib import Path
from vosk import Model, KaldiRecognizer

def main():
    audio_file = Path("C:/Users/User/.openclaw/media/inbound/file_0---85f5aaa3-330e-4371-9de1-b3eff91e8853.wav")
    model_path = Path.home() / "vosk-model-small-pt-0.3" / "vosk-model-small-pt-0.3"
    
    if not audio_file.exists():
        print("Arquivo WAV não encontrado")
        return
    
    if not model_path.exists():
        print("Modelo Vosk não encontrado")
        return
    
    # Carregar modelo e transcrever
    model = Model(str(model_path))
    
    with wave.open(str(audio_file), "rb") as wf:
        if wf.getnchannels() != 1 or wf.getframerate() != 16000:
            print(f"Formato não suportado: {wf.getnchannels()} canais, {wf.getframerate()} Hz")
            return
        
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                results.append(json.loads(rec.Result()))
        
        results.append(json.loads(rec.FinalResult()))
    
    # Extrair texto
    texto = " ".join([r.get("text", "") for r in results if r.get("text")])
    print(f"\n=== TRANSCRIÇÃO ===\n{texto}\n")

if __name__ == "__main__":
    main()