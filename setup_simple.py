#!/usr/bin/env python3
"""Configuração simples para sistema autônomo"""

import os
import json
from pathlib import Path

BASE_DIR = Path(r"C:\Users\User\.openclaw\workspace")

def main():
    print("="*50)
    print("CONFIGURACAO AUTONOMA YOUTUBE")
    print("="*50)
    
    # 1. Criar pasta credentials
    creds_dir = BASE_DIR / "credentials"
    creds_dir.mkdir(exist_ok=True)
    print(f"[OK] Pasta criada: {creds_dir}")
    
    # 2. Template credenciais
    template = {
        "youtube_client_secret": "COLE_SEU_JSON_AQUI",
        "api_key": "SUA_API_KEY"
    }
    
    template_path = creds_dir / "credentials_template.json"
    with open(template_path, 'w') as f:
        json.dump(template, f, indent=2)
    print(f"[OK] Template: {template_path}")
    
    # 3. Instruções
    print("\n" + "="*50)
    print("PASSOS FINAIS:")
    print("="*50)
    print("1. Acesse: https://console.cloud.google.com/")
    print("2. Crie projeto e ative YouTube Data API v3")
    print("3. Crie credenciais OAuth 2.0 (Desktop)")
    print("4. Baixe client_secret.json")
    print("5. Salve em: credentials/client_secret.json")
    print("6. Execute uma vez: python authenticate.py")
    print("7. Ative o scheduler no Windows")
    
    # 4. Config salva
    config = {
        "status": "setup_pending",
        "scheduler": "youtube_scheduler.bat",
        "credentials_path": str(creds_dir)
    }
    
    config_path = BASE_DIR / "autonomous_config_simple.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n[OK] Configuração salva: {config_path}")

if __name__ == "__main__":
    main()