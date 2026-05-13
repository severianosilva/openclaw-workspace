#!/bin/bash

# Script auxiliar para configurar o RClone para backup do OpenClaw

echo "==========================================="
echo "Configuração do RClone para Backup na Nuvem"
echo "==========================================="
echo ""

# Verificar se o rclone está instalado
if ! command -v rclone &> /dev/null; then
    echo "ERRO: RClone não está instalado!"
    echo ""
    echo "Por favor, instale o RClone primeiro:"
    echo "  sudo snap install rclone --classic"
    echo "OU"
    echo "  curl https://rclone.org/install.sh | sudo bash"
    echo ""
    exit 1
fi

echo "RClone encontrado: $(rclone --version | head -n1)"

echo ""
echo "Este script irá configurar o RClone para backup na nuvem."
echo "Será criado um destino chamado 'gdrive' para backups no Google Drive."
echo ""
echo "Pressione ENTER para continuar ou Ctrl+C para cancelar..."
read

# Iniciar a configuração do rclone
echo ""
echo "Iniciando configuração do RClone..."
echo "Responda às perguntas da seguinte forma:"
echo ""
echo "1. Nome para o novo destino: gdrive"
echo "2. Tipo de armazenamento: Google Drive (digite 'drive')"
echo "3. Para as demais opções, pressione ENTER para usar os valores padrão"
echo "4. Quando pedir para autenticar, siga as instruções no navegador"
echo ""

# Iniciar o assistente de configuração
rclone config

echo ""
echo "==========================================="
echo "Configuração concluída!"
echo "==========================================="
echo ""
echo "Para testar a configuração, você pode executar:"
echo "  rclone ls gdrive: --max-depth 1"
echo ""
echo "O script de backup do OpenClaw já está configurado para usar o destino 'gdrive'"
echo "quando for fazer backup na nuvem."
echo ""
echo "O backup automático diário continuará funcionando normalmente e agora"
echo "também fará upload para o Google Drive se a configuração estiver correta."