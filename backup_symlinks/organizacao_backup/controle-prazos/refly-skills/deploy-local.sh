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
