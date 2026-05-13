# 🎬 YouTube Video Generation Agent

Automatiza a criação de vídeos para YouTube a partir de roteiros, usando APIs gratuitas e Google Colab.

## Visão Geral

Este agente conecta-se com o agente de geração de roteiros (`gerar_roteiro_youtube.py`) e produz vídeos completos:

1. **Lê roteiros** do agente anterior (arquivos JSON)
2. **Gera áudio TTS** usando gTTS (gratuito) ou ElevenLabs
3. **Cria cenas visuais** com imagens de stock (Unsplash, Picsum)
4. **Montage final** no Google Colab (processamento em nuvem grátis)
5. **Exporta vídeo** pronto para upload no YouTube

## Arquitetura

```
roteiro.json ──► agente_video.py ──► audio.mp3 ──► cenas/ ──► Google Colab ──► video_final.mp4
                    │                     │            │
                    │                     │            └── imagens + legendas
                    │                     │
                    └── TTS (gTTS/EL) ────┘
```

## Guia de Uso Rápido

```bash
# 1. Instalar dependências
pip install gtts moviepy pillow requests googletrans==4.0.0-rc1

# 2. Gerar roteiro (se já não existir)
python gerar_roteiro_youtube.py "Título do Vídeo" educacao

# 3. Executar agente de vídeo
python agente_video_youtube.py roteiro_como_aprender_inglês_rápido_em_2026.json

# 4. Upload no Colab (opcional, para renderização final)
# Abra notebook_producao_video.ipynb no Google Colab
```

## Fluxo Completo

### Etapa 1: Parse do Roteiro
- Extrai estrutura JSON
- Identifica pontos principais
- Gera narração completa

### Etapa 2: Geração de Áudio TTS
- Texto para fala com gTTS (grátis) ou ElevenLabs (melhor qualidade)
- Salva como MP3/WAV

### Etapa 3: Cenas Visuais
- Baixa imagens de stock (Unsplash API ou Picsum)
- Cria overlays de texto
- Gera legendas sincronizadas

### Etapa 4: Montagem no Colab
- Abra o notebook no Google Colab
- Faça upload do áudio + imagens
- Renderize vídeo completo

## APIs Gratuitas Suportadas

| API | Uso | Custo |
|-----|-----|-------|
| gTTS | Texto para fala | Grátis |
| Unsplash Source | Imagens de stock | Grátis |
| Picsum | Imagens aleatórias | Grátis |
| Pika Labs | Geração de vídeo AI | Free tier limitado |
| ElevenLabs | TTS premium | Free tier 10k chars/mês |

## Estrutura de Arquivos

```
youtube_video_agent/
├── agente_video_youtube.py     # Agente principal
├── workflow_video_cloud.ipynb  # Notebook Colab
├── templates/
│   ├── cena_template.json      # Template de cena
│   └── estilo_visual.json      # Configurações visuais
├── output/
│   ├── audio/                  # Áudios gerados
│   ├── imagens/                # Imagens de stock
│   └── legendas/               # SRT gerado
└── scripts/
    └── gerar_roteiro_youtube.py # Agente anterior
```

## Exemplo de Configuração

```python
# config.py
TTS_CONFIG = {
    "provider": "gtts",  # ou "elevenlabs"
    "language": "pt-BR",
    "slow": False
}

STOCK_CONFIG = {
    "source": "unsplash",  # ou "picsum"
    "width": 1920,
    "height": 1080
}

VIDEO_CONFIG = {
    "fps": 24,
    "codec": "libx264",
    "audio_codec": "aac",
    "bitrate": "5000k"
}
```