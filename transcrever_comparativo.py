#!/usr/bin/env python3
"""Comparativo de transcrição: Vosk vs Whisper"""
import json, wave, sys
from pathlib import Path

def transcrever_vosk(audio_file):
    """Transcreve com Vosk"""
    from vosk import Model, KaldiRecognizer
    
    model = Path.home() / "vosk-model-small-pt-0.3" / "vosk-model-small-pt-0.3"
    model = Model(str(model))
    
    with wave.open(str(audio_file), "rb") as wf:
        rec = KaldiRecognizer(model, wf.getframerate())
        results = []
        while data := wf.readframes(4000):
            if rec.AcceptWaveform(data):
                results.append(json.loads(rec.Result()))
        results.append(json.loads(rec.FinalResult()))
    
    return " ".join([r.get("text", "") for r in results if r.get("text")])

def transcrever_whisper(audio_file):
    """Transcreve com Whisper"""
    import whisper
    model = whisper.load_model("tiny")
    result = model.transcribe(str(audio_file), language="pt")
    return result["text"]

if __name__ == "__main__":
    audio = Path("C:/Users/User/.openclaw/media/inbound/file_0---85f5aaa3-330e-4371-9de1-b3eff91e8853.wav")
    
    print(f"\n=== Comparativo para {audio.name} ===")
    
    # Vosk
    print("Vosk:")
    print(f"  {transcrever_vosk(audio)}\n")
    
    # Whisper  
    print("Whisper:")
    print(f"  {transcrever_whisper(audio)}\n")