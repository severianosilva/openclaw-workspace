#!/usr/bin/env python3
"""
🤖 YouTube Autonomous Agent - VERSÃO FINAL
100% autônomo - sem intervenção humana!
"""

import json
import os
import time
import random
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"C:\Users\User\.openclaw\workspace")
OUTPUT_DIR = BASE_DIR / "autonomous_output"

# Criar diretório
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_script_autonomous(topic="finanças"):
    """Gera roteiro usando templates pré-configurados"""
    
    templates = {
        "finanças": {
            "titulo": f"Como Ganhar Dinheiro Online - {datetime.now().strftime('%B %Y')}",
            "hook": "Você já gastou dinheiro com cursos que não funcionaram?",
            "pontos": [
                "Método 1: Freelancer de alta demanda",
                "Método 2: Vendas digitais passivas", 
                "Método 3: Afiliados com SEO"
            ]
        },
        "tecnologia": {
            "titulo": f"Tecnologia que vai bombar - {datetime.now().year}",
            "hook": "Estes avanços vão mudar tudo em 2026!",
            "pontos": [
                "AI que todo mundo vai usar",
                "Ferramentas gratuitas poderosas",
                "Como monetizar agora"
            ]
        },
        "educação": {
            "titulo": f"Aprenda em 30 dias - {datetime.now().strftime('%B')}",
            "hook": "Esqueça cursos caros - aprenda grátis!",
            "pontos": [
                "Recursos 100% gratuitos",
                "Plataformas que ninguém conhece",
                "Como praticar sozinho"
            ]
        }
    }
    
    return templates.get(topic, templates["finanças"])

def create_audio_simple(text, output_path):
    """Cria áudio com gTTS"""
    from gtts import gTTS
    tts = gTTS(text=text, lang='pt', slow=False)
    tts.save(output_path)
    return output_path

def download_free_images(search_term, count=5):
    """Baixa imagens grátis"""
    import requests
    
    images = []
    for i in range(count):
        try:
            url = f"https://picsum.photos/1920/1080?random={random.randint(1,1000)}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                path = OUTPUT_DIR / f"image_{i}.jpg"
                with open(path, 'wb') as f:
                    f.write(response.content)
                images.append(str(path))
        except:
            pass
    return images

def create_video_package(topic):
    """Cria pacote completo de vídeo"""
    
    print(f"\n{'='*50}")
    print(f"RODANDO AUTONOMO: {topic.upper()}")
    print(f"{'='*50}")
    
    # 1. Roteiro
    print("[1/4] Gerando roteiro...")
    script = generate_script_autonomous(topic)
    script_path = OUTPUT_DIR / "script.json"
    
    script_data = {
        "titulo": script["titulo"],
        "hook": script["hook"],
        "pontos": script["pontos"],
        "timestamp": datetime.now().isoformat()
    }
    
    with open(script_path, 'w') as f:
        json.dump(script_data, f, indent=2)
    
    # 2. Áudio
    print("[2/4] Criando áudio...")
    text = script["hook"] + " " + " ".join(script["pontos"])
    audio_path = OUTPUT_DIR / "narration.mp3"
    create_audio_simple(text, str(audio_path))
    
    # 3. Imagens
    print("[3/4] Baixando imagens...")
    images = download_free_images(topic, 5)
    
    # 4. Package final
    print("[4/4] Criando pacote...")
    package = {
        "script": script_data,
        "audio": str(audio_path),
        "images": images,
        "timestamp": datetime.now().isoformat()
    }
    
    package_path = OUTPUT_DIR / "video_package.json"
    with open(package_path, 'w') as f:
        json.dump(package, f, indent=2)
    
    print(f"\n[SUCESSO] Pacote criado: {package_path}")
    return package

def main():
    """Loop autônomo"""
    
    topics = ["finanças", "tecnologia", "educação", "saúde"]
    
    print("🤖 YOUTUBE AUTONOMO INICIADO")
    print("Rodando 24/7 sem intervenção humana...")
    
    while True:
        for topic in topics:
            try:
                create_video_package(topic)
            except Exception as e:
                print(f"[ERRO] {e}")
            
            time.sleep(300)  # 5 minutos entre cada tema

if __name__ == "__main__":
    # Roda uma vez para teste
    create_video_package("finanças")