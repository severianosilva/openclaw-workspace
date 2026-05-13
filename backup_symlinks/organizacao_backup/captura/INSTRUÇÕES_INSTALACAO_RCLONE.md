# Instruções para Instalação do RClone

O RClone é necessário para fazer backup dos dados do OpenClaw para serviços de nuvem como Google Drive, Dropbox, etc.

## Instalação

Para instalar o RClone, execute o seguinte comando no terminal:

```bash
sudo snap install rclone --classic
```

OU alternativamente:

```bash
curl https://rclone.org/install.sh | sudo bash
```

## Configuração

Após a instalação, você tem duas opções para configurar o RClone:

### Opção 1: Usar o script auxiliar (recomendado)
Execute o script auxiliar que guiará você pelo processo:

```bash
/home/severosa/organizacao/captura/configurar_rclone_para_backup.sh
```

### Opção 2: Configuração manual
Execute o comando e siga as instruções na tela para adicionar um novo provedor de nuvem:

```bash
rclone config
```

## Configuração para Google Drive (detalhes)

1. Execute `rclone config`
2. Escolha "n" para New remote
3. Dê um nome (use "gdrive" para que o script de backup funcione automaticamente)
4. Escolha "drive" para Google Drive
5. Pressione ENTER para usar os valores padrão para as próximas opções
6. Quando chegar na autenticação OAuth, copie o link fornecido e abra em um navegador
7. Faça login na sua conta Google e autorize o acesso
8. Copie o código de autorização de volta para o terminal
9. Responda "n" para editar advanced config
10. Responda "y" para confirmar a configuração

## Uso com o Script de Backup do OpenClaw

Depois de configurado, o script `/home/severosa/organizacao/captura/backup_openclaw.sh` automaticamente detectará o RClone e fará upload dos backups para o serviço de nuvem configurado.

## Observação

O script de backup do OpenClaw já está preparado para usar o RClone caso esteja instalado e configurado. Ele tentará fazer upload dos backups para o destino configurado como "gdrive" por padrão.