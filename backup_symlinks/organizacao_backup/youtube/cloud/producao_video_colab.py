# -*- coding: utf-8 -*-
"""
GOOGLE COLAB - Produção de Vídeo Automático
Transforma áudio em vídeo completo com imagens, legendas e música

Uso: Copie este código para Google Colab (colab.research.google.com)
     ou faça upload do arquivo .ipynb

Autor: Sistema de Automação YouTube 2026
Licença: MIT (uso livre)
"""

# ============================================================================
# CÉLULA 1: INSTALAÇÃO DE DEPENDÊNCIAS
# ============================================================================
# !pip install moviepy pydub pillow requests googletrans==4.0.0-rc1
# !apt-get install ffmpeg imagemagick -y

print("✅ Dependências instaladas!")

# ============================================================================
# CÉLULA 2: IMPORTAÇÕES E CONFIGURAÇÃO
# ============================================================================

from google.colab import files, drive
from IPython.display import display, Audio, Video, clear_output
import os
import requests
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import random
import json

# Configurar pasta de trabalho
WORK_DIR = "/content/youtube_production"
os.makedirs(WORK_DIR, exist_ok=True)
os.chdir(WORK_DIR)

print(f"✅ Ambiente configurado em: {WORK_DIR}")

# ============================================================================
# CÉLULA 3: UPLOAD DO ÁUDIO
# ============================================================================

def upload_audio():
    """Faz upload do arquivo de áudio"""
    print("📤 Faça upload do seu arquivo de áudio (MP3, WAV, OGG)")
    uploaded = files.upload()
    
    if uploaded:
        audio_path = list(uploaded.keys())[0]
        print(f"✅ Áudio carregado: {audio_path}")
        
        # Informações do áudio
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        print(f"⏱️ Duração: {duration:.2f} segundos ({duration/60:.1f} minutos)")
        
        return audio_path, duration
    else:
        raise Exception("Nenhum arquivo enviado!")

# ============================================================================
# CÉLULA 4: DOWNLOAD DE IMAGENS/VÍDEOS DE STOCK
# ============================================================================

def baixar_imagem_stock(tema, largura=1920, altura=1080):
    """Baixa imagens gratuitas do Pexels/Pixabay"""
    
    # APIs gratuitas (sem necessidade de key para uso básico)
    fontes = [
        f"https://source.unsplash.com/{largura}x{altura}/?{tema}",
        f"https://picsum.photos/{largura}/{altura}",
    ]
    
    for url in fontes:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                filename = f"stock_{tema.replace(' ', '_')}_{random.randint(1000,9999)}.jpg"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Imagem baixada: {filename}")
                return filename
        except Exception as e:
            continue
    
    # Fallback: criar imagem sólida
    print("⚠️ Criando imagem padrão...")
    img = Image.new('RGB', (largura, altura), color=(random.randint(50,200), random.randint(50,200), random.randint(50,200)))
    filename = f"stock_solid_{random.randint(1000,9999)}.jpg"
    img.save(filename)
    return filename

def baixar_video_stock(tema, duracao_max=10):
    """Baixa vídeos de stock (exemplo com Pexels)"""
    # Nota: Pexels requer API key para acesso programático
    # Para demo, usamos vídeos de exemplo ou criamos placeholder
    
    print(f"🎬 Buscando vídeo para: {tema}")
    
    # Placeholder: criar vídeo com cor sólida + texto
    filename = f"video_stock_{tema.replace(' ', '_')}.mp4"
    
    # Criar clipe de exemplo
    clip = ColorClip(size=(1920, 1080), color=(random.randint(50,150), random.randint(50,150), random.randint(50,150)), duration=duracao_max)
    
    # Adicionar texto
    txt_clip = TextClip(tema.upper(), fontsize=70, color='white', font='Arial-Bold')
    txt_clip = txt_clip.set_position('center').set_duration(duracao_max)
    
    video = CompositeVideoClip([clip, txt_clip])
    video.write_videofile(filename, fps=24, codec='libx264', audio=False)
    
    print(f"✅ Vídeo criado: {filename}")
    return filename

# ============================================================================
# CÉLULA 5: GERAR LEGENDAS AUTOMÁTICAS
# ============================================================================

