#!/bin/bash
# Criar Backup para Migração Tablet
# PC → Dropbox → Tablet

set -e

echo "=========================================="
echo "  BACKUP MIGRAÇÃO - PC PARA TABLET"
echo "=========================================="
echo ""

# Configurações
BACKUP_NAME="openclaw_migracao_$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="$HOME/backup_migracao"
RCLONE="$HOME/.local/bin/rclone"
DROPBOX_REMOTE="gdrive"  # Nome que você configurou

echo "📁 Diretório backup: $BACKUP_DIR"
echo "📦 Nome: $BACKUP_NAME"
echo "☁️  Dropbox remote: $DROPBOX_REMOTE"
echo ""

# Criar diretório
mkdir -p "$BACKUP_DIR"

# ==========================================
# BACKUP ESSENCIAL (~250 MB)
# ==========================================

echo "📦 Criando backup ESSENCIAL..."
echo ""

# Lista de arquivos essenciais
ESSENCIAL_LIST="$BACKUP_DIR/essencial_list.txt"
cat > "$ESSENCIAL_LIST" << 'LISTA'
.openclaw/openclaw.json
.openclaw/workspace/
.openclaw/memory/
.openclaw/sessions/
organizacao/advocacia/
organizacao/servidor-publico/
organizacao/controle-prazos/
organizacao/captura/
organizacao/youtube/
organizacao/notebooklm_integration/
organizacao/scripts/
organizacao/monitoramento/
organizacao/seguranca/
organizacao/configuracao/
.config/rclone/
LISTA

# Criar tar essencial
cd ~
tar -czf "$BACKUP_DIR/${BACKUP_NAME}_essencial.tar.gz" \
  --files-from="$ESSENCIAL_LIST" \
  --exclude="*.tar.gz" \
  --exclude="backup/" \
  --exclude="youtube/uploads/" \
  --exclude="youtube/producao/" \
  2>/dev/null || true

ESSENCIAL_SIZE=$(du -h "$BACKUP_DIR/${BACKUP_NAME}_essencial.tar.gz" | cut -f1)
echo "✅ Backup essencial criado: $ESSENCIAL_SIZE"
echo ""

# ==========================================
# BACKUP COMPLETO (OPCIONAL, ~4-5 GB)
# ==========================================

echo "📦 Criando backup COMPLETO (opcional, maior)..."
echo ""

COMPLETO_LIST="$BACKUP_DIR/completo_list.txt"
cat > "$COMPLETO_LIST" << 'LISTA'
.openclaw/
organizacao/
.config/rclone/
LISTA

# Criar tar completo (exclui arquivos muito grandes)
cd ~
tar -czf "$BACKUP_DIR/${BACKUP_NAME}_completo.tar.gz" \
  --files-from="$COMPLETO_LIST" \
  --exclude="organizacao/backup/*.tar.gz" \
  --exclude="organizacao/youtube/uploads/*.mp4" \
  --exclude="organizacao/youtube/producao/*" \
  --exclude=".openclaw/media/inbound/*.mp4" \
  --exclude=".openclaw/media/inbound/*.wav" \
  2>/dev/null || true

if [ -f "$BACKUP_DIR/${BACKUP_NAME}_completo.tar.gz" ]; then
    COMPLETO_SIZE=$(du -h "$BACKUP_DIR/${BACKUP_NAME}_completo.tar.gz" | cut -f1)
    echo "✅ Backup completo criado: $COMPLETO_SIZE"
else
    echo "⚠️  Backup completo não criado (pode ser muito grande)"
fi
echo ""

# ==========================================
# UPLOAD PARA DROPBOX
# ==========================================

echo "☁️  Enviando para Dropbox..."
echo ""

# Criar pasta no Dropbox
$RCLONE mkdir "$DROPBOX_REMOTE:OpenClaw_Backup/Migracao_Tablet/" 2>/dev/null || true

# Upload essencial
echo "  📤 Upload essencial..."
$RCLONE copy \
  "$BACKUP_DIR/${BACKUP_NAME}_essencial.tar.gz" \
  "$DROPBOX_REMOTE:OpenClaw_Backup/Migracao_Tablet/" \
  --progress

# Upload completo (se existir)
if [ -f "$BACKUP_DIR/${BACKUP_NAME}_completo.tar.gz" ]; then
    echo "  📤 Upload completo..."
    $RCLONE copy \
      "$BACKUP_DIR/${BACKUP_NAME}_completo.tar.gz" \
      "$DROPBOX_REMOTE:OpenClaw_Backup/Migracao_Tablet/" \
      --progress
fi

echo ""

# ==========================================
# VERIFICAÇÃO
# ==========================================

echo "🔍 Verificando arquivos no Dropbox..."
echo ""
$RCLONE ls "$DROPBOX_REMOTE:OpenClaw_Backup/Migracao_Tablet/" --max-depth 1

echo ""
echo "=========================================="
echo "  BACKUP CONCLUÍDO!"
echo "=========================================="
echo ""
echo "📋 RESUMO:"
echo "  • Backup essencial: $ESSENCIAL_SIZE"
if [ -f "$BACKUP_DIR/${BACKUP_NAME}_completo.tar.gz" ]; then
    echo "  • Backup completo: $COMPLETO_SIZE"
fi
echo "  • Local: $BACKUP_DIR"
echo "  • Dropbox: OpenClaw_Backup/Migracao_Tablet/"
echo ""
echo "📱 PRÓXIMO PASSO (Tablet):"
echo "  1. Instalar Termux"
echo "  2. Instalar OpenClaw"
echo "  3. Executar: restaurar_backup_migracao.sh"
echo ""
echo "=========================================="

# Criar arquivo de instruções
cat > "$BACKUP_DIR/INSTRUCOES_TABLET.md" << 'INSTRUCOES'
# Instruções para Tablet

## 1. Instalar Termux
- Baixe do F-Droid: https://f-droid.org/packages/com.termux/
- NÃO use Play Store (versão desatualizada)

## 2. Instalar Dependências
```bash
pkg update
pkg install python nodejs git curl wget
```

## 3. Instalar OpenClaw
```bash
curl -fsSL https://openclaw.sh/install.sh | sh
```

## 4. Instalar rclone
```bash
curl https://rclone.org/install.sh | sudo bash
```

## 5. Configurar Dropbox
```bash
rclone config
# Siga instruções (igual ao PC)
# Nomeie como "gdrive" para compatibilidade
```

## 6. Baixar Backup
```bash
rclone copy gdrive:OpenClaw_Backup/Migracao_Tablet/ ~/
```

## 7. Extrair
```bash
cd ~
tar -xzf openclaw_migracao_*_essencial.tar.gz
```

## 8. Restaurar Configurações
```bash
cp .bashrc ~/.bashrc
source ~/.bashrc
```

## 9. Iniciar OpenClaw
```bash
openclaw start
```

## 10. Testar
```bash
openclaw status
```
INSTRUCOES

echo "✅ Instruções salvas: $BACKUP_DIR/INSTRUCOES_TABLET.md"
