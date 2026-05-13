# YouTube Script Generator Agent

Agente especializado em geração automática de roteiros para YouTube.

## Estrutura do Projeto

```
youtube-script/
├── SKILL.md                    # Documentação principal
├── youtube_script_agent.py     # Script Python principal
├── templates.json               # Templates de roteiro
├── README.md                   # Este arquivo
└── references/
    ├── youtube-script-basic-usage.md
    └── youtube-script-lark-integration.md
```

## Uso Rápido

```bash
# Gerar roteiro básico
python youtube_script_agent.py "Título do Vídeo" nicho

# Com pesquisa de tendências
python youtube_script_agent.py "5 Dicas" produtividade --trends

# Com template específico
python youtube_script_agent.py "Review do Produto" tech --template review

# Exportar para Markdown
python youtube_script_agent.py "Título" nicho --output markdown
```

## Templates Disponíveis

- **educacional** - Para tutoriais e aulas
- **entretenimento** - Para storytelling e vlogs
- **review** - Para análise de produtos
- **noticia** - Para conteúdo noticioso

## Saída Padrão

Roteiros são salvos em: `~/organizacao/youtube/roteiros/roteiro_[slug].json`

Formato JSON com:
- Estrutura de tempo (hook, intro, conteúdo, CTAs)
- Metadata otimizada (títulos, tags, thumbnails)
- Score de viabilidade
- Palavras-chave de tendência

## Integração Lark (Opcional)

Para armazenar roteiros no Lark Base:
1. Configure lark-cli
2. Use `--export-lark` flag
3. Veja youtube-script-lark-integration.md para detalhes