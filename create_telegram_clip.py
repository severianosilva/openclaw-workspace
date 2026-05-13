#!/usr/bin/env python3
"""
📱 Cria clipe curto para Telegram (até 50MB)
"""

import json
import os
from pathlib import Path
from gtts import gTTS
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(r"C:\Users\User\.openclaw\workspace")
OUTPUT_DIR = BASE_DIR / "telegram_clip"
OUTPUT_DIR.mkdir(exist_ok=True)

def create_telegram_clip():
    print("="*50)
    print("CRIANDO CLIP PARA TELEGRAM")
    print("="*50)
    
    # Texto curto (15 segundos)
    text = "3 métodos rápidos para ganhar dinheiro online! Método 1: Freelance. Método 2: Afiliados. Método 3: Cursos digitais. Comece hoje!"
    
    # 1. Áudio curto
    print("[1/3] Gerando áudio curto...")
    tts = gTTS(text=text, lang='pt', slow=False)
    audio_path = OUTPUT_DIR / "clip_audio.mp3"
    tts.save(str(audio_path))
    print(f"    [OK] {audio_path}")
    
    # 2. Imagem para vídeo
    print("[2/3] Criando imagem...")
    img = Image.new('RGB', (720, 1280), color=(30, 30, 80))
    draw = ImageDraw.Draw(img)
    
    # Texto na imagem
    lines = [
        "3 MÉTODOS",
        "RÁPIDOS",
        "",
        "1. Freelance",
        "2. Afiliados", 
        "3. Cursos"
    ]
    
    y = 400
    for line in lines:
        draw.text((50, y), line, fill=(255, 255, 255))
        y += 120
    
    img_path = OUTPUT_DIR / "clip_image.jpg"
    img.save(img_path)
    print(f"    [OK] {img_path}")
    
    # 3. Criar vídeo simples (imagem + áudio)
    print("[3/3] Criando vídeo...")
    try:
        from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
        
        # Criar vídeo: imagem estática com áudio
        img_clip = ImageClip(str(img_path)).set_duration(15)
        audio_clip = AudioFileClip(str(audio_path))
        
        video = CompositeVideoClip([img_clip.set_audio(audio_clip)])
        video_path = OUTPUT_DIR / "telegram_clip.mp4"
        video.write_videofile(str(video_path), fps=24, codec='libx264', audio_codec='aac')
        
        size_mb = os.path.getsize(video_path) / (1024*1024)
        print(f"    [OK] {video_path}")
        print(f"    Tamanho: {size_mb:.2f} MB")
        
        result = {"success": True, "video": str(video_path), "size_mb": size_mb}
        
    except Exception as e:
        print(f"    [AVISO] {e}")
        print("    Criando versão alternativa...")
        
        # Sem MoviePy, salvar só áudio + imagem
        result = {
            "success": True,
            "audio": str(audio_path),
            "image": str(img_path),
            "note": "Use Kinemaster ou CapCut para juntar no celular"
        }
    
    # Info
    info = {
        "titulo": "3 Métodos Rápidos - Telegram Clip",
        "duracao": "15 segundos",
        "texto": text,
        "arquivos": result
    }
    
    info_path = OUTPUT_DIR / "clip_info.json"
    with open(info_path, 'w') as f:
        json.dump(info, f, indent=2)
    
    print(f"\n[SUCESSO] Clip criado!")
    print(f"Diretório: {OUTPUT_DIR}")
    
    return result

if __name__ == "__main__":
    result = create_telegram_clip()
    
    if result.get("success") and result.get("video"):
        path = Path(result["video"])
        if path.exists():
            print(f"\n✅ Pronto para enviar: {path}")
    elif result.get("audio") and result.get("image"):
        print(f"\n📱 Para enviar no Telegram:")
        print(f"   Áudio: {result['audio']}")
        print(f"   Imagem: {result['image']}")
        print(f"   Use Kinemaster para unir")