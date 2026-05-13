#!/bin/bash
# LIMPEZA DE SEGURANÇA - WhatsApp Credentials
# Remove todas as credenciais antigas e força novo pareamento

echo "🚨 LIMPEZA DE SEGURANÇA - WhatsApp"
echo "=================================="
echo ""

# Parar gateway
echo "⏹️  Parando gateway..."
openclaw gateway stop 2>/dev/null || pkill -f openclaw-gateway
sleep 3

# Backup das credenciais atuais
echo "💾 Criando backup das credenciais atuais..."
BACKUP_DIR="/home/severosa/.openclaw/credentials/whatsapp/backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r /home/severosa/.openclaw/credentials/whatsapp/default/* "$BACKUP_DIR/" 2>/dev/null
echo "   Backup salvo em: $BACKUP_DIR"

# Limpar credenciais do WhatsApp
echo ""
echo "🧹 Limpando credenciais do WhatsApp..."
rm -rf /home/severosa/.openclaw/credentials/whatsapp/default/*
echo "   ✅ Credenciais removidas"

# Limpar cache de sessão
echo ""
echo "🧹 Limpando cache de sessão..."
rm -rf /home/severosa/.openclaw/.cache/* 2>/dev/null
rm -rf /home/severosa/.openclaw/temp/* 2>/dev/null
echo "   ✅ Cache removido"

# Limpar sessões antigas
echo ""
echo "🧹 Limpando sessões antigas..."
rm -f /home/severosa/.openclaw/agents/main/sessions/*.jsonl 2>/dev/null
echo "   ✅ Sessões removidas"

# Iniciar gateway
echo ""
echo "▶️  Iniciando gateway..."
openclaw gateway start
sleep 5

# Verificar status
echo ""
echo "📊 Verificando status..."
if pgrep -f "openclaw-gateway" > /dev/null; then
    echo "   ✅ Gateway rodando"
else
    echo "   ❌ Gateway NÃO rodando"
fi

echo ""
echo "=================================="
echo "✅ LIMPEZA CONCLUÍDA!"
echo "=================================="
echo ""
echo "📱 PRÓXIMO PASSO - PAREAR WHATSAPP:"
echo ""
echo "1. Execute no terminal:"
echo "   openclaw channels login --channel whatsapp --account default"
echo ""
echo "2. Um código de pareamento será exibido NO TERMINAL"
echo ""
echo "3. Abra WhatsApp no celular → Aparelhos conectados → Conectar dispositivo"
echo ""
echo "4. Escaneie o QR code ou digite o código"
echo ""
echo "⚠️  IMPORTANTE:"
echo "   - O código aparecerá APENAS no terminal"
echo "   - NÃO será enviado por WhatsApp"
echo "   - Isso previne envio para números errados"
echo ""
