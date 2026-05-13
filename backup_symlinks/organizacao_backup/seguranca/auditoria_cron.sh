#!/bin/bash
# CRON JOB DE AUDITORIA DE SEGURANÇA
# Executa auditoria a cada 2 horas e envia relatório

LOG_FILE="/home/severosa/organizacao/seguranca/logs/audit_cron_$(date +%Y%m%d).log"
REPORT_FILE="/home/severosa/organizacao/seguranca/relatorios/relatorio_$(date +%Y%m%d_%H%M).json"

# Criar diretório de relatórios
mkdir -p /home/severosa/organizacao/seguranca/relatorios

echo "$(date): Iniciando auditoria de segurança..." >> "$LOG_FILE"

# Executar auditoria Python
python3 /home/severosa/organizacao/seguranca/sistema_auditoria.py >> "$LOG_FILE" 2>&1

# Verificar se há alertas críticos no log de hoje
TODAY_LOG="/home/severosa/organizacao/seguranca/logs/security_$(date +%Y-%m-%d).log"

if [ -f "$TODAY_LOG" ]; then
    CRITICAL_COUNT=$(grep -c '"level": "CRITICAL"' "$TODAY_LOG" 2>/dev/null || echo "0")
    WARNING_COUNT=$(grep -c '"level": "WARNING"' "$TODAY_LOG" 2>/dev/null || echo "0")
    
    echo "$(date): Alertas encontrados - CRITICAL: $CRITICAL_COUNT, WARNING: $WARNING_COUNT" >> "$LOG_FILE"
    
    # Se houver alertas críticos, notificar
    if [ "$CRITICAL_COUNT" -gt 0 ]; then
        echo "$(date): 🚨 ALERTAS CRÍTICOS DETECTADOS! Reveja o log imediatamente." >> "$LOG_FILE"
    fi
else
    echo "$(date): Log de hoje não encontrado" >> "$LOG_FILE"
fi

echo "$(date): Auditoria concluída." >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"
