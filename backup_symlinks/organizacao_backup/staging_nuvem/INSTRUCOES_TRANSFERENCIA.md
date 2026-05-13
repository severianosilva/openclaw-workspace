# Instruções para Transferência Manual

## Arquivos Preparados

### 📦 Backups Antigos
- Arquivo: `backups_antigos.tar.gz`
- Transferir para: Google Drive > OpenClaw_Backup > Backups
- Pode ser excluído do local após confirmação

### 🎵 Mídia Antiga
- Arquivo: `midia_antiga.tar.gz`
- Transferir para: Google Drive > OpenClaw_Backup > Media_Historico
- Áudios antigos do WhatsApp/Telegram

### 📝 Relatórios Antigos
- Lista em: `lista_relatorios.txt`
- Transferir para: Google Drive > OpenClaw_Backup > Relatorios

## Como Transferir Manualmente

### Opção 1: Via Navegador (Fácil)
1. Acesse: https://drive.google.com
2. Crie pasta: OpenClaw_Backup
3. Arraste os arquivos .tar.gz
4. Aguarde upload

### Opção 2: Via rclone (Quando instalar)
```bash
# Instalar rclone
sudo apt install rclone

# Configurar
rclone config

# Transferir automaticamente
~/organizacao/scripts/transferir_nuvem.sh
```

### Opção 3: Microsoft OneDrive
1. Acesse: https://onedrive.live.com
2. Upload direto

## Após Transferência

1. ✅ Verifique se arquivos estão na nuvem
2. ✅ Baixe um arquivo de teste para confirmar
3. ✅ Só então exclua os arquivos locais
4. ✅ Libere espaço no computador

## Espaço a ser Liberado

Veja o relatório em: `relatorio_espaco.txt`
