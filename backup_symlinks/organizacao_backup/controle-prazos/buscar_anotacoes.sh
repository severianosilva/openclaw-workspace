#!/bin/bash

# Script para buscar anotações nos processos

echo "=== Busca de Anotações nos Processos ==="
echo ""

if [ $# -eq 0 ]; then
    echo "Uso: $0 <termo_de_busca>"
    echo ""
    echo "Exemplo: $0 'constitucional'"
    exit 1
fi

TERMO_BUSCA="$1"
DIRETORIO_BASE="/home/severosa/organizacao/advocacia/ativos/"

echo "Buscando por '$TERMO_BUSCA' nas anotações de processos..."
echo ""

# Procurar o termo nas anotações de todos os processos
RESULTADOS=$(find "$DIRETORIO_BASE" -name "*.md" -path "*/anotacoes/*" -exec grep -l -i "$TERMO_BUSCA" {} \; 2>/dev/null)

if [ -z "$RESULTADOS" ]; then
    echo "Nenhum resultado encontrado para '$TERMO_BUSCA' nas anotações."
else
    echo "Resultados encontrados:"
    echo "$RESULTADOS"
    echo ""
    echo "Detalhes:"
    echo "--------"
    echo "$RESULTADOS" | while read -r arquivo; do
        echo ""
        echo "Arquivo: $arquivo"
        echo "$(grep -n -i -A 2 -B 2 "$TERMO_BUSCA" "$arquivo" 2>/dev/null)"
        echo "----------------------------------------"
    done
fi

# Também buscar em outros locais relevantes
echo ""
echo "Buscando em outros arquivos de controle..."
OUTROS_RESULTADOS=$(find "$DIRETORIO_BASE" -name "controle-processo.md" -exec grep -l -i "$TERMO_BUSCA" {} \; 2>/dev/null)

if [ -n "$OUTROS_RESULTADOS" ]; then
    echo "Resultados adicionais encontrados em controles de processo:"
    echo "$OUTROS_RESULTADOS"
    echo ""
    echo "Detalhes:"
    echo "--------"
    echo "$OUTROS_RESULTADOS" | while read -r arquivo; do
        echo ""
        echo "Arquivo: $arquivo"
        echo "$(grep -n -i -A 2 -B 2 "$TERMO_BUSCA" "$arquivo" 2>/dev/null)"
        echo "----------------------------------------"
    done
fi