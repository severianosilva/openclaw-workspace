#!/bin/bash
# Script de configuração da integração NotebookLM + OpenClaw + Cloud Storage

echo "=========================================="
echo "  CONFIGURAÇÃO NOTEBOOKLM + OPENC LAW"
echo "  + Cloud Storage (Lark, Baidu, etc.)"
echo "=========================================="
echo ""

# Criar diretório
INTEGRATION_DIR="$HOME/organizacao/notebooklm_integration"
mkdir -p "$INTEGRATION_DIR"
echo "✅ Diretório: $INTEGRATION_DIR"

# Criar arquivo .env
ENV_FILE="$INTEGRATION_DIR/.env"
cat > "$ENV_FILE" << 'EOF'
# ===========================================
# NOTEBOOKLM (Google)
# ===========================================
# Obter em: https://notebooklm.google.com
NOTEBOOKLM_API_KEY=sua_chave_aqui
NOTEBOOKLM_EMAIL=seu_email@gmail.com

# ===========================================
# LARK (200 GB Grátis)
# ===========================================
# Obter em: https://open.larksuite.com/
LARK_APP_ID=cli_xxxxxxxxxxxxx
LARK_APP_SECRET=xxxxxxxxxxxxxxxxxxxxx
LARK_REDIRECT_URI=https://seu-dominio.com/callback

# ===========================================
# BAIDU YUN PAN (2 TB Grátis)
# ===========================================
# Obter em: https://pan.baidu.com/union/console
BAIDU_ACCESS_TOKEN=seu_access_token
BAIDU_API_KEY=sua_api_key
BAIDU_SECRET_KEY=seu_secret_key

# ===========================================
# OUTROS SERVIÇOS (Opcional)
# ===========================================
# Google Drive
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REFRESH_TOKEN=

# MEGA (20 GB)
MEGA_EMAIL=
MEGA_PASSWORD=

# pCloud (10 GB)
PCLOUD_CLIENT_ID=
PCLOUD_CLIENT_SECRET=
EOF

echo "✅ Arquivo .env criado: $ENV_FILE"
echo ""

# Instruções
cat << 'INSTRUCOES'

===========================================
  PRÓXIMOS PASSOS
===========================================

📝 1. PREENCHA AS CREDENCIAIS NO .env

Edite o arquivo: nano ~/organizacao/notebooklm_integration/.env

---

🔑 2. COMO OBTER CADA CREDENCIAL

### NOTEBOOKLM (Google)
1. Acesse: https://notebooklm.google.com
2. Faça login com Google
3. Crie um notebook de teste
4. Verifique se há opção "API" ou "Developers"
5. Se não tiver API pública, use via web scraping

### LARK (200 GB Grátis)
1. Acesse: https://open.larksuite.com/
2. Clique "Create App"
3. Preencha informações do app
4. Copie App ID e App Secret
5. Adicione ao .env

### BAIDU YUN PAN (2 TB Grátis)
1. Acesse: https://pan.baidu.com/union/console
2. Faça login (pode precisar de VPN)
3. Crie um app
4. Obtenha API Key e Secret
5. Autorize via OAuth para obter access_token
6. Adicione ao .env

---

🧪 3. TESTE AS INTEGRAÇÕES

# Testar Lark
cd ~/organizacao/notebooklm_integration
python3 storage_lark.py

# Testar Baidu
python3 storage_baidu.py

# Testar NotebookLM (quando API disponível)
python3 notebooklm_client.py

---

📚 4. DOCUMENTAÇÃO COMPLETA

Leia: ~/organizacao/notebooklm_integration/README.md

===========================================

INSTRUCOES

# Criar script de teste rápido
TEST_FILE="$INTEGRATION_DIR/testar_tudo.py"
cat > "$TEST_FILE" << 'TESTEOF'
#!/usr/bin/env python3
"""Teste rápido de todas as integrações"""

import sys
sys.path.insert(0, '/home/severosa/organizacao/notebooklm_integration')

from dotenv import load_dotenv
load_dotenv()

print("="*50)
print("  TESTE DE INTEGRAÇÕES")
print("="*50)

# Testar Lark
print("\n🔵 LARK (200 GB)")
try:
    from storage_lark import LarkStorage
    lark = LarkStorage()
    if lark.autenticar():
        print("  ✅ Autenticação OK")
        espaco = lark.espaco_usado()
        print(f"  💾 Espaço: {espaco['total']} grátis")
    else:
        print("  ⚠️  Configure credenciais no .env")
except Exception as e:
    print(f"  ❌ Erro: {e}")

# Testar Baidu
print("\n🔴 BAIDU YUN PAN (2 TB)")
try:
    from storage_baidu import BaiduStorage
    baidu = BaiduStorage()
    if baidu.access_token:
        print("  ✅ Token configurado")
        espaco = baidu.espaco_usado()
        if "erro" not in espaco:
            print(f"  💾 Espaço: {espaco['total']} total")
    else:
        print("  ⚠️  Configure BAIDU_ACCESS_TOKEN no .env")
except Exception as e:
    print(f"  ❌ Erro: {e}")

print("\n" + "="*50)
print("  TESTE CONCLUÍDO")
print("="*50)
TESTEOF

chmod +x "$TEST_FILE"
echo "✅ Script de teste criado: $TEST_FILE"

echo ""
echo "=========================================="
echo "  CONFIGURAÇÃO PRONTA!"
echo "=========================================="
echo ""
echo "Agora edite o .env com suas credenciais:"
echo "  nano $ENV_FILE"
echo ""
echo "Depois teste:"
echo "  python3 $TEST_FILE"
echo ""
echo "=========================================="
