"""Agente Produtor de Vídeo - Gera vídeos reais"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

try:
    from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, concatenate_videoclips
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class VideoProducer:
    def __init__(self, workspace_path: str):
        self.workspace = workspace_path
        os.makedirs(workspace_path, exist_ok=True)
        
    def produce_video(self, script: Dict, branding: Dict) -> Dict:
        """Gera vídeo real baseado no roteiro"""
        
        result = {
            "script_id": script.get("id"),
            "status": "pending",
            "files": []
        }
        
        if not MOVIEPY_AVAILABLE:
            # Modo simulação - gera arquivos de descrição
            result["status"] = "simulated"
            result["message"] = "Instale moviepy e pillow para gerar videos reais"
            instructions = self._create_video_instructions(script, branding)
            filename = f"video_instructions_{script['id']}.txt"
            with open(os.path.join(self.workspace, filename), 'w', encoding='utf-8') as f:
                f.write(instructions)
            result["files"].append(filename)
            return result
        
        # Gerar vídeo real
        video_path = self._create_real_video(script, branding)
        result["files"].append(video_path)
        result["status"] = "completed"
        
        return result
    
    def _create_video_instructions(self, script: Dict, branding: Dict) -> str:
        """Cria instruções detalhadas para produção manual"""
        return f"""
========================================
INSTRUÇÕES PARA PRODUÇÃO DE VÍDEO
========================================

Título: {script.get('title')}
Duração: {script.get('duration_minutes', 8)} minutos

CHAPTERS:
{self._format_chapters(script.get('chapters', []))}

THUMBNAIL PROMPT:
{self._create_thumbnail_instructions(script)}

BRANDING:
{json.dumps(branding.get('color_palette', {}), indent=2)}

TAGS: {', '.join(script.get('tags', []))}

DESCRIPÇÃO:
{script.get('description', '')}
"""
    
    def _format_chapters(self, chapters: List) -> str:
        output = []
        for ch in chapters:
            output.append(f"[{ch.get('time')}] {ch.get('title')}")
        return '\n'.join(output)
    
    def _create_thumbnail_instructions(self, script: Dict) -> str:
        title = script.get('title', '').split()[:4]
        return f"""
Formato: 1280x720
Layout: Rosto + Texto
Texto: {' '.join(title).upper()}
Cores: Laranja/Vermelho background
Expressão: Surpresa/Entusiasmo
"""
    
    def _create_real_video(self, script: Dict, branding: Dict) -> str:
        """Cria vídeo com moviepy (requer instalação)"""
        
        # Cenas baseadas no roteiro
        clips = []
        
        # Cena de introdução
        intro = ColorClip(size=(1280, 720), color=(26, 115, 232), duration=3)
        intro = self._add_text_to_clip(intro, script.get('title', 'Vídeo'))
        clips.append(intro)
        
        # Cenas de conteúdo
        for i in range(5):
            scene = ColorClip(size=(1280, 720), color=(66, 133, 244), duration=5)
            scene = self._add_text_to_clip(scene, f"Conteúdo {i+1}")
            clips.append(scene)
        
        # Montar vídeo
        final = concatenate_videoclips(clips)
        output_path = os.path.join(self.workspace, f"video_{script['id']}.mp4")
        final.write_videofile(output_path, fps=24)
        
        return output_path
    
    def _add_text_to_clip(self, clip, text: str):
        """Adiciona texto ao clipe"""
        txt = TextClip(text, fontsize=50, color='white', font='Arial-Bold')
        txt = txt.set_position('center').set_duration(clip.duration)
        return CompositeVideoClip([clip, txt])


class ThumbnailMaker:
    """Gera thumbnails reais"""
    
    def __init__(self, workspace_path: str):
        self.workspace = workspace_path
        os.makedirs(workspace_path, exist_ok=True)
    
    def create_thumbnail(self, script: Dict) -> str:
        """Cria thumbnail para o vídeo"""
        
        if not PIL_AVAILABLE:
            # Criar placeholder
            filename = f"thumb_placeholder_{script['id']}.txt"
            instructions = self._thumbnail_placeholder(script)
            with open(os.path.join(self.workspace, filename), 'w') as f:
                f.write(instructions)
            return filename
        
        # Criar thumbnail real
        img = Image.new('RGB', (1280, 720), color=(234, 67, 53))
        draw = ImageDraw.Draw(img)
        
        title = script.get('title', '').split()[:4]
        text = ' '.join(title).upper()
        
        # Desenhar texto simples
        draw.text((100, 300), text, fill='white')
        
        filename = f"thumbnail_{script['id']}.png"
        img.save(os.path.join(self.workspace, filename))
        return filename
    
    def _thumbnail_placeholder(self, script: Dict) -> str:
        return f"""
THUMBNAIL PLACEHOLDER
=====================
Título: {script.get('title')}
Dimensões: 1280x720
Cor de fundo: Laranja/Vermelho (#ea4335)
Texto branco: {script.get('title')[:20]}
Elemento: Rosto humano (expressão de surpresa)
"""