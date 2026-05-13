#!/usr/bin/env python3
"""Criar vídeo profissional com imagens e texto"""

import subprocess
import os
from pathlib import Path

WORKSPACE = Path(__file__).parent / "workspace"
OUTPUT = WORKSPACE / "output"

def create_simple_video():
    """Cria vídeo simples mas profissional"""
    
    os.makedirs(OUTPUT, exist_ok=True)
    
    # Criar imagem para vídeo
    create_intro_image()
    
    # Criar vídeo com essa imagem
    output_path = OUTPUT / "youtube_pro_intro.mp4"
    
    cmd = [
        'ffmpeg', '-y',
        '-loop', '1', '-i', str(OUTPUT / 'intro_image.png'),
        '-c:v', 'libx264', '-tune', 'stillimage',
        '-pix_fmt', 'yuv420p', '-t', '5',
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        print(f"[OK] Vídeo criado: {output_path}")
        size = os.path.getsize(output_path)
        print(f"[INFO] Tamanho: {size} bytes")
        return output_path
    except Exception as e:
        print(f"[ERRO] {e}")
        return None

def create_intro_image():
    """Cria imagem de introdução"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Criar imagem
        img = Image.new('RGB', (1920, 1080), color=(26, 115, 232))
        draw = ImageDraw.Draw(img)
        
        # Texto
        text = "YouTube Money Agents"
        
        # Fonte
        try:
            font = ImageFont.truetype("arialbd.ttf", 80)
        except:
            font = ImageFont.load_default()
        
        # Texto com tamanho (PIL versão nova usa textbbox)
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(((1920-w)/2, (1080-h)/2), text, fill='white', font=font)
        
        # Subtítulo
        try:
            font2 = ImageFont.truetype("arial.ttf", 40)
        except:
            font2 = font
        
        draw.text((800, 600), "Sistema Autonomo", fill='yellow', font=font2)
        
        # Salvar
        img.save(OUTPUT / 'intro_image.png')
        print("[OK] Imagem criada")
        
    except ImportError:
        print("[AVISO] PIL não disponível")
        # Criar PNG simples com FFmpeg
        create_solid_color_image()

def create_solid_color_image():
    """Cria imagem sólida com FFmpeg"""
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=#1a73e8:s=1920x1080:d=1',
        str(OUTPUT / 'intro_image.png')
    ]
    subprocess.run(cmd, capture_output=True)

if __name__ == "__main__":
    print("=" * 50)
    print("CRIANDO VÍDEO PROFISSIONAL")
    print("=" * 50)
    create_simple_video()