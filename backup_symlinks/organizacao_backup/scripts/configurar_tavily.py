#!/usr/bin/env python3
"""Configurar Tavily Web Search"""

import json

CONFIG_PATH = "/home/severosa/.openclaw/openclaw.json"

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

# Configurar Tavily
config['tools'] = {
    "web": {
        "enabled": True,
        "provider": "tavily",
        "tavily": {
            "apiKey": "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",
            "maxResults": 5,
            "includeAnswer": True,
            "includeImages": False,
            "searchDepth": "basic"
        }
    }
}

with open(CONFIG_PATH, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Tavily configurado!")
print("📊 Limite: 1.000 requests/mês (plano gratuito)")
print("🔍 Comandos disponíveis: /search, /research")
