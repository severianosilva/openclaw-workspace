#!/usr/bin/env python3
"""YouTube Agents - Produção para Nuvem (Free Tier)"""

import os
from pathlib import Path

# Usar APIs grátis
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")
HF_TOKEN = os.getenv("HF_TOKEN", "")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

BASE_DIR = Path(__file__).parent

def get_config():
    """Configuração para nuvem"""
    return {
        "llm": {
            "provider": "groq",  # Grátis até 14.400 tokens/dia
            "model": "llama3-8b-8192",
            "api_key": GROQ_API_KEY
        },
        "tts": {
            "provider": "huggingface",  # Grátis
            "voice": "pt-BR-faber"
        },
        "storage": {
            "type": "github",
            "repo": "youtube-money-agents/videos"
        },
        "schedule": {
            "frequency": "3x per week",
            "times": ["18:00"]
        }
    }

def create_github_workflow():
    """Cria workflow GitHub Actions"""
    
    workflow = """name: YouTube Money Agents

on:
  schedule:
    - cron: '0 21 * * 1,3,5'  # Seg, Qua, Sex 21h UTC (18h BR)
  workflow_dispatch:

jobs:
  produce-video:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install FFmpeg
      run: |
        sudo apt-get update
        sudo apt-get install -y ffmpeg
    
    - name: Install Dependencies
      run: |
        pip install groq together pillow moviepy python-dotenv google-api-python-client
    
    - name: Run Agent Production
      env:
        GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
        YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
      run: |
        python cloud_production.py
    
    - name: Commit Output
      run: |
        git config --global user.name 'youtube-bot'
        git config --global user.email 'bot@github.com'
        git add output/
        git commit -m "Add new video content" || exit 0
        git push
"""
    
    workflow_path = BASE_DIR / ".github" / "workflows" / "youtube-bot.yml"
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(workflow_path, 'w') as f:
        f.write(workflow)
    
    return workflow_path

if __name__ == "__main__":
    path = create_github_workflow()
    print(f"[OK] Workflow criado: {path}")
    print("\nPróximos passos:")
    print("1. git push origin main")
    print("2. Configure secrets no GitHub:")
    print("   - GROQ_API_KEY")
    print("   - YOUTUBE_API_KEY")