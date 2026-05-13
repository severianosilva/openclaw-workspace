#!/bin/bash

# Script para enviar relatório diário por e-mail e WhatsApp

DATA_ATUAL=$(date +%Y-%m-%d)
RELATORIO_PATH="/home/severosa/organizacao/monitoramento/relatorios-diarios/relatorio_$DATA_ATUAL.txt"

echo "Verificando relatório de hoje: $DATA_ATUAL"

if [ -f "$RELATORIO_PATH" ]; then
    echo "Relatório encontrado, preparando envio..."
    
    # Ler o conteúdo do relatório
    CONTEUDO_RELATORIO=$(head -20 "$RELATORIO_PATH")  # Pegar apenas as primeiras 20 linhas como resumo
    
    # Criar resumo do relatório
    RESUMO_RELATORIO="RESUMO DO RELATÓRIO DIÁRIO - $DATA_ATUAL

$(echo "$CONTEUDO_RELATORIO")

Para ver o relatório completo, acesse:
$RELATORIO_PATH

Próximos passos para envio automático:
1. Para WhatsApp: Configurar envio via API do WhatsApp Business
2. Para e-mail: Configurar credenciais SMTP com os modelos em /home/severosa/organizacao/monitoramento/modelo_verificar_emails.py"
    
    # Exibir o resumo que seria enviado
    echo "=== RESUMO QUE SERIA ENVIADO ==="
    echo "$RESUMO_RELATORIO"
    echo "==============================="
    
    # Indicar como seria feito o envio por WhatsApp
    echo "NOTA: Para envio automático por WhatsApp, é necessário:"
    echo "  - Configurar a API do WhatsApp Business"
    echo "  - Ou usar o gateway do OpenClaw com as credenciais corretas"
    echo "  - O comando seria semelhante a: openclaw message send --channel whatsapp --target '+5531982436396' --message '...'"
    
    # Indicar como seria feito o envio por e-mail
    echo ""
    echo "NOTA: Para envio automático por e-mail, é necessário:"
    echo "  - Configurar credenciais SMTP (usuário, senha, servidor)"
    echo "  - As configurações de e-mail estão nos modelos em /home/severosa/organizacao/monitoramento/modelo_verificar_emails.py"
    echo "  - Após configurar as credenciais, o envio automático pode ser adicionado a este script."
    
    echo ""
    echo "Relatório diário gerado com sucesso e disponível em: $RELATORIO_PATH"
else
    echo "Nenhum relatório encontrado para hoje: $DATA_ATUAL"
    echo "O relatório será gerado automaticamente às 8h da manhã pelo cron job."
fi