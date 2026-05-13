#!/bin/bash

# Script para envio de relatórios por WhatsApp

DESTINATARIO="$1"
CAMINHO_RELATORIO="$2"
TIPO_RELATORIO="$3"

if [ -z "$DESTINATARIO" ] || [ -z "$CAMINHO_RELATORIO" ] || [ -z "$TIPO_RELATORIO" ]; then
    echo "Uso: $0 <destinatario> <caminho_relatorio> <tipo_relatorio>"
    exit 1
fi

echo "Enviando relatório $TIPO_RELATORIO por WhatsApp para $DESTINATARIO"

# Ler o conteúdo do relatório
CONTEUDO_RELATORIO=$(cat "$CAMINHO_RELATORIO")

# Limitar o tamanho do conteúdo para envio via WhatsApp
if [ ${#CONTEUDO_RELATORIO} -gt 10000 ]; then
    CONTEUDO_RESUMIDO="${CONTEUDO_RELATORIO:0:10000}[...conteúdo truncado...]"
else
    CONTEUDO_RESUMIDO="$CONTEUDO_RELATORIO"
fi

# Obter apenas o nome do arquivo do relatório
NOME_ARQUIVO=$(basename "$CAMINHO_RELATORIO")
MENSAGEM="Relatório $TIPO_RELATORIO gerado automaticamente. Arquivo: $NOME_ARQUIVO

${CONTEUDO_RESUMIDO:0:500}..."

echo "Enviando mensagem: ${MENSAGEM:0:100}..."

# Enviar via OpenClaw
openclaw message send --channel whatsapp --to "$DESTINATARIO" --message "$MENSAGEM"

if [ $? -eq 0 ]; then
    echo "Relatório enviado por WhatsApp com sucesso!"
    exit 0
else
    echo "Erro ao enviar via WhatsApp"
    exit 1
fi