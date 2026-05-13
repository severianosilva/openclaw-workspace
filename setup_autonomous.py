#!/usr/bin/env python3
"""
🔧 CONFIGURAÇÃO AUTOMÁTICA - YouTube Autonomous System
Configura credenciais e scheduler para autonomia total
"""

import os
import json
from pathlib import Path

BASE_DIR = Path(r"C:\Users\User\.openclaw\workspace")
CONFIG_FILE = BASE_DIR / "autonomous_config.json"

def setup_youtube_api():
    """Configura credenciais YouTube API"""
    
    print("="*60)
    print("CONFIGURANDO YOUTUBE API")
    print("="*60)
    
    # Instruções para obter credenciais
    steps = """
PASSO A PASSO PARA YOUTUBE API:

1. Acesse: https://console.cloud.google.com/
2. Crie projeto novo ou selecione existente
3. Ative APIs:
   - YouTube Data API v3
   - YouTube Analytics API
4. Crie credenciais OAuth 2.0:
   - Tipo: Desktop App
   - Baixe JSON como 'client_secret.json'
5. Salve em: credentials/client_secret.json
    """
    
    print(steps)
    
    return {
        "youtube_api_configured": False,
        "setup_instructions": steps.strip()
    }

def setup_scheduler():
    """Configura scheduler automático"""
    
    print("\n" + "="*60)
    print("CONFIGURANDO SCHEDULER")
    print("="*60)
    
    scheduler_script = BASE_DIR / "youtube_scheduler.bat"
    
    content = """@echo off
REM YouTube Autonomous Scheduler
REM Executa automaticamente todos os dias às 09:00

:loop
echo [%date% %time%] Verificando agendamento...

REM Verifica se é hora de rodar (09:00)
for /f "tokens=1-2 delims=: " %%a in ('time /t') do (
    set hour=%%a
)

if "%hour%"=="9" (
    echo Iniciando geração automática...
    python "C:\Users\User\.openclaw\workspace\run_autonomous.py"
    timeout /t 3600 /nobreak >nul
) else (
    timeout /t 300 /nobreak >nul
)

goto loop
"""
    
    with open(scheduler_script, 'w') as f:
        f.write(content)
    
    print(f"[OK] Scheduler criado: {scheduler_script}")
    
    # Task Scheduler do Windows
    scheduler_result = {
        "method": "windows_task_scheduler",
        "auto_start": True,
        "time": "09:00",
        "frequency": "daily",
        "script": str(scheduler_script)
    }
    
    return scheduler_result

def create_credentials_template():
    """Cria template de credenciais"""
    
    creds_dir = BASE_DIR / "credentials"
    creds_dir.mkdir(exist_ok=True)
    
    template = {
        "youtube": {
            "client_id": "SEU_CLIENT_ID",
            "client_secret": "SEU_CLIENT_SECRET",
            "api_key": "SUA_API_KEY"
        },
        "elevenlabs": {
            "api_key": "SUA_ELEVENLABS_KEY"
        }
    }
    
    template_file = creds_dir / "credentials_template.json"
    with open(template_file, 'w') as f:
        json.dump(template, f, indent=2)
    
    print(f"[OK] Template de credenciais: {template_file}")
    
    return str(template_file)

def main():
    """Configuração completa"""
    
    print("="*60)
    print("CONFIGURAÇÃO AUTÔNOMA YOUTUBE - INICIANDO")
    print("="*60)
    
    # 1. Credenciais
    youtube_config = setup_youtube_api()
    
    # 2. Scheduler
    scheduler_config = setup_scheduler()
    
    # 3. Template credenciais
    creds_template = create_credentials_template()
    
    # 4. Config final
    autonomous_config = {
        "status": "configured",
        "youtube_api": youtube_config,
        "scheduler": scheduler_config,
        "credentials_template": creds_template,
        "next_steps": [
            "1. Baixar client_secret.json do Google Cloud",
            "2. Salvar em credentials/client_secret.json", 
            "3. Executar: python authenticate_youtube.py (uma vez)",
            "4. Ativar scheduler no Windows Task Scheduler"
        ]
    }
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(autonomous_config, f, indent=2)
    
    print("\n" + "="*60)
    print("CONFIGURAÇÃO CONCLUÍDA!")
    print("="*60)
    
    print("\nPróximos passos:")
    for step in autonomous_config["next_steps"]:
        print(f"  {step}")
    
    print(f"\nArquivo de configuração: {CONFIG_FILE}")

if __name__ == "__main__":
    main()