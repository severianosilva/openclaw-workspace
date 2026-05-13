# YouTube Money Agents - CrewAI Edition

## Instalação

```bash
# 1. Instalar dependências
pip install crewai langchain langchain-openai python-dotenv pillow moviepy ffmpeg-python

# 2. Configurar API OpenAI
echo OPENAI_API_KEY="sua-chave-aqui" > .env

# 3. Executar
python crewai_agents.py
```

## Arquitetura CrewAI

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Researcher │────▶│ Scriptwriter│────▶│   Designer  │
└─────────────┘     └─────────────┘     └─────────────┘
                                                           
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ VideoEditor │◀────│  Publisher  │◀────│  (feedback) │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Agentes

| Agente | Função | Output |
|--------|--------|--------|
| **Researcher** | Pesquisa temas lucrativos | Topics JSON |
| **Scriptwriter** | Escreve roteiros virais | Script completo |
| **Designer** | Cria thumbnails profissionais | PNG thumbnails |
| **VideoEditor** | Produz vídeos com FFmpeg | MP4 final |
| **Publisher** | Upload e otimização | URL do vídeo |

## Uso

```python
from crewai_agents import run_crew

# Executar para nicho específico
result = run_crew("finances")
print(result)
```

## Workflows

### Produção Rápida (1 vídeo)
```bash
python crewai_agents.py --niche finances --type quick
```

### Produção em Massa
```bash
python crewai_agents.py --niche finances --type batch --count 10
```

## Integrações

- **OpenAI GPT-4** - Geração de conteúdo
- **FFmpeg** - Edição de vídeo
- **YouTube API** - Upload automático
- **Pillow** - Geração de imagens

## Projetos de Referência

- https://github.com/joaomdmoura/crewAI
- https://github.com/dairon/youtube-automation
- https://github.com/topics/youtube-automation

## Exemplo de Output

```json
{
  "video_id": "dQw4w9WgXcQ",
  "title": "5 Maneiras de Ganhar Dinheiro em 2024",
  "cpm": "$25.50",
  "estimated_revenue": "$765",
  "upload_date": "2024-01-15"
}
```