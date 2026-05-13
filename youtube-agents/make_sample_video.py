#!/usr/bin/env python3
"""Cria vídeo de amostra usando FFmpeg (se disponível)"""

import subprocess
import os
from pathlib import Path

WORKSPACE = Path(__file__).parent / "workspace"
OUTPUT_DIR = WORKSPACE / "output"
ASSETS_DIR = WORKSPACE / "assets"

def create_directories():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)

def check_ffmpeg():
    """Verifica se FFmpeg está disponível"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def create_sample_video():
    """Cria um vídeo de exemplo simples"""
    
    create_directories()
    
    if not check_ffmpeg():
        print("[AVISO] FFmpeg não encontrado")
        print("[INFO] Criando arquivos de referência...")
        
        # Criar arquivos de referência
        create_video_reference()
        return
    
    # Comando FFmpeg para criar vídeo de 8 segundos
    output_path = OUTPUT_DIR / "sample_video.mp4"
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=#1a73e8:s=1280x720:d=8:rate=30',
        '-vf', 'drawtext=fontfile=/Windows/Fonts/arialbd.ttf:text=\'YouTube Money Agent Demo\':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        print(f"[OK] Vídeo criado: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"[ERRO] {e}")

def create_video_reference():
    """Cria arquivo de referência para edição manual"""
    
    sample_data = """
# YouTube Money Agent - Vídeo de Exemplo

FORMATO: MP4 (H.264)
RESOLUÇÃO: 1280x720 (720p)
DURAÇÃO: 8 minutos
FRAMERATE: 30fps

## ESTRUTURA

00:00-00:30 - Introdução (Hook + Apresentação)
00:30-02:00 - Conteúdo principal parte 1
02:00-05:00 - Conteúdo principal parte 2
05:00-07:00 - Dicas práticas
07:00-08:00 - Conclusão + CTA

## ELEMENTOS VISUAIS

- Background: Azul degradê (#1a73e8 -> #4285f4)
- Texto branco: Arial Bold 48pt
- Overlay: Thumbnail no canto inferior direito

## PARA EDITAR MANUALMENTE

1. Abra no CapCut/Davinci/Shotcut
2. Importe assets da pasta workspace/assets/
3. Siga o arquivo workspace/video_project_*.json
"""
    
    with open(WORKSPACE / "video_edit_guide.txt", 'w', encoding='utf-8') as f:
        f.write(sample_data)
    
    print("[OK] Guia de edição criado: workspace/video_edit_guide.txt")

if __name__ == "__main__":
    print("=" * 50)
    print("GERADOR DE VÍDEO DE AMOSTRA")
    print("=" * 50)
    create_sample_video()