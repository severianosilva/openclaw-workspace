#!/usr/bin/env python3
"""
Script para limpar configuração do OpenClaw
- Remove modelos pagos/redundantes
- Configura Tavily para web search
"""

import json
import os

CONFIG_PATH = "/home/severosa/.openclaw/openclaw.json"

def limpar_configuracao():
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    
    # 1. Limpar fallbacks - manter apenas os melhores gratuitos
    config['agents']['defaults']['model']['fallbacks'] = [
        "synthetic/hf:moonshotai/Kimi-K2-Thinking",  # Raciocínio
        "synthetic/hf:deepseek-ai/DeepSeek-V3",      # Código
        "qwen-portal/coder-model"                     # Último recurso
    ]
    
    # 2. Limpar models - manter apenas essenciais
    config['agents']['defaults']['models'] = {
        "nvidia-nim/moonshotai/kimi-k2.5": {"alias": "kimi"},
        "synthetic/hf:moonshotai/Kimi-K2-Thinking": {"alias": "kimi-thinking"},
        "synthetic/hf:deepseek-ai/DeepSeek-V3": {"alias": "deepseek"},
        "qwen-portal/coder-model": {"alias": "qwen"},
        "qwen-portal/vision-model": {"alias": "qwen-vision"}
    }
    
    # 3. Adicionar configuração Tavily para web search
    if 'tools' not in config:
        config['tools'] = {}
    
    config['tools']['web'] = {
        "enabled": True,
        "provider": "tavily",
        "tavily": {
            "apiKey": "tvly-PLACEHOLDER",  # Será atualizado pelo usuário
            "maxResults": 5,
            "includeAnswer": True,
            "searchDepth": "basic"
        }
    }
    
    # 4. Salvar configuração
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuração limpa com sucesso!")
    print("\nModelos mantidos:")
    print("  🎯 Primário: nvidia-nim/moonshotai/kimi-k2.5")
    print("  1️⃣ Fallback: synthetic/hf:moonshotai/Kimi-K2-Thinking")
    print("  2️⃣ Fallback: synthetic/hf:deepseek-ai/DeepSeek-V3")
    print("  3️⃣ Fallback: qwen-portal/coder-model")
    print("\nWeb search configurado (Tavily)")
    print("⚠️  ATENÇÃO: Substitua 'tvly-PLACEHOLDER' pela sua API key do Tavily")

if __name__ == "__main__":
    limpar_configuracao()
