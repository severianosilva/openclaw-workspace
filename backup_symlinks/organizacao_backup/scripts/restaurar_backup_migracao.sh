#!/bin/bash
# Restaurar Backup no Tablet
# Dropbox → Tablet

set -e

echo "=========================================="
echo "  RESTAURAR BACKUP - TABLET"
echo "=========================================="
echo ""

# Configurações
RCLONE_CMD="rclone"
DROPBOX_REMOTE="gdrive"

# Detectar se está no Termux
if [ -d "/data/data/com.termux" ]; then
    echo "📱 Detectado: Termux (Android)"
    HOME_DIR="/data/data/com.termux/files/home"
else
    echo "💻 Detectado: Linux padrão"
    HOME_DIR="$HOME"
fi

echo "🏠 Home directory: $HOME_DIR"
echo ""

# ==========================================
# VERIFICAÇÕES PRÉVIAS
# ==========================================

echo "🔍 Verificando pré-requisitos..."
echo ""

# Verificar rclone
if ! command -v rclone &> /dev/null; then
    echo "❌ rclone não encontrado!"
    echo ""
    echo "Instale com:"
    echo "  curl https://rclone.org/install.sh | sudo bash"
    echo "OU (Termux):"
    echo "  pkg install rclone"
    exit 1
fi

echo "✅ rclone: $(rclone version | head -1)"

# Verificar conexão Dropbox
echo ""
echo "🔍 Testando conexão Dropbox..."
if ! $RCLONE_CMD lsd "$DROPBOX_REMOTE:" > /dev/null 2>&1; then
    echo "❌ Dropbox não configurado ou sem conexão!"
    echo ""
    echo "Configure com:"
    echo "  rclone config"
    echo ""
    echo "Ou verifique conexão com internet."
    exit 1
fi

echo "✅ Dropbox conectado"

# ==========================================
# BAIXAR BACKUP
# ==========================================

echo ""
echo "📥 Baixando backup do Dropbox..."
echo ""

# Listar backups disponíveis
echo "📋 Backups disponíveis:"
$RCLONE_CMD ls "$DROPBOX_REMOTE:OpenClaw_Backup/Migracao_Tablet/" --max-depth 1

echo ""
echo "Digite o nome do backup (ou 'essencial' para o menor):"
read -p "> " BACKUP_CHOICE

if [ "$BACKUP_CHOICE" = "essencial" ]; then
    # Baixar mais recente essencial
    BACKUP_FILE=$($RCLONE_CMD ls "$DROPBOX_REMOTE:OpenClaw_Backup/Migracao_Tablet/" | grep "essencial" | sort -r | head -1 | awk '{print $4}')
else
    BACKUP_FILE="$BACKUP_CHOICE"
fi

echo ""
echo "📦 Baixando: $BACKUP_FILE"
$RCLONE_CMD copy \
  "$DROPBOX_REMOTE:OpenClaw_Backup/Migracao_Tablet/$BACKUP_FILE" \
  "$HOME_DIR/" \
  --progress

# ==========================================
# EXTRAIR BACKUP
# ==========================================

echo ""
echo "📦 Extraindo backup..."
echo ""

cd "$HOME_DIR"
tar -xzf "$BACKUP_FILE"

echo "✅ Backup extraído!"

# ==========================================
# RESTAURAR CONFIGURAÇÕES
# ==========================================

echo ""
echo "🔧 Restaurando configurações..."
echo ""

# Restaurar .bashrc
if [ -f "$HOME_DIR/.bashrc" ]; then
    echo "  • .bashrc"
    # Adicionar PATH do rclone se não existir
    if ! grep -q ".local/bin" "$HOME_DIR/.bashrc"; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME_DIR/.bashrc"
    fi
    source "$HOME_DIR/.bashrc" 2>/dev/null || true
fi

# Verificar OpenClaw
if command -v openclaw &> /dev/null; then
    echo "  • OpenClaw: instalado"
else
    echo "  ⚠️  OpenClaw: não encontrado"
    echo ""
    echo "Instale com:"
    echo "  curl -fsSL https://openclaw.sh/install.sh | sh"
fi

# ==========================================
# VERIFICAÇÃO FINAL
# ==========================================

echo ""
echo "=========================================="
echo "  VERIFICAÇÃO FINAL"
echo "=========================================="
echo ""

echo "📁 Estrutura de diretórios:"
ls -la "$HOME_DIR/" | head -20

echo ""
echo "📊 Espaço utilizado:"
du -sh "$HOME_DIR/.openclaw" 2>/dev/null || echo "  .openclaw: não encontrado"
du -sh "$HOME_DIR/organizacao" 2>/dev/null || echo "  organizacao: não encontrado"

echo ""
echo "=========================================="
echo "  RESTAURAÇÃO CONCLUÍDA!"
echo "=========================================="
echo ""
echo "🚀 PRÓXIMOS PASSOS:"
echo ""
echo "1. Iniciar OpenClaw:"
echo "   openclaw start"
echo ""
echo "2. Verificar status:"
echo "   openclaw status"
echo ""
echo "3. Configurar gateways (se necessário):"
echo "   openclaw gateway status"
echo ""
echo "4. Testar WhatsApp/Telegram:"
echo "   Envie uma mensagem de teste"
echo ""
echo "5. Configurar sync contínuo (opcional):"
echo "   Execute: configurar_sync_continuo.sh"
echo ""
echo "=========================================="

# Criar arquivo de status
cat > "$HOME_DIR/MIGRACAO_STATUS.txt" << 'STATUS'
MIGRAÇÃO TABLET - STATUS
========================

Data: $(date)
Backup: $(basename $BACKUP_FILE)
Status: Restaurado com sucesso

Próximos passos:
1. openclaw start
2. openclaw status
3. Testar gateways
4. Configurar sync contínuo

Dúvidas? Consulte:
~/organizacao/MIGRACAO_TABLET.md
STATUS

echo "✅ Status salvo: $HOME_DIR/MIGRACAO_STATUS.txt"
