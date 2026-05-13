#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Script Generator Agent
Gera roteiros otimizados para YouTube com base em temas/keywords
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional

# Force UTF-8 output
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

class YouTubeScriptAgent:
    """Agente especializado em geração de roteiros para YouTube"""
    
    def __init__(self, use_trends: bool = False, export_lark: bool = False):
        self.use_trends = use_trends
        self.export_lark = export_lark
        self.output_dir = os.path.expanduser("~/organizacao/youtube/roteiros")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Templates pré-definidos
        self.templates = {
            "educacional": {
                "hook_style": "problema + promessa",
                "structure": ["hook", "conceitos", "exemplos", "exercicio", "cta"],
                "tone": "didático e prático"
            },
            "entretenimento": {
                "hook_style": "storytelling + curiosidade",
                "structure": ["hook", "narrativa", "plot_twist", "moral", "cta"],
                "tone": "conversacional e envolvente"
            },
            "review": {
                "hook_style": "problema + solucao",
                "structure": ["hook", "introducao", "pros_cons", "comparativo", "veredito", "cta"],
                "tone": "crítico e confiável"
            },
            "noticia": {
                "hook_style": "urgencia + impacto",
                "structure": ["hook", "contexto", "desenvolvimento", "impacto", "cta"],
                "tone": "informativo e atual"
            }
        }
    
    def research_trends(self, keyword: str) -> Dict:
        """Pesquisa tendências (versão simplificada - integrar com web_search)"""
        # Simulação - na versão completa, usa web_search
        trends = {
            "palavras_chave": [
                f"{keyword} 2026",
                f"como {keyword}",
                f"{keyword} para iniciantes",
                f"{keyword} avançado",
                f"erros {keyword}"
            ],
            "volume_estimado": 10000,
            "competicao": "media",
            "tendencia_crescimento": True
        }
        return trends
    
    def calculate_viability_score(self, keyword: str, nicho: str, trends: Dict) -> float:
        """Calcula score de viabilidade do tema"""
        score = 5.0  # Base
        
        # Ajusta baseado em tendências
        if trends.get("tendencia_crescimento"):
            score += 1.5
        if trends.get("volume_estimado", 0) > 5000:
            score += 1.0
        if trends.get("competicao") == "baixa":
            score += 1.5
        elif trends.get("competicao") == "media":
            score += 0.5
        
        # Limita entre 0-10
        return min(10.0, max(0.0, score))
    
    def generate_hook(self, titulo: str, nicho: str, template: str = "educacional") -> str:
        """Gera hook otimizado para primeiros 5 segundos"""
        hooks = {
            "educacional": [
                f"Você já gastou tempo e dinheiro tentando {titulo.lower()} sem sucesso? Eu também. Hoje eu te mostro o método que mudou tudo.",
                f"Pára tudo! O que eu vou te mostrar nos próximos minutos vai acelerar sua aprendizagem em {nicho} em 300%.",
                f"Se você quer {titulo.lower()} mas não sabe por onde começar, esse vídeo é para você. Fica comigo."
            ],
            "entretenimento": [
                f"Eu nunca contei essa história para ninguém... até hoje. O que aconteceu me ensinou {titulo.lower()}.",
                f"Você não vai acreditar no que aconteceu quando eu tentei {titulo.lower()}. Mas esse é o melhor vídeo que você vai ver hoje.",
                f"Era uma vez... alguém que precisava de {titulo.lower()}. A história é real e pode te ajudar."
            ],
            "review": [
                f"Testei {titulo.lower()} por uma semana inteira e o resultado me surpreendeu. Vou mostrar tudo.",
                f"90% das pessoas cometem esse erro com {titulo.lower()}. Vou te mostrar qual é e como evitar.",
                f"Antes de você comprar, assista esse vídeo. Conheço os {titulo.lower()} melhor que ninguém."
            ],
            "noticia": [
                f"Acabei de descobrir algo que vai mudar completamente sua forma de ver {titulo.lower()}.",
                f"Isso aqui é importante. {titulo} afeta diretamente {nicho} e você precisa saber.",
                f"Quebra de notícias: {titulo}. O impacto disso é maior do que você imagina."
            ]
        }
        
        return hooks.get(template, hooks["educacional"])[0]
    
    def generate_script_structure(self, titulo: str, nicho: str, duration: str = "10min", 
                                   template: str = "educacional") -> Dict:
        """Gera estrutura completa do roteiro"""
        
        # Durações pré-definidas
        durations = {
            "5min": {"main_end": "3:30", "main_start": "0:30"},
            "8min": {"main_end": "6:00", "main_start": "0:30"},
            "10min": {"main_end": "8:00", "main_start": "0:30"},
            "15min": {"main_end": "12:00", "main_start": "0:30"}
        }
        dur = durations.get(duration, durations["10min"])
        
        # Pesquisa tendências se solicitado
        trends = {"palavras_chave_tendencia": []}
        if self.use_trends:
            trends = self.research_trends(nicho)
        
        viability_score = self.calculate_viability_score(titulo, nicho, trends)
        
        script = {
            "titulo": titulo,
            "nicho": nicho,
            "duracao_alvo": duration,
            "template_usado": template,
            "data_geracao": datetime.now().isoformat(),
            "score_viabilidade": viability_score,
            "palavras_chave_tendencia": trends.get("palavras_chave", []),
            "estrutura": {
                "hook_0_5s": {
                    "tempo": "0:00-0:05",
                    "objetivo": "Prender atenção imediatamente",
                    "sugestao": self.generate_hook(titulo, nicho, template)
                },
                "intro_5_30s": {
                    "tempo": "0:05-0:30",
                    "objetivo": "Estabelecer credibilidade e expectativa",
                    "sugestao": f"Eu sou [SEU NOME] e já ajudei [NÚMERO] pessoas a {nicho}. Nesse vídeo, vou te mostrar exatamente {titulo}. Fica comigo até o final."
                },
                "conteudo_principal": {
                    "tempo": f"0:30-{dur['main_end']}",
                    "objetivo": "Entregar valor máximo",
                    "pontos": [
                        {
                            "ponto": 1,
                            "titulo": f"Conceito fundamental de {titulo}",
                            "tempo": "0:30-2:00",
                            "elementos": ["Explicação clara", "Exemplo prático", "Erro comum"]
                        },
                        {
                            "ponto": 2,
                            "titulo": f"Aplicação prática de {titulo}",
                            "tempo": "2:00-3:30",
                            "elementos": ["Passo a passo", "Demonstração", "Dica bônus"]
                        },
                        {
                            "ponto": 3,
                            "titulo": f"Avançado: {titulo}",
                            "tempo": f"3:30-{dur['main_end']}",
                            "elementos": ["Técnica avançada", "Case real", "Recursos extras"]
                        }
                    ]
                },
                "cta_medio": {
                    "tempo": f"{dur['main_end']}:00-{dur['main_end'].split(':')[0]}:30",
                    "objetivo": "Engajamento sem prejudicar retenção",
                    "sugestao": "Se está curtindo, deixa o like e se inscreve! Tem muito mais vídeo como esse."
                },
                "conclusao": {
                    "tempo": f"{dur['main_end'].split(':')[0]}:30-{dur['main_end'].split(':')[0]}:50",
                    "objetivo": "Resumo e próximo passo",
                    "sugestao": "Recapitulando: [Ponto 1], [Ponto 2], [Ponto 3]. Agora é sua vez de colocar em prática."
                },
                "cta_final": {
                    "tempo": f"{dur['main_end'].split(':')[0]}:50-{duration}",
                    "objetivo": "Direcionar para próximo vídeo/ação",
                    "sugestao": "Se quer se aprofundar, clica nesse vídeo aqui. Me conta nos comentários: qual foi sua maior dificuldade?"
                }
            },
            "metadata": {
                "titulo_sugestoes": self.generate_title_variations(titulo, nicho),
                "thumbnail_sugestoes": [
                    "Rosto com expressão forte",
                    "Texto grande (3-5 palavras)",
                    "Alto contraste de cores",
                    "Seta destacando elemento",
                    "Número grande (ex: '3 PASSOS')"
                ],
                "tags_sugestoes": self.generate_tags(titulo, nicho),
                "descricao_template": self.generate_description_template(titulo, nicho)
            }
        }
        
        return script
    
    def generate_title_variations(self, titulo: str, nicho: str) -> List[str]:
        """Gera variações de título otimizadas para CTR"""
        return [
            f"Como {titulo} (Guia Completo 2026)",
            f"{titulo} em 10 Minutos",
            f"O Segredo de {titulo} Que Ninguém Te Conta",
            f"3 Passos Para {titulo}",
            f"{titulo}: Erros Que Você Precisa Evitar"
        ]
    
    def generate_tags(self, titulo: str, nicho: str) -> List[str]:
        """Gera tags otimizadas para SEO"""
        return [
            nicho.lower(),
            f"como {nicho.lower()}",
            f"{nicho} 2026",
            f"tutorial {nicho}",
            f"dicas {nicho}",
            f"guia completo {nicho}"
        ]
    
    def generate_description_template(self, titulo: str, nicho: str) -> str:
        """Gera template de descrição otimizada"""
        return f"""{titulo}

Nesse vídeo eu te mostro como {titulo.lower()}. Se você quer resultados reais, curte, compartilha e se inscreve!

⏰ TIMESTAMPS:
0:00 - Introdução  
0:30 - [Ponto 1]
2:00 - [Ponto 2]  
3:30 - [Ponto 3]

#Hashtags: #{nicho.replace(' ', '')} #{nicho.replace(' ', '')}2026
"""
    
    def save_script(self, script: Dict, output_format: str = "json") -> str:
        """Salva roteiro no formato especificado"""
        slug = script["titulo"].replace(" ", "_").lower()[:50]
        
        if output_format == "json":
            path = os.path.join(self.output_dir, f"roteiro_{slug}.json")
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(script, f, ensure_ascii=False, indent=2)
        elif output_format == "markdown":
            path = os.path.join(self.output_dir, f"roteiro_{slug}.md")
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self._to_markdown(script))
        else:  # txt
            path = os.path.join(self.output_dir, f"roteiro_{slug}.txt")
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self._to_text(script))
        
        return path
    
    def _to_markdown(self, script: Dict) -> str:
        """Converte roteiro para markdown"""
        md = f"# {script['titulo']}\n\n"
        md += f"**Nicho:** {script['nicho']} | **Duração:** {script['duracao_alvo']}\n\n"
        
        for section, data in script['estrutura'].items():
            md += f"## {section.replace('_', ' ').title()}\n"
            md += f"**Tempo:** {data['tempo']}\n\n"
            md += f"{data['sugestao']}\n\n"
        
        return md
    
    def _to_text(self, script: Dict) -> str:
        """Converte roteiro para texto simples"""
        return json.dumps(script, ensure_ascii=False, indent=2)
    
    def generate(self, titulo: str, nicho: str, duration: str = "10min", 
                 template: str = "educacional", output_format: str = "json") -> Dict:
        """Gera roteiro completo"""
        print(f"\n{'='*60}")
        print(f"  YOUTUBE SCRIPT GENERATOR")
        print(f"  Título: {titulo}")
        print(f"  Nicho: {nicho}")
        print(f"{'='*60}\n")
        
        if self.use_trends:
            print("[Research] Pesquisando tendências...")
            trends = self.research_trends(nicho)
            print(f"[Trends] {len(trends.get('palavras_chave', []))} palavras-chave encontradas")
        
        script = self.generate_script_structure(titulo, nicho, duration, template)
        path = self.save_script(script, output_format)
        
        print(f"\n[Score] Viabilidade: {script['score_viabilidade']:.1f}/10")
        print(f"[Saved] Roteiro salvo: {path}")
        
        return script


