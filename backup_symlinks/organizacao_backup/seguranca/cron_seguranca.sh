#!/bin/bash
# CRON DE SEGURANÇA - Executa auditoria a cada 6 horas
# */6 * * * * /home/severosa/organizacao/seguranca/cron_seguranca.sh

LOG_FILE="/home/severosa/organizacao/seguranca/logs/cron_$(date +%Y%m%d).log"

{
    echo "=================================="
    echo "🛡️ CRON DE SEGURANÇA"
    echo "Data: $(date)"
    echo "=================================="
    echo ""
    
    # Rodar auditoria
    python3 /home/severosa/organizacao/seguranca/sistema_auditoria.py
    
    echo ""
    echo "✅ Auditoria concluída em $(date)"
    echo "=================================="
} >> "$LOG_FILE" 2>&1
