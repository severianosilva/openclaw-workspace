#!/usr/bin/env python3
"""Instalador automático do CrewAI para YouTube Agents"""

import subprocess
import sys
from pathlib import Path

def install_dependencies():
    """Instala todas as dependências necessárias"""
    
    packages = [
        "crewai>=0.22.0",
        "langchain>=0.1.0", 
        "langchain-openai>=0.0.2",
        "python-dotenv>=1.0.0",
        "pillow>=10.0.0",
        "moviepy>=1.0.3",
        "ffmpeg-python>=0.2.0",
        "google-api-python-client>=2.100.0",
        "google-auth-httplib2>=0.2.0",
        "google-auth-oauthlib>=1.2.0"
    ]
    
    print("=" * 50)
    print("INSTALANDO DEPENDÊNCIAS CREWAI")
    print("=" * 50)
    
    for pkg in packages:
        print(f"\nInstalando: {pkg}")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", pkg], check=True)
        except subprocess.CalledProcessError:
            print(f"[AVISO] Falha ao instalar {pkg}")
    
    print("\n[OK] Instalação concluída!")

def create_env_file():
    """Cria arquivo .env para configurações"""
    
    env_content = """# YouTube Money Agents - Configurações
OPENAI_API_KEY=sk-your-key-here
YOUTUBE_API_KEY=your-youtube-api-key
YOUTUBE_CLIENT_ID=your-client-id
YOUTUBE_CLIENT_SECRET=your-client-secret

# Configurações
NITCHY_KEYWORDS=financas,investimento,cripto
DEFAULT_CPM=25.50
VIDEO_DURATION=8
"""
    
    env_path = Path(__file__).parent / ".env"
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print(f"[OK] Arquivo .env criado em {env_path}")

if __name__ == "__main__":
    install_dependencies()
    create_env_file()
    
    print("\n" + "=" * 50)
    print("PRÓXIMOS PASSOS")
    print("=" * 50)
    print("1. Editar .env com sua API key")
    print("2. python crewai_agents.py")
    print("3. Aguardar produção automática")