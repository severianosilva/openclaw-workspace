#!/bin/bash
# INSTALADOR DO SISTEMA DE AUDITORIA E SEGURANÇA

echo "🛡️ INSTALADOR DO SISTEMA DE AUDITORIA"
echo "======================================"
echo ""

# Criar diretórios
mkdir -p /home/severosa/organizacao/seguranca/logs
mkdir -p /home/severosa/organizacao/seguranca/backup

# Tornar scripts executáveis
chmod +x /home/severosa/organizacao/seguranca/*.py
chmod +x /home/severosa/organizacao/seguranca/*.sh

echo "📁 Diretórios criados:"
echo "   - /home/severosa/organizacao/seguranca/"
echo "   - /home/severosa/organizacao/seguranca/logs"
echo "   - /home/severosa/organizacao/seguranca/backup"
echo ""

# Verificar Python
echo "🐍 Verificando Python..."
if command -v python3 &> /dev/null; then
    echo "   ✅ Python3 encontrado"
else
    echo "   ❌ Python3 não encontrado!"
    exit 1
fi

echo ""
echo "🔧 FERRAMENTAS INSTALADAS:"
echo "   1. sistema_auditoria.py - Auditoria completa"
echo "   2. monitor_intrusao.py - Monitoramento em tempo real"  
echo "   3. cron_seguranca.sh - Agendamento automático"
echo ""

# Configurar cron (opcional)
echo "📅 CONFIGURAÇÃO DO CRON:"
echo "   Executar: crontab -e"
echo "   Adicionar linha:"
echo "   */6 * * * * /home/severosa/organizacao/seguranca/cron_seguranca.sh"
echo ""

# Teste inicial
echo "🧪 EXECUTANDO TESTE INICIAL..."
python3 /home/severosa/organizacao/seguranca/sistema_auditoria.py

echo ""
echo "======================================"
echo "✅ INSTALAÇÃO CONCLUÍDA!"
echo "======================================"
echo ""
echo "📋 COMANDOS DISPONÍVEIS:"
echo ""
echo "1. Auditoria completa:"
echo "   python3 /home/severosa/organizacao/seguranca/sistema_auditoria.py"
echo ""
echo "2. Monitoramento em tempo real:"
echo "   python3 /home/severosa/organizacao/seguranca/monitor_intrusao.py"
echo ""
echo "3. Verificar logs:"
echo "   ls -la /home/severosa/organizacao/seguranca/logs/"
echo ""
echo "🔒 Sistema blindado e protegido!"
