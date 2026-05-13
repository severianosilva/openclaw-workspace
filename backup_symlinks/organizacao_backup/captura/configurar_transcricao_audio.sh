#!/bin/bash

# Script para configurar a transcrição de áudio GRATUITA
# Explica as opções de transcrição gratuitas disponíveis

echo "Configuração do Sistema de Transcrição de Áudio GRATUITO"
echo "======================================================="

echo ""
echo "A transcrição automática de mensagens de áudio recebidas via WhatsApp"
echo "pode ser feita de forma GRATUITA usando tecnologias open-source."
echo ""

echo "Opções disponíveis:"
echo "1. Whisper local (open-source, funciona offline após instalação)"
echo "2. Google STT gratuito (online, com limites diários)"
echo "3. Ambos (recomendado)"
echo ""

read -p "Deseja prosseguir com a configuração? (s/n): " resposta

if [[ $resposta =~ ^[Ss]$ ]]; then
    echo ""
    echo "Executando script de configuração gratuito..."
    
    # Executar o script de configuração gratuito
    bash /home/severosa/organizacao/captura/configurar_transcricao_gratuita.sh
    
    echo ""
    echo "Configuração gratuita concluída!"
    echo ""
    echo "A transcrição de áudio está agora configurada e pronta para uso."
    echo "Os arquivos de áudio recebidos via WhatsApp serão automaticamente"
    echo "transcritos usando métodos gratuitos e salvos em ~/organizacao/captura/transcricoes/"
else
    echo ""
    echo "Você também pode usar o serviço pago da OpenAI Whisper:"
    echo ""
    echo "Para obter uma chave de API da OpenAI:"
    echo ""
    echo "1. Acesse https://platform.openai.com/api-keys"
    echo "2. Faça login na sua conta OpenAI"
    echo "3. Clique em 'Create new secret key'"
    echo "4. Copie a chave gerada e execute o script antigo:"
    echo "   ~/organizacao/captura/configurar_transcricao_audio_original.sh"
fi

echo ""
echo "Configuração gratuita finalizada."