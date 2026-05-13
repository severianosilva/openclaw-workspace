# Agente de Geração Automática de Vídeos para YouTube

## O que foi criado

Um sistema completo para automatizar a criação de vídeos para YouTube, conectando-se com o agente de roteiros existente.

### Arquivos principais

| Arquivo | Descricao |
|---------|-----------|
| agente_video_youtube.py | Agente principal - gera audio TTS, imagens e prepara arquivos |
| workflow_video_cloud.ipynb | Notebook Google Colab para renderizacao final |
| ai_video_api.py | Integracao com APIs de video AI (Pika, Stable, Runway) |
| exemplo_uso.py | Script de demonstracao |
| requirements.txt | Dependencias Python |
| config.json | Configuracoes do agente |
| QUICKSTART.md | Guia de inicio rapido |

## Como usar

### Instalacao
```
pip install -r requirements.txt
```

### Fluxo completo
```
# 1. Gerar roteiro (ja existe no backup)
# Arquivo: youtube_backup/roteiros/roteiro_como_aprender_ingles_rapido_em_2026.json

# 2. Executar agente de video
python agente_video_youtube.py ../youtube_backup/roteiros/roteiro_como_aprender_ingles_rapido_em_2026.json

# 3. Abrir no Colab e renderizar
# Upload workflow_video_cloud.ipynb no Google Colab
```

## Caracteristicas

### TTS (Texto para Falas)
- gTTS: Gratis, sem necessidade de API key
- ElevenLabs: Qualidade premium, free tier (10k chars/mes)

### Imagens de Stock
- Unsplash Source (gratis, sem API key)
- Picsum (alternativa)
- Fallback com cor solida

### APIs de Video AI (opcional)
- Pika Labs: free tier ~12s de video/mes
- Stable Video Diffusion: 50 credits trial
- RunwayML: 125 segundos/mes

### Renderizacao
- Google Colab (gratis, GPU opcional)
- MoviePy para montagem
- Exportacao MP4 1080p

## Saida

```
output/
├── audio/              # Audio da narracao (MP3)
├── images/             # Imagens de cena (JPG)
├── subtitles/          # Legendas (SRT)
└── colab_package.json  # Manifesto para Colab
```

## Configuracao

Edite config.json para ajustar:
- Configuracoes de TTS
- Resolucao de video
- Fonte de imagens
- Parametros de renderizacao