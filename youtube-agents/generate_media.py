#!/usr/bin/env python3
"""Gera arquivos de mídia (vídeos, thumbnails) - Versão sem dependências"""

import os
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
WORKSPACE = BASE_DIR / "workspace"

def generate_video_files():
    """Gera arquivos de mídia reais (formato texto para demonstração)"""
    
    os.makedirs(WORKSPACE, exist_ok=True)
    
    # Carregar scripts gerados
    scripts = []
    for f in os.listdir(WORKSPACE):
        if f.startswith("script_") and f.endswith(".json"):
            with open(WORKSPACE / f, 'r', encoding='utf-8') as file:
                scripts.append(json.load(file))
    
    print(f"[MEDIA] Gerando arquivos para {len(scripts)} vídeos...")
    
    for script in scripts:
        # Gerar vídeo (arquivo de projeto)
        video_project = {
            "script_id": script.get("id"),
            "title": script.get("title"),
            "duration": f"{script.get('duration_minutes', 8)}:00",
            "chapters": script.get("chapters", []),
            "assets": {
                "intro_video": f"assets/intro_{script['id']}.mp4",
                "broll_clips": [f"assets/broll_{script['id']}_{i}.mp4" for i in range(5)],
                "music": "assets/background_music.mp3"
            },
            "output": f"output/video_{script['id']}.mp4"
        }
        
        video_file = f"video_project_{script['id']}.json"
        with open(WORKSPACE / video_file, 'w', encoding='utf-8') as f:
            json.dump(video_project, f, indent=2, ensure_ascii=False)
        
        print(f"   [OK] {video_file}")
        
        # Gerar thumbnail (prompt para IA ou Photoshop)
        thumb_prompt = f"""
THUMBNAIL PROMPT - {script.get('title')}
==========================================
Tamanho: 1280x720px
Layout: Rosto (esquerda) + Texto (direita)
Cor de fundo: Laranja/Vermelho (#ea4335)
Texto: {script.get('title')[:30]}
Fonte: Anton, Oswald (negrito)
Expressão: Surpresa emocionada
Elementos: "Você sabia?" badge esquerdo superior
"""
        
        thumb_file = f"thumbnail_prompt_{script['id']}.txt"
        with open(WORKSPACE / thumb_file, 'w', encoding='utf-8') as f:
            f.write(thumb_prompt)
        
        print(f"   [OK] {thumb_file}")

def create_sample_video():
    """Cria um vídeo de exemplo simples usando FFmpeg (se disponível)"""
    
    # Criar vídeo de exemplo com FFmpeg
    video_content = f"""
# Comando FFmpeg para gerar vídeo de exemplo
ffmpeg -f lavfi -i color=c=blue:s=1280x720:d=8 -vf "drawtext=fontfile=/Windows/Fonts/arial.ttf:text='{datetime.now().strftime('%Y-%m-%d')}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2" "output/sample_video.mp4"
"""
    
    with open(WORKSPACE / "ffmpeg_commands.txt", 'w') as f:
        f.write(video_content)
    
    print("[FFMPEG] Comandos salvos em workspace/ffmpeg_commands.txt")

if __name__ == "__main__":
    print("=" * 50)
    print("GERADOR DE ARQUIVOS DE MÍDIA")
    print("=" * 50)
    
    generate_video_files()
    create_sample_video()
    
    print("\n[PRONTO] Arquivos gerados em workspace/")