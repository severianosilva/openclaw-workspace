#!/bin/bash
# Configuração Completa do RClone
# Conecta Google Drive, OneDrive, Dropbox e outros serviços

set -e

echo "=========================================="
echo "  CONFIGURAÇÃO RCLONE - OPENCLAW"
echo "=========================================="
echo ""

# Verificar se rclone existe
if command -v rclone &> /dev/null; then
    RCLONE_CMD="rclone"
    echo "✅ rclone encontrado: $(rclone version | head -1)"
elif [ -f "$HOME/.local/bin/rclone" ]; then
    RCLONE_CMD="$HOME/.local/bin/rclone"
    echo "✅ rclone encontrado em: $HOME/.local/bin/"
else
    echo "❌ rclone não encontrado"
    echo ""
    echo "Instalando rclone..."
    
    # Tentar instalar
    if command -v curl &> /dev/null; then
        # Baixar e instalar manualmente
        cd /tmp
        curl -O https://downloads.rclone.org/rclone-current-linux-amd64.zip
        unzip -o rclone-current-linux-amd64.zip
        cd rclone-*-linux-amd64
        
        # Criar diretório local
        mkdir -p "$HOME/.local/bin"
        cp rclone "$HOME/.local/bin/"
        chmod +x "$HOME/.local/bin/rclone"
        
        # Verificar se PATH inclui .local/bin
        if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
            export PATH="$HOME/.local/bin:$PATH"
        fi
        
        RCLONE_CMD="$HOME/.local/bin/rclone"
        echo "✅ rclone instalado em: $HOME/.local/bin/"
    else
        echo "❌ curl não encontrado. Não é possível instalar rclone."
        exit 1
    fi
fi

echo ""

# Criar diretório de configuração
CONFIG_DIR="$HOME/.config/rclone"
mkdir -p "$CONFIG_DIR"

# Verificar configuração existente
echo "📋 Configurações existentes:"
if [ -f "$CONFIG_DIR/rclone.conf" ]; then
    echo "  Arquivo de configuração encontrado"
    $RCLONE_CMD listremotes 2>/dev/null | while read remote; do
        echo "    • $remote"
    done
else
    echo "  Nenhuma configuração encontrada (novo)"
fi

echo ""
echo "=========================================="
echo "  CONFIGURAÇÃO GOOGLE DRIVE"
echo "=========================================="
echo ""
echo "Vamos configurar Google Drive como backend de nuvem."
echo ""
echo "Siga as instruções abaixo:"
echo ""

# Guia interativo
cat << 'INSTRUCOES'
🔧 PASSO A PASSO:

1. Execute o comando manual:
   rclone config

2. Escolha 'n' (new remote)

3. Nome: gdrive

4. Selecione: 13 (Google Drive)

5. Client ID: (deixe em branco)

6. Client Secret: (deixe em branco)

7. Scope: 1 (Full access)

8. ID da pasta raiz: (deixe em branco)

9. Editando: n

10. Use auto config? y

11. Será aberto navegador - faça login com Google

12. Copie o código e cole no terminal

13. Configure como team drive? n

14. Confirm: y

✅ PRONTO!
INSTRUCOES

echo ""
echo "Execute agora: rclone config"
echo ""
read -p "Pressione ENTER quando terminar a configuração..."

# Verificar se configurou
if $RCLONE_CMD listremotes | grep -q "gdrive:"; then
    echo ""
    echo "✅ Google Drive configurado!"
    
    # Testar
    echo ""
    echo "🧪 Testando conexão..."
    if $RCLONE_CMD ls gdrive: --max-depth 1 > /dev/null 2>&1; then
        echo "✅ Conexão bem-sucedida!"
        
        # Criar pasta OpenClaw_Backup
        echo ""
        echo "📁 Criando estrutura de pastas..."
        $RCLONE_CMD mkdir gdrive:OpenClaw_Backup 2>/dev/null || true
        $RCLONE_CMD mkdir gdrive:OpenClaw_Backup/Backups 2>/dev/null || true
        $RCLONE_CMD mkdir gdrive:OpenClaw_Backup/Videos 2>/dev/null || true
        $RCLONE_CMD mkdir gdrive:OpenClaw_Backup/Relatorios 2>/dev/null || true
        $RCLONE_CMD mkdir gdrive:OpenClaw_Backup/Midia 2>/dev/null || true
        
        echo "✅ Pastas criadas:"
        $RCLONE_CMD ls gdrive:OpenClaw_Backup --max-depth 1
    else
        echo "⚠️ Conexão falhou. Verifique as credenciais."
    fi
