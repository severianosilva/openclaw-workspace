#!/bin/bash

# Script para configurar backup automático do OpenClaw

echo "Configurando backup automático do OpenClaw..."

# Criar diretório de backup se não existir
mkdir -p /home/severosa/organizacao/backup

# Adicionar ao crontab um backup diário às 2h da manhã
(crontab -l 2>/dev/null | grep -v "backup_openclaw.sh"; echo "0 2 * * * DISPLAY=:0 /home/severosa/organizacao/captura/backup_openclaw.sh >> /home/severosa/organizacao/backup/backup.log 2>&1") | crontab -

echo "Backup automático configurado!"
echo "O backup será feito diariamente às 2h da manhã"
echo "Os backups serão salvos em: /home/severosa/organizacao/backup/"
echo ""
echo "Para testar o backup manualmente, execute:"
echo "  /home/severosa/organizacao/captura/backup_openclaw.sh"
echo ""
echo "Para verificar os backups existentes:"
echo "  ls -la /home/severosa/organizacao/backup/"