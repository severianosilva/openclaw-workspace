#!/usr/bin/env python3
import json

CONFIG_PATH = "/home/severosa/.openclaw/openclaw.json"

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

# Remover seção tools vazia
if 'tools' in config:
    del config['tools']
    print("✅ Seção 'tools' vazia removida")

# Salvar configuração corrigida
with open(CONFIG_PATH, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Configuração corrigida com sucesso!")
print("🔄 Reinicie o gateway: openclaw gateway restart")
