#!/usr/bin/env python3
"""Demo rapido do pipeline YouTube"""

import json
import os

# 1. Mostrar roteiro gerado
script_file = r"C:\Users\User\organizacao\youtube\roteiros\roteiro_como_ganhar_dinheiro_online_em_2026.json"

with open(script_file, 'r', encoding='utf-8') as f:
    script = json.load(f)

print("="*60)
print("DEMO PIPELINE YOUTUBE AUTOMATIZADO")
print("="*60)

print(f"\n[Titulo] {script['titulo']}")
print(f"[Nicho] {script['nicho']}")
print(f"[Score] {script['score_viabilidade']}/10")

# 2. Mostrar estrutura do vídeo
print("\n[Estrutura do Video]")
print(f"  Hook (0:00-0:05): {script['estrutura']['hook_0_5s']['sugestao'][:50]}...")
print(f"  Intro (0:05-0:30): {script['estrutura']['intro_5_30s']['sugestao'][:50]}...")

# 3. Pontos principais
print("\n[Pontos Principais]")
for ponto in script['estrutura']['conteudo_principal']['pontos']:
    print(f"  Ponto {ponto['ponto']}: {ponto['titulo']}")

# 4. Simular geração de áudio
print("\n[Gerando audio TTS com gTTS...]")
try:
    from gtts import gTTS
    
    # Texto de narração combinado
    narration = script['estrutura']['hook_0_5s']['sugestao'] + " "
    narration += script['estrutura']['intro_5_30s']['sugestao'] + " "
    
    for ponto in script['estrutura']['conteudo_principal']['pontos']:
        narration += f"Ponto {ponto['ponto']}: {ponto['titulo']}. "
    
    # Gerar áudio
    tts = gTTS(text=narration, lang='pt', slow=False)
    output_path = r"C:\Users\User\.openclaw\workspace\demo_audio.mp3"
    tts.save(output_path)
    print(f"[OK] Audio salvo: {output_path}")
except Exception as e:
    print(f"[Erro] {e}")

# 5. Simular imagens
print("\n[Gerando imagens de cena...]")
import random
import requests

img_dir = r"C:\Users\User\.openclaw\workspace\demo_images"
os.makedirs(img_dir, exist_ok=True)

for i, ponto in enumerate(script['estrutura']['conteudo_principal']['pontos']):
    try:
        url = f"https://picsum.photos/1920/1080?random={random.randint(1,1000)}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            with open(f"{img_dir}/cena_{i+1}.jpg", 'wb') as f:
                f.write(response.content)
            print(f"[OK] Cena {i+1} criada")
    except Exception as e:
        print(f"[Erro] Cena {i+1}: {e}")

print("\n" + "="*60)
print("DEMO CONCLUIDA!")
print("="*60)
print("\nPróximos passos:")
print("1. Abra Google Colab: youtube_video_agent/workflow_video_cloud.ipynb")
print("2. Faça upload dos arquivos gerados")
print("3. Execute a renderização final")
print("\nArquivos prontos em:")
print(f"  Audio: {output_path}")
print(f"  Imagens: {img_dir}/")