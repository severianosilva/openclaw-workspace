# YouTube Script Agent - Summary

## Created Files

### 1. SKILL.md
Main documentation with usage instructions, CLI arguments, and integration details.

### 2. youtube_script_agent.py
Python agent that generates YouTube scripts with:
- Hook generation for first 5 seconds
- Complete script structure (hook, intro, main content, CTAs)
- 4 template types: educacional, entretenimento, review, noticia
- Trend research capability
- Metadata generation (titles, tags, thumbnails, descriptions)
- Score calculation for topic viability

### 3. templates.json
JSON file with template configurations for each type.

### 4. README.md
Project documentation.

### 5. references/
- youtube-script-basic-usage.md - Quick start guide
- youtube-script-lark-integration.md - Lark Base integration guide

## Usage Examples

```bash
# Basic usage
python youtube_script_agent.py "Como Aprender Inglês Rápido" educacao --trends

# Review template
python youtube_script_agent.py "Review do iPhone 16" tecnologia --template review --duration 5min

# Export to markdown
python youtube_script_agent.py "Título" nicho --output markdown
```

## Output Structure

```json
{
  "titulo": "...",
  "nicho": "...",
  "duracao_alvo": "10min",
  "template_usado": "educacional",
  "score_viabilidade": 8.0,
  "estrutura": {
    "hook_0_5s": {...},
    "intro_5_30s": {...},
    "conteudo_principal": {...},
    "cta_medio": {...},
    "conclusao": {...},
    "cta_final": {...}
  },
  "metadata": {
    "titulo_sugestoes": [...],
    "thumbnail_sugestoes": [...],
    "tags_sugestoes": [...],
    "descricao_template": "..."
  }
}
```

## Files Location
- Skill: `.agents/skills/youtube-script/`
- Generated scripts: `~/organizao/youtube/roteiros/`
- Registered in: `skills-lock.json`

## Next Steps
- Add web_search integration for real trend research
- Add --export-lark functionality
- Create Lark Base tables for script storage