else
    echo "⚠️ Google Drive não encontrado na configuração."
fi

echo ""
echo "=========================================="
echo "  CONFIGURAÇÃO ADICIONAL (OPCIONAL)"
echo "=========================================="
echo ""

cat << 'OUTROS'
Quer configurar outros serviços?

ONEDRIVE:
  rclone config
  → Escolha 'n' → Nome: onedrive
  → Selecione: 25 (OneDrive)
  → Siga autenticação

DROPBOX:
  rclone config
  → Escolha 'n' → Nome: dropbox
  → Selecione: 11 (Dropbox)
  → Crie app em https://www.dropbox.com/developers

MEGA:
  rclone config
  → Escolha 'n' → Nome: mega
  → Selecione: 33 (Mega)
  → Insira email e senha

OUTROS:
  Veja lista completa: rclone listremotes
OUTROS

echo ""
echo "=========================================="
echo "  AUTOMATIZAÇÃO"
echo "=========================================="
echo ""

# Criar scripts de backup
SCRIPT_BACKUP="$HOME/organizacao/scripts/backup_automatico_rclone.sh"
cat > "$SCRIPT_BACKUP" << 'BACKUPSCRIPT'
#!/bin/bash
# Backup automático com rclone

DATA=$(date +%Y-%m-%d_%H-%M-%S)
LOG="$HOME/organizacao/backup/backup_rclone_$DATA.log"

echo "Backup automático - $DATA" | tee "$LOG"

# Sync pastas importantes
rclone sync "$HOME/organizacao/advocacia/" gdrive:OpenClaw_Backup/Advocacia/ --progress --create-empty-src-dirs 2>&1 | tee -a "$LOG"
rclone sync "$HOME/organizacao/servidor-publico/" gdrive:OpenClaw_Backup/Servidor_Publico/ --progress --create-empty-src-dirs 2>&1 | tee -a "$LOG"
rclone sync "$HOME/.openclaw/config/" gdrive:OpenClaw_Backup/Config/ --progress 2>&1 | tee -a "$LOG"

# Upload de relatórios
cd "$HOME/organizacao/monitoramento/relatorios-diarios"
for file in *.md; do
    rclone copy "$file" gdrive:OpenClaw_Backup/Relatorios/ 2>&1 | tee -a "$LOG"
done

echo "✅ Backup concluído!" | tee -a "$LOG"
BACKUPSCRIPT

chmod +x "$SCRIPT_BACKUP"
echo "✅ Script criado: $SCRIPT_BACKUP"

echo ""
echo "=========================================="
echo "  AGENDAMENTO (CRON)"
echo "=========================================="
echo ""

# Agendar backup diário
CRON_JOB="0 2 * * * $SCRIPT_BACKUP"
(crontab -l 2>/dev/null | grep -v "$SCRIPT_BACKUP"; echo "$CRON_JOB") | crontab -

echo "✅ Backup agendado todos os dias às 2h da manhã"
echo "   Para verificar: crontab -l"
echo "   Para desativar: crontab -e e delete a linha"

echo ""
echo "=========================================="
echo "  COMANDOS ÚTEIS"
echo "=========================================="
echo ""

cat << 'COMANDOS'
Ver arquivos no Google Drive:
  rclone ls gdrive: --max-depth 1

Sync local → nuvem (sobrescreve nuvem):
  rclone sync /caminho/local gdrive:/caminho/destino

Copiar local → nuvem (sem deletar):
  rclone copy /caminho/local gdrive:/caminho/destino

Copiar nuvem → local:
  rclone copy gdrive:/caminho /caminho/local

Mover arquivos:
  rclone move /caminho/local gdrive:/caminho

Ver espaço:
  rclone about gdrive:

Montar Google Drive (Linux):
  mkdir ~/gdrive
  rclone mount gdrive: ~/gdrive

Limpar lixo (vazio lixeira):
  rclone cleanup gdrive:
COMANDOS

echo ""
echo "=========================================="
echo "  PRÓXIMOS PASSOS"
echo "=========================================="
echo ""
echo "✅ rclone configurado (espero!)"
echo ""
echo "Para transferir os 304 MB de backups agora:"
echo "  rclone copy ~/organizacao/staging_nuvem/backups_transferir.tar.gz gdrive:OpenClaw_Backup/Backups/"
echo ""
echo "Ou execute o backup automático:"
echo "  ~/organizacao/scripts/backup_automatico_rclone.sh"
echo ""
echo "=========================================="
