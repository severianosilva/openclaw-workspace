#!/bin/bash

# Script para configurar o sistema de transcrição de áudio gratuito
# Instala dependências e prepara o ambiente

echo "Configuração do Sistema de Transcrição de Áudio Gratuito"
echo "========================================================"

echo ""
echo "Este script irá configurar o sistema para usar transcrição de áudio gratuita"
echo "usando tecnologias open-source como Whisper local ou outros serviços."
echo ""

# Verificar se o ffmpeg está instalado
if command -v ffmpeg &> /dev/null; then
    echo "✓ FFmpeg já está instalado"
else
    echo "✗ FFmpeg não encontrado"
    echo ""
    echo "Para instalar o FFmpeg (necessário para processar arquivos de áudio):"
    echo "Ubuntu/Debian: sudo apt update && sudo apt install ffmpeg"
    echo "macOS: brew install ffmpeg"
    echo "Windows: Baixar do site oficial https://ffmpeg.org/download.html"
    echo ""
    echo "AVISO: Este script não pode instalar o FFmpeg automaticamente sem permissões sudo."
fi

echo ""
echo "Opções de configuração:"
echo "1. Configurar Whisper local (requer Python e pip)"
echo "2. Configurar apenas serviços online gratuitos (Google STT)"
echo "3. Ambos"
echo ""

read -p "Escolha uma opção (1/2/3): " opcao

case $opcao in
    1)
        echo ""
        echo "Instalando Whisper local..."
        echo "Verificando se Python e pip estão disponíveis..."
        
        if command -v python3 &> /dev/null && command -v pip3 &> /dev/null; then
            echo "✓ Python3 e pip3 encontrados"
            echo "Instalando OpenAI Whisper..."
            pip3 install openai-whisper
            
            if [ $? -eq 0 ]; then
                echo "✓ Whisper instalado com sucesso"
                echo ""
                echo "OPCIONAL: Para melhor desempenho, instale também:"
                echo "pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu"
            else
                echo "✗ Falha na instalação do Whisper"
            fi
        else
            echo "✗ Python3 ou pip3 não encontrados"
            echo "Instale Python 3.8 ou superior e pip para continuar"
        fi
        ;;
    2)
        echo ""
        echo "Instalando bibliotecas para serviços online gratuitos..."
        echo "Verificando se Python e pip estão disponíveis..."
        
        if command -v python3 &> /dev/null && command -v pip3 &> /dev/null; then
            echo "✓ Python3 e pip3 encontrados"
            echo "Instalando SpeechRecognition..."
            pip3 install SpeechRecognition pyaudio
            
            if [ $? -eq 0 ]; then
                echo "✓ SpeechRecognition instalado com sucesso"
                echo ""
                echo "AVISO: O serviço Google STT tem limites gratuitos diários."
                echo "Para uso intensivo, considere obter uma chave de API ou usar Whisper local."
            else
                echo "✗ Falha na instalação do SpeechRecognition"
                echo "Tentando alternativa..."
                pip3 install SpeechRecognition
            fi
        else
            echo "✗ Python3 ou pip3 não encontrados"
            echo "Instale Python 3.8 ou superior e pip para continuar"
        fi
        ;;
    3)
        echo ""
        echo "Instalando ambos os sistemas..."
        echo "Verificando se Python e pip estão disponíveis..."
        
        if command -v python3 &> /dev/null && command -v pip3 &> /dev/null; then
            echo "✓ Python3 e pip3 encontrados"
            
            echo "Instalando OpenAI Whisper..."
            pip3 install openai-whisper
            
            if [ $? -eq 0 ]; then
                echo "✓ Whisper instalado com sucesso"
            else
                echo "✗ Falha na instalação do Whisper"
            fi
            
            echo "Instalando SpeechRecognition..."
            pip3 install SpeechRecognition pyaudio
            
            if [ $? -eq 0 ]; then
                echo "✓ SpeechRecognition instalado com sucesso"
            else
                echo "✗ Falha na instalação do SpeechRecognition"
                echo "Tentando alternativa..."
                pip3 install SpeechRecognition
            fi
            
            echo ""
            echo "OPCIONAL: Para melhor desempenho do Whisper, instale também:"
            echo "pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu"
        else
            echo "✗ Python3 ou pip3 não encontrados"
            echo "Instale Python 3.8 ou superior e pip para continuar"
        fi
        ;;
    *)
        echo "Opção inválida. Saindo."
        exit 1
        ;;
esac

echo ""
echo "Configuração concluída!"
echo ""
echo "Para testar o sistema, execute:"
echo "python3 /home/severosa/organizacao/captura/transcricao_falante_local.py"
echo ""
echo "O sistema tentará usar o melhor método disponível (local primeiro, depois online)."