# YouTube Money Agents - Solução Nuvem Grátis

## 🆓 Opções de Nuvem Grátis

### 1. **GitHub Actions** (Recomendado)
- 2.000 minutos/mês grátis
- Roda Python, FFmpeg
- Agendamento automático
- Upload via CLI

```yaml
# .github/workflows/youtube-bot.yml
name: YouTube Producer
on:
  schedule:
    - cron: '0 18 * * 1,3,5'  # Seg, Qua, Sex às 18h
  workflow_dispatch:

jobs:
  produce:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup FFmpeg
        run: sudo apt-get install ffmpeg
      - name: Generate Content
        run: python crewai_production.py
      - name: Upload
        run: python youtube_upload.py
```

### 2. **Google Colab** (Grátis com conta)
- GPU/TPU grátis
- Execução por até 12h
- Montar Google Drive

```python
# colab_production.py
from google.colab import drive
drive.mount('/content/drive')

# Executar agentes
!python youtube_agents.py --run-all

# Salvar no Drive
!cp output/*.mp4 /content/drive/MyDrive/youtube_videos/
```

### 3. **Replit** (Plano Hacker - grátis)
- 500MB storage
- Sempre ativo
- Web IDE integrado

### 4. **Railway.app** ($5 créditos iniciais)
- Deploy fácil
- Cron jobs
- PostgreSQL incluso

## 🛠️ Arquitetura Nuvem

```
GitHub Repo
    │
    ├── crewai_production.py  (lógica dos agentes)
    ├── cloud_config.py       (config nuvem)
    └── requirements.txt

GitHub Actions (Agendado)
    │
    ├── Gerar roteiro        (LLM API grátis: Groq, Together)
    ├── Criar vídeo          (FFmpeg)
    ├── Gerar thumbnail      (Pillow)
    └── Upload YouTube       (YouTube API)
```

## 🔑 APIs Grátis Recomendadas

| API | Grátis | Quota |
|-----|--------|-------|
| **Groq** | 14.400 tokens/dia | LLM rápido |
| **Together.ai** | $25 créditos | Varios modelos |
| **Hugging Face** | 30.000 chars/mês | Texto + áudio |
| **YouTube API** | Ilimitado | 10.000 unidades/dia |

## 🚀 Setup Rápido

```bash
# 1. Fork no GitHub
# 2. Adicionar secrets:
#    - YOUTUBE_API_KEY
#    - GROQ_API_KEY
#    - HF_TOKEN
# 3. Ativar GitHub Actions
```

## 💰 Custos Reais

| Recurso | Custo |
|---------|-------|
| GitHub Actions | **$0** (2k min grátis) |
| Groq API | **$0** (14k tokens/dia) |
| YouTube API | **$0** (grátis) |
| Armazenamento | **$0** (no repo) |

**Total: R$ 0,00/mês**

## 📋 Próximos Passos

1. Criar repo no GitHub
2. Configurar secrets
3. Ativar workflow
4. Aguardar primeiro vídeo!