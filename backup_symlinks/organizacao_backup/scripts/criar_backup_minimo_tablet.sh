#!/bin/bash
# Backup MÍNIMO ESSENCIAL para Tablet
# Só o básico para funcionar - tudo grande fica na nuvem!

set -e

echo "=========================================="
echo "  BACKUP MÍNIMO - TABLET"
echo "=========================================="
echo ""

BACKUP_NAME="openclaw_MINIMO_$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="$HOME/backup_migracao/MINIMO"
DROPBOX_REMOTE="gdrive"

echo "🎯 PRINCÍPIO: Apenas essencial local!"
echo "  💾 Local (Tablet): Configs + Scripts pequenos"
echo "  ☁️  Nuvem (Dropbox): Mídia + Backups + Projetos grandes"
echo ""

mkdir -p "$BACKUP_DIR"

# ==========================================
# O QUE VAI PARA TABLET (MÍNIMO)
# ==========================================

echo "📦 Compactando ESSENCIAL MÍNIMO..."

cd ~
tar -czf "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" \
  \
  1. OPENCLAW (config principal) \
  --exclude=".openclaw/media/" \
  --exclude=".openclaw/sessions/*/media/" \
  --exclude="*.log" \
  --exclude="*.tmp" \
  .openclaw/openclaw.json \
  .openclaw/workspace/ \
  .openclaw/memory/ \
  \
  2. SCRIPTS FUNCIONAIS \
  organizacao/scripts/ \
  \
  3. ATIVOS MÍNIMOS (processos) \
  --exclude="*.pdf" \
  --exclude="*.docx" \
  --exclude="*.xlsx" \
  organizacao/controle-prazos/ \
  \
  4. CONFIGURAÇÕES \
  .config/rclone/rclone.conf \
  .bashrc \
  \
  2>/dev/null || true

SIZE=$(du -h "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" | cut -f1)
echo "✅ Backup mínimo: $SIZE"

# ==========================================
# O QUE FICA NA NUVEM (NÃO VAI PRO TABLET)
# ==========================================

echo ""
echo "☁️  NA NUVEM (acesso remoto):"
echo "  • organizacao/backup/ (3 GB)"
echo "  • organizacao/youtube/uploads/ (vídeos)"
echo "  • organizacao/youtube/producao/ (projetos)"
echo "  • .openclaw/media/ (áudios/fotos)"
echo "  • Arquivos PDF grandes (processos)"
echo ""

# Enviar MÍNIMO para Dropbox primeiro
echo "📤 Enviando backup mínimo para Dropbox..."
~/.local/bin/rclone mkdir "$DROPBOX_REMOTE:OpenClaw_Backup/Migracao_Tablet/" 2>/dev/null || true

~/.local/bin/rclone copy \
  "$BACKUP_DIR/${BACKUP_NAME}.tar.gz" \
  "$DROPBOX_REMOTE:OpenClaw_Backup/Migracao_Tablet/" \
  --progress

echo ""

# ==========================================
# CRIAR ÍNDICE DA NUVEM
# ==========================================

echo "📋 Criando índice de arquivos na nuvem..."

cat > "$BACKUP_DIR/INDICE_NUVEM.txt" << 'INDICE'
ARQUIVOS NA NUVEM - Acessíveis do Tablet
==========================================

DATA: $(date +%Y-%m-%d)

## LOCALIZAÇÃO DROPBOX:
OpenClaw_Backup/
├── Backups/                    ← Backups diários
├── Backups_legados/            ← Backups antigos
├── Migracao_Tablet/            ← Backup mínimo
└── Sync_Continuo/              ← Sync automático

## ACESSO DO TABLET:
Para acessar arquivos grandes, use:

# Listar arquivos na nuvem:
rclone ls gdrive:OpenClaw_Backup/

# Baixar arquivo específico:
rclone copy gdrive:OpenClaw_Backup/Backups/backup_2026-03-01.tar.gz ~/

# Stream de vídeo (sem baixar):
rclone cat gdrive:OpenClaw_Backup/videos/exemplo.mp4 | vlc -

## DIRETÓRIOS DISPONÍVEIS:
- Backups/: Todos backups diários
- Backups_legados/: Backups históricos
- Sync_Continuo/: Arquivos em sincronização

## USO DO ESPAÇO:
- Tablet Local: Configs + Scripts (~50 MB)
- Cloud Dropbox: Tudo o mais (~3 GB+)
- Total disponível quando conectado: ~2.1 TB

ESTRATÉGIA: Configurações locais, dados na nuvem!
INDICE

# Enviar índice
~/.local/bin/rclone copy \
  "$BACKUP_DIR/INDICE_NUVEM.txt" \
  "$DROPBOX_REMOTE:OpenClaw_Backup/Migracao_Tablet/"

echo ""
echo "=========================================="
echo "  BACKUP MÍNIMO CONCLUÍDO!"
echo "=========================================="
echo ""
echo "📊 RESUMO:"
echo "  • Backup mínimo: $SIZE"
echo "  • Local: $BACKUP_DIR/${BACKUP_NAME}.tar.gz"
echo "  • Dropbox: OpenClaw_Backup/Migracao_Tablet/"
echo ""
echo "🎯 ESTRATÉGIA:"
echo "  ✅ Tablet: Configs + Scripts necessários"
echo "  ☁️  Nuvem: Todos os dados pesados"
echo ""
echo "💡 DICAS TABLET:"
echo "  • Baixe só quando precisar"
echo "  • Stream arquivos grandes"
echo "  • Sync configurado automático"
echo ""
echo "📱 Próximo: Executar no tablet:"
echo "  restaurar_backup_migracao.sh"
echo ""
echo "=========================================="
