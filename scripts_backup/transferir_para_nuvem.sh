#!/bin/bash
# =============================================================================
# SISTEMA DE LIMPEZA E TRANSFERÊNCIA PARA NUVEM
# Move arquivos não-essenciais para nuvem e libera espaço local
# =============================================================================

set -e  # Parar em caso de erro

# Configurações
BACKUP_DIR="/home/severosa/organizacao/backup"
MEDIA_DIR="/home/severosa/.openclaw/media/inbound"
CLOUD_DEST="gdrive:OpenClaw-Offload"  # Destino RClone
LOG_FILE="/home/severosa/organizacao/transferencia_nuvem.log"
DAYS_OLD=30  # Arquivos mais antigos que X dias vão para nuvem

echo "=========================================="
echo "  TRANSFERÊNCIA PARA NUVEM - OPENCLAW"
echo "=========================================="
echo ""
echo "Data: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Log: $LOG_FILE"
echo ""

# Função para log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Verificar se RClone está configurado
if ! command -v rclone &> /dev/null; then
    log "ERRO: RClone não encontrado. Instale primeiro."
    echo "Execute: sudo snap install rclone --classic"
    exit 1
fi

# Verificar conexão com nuvem
log "Verificando conexão com Google Drive..."
if ! rclone lsd gdrive: &> /dev/null; then
    log "ERRO: Google Drive não configurado. execute: rclone config"
    exit 1
fi

# Criar diretórios na nuvem se não existirem
rclone mkdir "$CLOUD_DEST/backups-antigos" 2>/dev/null || true
rclone mkdir "$CLOUD_DEST/media-audio" 2>/dev/null || true
rclone mkdir "$CLOUD_DEST/transcricoes" 2>/dev/null || true

# =============================================================================
# 1. BACKUPS ANTIGOS (Maiores consumidores de espaço)
# =============================================================================
echo ""
echo "1️⃣  Processando BACKUPS ANTIGOS..."
echo "---------------------------------------"

BACKUP_COUNT=0
BACKUP_SIZE=0

# Listar backups antigos (mais de $DAYS_OLD dias)
while IFS= read -r file; do
    if [ -f "$file" ]; then
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "0")
        filename=$(basename "$file")
        
        # Manter os 2 últimos backups localmente (mais recentes)
        log "Transferindo backup: $filename ($(numfmt --to=iec $size 2>/dev/null || echo "${size}B"))"
        
        # Transferir para nuvem
        if rclone move "$file" "$CLOUD_DEST/backups-antigos/" --progress 2>/dev/null; then
            log "✅ Sucesso: $filename"
            ((BACKUP_COUNT++))
            ((BACKUP_SIZE+=size))
        else
            log "⚠️  Falha: $filename (mantido local)"
        fi
    fi
done < <(find "$BACKUP_DIR" -name "backup_openclaw_*.tar.gz" -mtime +$DAYS_OLD -type f 2>/dev/null | sort -r | tail -n +3)

echo "   Backups transferidos: $BACKUP_COUNT"
echo "   Espaço liberado: $(numfmt --to=iec $BACKUP_SIZE 2>/dev/null || echo "${BACKUP_SIZE} bytes")"

# =============================================================================
# 2. ARQUIVOS DE ÁUDIO ANTIGOS
# =============================================================================
echo ""
echo "2️⃣  Processando ARQUIVOS DE ÁUDIO..."
echo "---------------------------------------"

AUDIO_COUNT=0
AUDIO_SIZE=0

# Listar áudios antigos
while IFS= read -r file; do
    if [ -f "$file" ]; then
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "0")
        filename=$(basename "$file")
        
        # Manter áudios dos últimos 7 dias localmente
        if [ $(find "$file" -mtime +7 -print 2>/dev/null | wc -l) -gt 0 ]; then
            log "Transferindo áudio: $filename ($(numfmt --to=iec $size 2>/dev/null || echo "${size}B"))"
            
            if rclone move "$file" "$CLOUD_DEST/media-audio/" --progress 2>/dev/null; then
                log "✅ Sucesso: $filename"
                ((AUDIO_COUNT++))
                ((AUDIO_SIZE+=size))
            else
                log "⚠️  Falha: $filename"
            fi
        fi
    fi
done < <(find "$MEDIA_DIR" -name "*.ogg" -o -name "*.mp3" -o -name "*.wav" 2>/dev/null)

echo "   Áudios transferidos: $AUDIO_COUNT"
echo "   Espaço liberado: $(numfmt --to=iec $AUDIO_SIZE 2>/dev/null || echo "${AUDIO_SIZE} bytes")"

# =============================================================================
# 3. TRANSCRIÇÕES ANTIGAS
# =============================================================================
echo ""
echo "3️⃣  Processando TRANSCRIÇÕES..."
echo "---------------------------------------"

TRANS_COUNT=0
TRANS_SIZE=0

while IFS= read -r file; do
    if [ -f "$file" ]; then
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "0")
        filename=$(basename "$file")
        
        if [ $(find "$file" -mtime +14 -print 2>/dev/null | wc -l) -gt 0 ]; then
            log "Transferindo transcrição: $filename"
            
            if rclone move "$file" "$CLOUD_DEST/transcricoes/" --progress 2>/dev/null; then
                log "✅ Sucesso: $filename"
                ((TRANS_COUNT++))
                ((TRANS_SIZE+=size))
            else
                log "⚠️  Falha: $filename"
            fi
        fi
    fi
done < <(find "$MEDIA_DIR" -name "*.transcricao*.txt" 2>/dev/null)

echo "   Transcrições transferidas: $TRANS_COUNT"
echo "   Espaço liberado: $(numfmt --to=iec $TRANS_SIZE 2>/dev/null || echo "${TRANS_SIZE} bytes")"

# =============================================================================
# RESUMO FINAL
# =============================================================================
echo ""
echo "=========================================="
echo "  ✅ TRANSFERÊNCIA CONCLUÍDA!"
echo "=========================================="
echo ""

total_count=$((BACKUP_COUNT + AUDIO_COUNT + TRANS_COUNT))
total_size=$((BACKUP_SIZE + AUDIO_SIZE + TRANS_SIZE))

echo "📊 RESUMO:"
echo "   Backups: $BACKUP_COUNT arquivos"
echo "   Áudios: $AUDIO_COUNT arquivos"
echo "   Transcrições: $TRANS_COUNT arquivos"
echo "   TOTAL: $total_count arquivos"
echo "   ESPAÇO LIBERADO: $(numfmt --to=iec $total_size 2>/dev/null || echo "${total_size} bytes")"
echo ""

# Espaço atual
echo "💾 ESPAÇO EM DISCO ATUAL:"
df -h /home/severosa | tee -a "$LOG_FILE"

echo ""
echo "📁 Arquivos na nuvem:"
rclone tree "$CLOUD_DEST" --level 2 2>/dev/null || echo "Use: rclone tree $CLOUD_DEST"

echo ""
echo "Para recuperar arquivos da nuvem:"
echo "  rclone copy $CLOUD_DEST/backups-antigos/ARQUIVO.tar.gz $BACKUP_DIR/"
echo ""
echo "Log completo: $LOG_FILE"
echo ""

log "=== FIM DA TRANSFERÊNCIA ==="
