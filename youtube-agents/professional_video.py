#!/usr/bin/env python3
"""
YouTube Video Production - Integração com ferramentas profissionais
Baseado em: CrewAI, n8n, FFmpeg, e projetos open-source
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

WORKSPACE = Path(__file__).parent / "workspace"
ASSETS = WORKSPACE / "assets"

def create_professional_video(script_data: dict):
    """Cria vídeo profissional usando FFmpeg avançado"""
    
    os.makedirs(ASSETS, exist_ok=True)
    os.makedirs(WORKSPACE / "output", exist_ok=True)
    
    # Gerar assets individuais
    assets = generate_video_assets(script_data)
    
    # Montar vídeo final
    output_path = WORKSPACE / "output" / f"final_{script_data['id']}.mp4"
    
    # Comando FFmpeg profissional
    cmd = build_ffmpeg_command(assets, script_data, output_path)
    
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        return str(output_path)
    except subprocess.CalledProcessError as e:
        print(f"Erro FFmpeg: {e}")
        return None

def generate_video_assets(script_data: dict):
    """Gera assets necessários"""
    assets = {}
    
    # 1. Intro (3 segundos)
    intro_path = ASSETS / f"intro_{script_data['id']}.mp4"
    assets['intro'] = create_intro(intro_path, script_data['title'])
    
    # 2. Conteúdo por capítulo
    content_clips = []
    for i, chapter in enumerate(script_data.get('chapters', [])):
        clip_path = ASSETS / f"chapter_{script_data['id']}_{i}.mp4"
        create_chapter_clip(clip_path, chapter, script_data['duration_minutes'])
        content_clips.append(str(clip_path))
    
    assets['chapters'] = content_clips
    
    # 3. Outro
    outro_path = ASSETS / f"outro_{script_data['id']}.mp4"
    assets['outro'] = create_outro(outro_path)
    
    return assets

def create_intro(path, title):
    """Cria clipe de introdução"""
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=#1a73e8:s=1920x1080:d=3:rate=30',
        '-vf', f'drawtext=fontfile=/Windows/Fonts/arialbd.ttf:text=\'{title}\':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        str(path)
    ]
    subprocess.run(cmd, capture_output=True)
    return str(path)

def create_chapter_clip(path, chapter, duration_min):
    """Cria clipe de capítulo"""
    duration = 8 if chapter.get('hook') else 15
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=#34a853:s=1920x1080:d=' + str(duration) + ':rate=30',
        '-vf', f'drawtext=fontfile=/Windows/Fonts/arial.ttf:text=\'{chapter.get("title", "")}\':fontcolor=white:fontsize=48:x=100:y=100',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        str(path)
    ]
    subprocess.run(cmd, capture_output=True)

def create_outro(path):
    """Cria clipe de encerramento"""
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=#ea4335:s=1920x1080:d=2:rate=30',
        '-vf', 'drawtext=fontfile=/Windows/Fonts/arialbd.ttf:text=\'INSCREVA-SE\':fontcolor=white:fontsize=72:x=(w-text_w)/2:y=(h-text_h)/2',
        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
        str(path)
    ]
    subprocess.run(cmd, capture_output=True)
    return str(path)

def build_ffmpeg_command(assets, script, output):
    """Montagem do vídeo final"""
    # Criar arquivo de lista
    list_file = ASSETS / f"list_{script['id']}.txt"
    
    with open(list_file, 'w') as f:
        f.write(f"file '{assets['intro']}'\n")
        for chapter in assets['chapters']:
            f.write(f"file '{chapter}'\n")
        f.write(f"file '{assets['outro']}'\n")
    
    # Concatenar
    cmd = [
        'ffmpeg', '-y',
        '-f', 'concat', '-safe', '0', '-i', str(list_file),
        '-c:v', 'libx264', '-preset', 'medium',
        '-crf', '23', '-pix_fmt', 'yuv420p',
        str(output)
    ]
    
    return cmd

def create_thumbnail_professional(title: str):
    """Cria thumbnail profissional usando FFmpeg"""
    output = WORKSPACE / "output" / f"thumbnail_{datetime.now().strftime('%Y%m%d')}.png"
    
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', 'color=c=#ea4335:s=1280x720:d=1',
        '-vf', f'drawtext=fontfile=/Windows/Fonts/arialbd.ttf:text=\'{title}\':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2,drawtext=fontfile=/Windows/Fonts/arial.ttf:text=\'Vídeo Importante!\':fontcolor=yellow:fontsize=32:x=50:y=50',
        '-frames:v', '1',
        str(output)
    ]
    
    subprocess.run(cmd, capture_output=True)
    return str(output)

if __name__ == "__main__":
    print("[VIDEO] Produção profissional iniciada...")
    
    # Carregar script
    scripts = list(WORKSPACE.glob("script_*.json"))
    if scripts:
        with open(scripts[-1], 'r', encoding='utf-8') as f:
            script = json.load(f)
        
        video = create_professional_video(script)
        if video:
            print(f"[OK] Vídeo: {video}")
        
        thumb = create_thumbnail_professional(script['title'])
        print(f"[OK] Thumbnail: {thumb}")