# YouTube Money Agents - Sistema 100% Autônomo

## Agentes do Sistema (9 Agentes)

| Agente | Arquivo | Função |
|--------|---------|--------|
| Research | `research_agent.py` | Pesquisa temas lucrativos (CPM R$ 25,50 finanças) |
| Content | `content_agent.py` | Cria roteiros otimizados SEO |
| Design | `design_agent.py` | Cria thumbnails, banners, identidade visual |
| Video | `video_agent.py` | Planeja produção de vídeos |
| Channel | `channel_agent.py` | Configura canal YouTube |
| Upload | `upload_agent.py` | Prepara publicação de vídeos |
| Audience | `upload_agent.py` | Monitora audiência e ajusta estratégias |
| Strategist | `strategist_agent.py` | Estrategista monetização |
| Monetization | `monetization_agent.py` | Plano de afiliados e sponsors |

## Fluxo Completo Automatizado

```
Pesquisa → Design → Conteúdo → Produção → Upload → Análise → Otimização
```

## Como Usar

**Demo completa:**
```bash
python full_demo.py
```

**Modo interativo:**
```bash
python main.py --start
```

**Criar canal específico:**
```bash
python main.py --new-channel "financas"
```

## Resultados da Demo

```
Canal: Money Empire BR
Temas: 3 prontos (CPM R$ 25,50)
Roteiros: 2 criados
Receita projetada: R$ 2250/mês
Break-even: 3 meses
Afiliados: Hotmart, Monetizze, Eduzz
```

## Arquivos Gerados

- `workspace/script_*.json` - Roteiros prontos
- `workspace/branding_*.json` - Identidade visual
- `workspace/production_*.json` - Plano de produção
- `workspace/upload_*.json` - Dados para upload
- `memory/research.json` - Temas pesquisados
- `memory/strategy.json` - Estratégia de monetização

## Próximas Integrações

1. YouTube Data API v3 (upload automático)
2. Ferramentas de edição (FFmpeg, MoviePy)
3. Geração de thumbnails com IA
4. Webhooks para monitoramento real