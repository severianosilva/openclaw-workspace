#!/bin/bash
# Configuração Dropbox (fallback se Google Drive não funcionar)

RCLONE="$HOME/.local/bin/rclone"

echo "=========================================="
echo "  CONFIGURAÇÃO RCLONE + DROPBOX"
echo "=========================================="
echo ""

# Verificar rclone
if ! $RCLONE version > /dev/null 2>&1; then
    echo "❌ rclone não encontrado"
    exit 1
fi

echo "✅ rclone: $($RCLONE version | head -1)"
echo ""

# Instruções simplificadas
cat << 'INSTRUCOES'
==================================================
  CONFIGURAR DROPBOX
==================================================

Execute:
  ~/.local/bin/rclone config

Opções:
  n              ← novo remote
  dropbox        ← nome
  11             ← Dropbox
  (enter)        ← Client ID (opcional)
  (enter)        ← Client Secret (opcional)
  y              ← Edit advanced? sim
  (enter)        ← Configurações avançadas padrão
  y              ← Auto config? sim
  
  → NAVEGADOR ABRE ←
  → Login Dropbox ←
  → Autorizar ←
  → Copiar código ←
  
  y              ← Confirm
  q              ← Sair

Comando para verificar:
  ~/.local/bin/rclone listremotes

==================================================
INSTRUCOES

echo ""
echo "Você já configurou? (s/n)"
read CONFIGURADO

if [ "$CONFIGURADO" = "s" ]; then
    echo ""
    echo "📋 Remotes configurados:"
    $RCLONE listremotes
    
    # Verificar qual está configurado
    echo ""
    echo "Qual nome você deu? (ex: dropbox, gdrive)"
    read REMOTE_NAME
    
    if [ -n "$REMOTE_NAME" ]; then
        echo ""
        echo "✅ Configuração encontrada: $REMOTE_NAME"
        
        # Criar pastas
        echo ""
        echo "📁 Criando estrutura..."
        $RCLONE mkdir "$REMOTE_NAME":OpenClaw_Backup 2>/dev/null || echo "  (pasta já existe ou erro de conexão)"
        
        echo ""
        echo "=========================================="
        echo "  PRONTO!"
        echo "=========================================="
        echo ""
        echo "Comandos úteis:"
        echo ""
        echo "  # Ver arquivos:"
        echo "  $RCLONE ls $REMOTE_NAME:OpenClaw_Backup"
        echo ""
        echo "  # Transferir backups:"
        echo "  $RCLONE copy ~/organizacao/staging_nuvem/backups_transferir.tar.gz $REMOTE_NAME:OpenClaw_Backup/"
        echo ""
        echo "  # Backup completo:"
        echo "  $RCLONE sync ~/organizacao/backup/ $REMOTE_NAME:OpenClaw_Backup/backup/ --max-size 500M"
        echo ""
    fi
fi

echo ""
echo "=========================================="