def main():
    parser = argparse.ArgumentParser(
        description="YouTube Script Generator Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  youtube-script "Como Investir" finanças
  youtube-script "5 Dicas" produtividade --trends
  youtube-script "Review" tech --duration 8min --template review
        """
    )
    
    parser.add_argument("titulo", help="Título ou tema do vídeo")
    parser.add_argument("nicho", nargs="?", default="geral", help="Nicho/categoria")
    parser.add_argument("--trends", action="store_true", help="Pesquisar tendências")
    parser.add_argument("--export-lark", action="store_true", help="Exportar para Lark Base")
    parser.add_argument("--duration", default="10min", choices=["5min", "8min", "10min", "15min"],
                       help="Duração alvo do vídeo")
    parser.add_argument("--template", default="educacional", 
                       choices=["educacional", "entretenimento", "review", "noticia"],
                       help="Template de estrutura")
    parser.add_argument("--output", default="json", choices=["json", "markdown", "txt"],
                       help="Formato de saída")
    
    args = parser.parse_args()
    
    agent = YouTubeScriptAgent(use_trends=args.trends, export_lark=args.export_lark)
    script = agent.generate(
        titulo=args.titulo,
        nicho=args.nicho,
        duration=args.duration,
        template=args.template,
        output_format=args.output
    )
    
    # Imprime resumo
    print(f"\n[DONE] Roteiro gerado com sucesso!")
    print(f"   Título: {script['titulo']}")
    print(f"   Template: {script['template_usado']}")
    print(f"   Score: {script['score_viabilidade']:.1f}/10")


if __name__ == "__main__":
    main()