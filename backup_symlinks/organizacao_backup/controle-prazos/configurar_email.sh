#!/bin/bash

# Script para configurar o envio de relatórios por e-mail e WhatsApp

echo "Configuração do sistema de envio de relatórios"
echo "=============================================="
echo ""

echo "O sistema de envio por WhatsApp já está configurado pois você está conectado como:"
echo "$(openclaw sessions_list | grep whatsapp || echo '+553182436396')"
echo ""

echo "Para o envio por e-mail, configure suas credenciais:"
echo ""

# Solicitar informações do usuário
read -p "Digite seu e-mail remetente: " email_remetente
read -s -p "Digite sua senha de app (Gmail) ou senha de e-mail: " senha_email
echo ""
read -p "Digite o SMTP server (padrão: smtp.gmail.com): " smtp_server
smtp_server=${smtp_server:-smtp.gmail.com}
read -p "Digite a porta SMTP (padrão: 587): " smtp_port
smtp_port=${smtp_port:-587}

# Criar arquivo de configuração
cat > ~/.openclaw/email_config.env << EOF
export EMAIL_REMETENTE="$email_remetente"
export SENHA_EMAIL="$senha_email"
export SMTP_SERVER="$smtp_server"
export SMTP_PORT="$smtp_port"
EOF

echo ""
echo "Configuração salva em ~/.openclaw/email_config.env"
echo ""
echo "O sistema está configurado para envio por:"
echo "- WhatsApp: Automaticamente via sua conta conectada (+553182436396)"
echo "- E-mail: Usando as credenciais configuradas acima"
echo ""
echo "Para carregar as configurações de e-mail, use:"
echo "source ~/.openclaw/email_config.env"
echo ""
echo "Para testar o envio de relatório:"
echo "python3 enviar_relatorios_email.py seu_email_destinatario@dominio.com diario ambos"
echo "(envia por ambos os canais)"
echo ""
echo "Opções de canal:"
echo "- email: Apenas por e-mail"
echo "- whatsapp: Apenas por WhatsApp"
echo "- ambos: Por ambos os canais"
echo ""