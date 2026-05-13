#!/bin/bash
# Diagnóstico do Sistema OpenClaw

echo "============================================================"
echo "DIAGNÓSTICO DO SISTEMA OPENCLAW"
echo "Data: $(date)"
echo "============================================================"
echo ""

# 1. Status do Gateway
echo "1. STATUS DO GATEWAY"
echo "-----------------------------------------------------------"
pgrep -a openclaw | head -5
if [ $? -eq 0 ]; then
    echo "✅ Gateway está rodando"
else
    echo "❌ Gateway NÃO está rodando"
fi
echo ""

# 2. WhatsApp
echo "2. WHATSAPP"
echo "-----------------------------------------------------------"
if [ -d "/home/severosa/.openclaw/telegram" ]; then
    echo "✅ Pasta Telegram existe"
fi
# Verificar se há configuração do WhatsApp
grep -q "whatsapp" /home/severosa/.openclaw/openclaw.json 2>/dev/null && echo "✅ WhatsApp configurado no openclaw.json" || echo "❌ WhatsApp não configurado"
echo ""

# 3. Browser Extension
echo "3. BROWSER EXTENSION (Chrome)"
echo "-----------------------------------------------------------"
if [ -d "/home/severosa/.npm-global/lib/node_modules/openclaw/extensions/chrome" ]; then
    echo "✅ Extensão Chrome encontrada"
    ls -la /home/severosa/.npm-global/lib/node_modules/openclaw/extensions/chrome/ 2>/dev/null | head -5
else
    echo "⚠️  Extensão Chrome não encontrada em extensions/chrome"
    echo "    Pode estar em outro local ou precisa ser instalada"
fi
echo ""

# 4. Sistema de Áudio
echo "4. SISTEMA DE TRANSCRIÇÃO DE ÁUDIO"
echo "-----------------------------------------------------------"
if [ -f "/home/severosa/organizacao/captura/converter_e_transcrever.py" ]; then
    echo "✅ Script de transcrição existe"
else
    echo "❌ Script de transcrição não encontrado"
fi

if [ -d "/tmp/vosk-model-small-pt-0.3" ]; then
    echo "✅ Modelo Vosk em português presente"
else
    echo "⚠️  Modelo Vosk não encontrado"
fi

python3 -c "import vosk" 2>/dev/null && echo "✅ Vosk instalado" || echo "❌ Vosk não instalado"
python3 -c "import speech_recognition" 2>/dev/null && echo "✅ speech_recognition instalado" || echo "❌ speech_recognition não instalado"
echo ""

# 5. Sistema de Processos Administrativos
echo "5. SISTEMA DE PROCESSOS ADMINISTRATIVOS"
echo "-----------------------------------------------------------"
if [ -d "/home/severosa/organizacao/advocacia/processos-administrativos" ]; then
    echo "✅ Pasta de processos administrativos existe"
    ls /home/severosa/organizacao/advocacia/processos-administrativos/*.py 2>/dev/null | wc -l | xargs -I {} echo "   {} scripts Python encontrados"
else
    echo "❌ Pasta de processos administrativos não encontrada"
fi
echo ""

# 6. Espaço em Disco
echo "6. ESPAÇO EM DISCO"
echo "-----------------------------------------------------------"
df -h /home | tail -1
echo ""

# 7. Memória RAM
echo "7. MEMÓRIA RAM"
echo "-----------------------------------------------------------"
free -h | grep -E "^Mem:"
echo ""

# 8. Processos Recentes com Erro
echo "8. PROCESSOS RECENTES (últimos 5)"
echo "-----------------------------------------------------------"
ps aux --sort=-start_time | grep -E "openclaw|python|node" | head -5
echo ""

echo "============================================================"
echo "DIAGNÓSTICO CONCLUÍDO"
echo "============================================================"
