#!/bin/bash

# Script de configuração para instalação e setup do Refly
echo "Configuração do Refly para o Sistema Jurídico Automatizado"
echo "========================================================"

# Verificar se o Node.js está instalado
if ! command -v node &> /dev/null; then
    echo "Node.js não encontrado. Por favor, instale o Node.js antes de continuar."
    echo "Você pode instalar via: https://nodejs.org/"
    exit 1
fi

# Verificar versão do Node.js
NODE_VERSION=$(node -v | cut -d'v' -f2)
NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1)

if [ "$NODE_MAJOR" -lt 18 ]; then
    echo "Versão do Node.js muito antiga: $NODE_VERSION"
    echo "Por favor, atualize para Node.js 18 ou superior"
    exit 1
fi

echo "Node.js versão $NODE_VERSION encontrada."

# Verificar se o npm está instalado
if ! command -v npm &> /dev/null; then
    echo "npm não encontrado. Por favor, verifique sua instalação do Node.js"
    exit 1
fi

echo "npm encontrado."

# Instalar o CLI do Refly globalmente
echo "Instalando o CLI do Refly..."
npm install -g @powerformer/refly-cli@0.1.25

if [ $? -ne 0 ]; then
    echo "Falha na instalação do CLI do Refly"
    echo "Tentando com --force..."
    npm install -g --force @powerformer/refly-cli@0.1.25
    
    if [ $? -ne 0 ]; then
        echo "Falha na instalação do CLI do Refly mesmo com --force"
        exit 1
    fi
fi

echo "CLI do Refly instalado com sucesso!"

# Criar diretório para as skills do Refly
REFLY_SKILLS_DIR="/home/severosa/organizacao/controle-prazos/refly-skills"
mkdir -p "$REFLY_SKILLS_DIR"

echo "Diretório para skills do Refly criado: $REFLY_SKILLS_DIR"

# Criar estrutura básica de uma skill de exemplo
EXAMPLE_SKILL_DIR="$REFLY_SKILLS_DIR/juridical-ocr-processor"
mkdir -p "$EXAMPLE_SKILL_DIR"

cat > "$EXAMPLE_SKILL_DIR/SKILL.md" << 'EOF'
---
name: juridical-ocr-processor
description: Processador de OCR especializado para documentos jurídicos
author: Sistema Jurídico Automatizado
version: 1.0.0
category: document-processing
tags: [ocr, legal, document-analysis, text-extraction]
---

# Processador de OCR Jurídico

Esta skill aplica OCR especializado em documentos jurídicos usando múltiplas estratégias para máxima precisão.

## Funcionalidades

- Extração de texto de documentos PDF jurídicos
- Aplicação de OCR usando Tesseract como primeira tentativa
- Fallback para Qwen-VL OCR quando necessário
- Análise de confiança do OCR
- Formatação de texto para análise jurídica subsequente

## Configuração

A skill requer acesso aos seguintes recursos:

- Motor OCR Tesseract instalado
- Acesso à API Qwen-VL (quando configurada)
- Permissões de leitura para arquivos de entrada
- Permissões de escrita para arquivos de saída

## Uso

A skill pode ser invocada diretamente ou como parte de fluxos maiores de análise jurídica.
EOF

echo "Skill de exemplo criada: $EXAMPLE_SKILL_DIR/SKILL.md"

# Criar arquivo de configuração do Refly
cat > "$REFLY_SKILLS_DIR/refly.config.json" << 'EOF'
{
  "name": "Sistema Jurídico Automatizado - Skills",
  "description": "Coleção de skills para automação de tarefas jurídicas",
  "version": "1.0.0",
  "skillsDirectory": "./skills",
  "development": {
    "autoReload": true,
    "debug": true
  },
  "production": {
    "autoReload": false,
    "debug": false
  },
  "integrations": {
    "models": {
      "default": "qwen-portal/coder-model"
    },
    "storage": {
      "type": "local",
      "path": "./data"
    }
  }
}
EOF

echo "Arquivo de configuração do Refly criado."

# Criar README explicativo
cat > "$REFLY_SKILLS_DIR/README.md" << 'EOF'
# Skills do Refly para o Sistema Jurídico Automatizado

Este diretório contém as skills do Refly que fazem parte do sistema jurídico automatizado.

## Estrutura

- `skills/` - Diretório contendo as skills individuais
- `data/` - Diretório para dados persistentes
- `refly.config.json` - Configuração do ambiente Refly

## Skills Implementadas

### juridical-ocr-processor
Processa documentos jurídicos com OCR especializado para extração de texto.

### Próximas Skills a Serem Implementadas
- juridical-document-analyzer
- juridical-reminder-creator
- juridical-document-classifier
- juridical-precedents-search
- juridical-report-generator

## Instalação

1. Certifique-se de que o CLI do Refly está instalado:
   ```bash
   npm install -g @powerformer/refly-cli
   ```

2. Navegue até este diretório e instale as dependências:
   ```bash
   cd /caminho/para/refly-skills
   npm install
   ```

3. Para desenvolvimento, inicie o servidor de desenvolvimento:
   ```bash
   refly dev
   ```

## Uso

As skills podem ser chamadas diretamente ou compostas em fluxos de trabalho mais complexos.
EOF

echo "README do Refly criado."

# Criar esqueleto para o próximo passo: implantação local do Refly
cat > "$REFLY_SKILLS_DIR/deploy-local.sh" << 'EOF'
#!/bin/bash

# Script para implantação local do Refly
echo "Implantando Refly localmente..."

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "Docker não encontrado. Instalando Docker..."
    
    # Detectar sistema operacional
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
    else
        echo "Não foi possível detectar o sistema operacional"
        exit 1
    fi
    
    if [[ $OS == *"Ubuntu"* ]] || [[ $OS == *"Debian"* ]]; then
        sudo apt update
        sudo apt install -y docker.io docker-compose
        sudo systemctl start docker
        sudo systemctl enable docker
        sudo usermod -aG docker $USER
    else
        echo "Sistema operacional não suportado automaticamente para instalação do Docker"
        echo "Por favor, instale o Docker manualmente."
        exit 1
    fi
fi

# Criar docker-compose.yml para o Refly
cat > "$REFLY_SKILLS_DIR/docker-compose.yml" << 'DOCKER_EOF'
version: '3.8'

services:
  refly-server:
    image: reflyai/refly:latest
    container_name: refly-server
    ports:
      - "5700:5700"
    volumes:
      - ./skills:/app/skills
      - ./data:/app/data
      - ./refly.config.json:/app/config.json
    environment:
      - NODE_ENV=production
      - PORT=5700
    restart: unless-stopped
    networks:
      - refly-network

networks:
  refly-network:
    driver: bridge
DOCKER_EOF

echo "docker-compose.yml criado para implantação local do Refly."
echo ""
echo "Para iniciar o Refly localmente, execute:"
echo "cd $REFLY_SKILLS_DIR"
echo "docker-compose up -d"
echo ""
echo "O Refly estará disponível em: http://localhost:5700"
EOF

chmod +x "$REFLY_SKILLS_DIR/deploy-local.sh"

echo "Script de implantação local criado."

echo ""
echo "Configuração do Refly concluída!"
echo ""
echo "Próximos passos:"
echo "1. Revise os arquivos criados em $REFLY_SKILLS_DIR"
echo "2. Personalize as skills conforme necessário"
echo "3. Execute o script deploy-local.sh para iniciar o Refly localmente"
echo "4. Acesse http://localhost:5700 para configurar o Refly"
echo ""
echo "A integração do Refly com o sistema jurídico automatizado está pronta para início!"