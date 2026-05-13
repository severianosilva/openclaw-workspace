# YouTube Money Agents - Produção Profissional

## Projetos Open Source de Referência

### 1. **CrewAI** - Framework de Agentes
- GitHub: github.com/joaomdmoura/crewAI
- Agentes especializados: writer, editor, strategist
- Integração com LLMs para roteirização

### 2. **n8n + FFmpeg** - Automação
- Workflow: n8n.io/integrations/youtube/
- Edição automática: FFmpeg
- Scheduling: YouTube API

### 3. **YouTube Automation (daican.dev)**
- AI voiceovers
- Text-to-video
- Auto metadata optimization

## Implementação Profissional

### Estrutura do Projeto

```
youtube-agents/
├── agents/
│   ├── researcher.py      # Pesquisa de temas
│   ├── scriptwriter.py    # Roteirista AI
│   ├── designer.py        # Designer gráfico
│   ├── editor.py          # Editor de vídeo
│   ├── publisher.py       # Upload YouTube
│   └── analyst.py         # Otimização
├── tools/
│   ├── ffmpeg_wrapper.py  # Wrapper FFmpeg
│   ├── tts.py            # Text-to-speech
│   └── thumbnail_ai.py   # Geração thumbnails
├── workflows/
│   └── video_production.yaml  # Pipeline completo
└── output/
    ├── videos/           # Vídeos finais
    ├── thumbnails/       # Thumbnails
    └── assets/           # Recursos
```

### Pipeline Profissional

```python
# Exemplo de workflow usando CrewAI
from crewai import Agent, Task, Crew

# Agentes
researcher = Agent(
    role='Topic Researcher',
    goal='Find profitable YouTube topics',
    tools=[google_trends, keyword_planner]
)

scriptwriter = Agent(
    role='Script Writer',
    goal='Create engaging video scripts',
    tools=[gpt4, seo_optimizer]
)

video_editor = Agent(
    role='Video Editor',
    goal='Produce professional videos',
    tools=[ffmpeg, moviepy]
)

# Tasks
tasks = [
    Task(researcher, "Research trending topics in finance"),
    Task(scriptwriter, "Write 8-minute script"),
    Task(video_editor, "Create video with intro/outro")
]

crew = Crew(tasks)
crew.run()
```

### Produção com FFmpeg (Profissional)

```bash
# Intro profissional
ffmpeg -f lavfi -i color=c=blue:s=1920x1080:d=3 \
  -vf "drawtext=fontfile=Arial-Bold.ttf:text='TITLE':fontsize=72" \
  -c:v libx264 intro.mp4

# Concatenar clipes
ffmpeg -f concat -i list.txt -c copy output.mp4

# Adicionar áudio
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac final.mp4
```

## Próximos Passos

1. Instalar dependências profissionais:
   - FFmpeg
   - MoviePy
   - CrewAI
   - TTS (text-to-speech)

2. Configurar YouTube API
3. Testar pipeline completo