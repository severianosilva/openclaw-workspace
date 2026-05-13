#!/bin/bash
# Verifica espaço e lista arquivos para mover

echo "=========================================="
echo "  DIAGNÓSTICO DE ESPAÇO"
echo "=========================================="
echo ""

# Espaço geral
echo "💾 ESPAÇO GERAL:"
df -h ~ | head -2
echo ""

# Maiores pastas
echo "📁 MAIORES PASTAS:"
du -sh ~/*/ 2>/dev/null | sort -rh | head -10 || echo "  (acesso limitado)"
echo ""

# Maiores arquivos individuais
echo "📄 MAIORES ARQUIVOS:"
find ~ -type f -size +50M 2>/dev/null | xargs -I{} du -sh {} 2>/dev/null | sort -rh | head -10 || echo "  (sem arquivos grandes)"
echo ""

# Arquivos de backup para mover
echo "📦 BACKUPS PARA MOVER:"
find ~/organizacao/backup -name "*.tar.gz" -size +100M -mtime +7 2>/dev/null -exec ls -lh {} \; | awk '{print $5, $9}' || echo "  Nenhum backup grande encontrado"
echo ""

# Mídia antiga
echo "🎵 MÍDIA ANTIGA:"
find ~/.openclaw/media/inbound -type f -mtime +30 2>/dev/null | wc -l | xargs -I{} echo "  {} arquivos com mais de 30 dias"
du -sh ~/.openclaw/media/inbound 2>/dev/null || echo "  0 bytes"
echo ""

echo "=========================================="
echo "✅ Diagnóstico concluído!"
echo ""
echo "Para instalar rclone e mover automaticamente:"
echo "  sudo apt install rclone"
echo ""
echo "Configure com: rclone config"
echo "Depois execute: ~/organizacao/scripts/transferir_nuvem.sh"
echo "=========================================="
