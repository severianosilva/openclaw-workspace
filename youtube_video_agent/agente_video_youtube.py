#!/usr/bin/env python3
"""
🤖 Agente de Geração Automática de Vídeos para YouTube

Conecta-se com o agente de roteiros e produz vídeos completos usando APIs gratuitas.

Fluxo:
1. Lê roteiro JSON do agente anterior
2. Gera áudio TTS (gTTS ou ElevenLabs)
3. Cria cenas visuais com stock images
4. Prepara arquivos para renderização no Colab

Autor: Sistema de Automação YouTube 2026
"""

import os
import json
import time
import random
import argparse
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

# TTS Libraries
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Image handling
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    from moviepy.editor import *
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False


class YouTubeVideoAgent:
    """Agente de geração automática de vídeos para YouTube"""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir or os.path.expanduser("~/youtube_production"))
        self.audio_dir = self.output_dir / "audio"
        self.images_dir = self.output_dir / "images"
        self.subtitles_dir = self.output_dir / "subtitles"
        self.scripts_dir = self.output_dir / "scripts"
        
        # Criar diretórios
        for d in [self.audio_dir, self.images_dir, self.subtitles_dir, self.scripts_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        self.config = {
            "tts": {
                "provider": "gtts",
                "language": "pt-BR",
                "slow": False
            },
            "stock": {
                "source": "unsplash",
                "width": 1920,
                "height": 1080
            },
            "video": {
                "fps": 24,
                "codec": "libx264",
                "audio_codec": "aac",
                "bitrate": "5000k"
            }
        }
    
    def load_script(self, script_path: str) -> Dict:
        """Carrega roteiro JSON do agente anterior"""
        print(f"📄 Carregando roteiro: {script_path}")
        
        with open(script_path, 'r', encoding='utf-8') as f:
            script = json.load(f)
        
        print(f"✅ Roteiro carregado: {script['titulo']}")
        return script
    
    def generate_narration_script(self, script: Dict) -> str:
        """Gera texto de narração completo a partir do roteiro"""
        parts = []
        
        # Hook
        parts.append(script['estrutura']['hook_0_5s']['sugestao'])
        
        # Intro
        intro = script['estrutura']['intro_5_30s']['sugestao']
        parts.append(intro)
        
        # Conteúdo principal - extrair pontos
        for ponto in script['estrutura']['conteudo_principal']['pontos']:
            parts.append(f"Ponto {ponto['ponto']}: {ponto['titulo']}")
            for elemento in ponto['elementos']:
                parts.append(elemento)
        
        # Conclusão
        parts.append(script['estrutura']['conclusao']['sugestao'])
        
        # CTA final
        parts.append(script['estrutura']['cta_final']['sugestao'])
        
        return "\n\n".join(parts)
    
    def generate_tts_audio(self, text: str, output_name: str, 
                           provider: str = "gtts", 
                           voice_id: str = None,
                           elevenlabs_api_key: str = None) -> str:
        """Gera áudio usando TTS (gTTS ou ElevenLabs)"""
        
        output_path = self.audio_dir / f"{output_name}.mp3"
        
        if provider == "gtts" and GTTS_AVAILABLE:
            print(f"🔊 Gerando áudio com gTTS...")
            
            # gTTS tem limite de caracteres, dividir em chunks
            max_chars = 10000
            chunks = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
            
            if len(chunks) == 1:
                tts = gTTS(text=text, lang=self.config['tts']['language'], 
                         slow=self.config['tts']['slow'])
                tts.save(str(output_path))
            else:
                # Concatenar múltiplos chunks
                from pydub import AudioSegment
                combined = AudioSegment.empty()
                
                for i, chunk in enumerate(chunks):
                    chunk_path = self.audio_dir / f"temp_chunk_{i}.mp3"
                    tts = gTTS(text=chunk, lang=self.config['tts']['language'], 
                             slow=self.config['tts']['slow'])
                    tts.save(str(chunk_path))
                    combined += AudioSegment.from_mp3(chunk_path)
                    os.remove(chunk_path)
                
                combined.export(output_path, format="mp3")
            
            print(f"✅ Áudio salvo: {output_path}")
            
        elif provider == "elevenlabs" and elevenlabs_api_key:
            print(f"🔊 Gerando áudio com ElevenLabs...")
            
            import elevenlabs
            elevenlabs.set_api_key(elevenlabs_api_key)
            
            audio = elevenlabs.generate(
                text=text,
                voice=voice_id or "Rachel",
                model="eleven_multilingual_v2"
            )
            
            with open(output_path, 'wb') as f:
                f.write(audio)
            
            print(f"✅ Áudio salvo: {output_path}")
        else:
            raise RuntimeError("TTS provider não disponível. Instale gtts ou configure ElevenLabs.")
        
        return str(output_path)
    
    def download_stock_image(self, query: str, width: int = 1920, height: int = 1080) -> str:
        """Baixa imagem de stock (Unsplash ou Picsum)"""
        
        filename = f"stock_{query.replace(' ', '_')}_{random.randint(1000, 9999)}.jpg"
        filepath = self.images_dir / filename
        
        try:
            # Tentar Unsplash Source (grátis, sem API key)
            url = f"https://source.unsplash.com/{width}x{height}/?{query}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Imagem baixada: {filename}")
                return str(filepath)
        except Exception as e:
            print(f"⚠️ Erro no Unsplash: {e}")
        
        # Fallback: Picsum
        try:
            url = f"https://picsum.photos/{width}/{height}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Imagem Picsum: {filename}")
                return str(filepath)
        except Exception as e:
            print(f"⚠️ Erro no Picsum: {e}")
        
        # Fallback final: imagem sólida
        if PIL_AVAILABLE:
            img = Image.new('RGB', (width, height), 
                          color=(random.randint(50, 150), 
                                random.randint(50, 150), 
                                random.randint(50, 150)))
            img.save(filepath)
            print(f"✅ Imagem criada (fallback): {filename}")
            return str(filepath)
        
        raise RuntimeError("Não foi possível baixar ou criar imagem")
    
    def generate_scene_images(self, script: Dict) -> List[str]:
        """Gera imagens para cada cena do vídeo"""
        
        images = []
        nicho = script['nicho']
        
        # Hook image
        hook_img = self.download_stock_image(f"{nicho} hook", 1920, 1080)
        images.append(hook_img)
        
        # Imagem para cada ponto
        for ponto in script['estrutura']['conteudo_principal']['pontos']:
            query = f"{nicho} {ponto['titulo']}"
            img = self.download_stock_image(query, 1920, 1080)
            images.append(img)
        
        # Thumbnail final
        thumb_img = self.download_stock_image(f"{nicho} final", 1280, 720)
        images.append(thumb_img)
        
        print(f"✅ Total de imagens: {len(images)}")
        return images
    
    def generate_subtitles(self, script: Dict, audio_duration: float) -> str:
        """Gera arquivo SRT de legendas sincronizadas"""
        
        lines = []
        segments = []
        
        # Extrair segmentos de texto
        segments.append(script['estrutura']['hook_0_5s']['sugestao'])
        segments.append(script['estrutura']['intro_5_30s']['sugestao'])
        
        for ponto in script['estrutura']['conteudo_principal']['pontos']:
            segments.append(f"{ponto['titulo']}")
        
        time_per_segment = audio_duration / len(segments)
        
        for i, segment in enumerate(segments):
            start_time = i * time_per_segment
            end_time = (i + 1) * time_per_segment
            
            lines.append(f"{i + 1}")
            lines.append(f"{self._format_srt_time(start_time)} --> {self._format_srt_time(end_time)}")
            lines.append(segment)
            lines.append("")
        
        output_path = self.subtitles_dir / f"legendas_{int(time.time())}.srt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ Legendas salvas: {output_path}")
        return str(output_path)
    
    def _format_srt_time(self, seconds: float) -> str:
        """Formata tempo para formato SRT"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def create_colab_package(self, script: Dict, audio_path: str, 
                            image_paths: List[str], subtitle_path: str) -> Dict:
        """Cria pacote de arquivos para upload no Google Colab"""
        
        package = {
            "script": script,
            "audio": {
                "path": audio_path,
                "filename": os.path.basename(audio_path)
            },
            "images": [{"path": p, "filename": os.path.basename(p)} for p in image_paths],
            "subtitles": {
                "path": subtitle_path,
                "filename": os.path.basename(subtitle_path)
            },
            "render_config": self.config['video']
        }
        
        # Salvar manifest
        manifest_path = self.output_dir / "colab_package.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(package, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Pacote Colab criado: {manifest_path}")
        return package
    
    def process_script_to_video(self, script_path: str, 
                               provider: str = "gtts",
                               voice_id: str = None,
                               elevenlabs_key: str = None) -> Dict:
        """Processa roteiro completo e prepara arquivos para renderização"""
        
        print("\n" + "="*60)
        print("  AGENTE DE GERAÇÃO DE VÍDEO YOUTUBE")
        print("="*60)
        
        # 1. Carregar roteiro
        script = self.load_script(script_path)
        
        # 2. Gerar texto de narração
        print("\n📝 Gerando texto de narração...")
        narration = self.generate_narration_script(script)
        print(f"  Caracteres: {len(narration)}")
        
        # 3. Gerar áudio TTS
        print("\n🔊 Gerando áudio TTS...")
        audio_path = self.generate_tts_audio(
            narration, 
            f"audio_{script['titulo'].replace(' ', '_')}",
            provider=provider,
            voice_id=voice_id,
            elevenlabs_api_key=elevenlabs_key
        )
        
        # 4. Gerar imagens de cena
        print("\n🖼️ Gerando imagens de cena...")
        image_paths = self.generate_scene_images(script)
        
        # 5. Gerar legendas
        print("\n💬 Gerando legendas...")
        audio_duration = self._get_audio_duration(audio_path)
        subtitle_path = self.generate_subtitles(script, audio_duration)
        
        # 6. Criar pacote para Colab
        print("\n📦 Preparando pacote para Google Colab...")
        package = self.create_colab_package(script, audio_path, image_paths, subtitle_path)
        
        print("\n" + "="*60)
        print("  ✅ PROCESSAMENTO CONCLUÍDO!")
        print("="*60)
        print(f"\nPróximos passos:")
        print(f"  1. Abra o Google Colab: workflow_video_cloud.ipynb")
        print(f"  2. Faça upload dos arquivos em: {self.output_dir}")
        print(f"  3. Renderize o vídeo final")
        
        return package
    
    def _get_audio_duration(self, audio_path: str) -> float:
        """Obtém duração do áudio"""
        if MOVIEPY_AVAILABLE:
            audio = AudioFileClip(audio_path)
            return audio.duration
        else:
            # Estimativa: ~150 palavras por minuto
            import wave
            with wave.open(audio_path, 'r') as f:
                frames = f.getnframes()
                rate = f.getframerate()
                return frames / rate


def main():
    parser = argparse.ArgumentParser(description="Agente de Geração de Vídeo YouTube")
    parser.add_argument("script", help="Caminho para roteiro JSON")
    parser.add_argument("--tts", choices=["gtts", "elevenlabs"], default="gtts",
                       help="Provedor TTS (padrão: gtts)")
    parser.add_argument("--elevenlabs-key", help="API key da ElevenLabs")
    parser.add_argument("--voice", help="Voice ID da ElevenLabs")
    parser.add_argument("--output", help="Diretório de saída")
    
    args = parser.parse_args()
    
    agent = YouTubeVideoAgent(output_dir=args.output)
    
    result = agent.process_script_to_video(
        script_path=args.script,
        provider=args.tts,
        voice_id=args.voice,
        elevenlabs_key=args.elevenlabs_key
    )
    
    print(f"\n📊 Resumo:")
    print(f"  Áudio: {result['audio']['filename']}")
    print(f"  Imagens: {len(result['images'])} arquivos")
    print(f"  Legendas: {result['subtitles']['filename']}")


if __name__ == "__main__":
    main()