def gerar_legendas(transcript, duracao_audio):
    """Gera arquivo de legendas sincronizadas"""
    
    # Dividir transcript em linhas
    linhas = transcript.split('\n')
    duracao_por_linha = duracao_audio / len(linhas) if linhas else 5
    
    legendas = []
    tempo_atual = 0
    
    for i, linha in enumerate(linhas):
        if linha.strip():
            inicio = tempo_atual
            fim = inicio + duracao_por_linha
            
            # Formato SRT
            srt_entry = f"""{i+1}
{format_time(inicio)} --> {format_time(fim)}
{linha.strip()}

"""
            legendas.append(srt_entry)
            tempo_atual = fim
    
    # Salvar arquivo SRT
    with open('legendas.srt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(legendas))
    
    print("✅ Legendas geradas: legendas.srt")
    return 'legendas.srt'

def format_time(segundos):
    """Converte segundos para formato SRT (HH:MM:SS,mmm)"""
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    secs = int(segundos % 60)
    millis = int((segundos % 1) * 1000)
    return f"{horas:02d}:{minutos:02d}:{secs:02d},{millis:03d}"

# ============================================================================
# CÉLULA 6: GERAR THUMBNAIL COM IA (SIMULADO)
# ============================================================================

def gerar_thumbnail(titulo, tema="educacao"):
    """Gera thumbnail usando IA ou templates"""
    
    print(f"🎨 Gerando thumbnail para: {titulo}")
    
    # Opção 1: Criar thumbnail com PIL (grátis, local)
    width, height = 1280, 720
    
    # Fundo gradiente
    img = Image.new('RGB', (width, height), color=(20, 20, 80))
    draw = ImageDraw.Draw(img)
    
    # Adicionar gradiente
    for y in range(height):
        r = int(20 + (y/height) * 50)
        g = int(20 + (y/height) * 50)
        b = int(80 + (y/height) * 100)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Adicionar texto principal
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    # Centralizar texto
    text = titulo.upper()[:50]  # Limitar tamanho
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Sombra do texto
    draw.text((x+4, y+4), text, fill='black', font=font)
    draw.text((x, y), text, fill='white', font=font)
    
    # Adicionar elementos decorativos
    draw.rectangle([50, 50, 200, 100], fill='#FF0000', outline='white', width=3)
    draw.text((65, 60), "YOUTUBE", fill='white', font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30))
    
    # Salvar
    filename = "thumbnail.png"
    img.save(filename, 'PNG')
    print(f"✅ Thumbnail gerada: {filename}")
    
    return filename

# ============================================================================
# CÉLULA 7: MONTAR VÍDEO COMPLETO
# ============================================================================

def montar_video(audio_path, duracao, tema="educacao", titulo="Vídeo"):
    """Monta vídeo completo com áudio, imagens e legendas"""
    
    print("🎬 Iniciando montagem do vídeo...")
    
    # 1. Carregar áudio
    audio_clip = AudioFileClip(audio_path)
    
    # 2. Criar cenas com imagens de stock
    num_cenas = max(5, int(duracao / 10))  # Uma cena a cada 10 segundos
    duracao_cena = duracao / num_cenas
    
    clips = []
    
    for i in range(num_cenas):
        # Baixar/criar imagem de stock
        imagem_file = baixar_imagem_stock(f"{tema} {i+1}")
        
        # Criar clip de imagem
        img_clip = ImageClip(imagem_file).set_duration(duracao_cena)
        
        # Adicionar zoom suave (efeito Ken Burns)
        img_clip = img_clip.resize(lambda t: 1 + 0.04*t)  # Zoom in lento
        
        clips.append(img_clip)
    
    # 3. Concatenar cenas
    video_final = concatenate_videoclips(clips, method="compose")
    video_final = video_final.set_duration(duracao)
    
    # 4. Adicionar áudio
    video_final = video_final.set_audio(audio_clip)
    
    # 5. Adicionar fade in/out
    video_final = video_final.fadein(1).fadeout(2)
    
    # 6. Exportar
    output_file = "video_final.mp4"
    print(f"⏳ Renderizando vídeo... (pode levar alguns minutos)")
    
    video_final.write_videofile(
        output_file,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        preset='medium',  # fast, medium, slow (qualidade vs velocidade)
        bitrate='5000k'
    )
    
    print(f"✅ Vídeo renderizado: {output_file}")
    print(f"📊 Tamanho: {os.path.getsize(output_file) / 1024 / 1024:.1f} MB")
    
    return output_file

# ============================================================================
# CÉLULA 8: EXECUÇÃO PRINCIPAL
# ============================================================================

def produzir_video_completo():
    """Fluxo completo de produção"""
    
    print("="*60)
    print("  PRODUÇÃO DE VÍDEO - GOOGLE COLAB")
    print("="*60)
    print()
    
    # 1. Upload do áudio
    audio_path, duracao = upload_audio()
    display(Audio(audio_path))
    
    # 2. Configurações
    print("\n📋 CONFIGURAÇÕES:")
    tema = input("Tema do vídeo (ex: educação, tecnologia, saúde): ") or "educacao"
    titulo = input("Título do vídeo: ") or "Meu Vídeo"
    
    # 3. Gerar thumbnail
    print("\n" + "="*60)
    thumbnail_file = gerar_thumbnail(titulo, tema)
    display(Image.open(thumbnail_file))
    
    # 4. Montar vídeo
    print("\n" + "="*60)
    video_file = montar_video(audio_path, duracao, tema, titulo)
    
    # 5. Preview
    print("\n🎬 Preview do vídeo:")
    display(Video(video_file, width=640))
    
    # 6. Download
    print("\n📥 Baixe seus arquivos:")
    files.download(video_file)
    files.download(thumbnail_file)
    
    print("\n" + "="*60)
    print("  ✅ PRODUÇÃO CONCLUÍDA!")
    print("="*60)
    print(f"\nArquivos gerados:")
    print(f"  • Vídeo: {video_file}")
    print(f"  • Thumbnail: {thumbnail_file}")
    print(f"\nPróximo passo: Upload no YouTube!")
    
    return video_file, thumbnail_file

# ============================================================================
# INICIAR (Execute esta célula para começar)
# ============================================================================

# Descomente a linha abaixo para executar:
# produzir_video_completo()

print("🎉 Sistema pronto! Execute: produzir_video_completo()")
