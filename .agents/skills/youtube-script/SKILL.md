---
name: youtube-script
version: 1.0.0
description: "Agente especializado em geração automática de roteiros para YouTube. Recebe tema/keyword, pesquisa tendências, gera roteiro comercialmente viável com estrutura otimizada (hook, conteúdo, CTA), e exporta no formato padrão. Armazena templates no Lark Base ou memória local."
metadata:
  requires:
    - bins: ["python3"]
    - lark-cli: "para armazenamento de templates (opcional)"
  cliHelp: "youtube-script --help"
---

# youtube-script — Gerador Automático de Roteiros para YouTube

Agente especializado que gera roteiros comerciais para YouTube com base em temas/keywords, pesquisando tendências e aplicando estruturas otimizadas.

## Uso Básico

```
youtube-script "TÍTULO DO VÍDEO" [nicho] [opções]
```

### Exemplos

```bash
# Roteiro básico
youtube-script "Como Investir na Bolsa em 2026" finanças

# Com pesquisa de tendências
youtube-script "5 Erros de Produtividade" produtividade --trends

# Exportar para Lark Base
youtube-script "Título" nicho --export-lark

# Especificar duração
youtube-script "Tutorial" tech --duration 8min
```

## Opções

| Opção | Descrição |
|-------|-----------|
| `--trends` | Pesquisar tendências atuais antes de gerar |
| `--export-lark` | Salvar roteiro no Lark Base (requer lark-cli) |
| `--duration [min]` | Duração alvo (5min, 8min, 10min, 15min) |
| `--template [nome]` | Usar template específico (educacional, entretenimento, review) |
| `--output [formato]` | Formato de saída: json, markdown, txt |

## Templates Disponíveis

### educacional
Estrutura focada em ensinar: hook → conceitos → exemplos → exercício prático → CTA

### entretenimento
Estrutura para storytelling: hook → narrativa → plot twist → moral → CTA

### review
Estrutura para análise de produtos: hook → introdução → pros/cons → comparativo → veredito → CTA

### noticia
Estrutura para notícias: hook → contexto → desenvolvimento → impacto → CTA

## Estrutura do Roteiro Gerado

```
{
  "titulo": "Título do vídeo",
  "nicho": "categoria",
  "duracao_alvo": "10min",
  "data_geracao": "ISO timestamp",
  "estrutura": {
    "hook_0_5s": { tempo: "0:00-0:05", sugestao: "..." },
    "intro_5_30s": { tempo: "0:05-0:30", sugestao: "..." },
    "conteudo_principal": { 
      "tempo": "0:30-8:00",
      "pontos": [...]
    },
    "cta_medio": { tempo: "8:00-8:30", sugestao: "..." },
    "conclusao": { tempo: "8:30-9:30", sugestao: "..." },
    "cta_final": { tempo: "9:30-10:00", sugestao: "..." }
  },
  "metadata": {
    "titulo_sugestoes": [...],
    "thumbnail_sugestoes": [...],
    "tags_sugestoes": [...],
    "descricao_template": "..."
  },
  "score_viabilidade": 8.5,
  "palavras_chave_tendencia": [...]
}
```

## Armazenamento de Templates

### Lark Base
Para armazenar templates e roteiros gerados:

1. Configure lark-cli: `lark-cli config init`
2. Crie uma base para templates: `lark-cli base base-create --name "YouTube Scripts"`
3. Use: `youtube-script "Título" nicho --export-lark`

### Estrutura da Base
- **Tabela Templates**: nome, tipo, estrutura_json, created_at
- **Tabela Roteiros**: titulo, nicho, score, estrutura_json, status
- **Tabela Tendências**: keyword, volume, competition, related_keywords

## Integração com Pesquisa

O agente pesquisa tendências usando:
- Google Trends (via web_search)
- Análise de concorrência
- Palavras-chave relacionadas

## Arquivos Gerados

Roteiros são salvos em:
- `~/organizacao/youtube/roteiros/roteiro_[slug].json`
- Formato padrão: JSON com estrutura completa

## Exemplo de Saída

```bash
$ youtube-script "Como Aprender Inglês Rápido" educacao --trends

🔍 Pesquisando tendências para: educacao
📈 Tendências encontradas: 12 palavras-chave
✅ Score de viabilidade: 8.2/10

📝 ESTRUTURA DO ROTEIRO:
  Hook (0-5s): "Você já gastou R$500 em curso de inglês e ainda assim..." 
  Intro (5-30s): "Eu sou professor de inglês há 10 anos..."
  
💾 Roteiro salvo: ~/organizao/youtube/roteiros/roteiro_como_aprender_ingles_rapido.json
```