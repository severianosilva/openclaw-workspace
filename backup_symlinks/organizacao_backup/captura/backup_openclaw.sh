#!/bin/bash

# Script de backup do sistema OpenClaw
# Faz backup de configurações, scripts e documentos importantes

DATA_ATUAL=$(date +%Y-%m-%d_%H-%M-%S)
NOME_BACKUP="backup_openclaw_${DATA_ATUAL}"
DIRETORIO_TEMP="/tmp/${NOME_BACKUP}"
DIRETORIO_BACKUP_FINAL="/home/severosa/organizacao/backup"

echo "Iniciando backup do sistema OpenClaw: ${NOME_BACKUP}"

# Criar diretórios temporários
mkdir -p "${DIRETORIO_TEMP}"
mkdir -p "${DIRETORIO_BACKUP_FINAL}"

# Backup da configuração principal do OpenClaw
cp -r "/home/severosa/.openclaw/openclaw.json" "${DIRETORIO_TEMP}/"

# Backup do workspace do OpenClaw
cp -r "/home/severosa/.openclaw/workspace/" "${DIRETORIO_TEMP}/workspace/"

# Backup dos scripts personalizados
cp -r "/home/severosa/organizacao/" "${DIRETORIO_TEMP}/organizacao/"

# Remover arquivos temporários e desnecessários do backup
find "${DIRETORIO_TEMP}" -name "*.tmp" -type f -delete
find "${DIRETORIO_TEMP}" -name "*.log" -type f -delete
find "${DIRETORIO_TEMP}" -name "*~" -type f -delete

# Criar arquivo TAR.GZ com o backup
cd /tmp
tar -czf "${DIRETORIO_BACKUP_FINAL}/${NOME_BACKUP}.tar.gz" "${NOME_BACKUP}"

# Remover diretório temporário
rm -rf "${DIRETORIO_TEMP}"

echo "Backup concluído: ${DIRETORIO_BACKUP_FINAL}/${NOME_BACKUP}.tar.gz"

# Opcional: Enviar cópia para Google Drive se configurado
if command -v rclone >/dev/null 2>&1; then
    echo "Enviando cópia para Google Drive..."
    rclone copy "${DIRETORIO_BACKUP_FINAL}/${NOME_BACKUP}.zip" "gdrive:/Backups_OpenClaw/" 2>/dev/null &
    echo "Envio para Google Drive iniciado em segundo plano"
else
    echo "Rclone não encontrado. Para enviar para Google Drive, instale o rclone:"
    echo "sudo snap install rclone --classic"
    echo "Depois configure com: rclone config"
fi

echo "Backup salvo localmente em: ${DIRETORIO_BACKUP_FINAL}/${NOME_BACKUP}.tar.gz"