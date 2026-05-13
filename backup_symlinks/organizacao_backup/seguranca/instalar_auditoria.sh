#!/bin/bash
# INSTALAÇÃO DO SISTEMA DE AUDITORIA DE SEGURANÇA
# Configura auditoria periódica e ferramentas de proteção

echo "🛡️  INSTALAÇÃO DO SISTEMA DE AUDITORIA"
echo "========================================"
echo ""

# Criar estrutura de diretórios
echo "📁 Criando estrutura de diretórios..."
mkdir -p /home/severosa/organizacao/seguranca/{logs,relatorios,quarentena,backups}
chmod 700 /home/severosa/organizacao/seguranca

echo "✅ Diretórios criados"
echo ""

# Tornar scripts executáveis
echo "🔧 Configurando permissões..."
chmod +x /home/severosa/organizacao/seguranca/sistema_auditoria.py
chmod +x /home/severosa/organizacao/seguranca/auditoria_cron.sh
echo "✅ Permissões configuradas"
echo ""

# Configurar cron job
echo "⏰ Configurando auditoria automática (a cada 2 horas)..."
CRON_ENTRY="0 */2 * * * /home/severosa/organizacao/seguranca/auditoria_cron.sh"

# Verificar se já existe
if crontab -l 2>/dev/null | grep -q "auditoria_cron.sh"; then
    echo "✅ Cron job já configurado"
else
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    echo "✅ Cron job adicionado"
fi

echo ""
echo "========================================"
echo "✅ INSTALAÇÃO CONCLUÍDA!"
echo "========================================"
echo ""
echo "📋 ESTRUTURA CRIADA:"
echo "   • sistema_auditoria.py    - Motor de auditoria"
echo "   • auditoria_cron.sh       - Agendador de tarefas"
echo "   • logs/                   - Logs de segurança"
echo "   • relatorios/             - Relatórios periódicos"
echo "   • quarentena/             - Arquivos suspeitos"
echo "   • backups/                - Backups antes de alterações"
echo ""
echo "🔄 AGENDAMENTO:"
echo "   • Auditoria automática: A cada 2 horas"
echo "   • Log de eventos: Diário"
echo "   • Alertas: Imediato (para eventos CRÍTICOS)"
echo ""
echo "🧪 TESTAR AGORA:"
echo "   bash /home/severosa/organizacao/seguranca/auditoria_cron.sh"
echo ""
echo "📖 VERIFICAR LOGS:"
echo "   tail -f /home/severosa/organizacao/seguranca/logs/*.log"
echo ""
echo "🛡️  Sistema protegido contra:"
echo "   • Dispositivos não autorizados"
echo "   • Modificações suspeitas de configuração"
echo "   • Acessos anômalos"
echo "   • Processos não identificados"
echo ""
