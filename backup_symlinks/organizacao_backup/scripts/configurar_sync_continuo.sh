#!/bin/bash
# Configurar Sync Contínuo: PC ↔ Dropbox ↔ Tablet

set -e

echo "=========================================="
echo "  SYNC CONTÍNUO - PC ↔ TABLET"
echo "=========================================="
echo ""

RCLONE="$HOME/.local/bin/rclone"
DROPBOX_REMOTE="gdrive"
SYNC_DIR="$HOME/organizacao"
REMOTE_DIR="$DROPBOX_REMOTE:OpenClaw_Backup/Sync_Continuo/"

echo "📁 Diretório local: $SYNC_DIR"
echo "☁️  Diretório remoto: $REMOTE_DIR"
echo ""

# ==========================================
# CONFIGURAR SYNC PC
# ==========================================

echo "🔧 Configurando sync no PC..."
echo ""

# Criar script de sync
SYNC_SCRIPT="$HOME/organizacao/scripts/sync_para_nuvem.sh"
cat > "$SYNC_SCRIPT" << 'SYNCSCRIPT'
#!/bin/bash
# Sync PC → Dropbox

RCLONE="$HOME/.local/bin/rclone"
DROPBOX_REMOTE="gdrive"

echo "🔄 Sync iniciado: $(date)"

# Sync essencial (rápido)
$RCLONE sync \
  "$HOME/organizacao/advocacia/" \
  "$DROPBOX_REMOTE:OpenClaw_Backup/Sync_Continuo/advocacia/" \
  --progress --create-empty-src-dirs

$RCLONE sync \
  "$HOME/organizacao/servidor-publico/" \
  "$DROPBOX_REMOTE:OpenClaw_Backup/Sync_Continuo/servidor-publico/" \
  --progress --create-empty-src-dirs

$RCLONE sync \
  "$HOME/organizacao/scripts/" \
  "$DROPBOX_REMOTE:OpenClaw_Backup/Sync_Continuo/scripts/" \
  --progress

$RCLONE sync \
  "$HOME/organizacao/controle-prazos/" \
  "$DROPBOX_REMOTE:OpenClaw_Backup/Sync_Continuo/controle-prazos/" \
  --progress

echo "✅ Sync concluído: $(date)"
SYNCSCRIPT

chmod +x "$SYNC_SCRIPT"
echo "✅ Script criado: $SYNC_SCRIPT"

# Agendar no cron (sync a cada 6 horas)
CRON_JOB="0 */6 * * * $SYNC_SCRIPT"
(crontab -l 2>/dev/null | grep -v "$SYNC_SCRIPT"; echo "$CRON_JOB") | crontab - 2>/dev/null || echo "⚠️  Cron não disponível"

echo "✅ Sync agendado (a cada 6 horas)"

# ==========================================
# CONFIGURAR SYNC TABLET (INSTRUÇÕES)
# ==========================================

echo ""
echo "📱 CONFIGURAÇÃO TABLET:"
echo ""
echo "No tablet, execute:"
echo ""
cat << 'TABLETSCRIPT'
# 1. Criar script de download
cat > ~/sync_da_nuvem.sh << 'EOF'
#!/bin/bash
RCLONE="rclone"
DROPBOX_REMOTE="gdrive"

# Baixar atualizações
$RCLONE copy \
  "$DROPBOX_REMOTE:OpenClaw_Backup/Sync_Continuo/advocacia/" \
  "~/organizacao/advocacia/" \
  --progress

$RCLONE copy \
  "$DROPBOX_REMOTE:OpenClaw_Backup/Sync_Continuo/scripts/" \
  "~/organizacao/scripts/" \
  --progress

echo "Sync tablet concluído!"
EOF

chmod +x ~/sync_da_nuvem.sh

# 2. Executar periodicamente
# (no Termux, use termux-job-scheduler ou alarme)
TABLETSCRIPT

# ==========================================
# TESTE DE SYNC
# ==========================================

echo ""
echo "🧪 Testando sync..."
echo ""

# Criar arquivo de teste
TEST_FILE="$SYNC_DIR/sync_teste_$(date +%Y%m%d_%H%M%S).txt"
echo "Teste de sync - $(date)" > "$TEST_FILE"

# Sync para nuvem
$RCLONE copy "$SYNC_DIR/" "$REMOTE_DIR" --include "sync_teste_*.txt" --progress

# Verificar
if $RCLONE_CMD ls "$REMOTE_DIR" | grep -q "sync_teste"; then
    echo "✅ Sync testado com sucesso!"
    # Limpar teste
    rm "$TEST_FILE"
    $RCLONE_CMD delete "$REMOTE_DIR" --include "sync_teste_*.txt"
else
    echo "⚠️  Teste falhou. Verifique conexão."
fi

# ==========================================
# RESUMO
# ==========================================

echo ""
echo "=========================================="
echo "  SYNC CONFIGURADO!"
echo "=========================================="
echo ""
echo "📋 RESUMO:"
echo ""
echo "PC (automático):"
echo "  • Script: $SYNC_SCRIPT"
echo "  • Agenda: A cada 6 horas"
echo "  • Comando manual: $SYNC_SCRIPT"
echo ""
echo "Tablet (manual):"
echo "  • Script: ~/sync_da_nuvem.sh"
echo "  • Execute quando quiser atualizar"
echo ""
echo "Fluxo:"
echo "  PC → (sync 6h) → Dropbox → (manual) → Tablet"
echo ""
echo "=========================================="
