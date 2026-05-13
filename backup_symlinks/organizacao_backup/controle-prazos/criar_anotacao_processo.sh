#!/bin/bash

# Script para criar anotações em um processo existente

echo "=== Criação de Anotação para Processo ==="
echo ""

if [ $# -eq 0 ]; then
    echo "Uso: $0 <caminho_do_processo> <tipo_de_anotacao>"
    echo ""
    echo "Tipos de anotação disponíveis:"
    echo "  - analise_inicial"
    echo "  - estrategia_defesa"
    echo "  - notas_pesquisa_juridica"
    echo "  - rascunhos_peca"
    echo "  - personalizado <nome_arquivo>"
    echo ""
    echo "Exemplo: $0 '/home/severosa/organizacao/advocacia/ativos/Caso Exemplo 001' 'analise_inicial'"
    exit 1
fi

PROCESSO_PATH="$1"
TIPO_ANOTACAO="$2"

# Verificar se o diretório do processo existe
if [ ! -d "$PROCESSO_PATH" ]; then
    echo "ERRO: Diretório do processo não encontrado: $PROCESSO_PATH"
    exit 1
fi

# Criar pasta de anotações se não existir
ANOTACOES_PATH="$PROCESSO_PATH/anotacoes"
mkdir -p "$ANOTACOES_PATH"

# Tratar tipo personalizado
if [ "$TIPO_ANOTACAO" = "personalizado" ]; then
    if [ -z "$3" ]; then
        echo "Para tipo personalizado, especifique o nome do arquivo"
        exit 1
    fi
    NOME_ARQUIVO="$3.md"
else
    NOME_ARQUIVO="${TIPO_ANOTACAO}.md"
fi

ARQUIVO_ANOTACAO="$ANOTACOES_PATH/$NOME_ARQUIVO"

# Criar arquivo de anotação com cabeçalho padrão
DATA_ATUAL=$(date +"%d/%m/%Y %H:%M:%S")

cat > "$ARQUIVO_ANOTACAO" << EOF
# Anotação: $NOME_ARQUIVO

**Data de Criação:** $DATA_ATUAL
**Tipo:** $TIPO_ANOTACAO

## Conteúdo da Anotação

<!-- Adicione seu conteúdo aqui -->

## Observações

<!-- Espaço para observações adicionais -->

---
Anotação criada automaticamente pelo sistema de controle processual
EOF

echo "Anotação criada com sucesso: $ARQUIVO_ANOTACAO"
echo ""
echo "Deseja abrir o editor para editar a anotação agora? (s/n)"
read resposta

if [ "$resposta" = "s" ] || [ "$resposta" = "S" ]; then
    if command -v nano >/dev/null 2>&1; then
        nano "$ARQUIVO_ANOTACAO"
    elif command -v vim >/dev/null 2>&1; then
        vim "$ARQUIVO_ANOTACAO"
    else
        echo "Editor não encontrado. Anotação criada em: $ARQUIVO_ANOTACAO"
    fi
fi