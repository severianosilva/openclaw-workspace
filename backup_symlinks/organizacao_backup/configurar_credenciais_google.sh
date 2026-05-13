#!/bin/bash
###############################################################################
# Script de Configuração de Credenciais Google Drive
# para Análise Processual Jurídica
###############################################################################

echo "======================================================================"
echo "  CONFIGURAÇÃO DE CREDENCIAIS GOOGLE DRIVE"
echo "  Sistema de Análise Processual Jurídica"
echo "======================================================================"
echo ""

# Cores para output
VERDE='\033[0;32m'
AMARELO='\033[1;33m'
VERMELHO='\033[0;31m'
AZUL='\033[0;34m'
NC='\033[0m' # No Color

# Diretório de configuração
CONFIG_DIR="$HOME/.openclaw/credentials"
CREDENTIALS_FILE="$CONFIG_DIR/google_credentials.json"
ENV_FILE="$CONFIG_DIR/google_env.sh"

echo -e "${AZUL}Passo 1: Criando diretório de configuração...${NC}"
mkdir -p "$CONFIG_DIR"
echo -e "${VERDE}✓ Diretório criado: $CONFIG_DIR${NC}"
echo ""

echo -e "${AMARELO}INSTRUÇÕES PARA OBTER CREDENCIAIS GOOGLE:${NC}"
echo "======================================================================"
echo ""
echo "1. Acesse: https://console.cloud.google.com/"
echo "2. Crie um novo projeto ou selecione um existente"
echo "3. No menu lateral, vá em 'APIs e Serviços' > 'Credenciais'"
echo "4. Clique em '+ Criar Credenciais' > 'ID do Cliente OAuth'"
echo "5. Configure a tela de consentimento:"
echo "   - Tipo: Externo"
echo "   - Preencha: Nome do app, email de suporte"
echo "   - Domínios: Não precisa adicionar"
echo "   - Escopos: Adicione 'Google Drive API' > '.../auth/drive.readonly'"
echo ""
echo "6. Crie as credenciais:"
echo "   - Tipo de aplicativo: Aplicativo de computador"
echo "   - Nome: OpenClaw-Legal-System"
echo ""
echo "7. Baixe o arquivo JSON e cole o conteúdo aqui:"
echo "======================================================================"
echo ""

# Se já existe arquivo, mostrar
if [ -f "$CREDENTIALS_FILE" ]; then
    echo -e "${VERDE}Arquivo de credenciais já existe em:${NC}"
    echo "$CREDENTIALS_FILE"
    echo ""
    read -p "Deseja recriar as credenciais? (s/N): " recriar
    if [[ ! "$recriar" =~ ^[Ss]$ ]]; then
        echo -e "${VERDE}Configuração existente mantida.${NC}"
        exit 0
    fi
fi

# Coletar informações manualmente
echo -e "${AZUL}Insira os valores das credenciais Google OAuth2:${NC}"
echo ""

read -p "Client ID: " CLIENT_ID
read -p "Client Secret: " CLIENT_SECRET
read -p "Project ID (opcional): " PROJECT_ID

echo ""
echo -e "${AZUL}Criando arquivo de credenciais...${NC}"

# Criar arquivo JSON no formato correto do Google
cat > "$CREDENTIALS_FILE" << EOF
{
    "installed": {
        "client_id": "$CLIENT_ID",
        "project_id": "$PROJECT_ID",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "$CLIENT_SECRET",
        "redirect_uris": ["http://localhost"]
    }
}
EOF

echo -e "${VERDE}✓ Arquivo de credenciais criado: $CREDENTIALS_FILE${NC}"

# Criar arquivo de variáveis de ambiente
cat > "$ENV_FILE" << EOF
#!/bin/bash
# Variáveis de ambiente Google Drive
export GOOGLE_CLIENT_ID="$CLIENT_ID"
export GOOGLE_CLIENT_SECRET="$CLIENT_SECRET"
export GOOGLE_PROJECT_ID="$PROJECT_ID"
export GOOGLE_CREDENTIALS_PATH="$CREDENTIALS_FILE"
echo "Credenciais Google carregadas com sucesso!"
EOF

chmod +x "$ENV_FILE"
echo -e "${VERDE}✓ Arquivo de ambiente criado: $ENV_FILE${NC}"

# Adicionar ao .bashrc se ainda não estiver presente
if ! grep -q "source $ENV_FILE" "$HOME/.bashrc" 2>/dev/null; then
    echo "" >> "$HOME/.bashrc"
    echo "# Carregar credenciais Google Drive para OpenClaw" >> "$HOME/.bashrc"
    echo "source $ENV_FILE" >> "$HOME/.bashrc"
    echo -e "${VERDE}✓ Configuração adicionada ao .bashrc${NC}"
fi

echo ""
echo "======================================================================"
echo -e "${VERDE}CONFIGURAÇÃO SALVA COM SUCESSO!${NC}"
echo "======================================================================"
echo ""
echo "Arquivos criados:"
echo "  • Credenciais: $CREDENTIALS_FILE"
echo "  • Variáveis:   $ENV_FILE"
echo ""
echo "PRÓXIMOS PASSOS:"
echo "----------------------------------------------------------------------"
echo "1. Execute primeiro a autenticação OAuth2:"
echo "   cd ~/organizacao/controle-prazos"
echo "   source $ENV_FILE"
echo "   python3 autenticar_google_drive.py"
echo ""
echo "2. Isso abrirá um navegador para você autorizar o acesso"
echo ""
echo "3. Após autenticar, o token será salvo automaticamente"
echo ""
echo "======================================================================"
