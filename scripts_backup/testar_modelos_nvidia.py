#!/usr/bin/env python3
"""Testar todos os modelos NVIDIA configurados"""

import subprocess
import json

modelos = [
    ("nvidia-nim/moonshotai/kimi-k2.5", "Kimi K2.5"),
    ("nvidia-nim/minimax/minimax-m2.1", "MiniMax M2.1"),
    ("nvidia-nim/zai-org/glm-4.7", "GLM 4.7"),
    ("nvidia-nim/deepseek-ai/deepseek-v3.2", "DeepSeek V3.2"),
]

print("🧪 TESTANDO MODELOS NVIDIA NIM")
print("=" * 50)

resultados = []

for model_id, nome in modelos:
    print(f"\n🔄 Testando: {nome}")
    print(f"   ID: {model_id}")
    
    try:
        # Testar com comando openclaw
        cmd = f'openclaw chat --model {model_id} "Qual seu nome?"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and result.stdout:
            print(f"   ✅ SUCESSO: {nome}")
            print(f"   📝 Resposta: {result.stdout[:100]}...")
            resultados.append((nome, "✅ Funcionando"))
        else:
            print(f"   ❌ ERRO: {nome}")
            print(f"   ⚠️  Detalhes: {result.stderr[:100] if result.stderr else 'Sem resposta'}")
            resultados.append((nome, "❌ Falhou"))
            
    except Exception as e:
        print(f"   ❌ EXCEÇÃO: {nome} - {str(e)}")
        resultados.append((nome, "❌ Erro"))

print("\n" + "=" * 50)
print("📊 RESULTADO DOS TESTES:")
print("=" * 50)

for nome, status in resultados:
    print(f"{status} {nome}")

print("\n✅ Testes concluídos!")
