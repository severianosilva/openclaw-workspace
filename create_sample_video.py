#!/usr/bin/env python3
"""
🎬 Cria vídeo de amostra completo
"""

import json
import os
from pathlib import Path
from gtts import gTTS

BASE_DIR = Path(r"C:\Users\User\.openclaw\workspace")
OUTPUT_DIR = BASE_DIR / "sample_video"
OUTPUT_DIR.mkdir(exist_ok=True)

def create_sample_video():
    print("="*50)
    print("CRIANDO VIDEO DE AMOSTRA")
    print("="*50)
    
    # 1. Roteiro de exemplo
    script = {
        "titulo": "3 Métodos para Ganhar Dinheiro Online em 2026",
        "duracao": "60 segundos",
        "cena_1": {
            "tempo": "0-10s",
            "texto": "Você já pensou em ganhar dinheiro sem sair de casa?",
            "imagem": "home office"
        },
        "cena_2": {
            "tempo": "10-30s",
            "texto": "Método 1: Freelance em alta demanda. Método 2: Afiliados. Método 3: Cursos digitais.",
            "imagem": "trabalho online"
        },
        "cena_3": {
            "tempo": "30-60s",
            "texto": "Comece hoje! Inscreva-se e ative o sininho.",
            "imagem": "inscrição"
        }
    }
    
    # 2. Áudio
    print("[1/3] Gerando áudio...")
    audio_text = f"{script['cena_1']['texto']} {script['cena_2']['texto']} {script['cena_3']['texto']}"
    tts = gTTS(text=audio_text, lang='pt', slow=False)
    audio_path = OUTPUT_DIR / "sample_audio.mp3"
    tts.save(str(audio_path))
    print(f"    [OK] {audio_path}")
    
    # 3. Imagens
    print("[2/3] Gerando imagens...")
    import requests
    images = []
    queries = ["home office", "freelance work", "digital marketing"]
    
    for i, q in enumerate(queries):
        try:
            url = f"https://picsum.photos/1280/720?random={i+100}"
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                path = OUTPUT_DIR / f"sample_{i}.jpg"
                with open(path, 'wb') as f:
                    f.write(r.content)
                images.append(str(path))
                print(f"    [OK] {path.name}")
        except Exception as e:
            print(f"    [ERRO] {e}")
    
    # 4. Arquivo final
    print("[3/3] Criando pacote...")
    sample = {
        "script": script,
        "audio": str(audio_path),
        "images": images,
        "ready_for_render": True
    }
    
    output_json = OUTPUT_DIR / "sample_package.json"
    with open(output_json, 'w') as f:
        json.dump(sample, f, indent=2)
    
    print(f"\n[SUCESSO] Vídeo amostra criado!")
    print(f"Diretório: {OUTPUT_DIR}")
    print(f"\nPara renderizar no Colab:")
    print(f"1. Abra: youtube_video_agent/workflow_video_cloud.ipynb")
    print(f"2. Faça upload dos arquivos acima")
    print(f"3. Execute a célula de renderização")
    
    return sample

if __name__ == "__main__":
    create_sample_video()