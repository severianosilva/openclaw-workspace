#!/bin/bash
# Configuração simplificada do rclone para Google Drive

RCLONE="$HOME/.local/bin/rclone"

echo "=========================================="
echo "  CONFIGURAÇÃO RCLONE + GOOGLE DRIVE"
echo "=========================================="
echo ""

# Verificar rclone
if ! $RCLONE version > /dev/null 2>&1; then
    echo "❌ rclone não encontrado"
    exit 1
fi

echo "✅ rclone: $($RCLONE version | head -1)"
echo ""

# Verificar configuração existente
echo "📋 Remotes configurados:"
$RCLONE listremotes 2>/dev/null || echo "  (nenhum)"
echo ""

# Instruções
cat << 'INSTRUCOES'
==================================================
  CONFIGURAÇÃO GOOGLE DRIVE
==================================================

Execute o comando abaixo:

  ~/.local/bin/rclone config

Siga estas opções:

  n              ← novo remote
  gdrive         ← nome
  13             ← Google Drive
  (enter)        ← Client ID em branco
  (enter)        ← Client Secret em branco
  1              ← Full access
  (enter)        ← Root folder em branco
  n              ← Edit advanced? não
  y              ← Auto config? sim
  
  → NAVEGADOR ABRIRÁ ←
  → Faça login no Google ←
  → Autorize o acesso ←
  → Copie o código ←
  
  (cole o código no terminal)
  n              ← Team drive? não
  y              ← Confirmar? sim
  q              ← Sair

==================================================
INSTRUCOES

echo ""
read -p "Pressione ENTER para abrir o rclone config..."

# Executar configuração
$RCLONE config

echo ""
echo "=========================================="
echo "  VERIFICANDO CONFIGURAÇÃO"
echo "=========================================="
echo ""

# Verificar se gdrive foi configurado
if $RCLONE listremotes | grep -q "gdrive:"; then
    echo "✅ Google Drive configurado!"
    echo ""
    
    # Testar conexão
    echo "🧪 Testando conexão..."
    if $RCLONE lsd gdrive: 2>/dev/null; then
        echo "✅ Conexão bem-sucedida!"
        echo ""
        
        # Criar estrutura de pastas
        echo "📁 Criando pastas OpenClaw..."
        $RCLONE mkdir gdrive:OpenClaw_Backup
        $RCLONE mkdir gdrive:OpenClaw_Backup/Backups
        $RCLONE mkdir gdrive:OpenClaw_Backup/Videos
        $RCLONE mkdir gdrive:OpenClaw_Backup/Relatorios
        $RCLONE mkdir gdrive:OpenClaw_Backup/Midia
        $RCLONE mkdir gdrive:OpenClaw_Backup/Config
        
        echo "✅ Pastas criadas!"
        echo ""
        
        # Mostrar espaço
        echo "💾 Espaço disponível:"
        $RCLONE about gdrive: 2>/dev/null || echo "  (não foi possível verificar)"
        
        echo ""
        echo "=========================================="
        echo "  PRONTO PARA USO!"
        echo "=========================================="
        echo ""
        echo "Comandos úteis:"
        echo ""
        echo "  # Ver arquivos:"
        echo "  $RCLONE ls gdrive: --max-depth 1"
        echo ""
        echo "  # Transferir backups (304 MB):"
        echo "  $RCLONE copy ~/organizacao/staging_nuvem/backups_transferir.tar.gz gdrive:OpenClaw_Backup/Backups/"
        echo ""
        echo "  # Sync automático:"
        echo "  ~/organizacao/scripts/backup_automatico_rclone.sh"
        echo ""
        echo "=========================================="
        
    else
        echo "⚠️ Conexão falhou. Tente reconfigurar."
    fi
else
    echo "⚠️ Google Drive não configurado."
    echo "Execute: $RCLONE config"
fi
