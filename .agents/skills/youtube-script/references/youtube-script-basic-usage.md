# YouTube Script Agent - Basic Usage

## Quick Start

```bash
# Basic usage
youtube-script "Como Aprender Inglês Rápido" educacao

# With trend research
youtube-script "5 Dicas de Produtividade" produtividade --trends

# Using entertainment template
youtube-script "Minha História Inspiradora" lifestyle --template entretenimento

# Short format
youtube-script "Review do iPhone 16" tech --duration 5min --template review

# Export to Lark Base
youtube-script "Título" nicho --export-lark
```

## Workflow

```
1. youtube-script "TÍTULO" nicho --trends
   ↓
2. Review trends and viability score
   ↓
3. Edit generated script
   ↓
4. Produce video
   ↓
5. Upload with generated metadata
```