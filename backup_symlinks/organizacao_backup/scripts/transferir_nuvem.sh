#!/bin/bash
# Transfere arquivos não-essenciais para nuvem
# Liberando espaço no computador local

echo "=========================================="
echo "  TRANSFERÊNCIA PARA NUVEM"
echo "=========================================="
echo ""

# Verificar se rclone está configurado
if ! command -v rclone &> /dev/null; then
    echo "❌ ERRO: rclone não instalado"
    echo "Instale com: sudo apt install rclone"
    exit 1
fi

# Verificar configuração
if ! rclone listremotes | grep -q "gdrive:"; then
    echo "⚠️ Configure rclone primeiro:"
    echo "rclone config"
    echo "Crie o remote 'gdrive' para Google Drive"
    exit 1
fi

echo "✅ rclone configurado"
echo ""

# Criar diretórios na nuvem
echo "📁 Criando estrutura na nuvem..."
rclone mkdir gdrive:OpenClaw_Backup/Backups_Antigos
rclone mkdir gdrive:OpenClaw_Backup/Media_Historico
rclone mkdir gdrive:OpenClaw_Backup/Relatorios_Anual
echo "✅ Diretórios criados"
echo ""

# 1. Transferir backups antigos (mais de 7 dias)
echo "🔄 Transferindo backups antigos..."
BACKUP_DIR="$HOME/organizacao/backup"
if [ -d "$BACKUP_DIR" ]; then
    # Listar arquivos maiores que 100MB
    find "$BACKUP_DIR" -name "*.tar.gz" -size +100M -mtime +7 | while read file; do
        filename=$(basename "$file")
        echo "  Transferindo: $filename"
        rclone move "$file" gdrive:OpenClaw_Backup/Backups_Antigos/ --progress
    done
    echo "✅ Backups transferidos"
else
    echo "⚠️ Diretório de backup não encontrado"
fi
echo ""

# 2. Transferir arquivos de mídia antigos
echo "🔄 Transferindo mídia histórica..."
MEDIA_DIR="$HOME/.openclaw/media/inbound"
if [ -d "$MEDIA_DIR" ]; then
    # Arquivos com mais de 30 dias
    find "$MEDIA_DIR" -type f -mtime +30 | while read file; do
        filename=$(basename "$file")
        echo "  Transferindo: $filename"
        rclone move "$file" gdrive:OpenClaw_Backup/Media_Historico/ --progress
    done
    echo "✅ Mídia transferida"
else
    echo "⚠️ Diretório de mídia não encontrado"
fi
echo ""

# 3. Relatórios diários antigos
echo "🔄 Transferindo relatórios antigos..."
RELATORIOS_DIR="$HOME/organizacao/monitoramento/relatorios-diarios"
if [ -d "$RELATORIOS_DIR" ]; then
    find "$RELATORIOS_DIR" -name "*.md" -type f -mtime +90 | while read file; do
        filename=$(basename "$file")
        rclone move "$file" gdrive:OpenClaw_Backup/Relatorios_Anual/ --progress
    done
    echo "✅ Relatórios transferidos"
fi
echo ""

# Mostrar espaço
SPACE_LOCAL=$(df -h ~ | tail -1 | awk '{print $3}')
SPACE_CLOUD=$(rclone size gdrive:OpenClaw_Backup/ 2>/dev/null | grep 'Total size' || echo "Não calculado")

echo "=========================================="
echo "  RESUMO"
echo "=========================================="
echo ""
echo "💾 Espaço local usado: $SPACE_LOCAL"
echo "☁️ Espaço em nuvem: $SPACE_CLOUD"
echo ""
echo "✅ Transferência concluída!"
echo ""
echo "📝 ARQUIVOS ESSENCIAIS MANTIDOS LOCAL:"
echo "  • Configurações (~/.openclaw/)"
echo "  • Scripts Python ativos"
echo "  • Processos jurídicos atuais"
echo "  • Sistema atual"
echo ""
echo "☁️ ARQUIVOS TRANSFERIDOS:"
echo "  • Backups antigos (Google Drive)"
echo "  • Mídia histórica"
echo "  • Relatórios antigos"
echo ""
echo "Para acessar: https://drive.google.com"
echo "=========================================="
