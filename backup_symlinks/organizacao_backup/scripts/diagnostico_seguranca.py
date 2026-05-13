#!/usr/bin/env python3
"""
DIAGNÓSTICO DE SEGURANÇA CRÍTICA
Verifica configurações incorretas que podem causar envio de dados para números errados
"""

import json
import os
import glob

CONFIG_PATH = "/home/severosa/.openclaw/openclaw.json"
WORKSPACE_PATH = "/home/severosa/.openclaw/workspace"

print("=" * 70)
print("🔍 DIAGNÓSTICO DE SEGURANÇA - OpenClaw")
print("=" * 70)

# Carregar configuração
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

SEU_NUMERO = "+5531982436396"
problemas = []

print(f"\n📱 NÚMERO ESPERADO: {SEU_NUMERO}")
print("-" * 70)

# 1. Verificar WhatsApp
print("\n🟢 VERIFICANDO WHATSAPP...")
whatsapp_config = config.get('channels', {}).get('whatsapp', {})

print(f"   dmPolicy: {whatsapp_config.get('dmPolicy')}")
print(f"   allowFrom: {whatsapp_config.get('allowFrom')}")
print(f"   groupPolicy: {whatsapp_config.get('groupPolicy')}")

if whatsapp_config.get('dmPolicy') != 'pairing':
    problemas.append("❌ WhatsApp dmPolicy deve ser 'pairing'")

if SEU_NUMERO not in whatsapp_config.get('allowFrom', []):
    problemas.append(f"❌ Número {SEU_NUMERO} não está em allowFrom do WhatsApp!")

# 2. Verificar Signal
print("\n🔵 VERIFICANDO SIGNAL...")
signal_config = config.get('channels', {}).get('signal', {})
print(f"   account: {signal_config.get('account')}")

if signal_config.get('account') == SEU_NUMERO:
    print("   ✅ Signal configurado corretamente")
else:
    problemas.append(f"⚠️ Signal account é {signal_config.get('account')}")

# 3. Verificar Telegram
print("\n🟡 VERIFICANDO TELEGRAM...")
telegram_config = config.get('channels', {}).get('telegram', {})
bot_token = telegram_config.get('botToken', '')
if bot_token:
    print(f"   Bot Token: {bot_token[:20]}... (parcial oculto)")
else:
    problemas.append("⚠️ Telegram sem bot token")

# 4. Verificar arquivos de cache/session
print("\n🗂️  VERIFICANDO ARQUIVOS DE CACHE/SESSÃO...")
cache_paths = [
    "/home/severosa/.openclaw/.cache",
    "/home/severosa/.openclaw/session",
    "/home/severosa/.openclaw/temp"
]

for path in cache_paths:
    if os.path.exists(path):
        print(f"   📁 {path} existe")
        # Listar arquivos
        try:
            files = os.listdir(path)[:5]  # Primeiros 5
            for f in files:
                print(f"      - {f}")
        except:
            pass
    else:
        print(f"   ❌ {path} não existe")

# 5. Verificar múltiplas configurações
print("\n🔎 VERIFICANDO CONFIGURAÇÕES DUPLICADAS...")
config_files = glob.glob("/home/severosa/.openclaw/*.json")
print(f"   Arquivos JSON encontrados: {len(config_files)}")
for cf in config_files:
    print(f"   - {os.path.basename(cf)}")

# 6. Verificar gateway
print("\n🌐 VERIFICANDO GATEWAY...")
gateway_config = config.get('gateway', {})
print(f"   modo: {gateway_config.get('mode')}")
print(f"   porta: {gateway_config.get('port')}")
print(f"   bind: {gateway_config.get('bind')}")

# 7. Verificar skills e plugins
print("\n📦 VERIFICANDO SKILLS...")
skills_entries = config.get('skills', {}).get('entries', {})
print(f"   Skills instalados: {len(skills_entries)}")

# 8. Alertas especiais
print("\n" + "=" * 70)
print("🚨 ALERTAS DE SEGURANÇA:")
print("=" * 70)

if problemas:
    for p in problemas:
        print(f"{p}")
else:
    print("✅ Nenhum problema crítico detectado na configuração")

print("\n" + "=" * 70)
print("✅ DIAGNÓSTICO CONCLUÍDO")
print("=" * 70)

# Recomendações
print("\n📋 RECOMENDAÇÕES:")
print("-" * 70)
print("""
1. Se códigos estão indo para outro número:
   → Verifique se há conta antiga em '~/.openclaw/'
   → Delete cache: rm -rf ~/.openclaw/.cache/*
   
2. Para reiniciar pareamento do zero:
   → 'openclaw channels logout --channel whatsapp'
   → 'openclaw channels login --channel whatsapp --account default'
   
3. Verifique se há múltiplos processos do gateway:
   → 'ps aux | grep openclaw-gateway'
   → Mate processos extras: 'pkill -9 openclaw-gateway'
   
4. Reinicie com configuração limpa:
   → 'openclaw gateway stop'
   → 'sleep 5'
   → 'openclaw gateway start'
""")
