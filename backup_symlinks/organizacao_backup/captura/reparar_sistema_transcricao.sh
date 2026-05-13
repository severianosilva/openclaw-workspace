#!/bin/bash
# Script para testar e reparar o sistema de transcrição de áudio

echo "=== Reparando Sistema de Transcrição de Áudio ==="
echo ""

# 1. Verificar/installar Vosk
echo "1. Verificando Vosk..."
python3 -c "import vosk" 2>/dev/null && echo "✓ Vosk instalado" || (echo "Instalando Vosk..." && pip3 install vosk --break-system-packages --quiet)

# 2. Verificar/installar ctranslate2 para Whisper
echo "2. Verificando ctranslate2..."
python3 -c "import ctranslate2" 2>/dev/null && echo "✓ ctranslate2 instalado" || (echo "Instalando ctranslate2..." && pip3 install ctranslate2 --break-system-packages --quiet)

# 3. Verificar modelo Vosk
echo "3. Verificando modelo Vosk em português..."
if [ -d "/tmp/vosk-model-small-pt-0.3" ]; then
    echo "✓ Modelo Vosk presente"
else
    echo "Baixando modelo Vosk..."
    wget -q https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip -O /tmp/vosk-model-pt.zip
    python3 -c "import zipfile; zipfile.ZipFile('/tmp/vosk-model-pt.zip', 'r').extractall('/tmp/')"
    echo "✓ Modelo baixado"
fi

# 4. Verificar ffmpeg
echo "4. Verificando ffmpeg..."
which ffmpeg >/dev/null && echo "✓ ffmpeg instalado" || echo "⚠ ffmpeg não encontrado - instale com: sudo apt install ffmpeg"

# 5. Verificar speech_recognition
echo "5. Verificando speech_recognition..."
python3 -c "import speech_recognition" 2>/dev/null && echo "✓ speech_recognition instalado" || (echo "Instalando speech_recognition..." && pip3 install SpeechRecognition --break-system-packages --quiet)

# 6. Verificar pydub
echo "6. Verificando pydub..."
python3 -c "import pydub" 2>/dev/null && echo "✓ pydub instalado" || (echo "Instalando pydub..." && pip3 install pydub --break-system-packages --quiet)

echo ""
echo "=== Sistema de Transcrição Reparado ==="
echo ""
echo "Para testar, execute:"
echo "  python3 /home/severosa/organizacao/captura/transcricao_rapida.py <arquivo_audio>"
echo ""
