# 🚀 Guia de Início Rápido

## 1. Instalação

```bash
# Entrar no diretório
cd youtube_video_agent

# Instalar dependências
pip install -r requirements.txt
```

## 2. Usar com Roteiro Existente

```bash
# Executar o agente com um roteiro existente
python agente_video_youtube.py ../youtube_backup/roteiros/roteiro_como_aprender_inglês_rápido_em_2026.json
```

## 3. Fluxo Completo (do início ao fim)

### Passo 1: Gerar Roteiro
```bash
cd ../youtube_backup
python gerar_roteiro_youtube.py "Como Investir na Bolsa em 2026" finanças
```

### Passo 2: Gerar Vídeo
```bash
cd ../youtube_video_agent
python agente_video_youtube.py ../youtube_backup/roteiros/roteiro_como_investir_na_bolsa_em_2026.json
```

### Passo 3: Renderizar no Colab
1. Acesse [Google Colab](https://colab.research.google.com)
2. Faça upload do arquivo `workflow_video_cloud.ipynb`
3. Execute todas as células
4. Faça upload dos arquivos gerados
5. Baixe o vídeo final

## 4. Usar com ElevenLabs (Qualidade Premium)

```bash
# Primeiro, obtenha sua API key em https://elevenlabs.io
export ELEVENLABS_API_KEY="sua_chave_aqui"

# Executar com ElevenLabs
python agente_video_youtube.py roteiro.json --tts elevenlabs --voice Rachel
```

## 5. Exemplo Completo

```bash
# Exemplo completo de uso
python agente_video_youtube.py \
  ../youtube_backup/roteiros/roteiro_como_aprender_inglês_rápido_em_2026.json \
  --tts gtts \
  --output ./meu_video
```

## 📂 O que é gerado?

```
output/
├── audio/
│   └── audio_titulo_do_video.mp3   # Áudio da narração
├── images/
│   └── stock_*.jpg                 # Imagens para cada cena
├── subtitles/
│   └── legendas_*.srt              # Legendas sincronizadas
└── colab_package.json              # Manifesto para o Colab
```

## 🎯 Dicas para Melhor Qualidade

1. **TTS**: gTTS é grátis, mas ElevenLabs tem qualidade superior
2. **Imagens**: Quanto mais específico o tema, melhor a imagem
3. **Roteiro**: Use títulos curtos e diretos para melhor engajamento
4. **Colab**: Use GPU em Runtime > Change runtime type

## ❓ Perguntas Frequentes

**Q: Preciso de GPU para executar?**
A: Não! O agente Python funciona em CPU. O Colab usa GPU grátis.

**Q: Qual a duração máxima do vídeo?**
A: Ilimitada, mas vídeos longos levam mais tempo para renderizar.

**Q: Posso usar outras API de TTS?**
A: Sim! Edite o código para adicionar sua API preferida.