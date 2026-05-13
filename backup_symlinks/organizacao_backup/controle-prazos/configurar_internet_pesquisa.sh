#!/bin/bash

# Script de configuração para integração com internet para pesquisa jurídica

echo "Configuração da Integração com Internet para Pesquisa Jurídica"
echo "=============================================================="

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python3 não encontrado. Por favor, instale o Python3."
    exit 1
fi

# Verificar se os pacotes necessários estão instalados
echo "Verificando pacotes necessários..."
python3 -c "import requests" 2>/dev/null || { echo "Instalando requests..."; pip3 install --break-system-packages requests; }
python3 -c "import bs4" 2>/dev/null || { echo "Instalando beautifulsoup4..."; pip3 install --break-system-packages beautifulsoup4; }
python3 -c "import lxml" 2>/dev/null || { echo "Instalando lxml..."; pip3 install --break-system-packages lxml; }

echo ""
echo "Configuração da API de Pesquisa"
echo "-------------------------------"

# Solicitar chave da API da Brave Search (opcional)
echo "Para utilizar a API de pesquisa avançada, você pode obter uma chave gratuita da Brave Search:"
echo "1. Acesse: https://brave.com/search/api/"
echo "2. Registre-se para obter uma chave de API gratuita"
echo "3. Cole a chave abaixo (ou deixe em branco para usar métodos alternativos)"
echo ""
read -p "Digite sua chave da API da Brave Search (ou pressione Enter para pular): " BRAVE_API_KEY

if [ ! -z "$BRAVE_API_KEY" ]; then
    # Configurar a variável de ambiente
    if grep -q "BRAVE_SEARCH_API_KEY" ~/.bashrc; then
        sed -i "s|export BRAVE_SEARCH_API_KEY=.*|export BRAVE_SEARCH_API_KEY=$BRAVE_API_KEY|" ~/.bashrc
    else
        echo "export BRAVE_SEARCH_API_KEY=$BRAVE_API_KEY" >> ~/.bashrc
    fi
    
    # Também exportar para a sessão atual
    export BRAVE_SEARCH_API_KEY=$BRAVE_API_KEY
    
    echo "Chave da API da Brave Search configurada com sucesso!"
else
    echo "Nenhuma chave da API fornecida. O sistema usará métodos alternativos de pesquisa."
fi

echo ""
echo "Configuração do Ambiente"
echo "------------------------"

# Verificar se os diretórios necessários existem
mkdir -p ~/organizacao/controle-prazos/cache_pesquisa
mkdir -p ~/organizacao/controle-prazos/resultados_pesquisa

echo "Diretórios de cache e resultados criados."

echo ""
echo "Testando Conexão"
echo "----------------"

# Testar conexão com alguns sites jurídicos importantes
sites_teste=("https://www.stf.jus.br" "https://www.stj.jus.br" "https://www.planalto.gov.br")

for site in "${sites_teste[@]}"; do
    if curl -s --head --request GET "$site" | grep "200\|301\|302" > /dev/null; then
        echo "✓ Conexão com $site: OK"
    else
        echo "✗ Conexão com $site: FALHOU"
    fi
done

echo ""
echo "Configuração Concluída"
echo "======================"
echo ""
echo "A integração com internet para pesquisa jurídica foi configurada com sucesso!"
echo ""
echo "Funcionalidades disponíveis:"
echo "- Pesquisa de jurisprudência em tribunais superiores"
echo "- Consulta a bases de dados jurídicas"
echo "- Verificação de atualizações legislativas"
echo "- Busca de precedentes similares"
echo ""
echo "Para usar a integração, execute:"
echo "python3 ~/organizacao/controle-prazos/integracao_internet_pesquisa_juridica.py '<termo_de_pesquisa>'"
echo ""
echo "Exemplos de uso:"
echo "python3 ~/organizacao/controle-prazos/integracao_internet_pesquisa_juridica.py 'indenização por danos morais'"
echo "python3 ~/organizacao/controle-prazos/integracao_internet_pesquisa_juridica.py --teste"
echo ""
echo "A integração irá funcionar tanto com a API da Brave Search (se configurada) quanto com métodos alternativos."