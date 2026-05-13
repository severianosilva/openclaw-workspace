#!/usr/bin/env python3
"""
Gerador de Roteiros para YouTube Otimizados
Baseado nas melhores práticas de 2025

- Hook nos primeiros 5 segundos
- Fórmula RIP (Relate, Identify, Proposal)
- Estrutura para retenção máxima
- CTA estratégico
"""

import os
import json
from datetime import datetime
from typing import Dict

class GeradorRoteiroYouTube:
    """Gera roteiros otimizados para YouTube"""
    
    def __init__(self):
        self.output_dir = os.path.expanduser("~/organizacao/youtube/roteiros")
        os.makedirs(self.output_dir, exist_ok=True)
        
    def gerar_hook(self, titulo: str, nicho: str) -> str:
        """
        Gera hook para primeiros 5 segundos
        Baseado em pesquisa: 70% dos viewers decidem nos primeiros segundos
        """
        hooks = [
            f"Você já se pegou pensando como {titulo.lower()}? Pois é, eu também. E hoje vou te mostrar exatamente como fazer isso.",
            f"Pára tudo o que você está fazendo! O que eu vou te mostrar nos próximos minutos pode mudar completamente sua forma de pensar sobre {nicho}.",
            f"Se você quer {titulo.lower()} mas não sabe por onde começar, esse vídeo é para você. Fica comigo até o final que eu vou te mostrar o passo a passo.",
            f"Eu aposto que você não sabia disso sobre {nicho}. E é exatamente por isso que a maioria das pessoas falha quando tenta.",
            f"Imagine conseguir seu objetivo em apenas 30 dias. Parece bom demais pra ser verdade? Eu também achava, até descobrir isso..."
        ]
        
        return hooks[0]  # Simplificado - ideal usar IA para gerar personalizado
    
    def gerar_estrutura_roteiro(self, titulo: str, nicho: str, duracao_alvo: str = "10min") -> Dict:
        """
        Gera estrutura completa do roteiro
        """
        estrutura = {
            "titulo": titulo,
            "nicho": nicho,
            "duracao_alvo": duracao_alvo,
            "data_geracao": datetime.now().isoformat(),
            "estrutura": {
                "hook_0_5s": {
                    "tempo": "0:00-0:05",
                    "objetivo": "Prender atenção imediatamente",
                    "dicas": [
                        "Corte direto para ação",
                        "Use texto na tela",
                        "Faça promessa específica",
                        "Evite introduções longas"
                    ],
                    "sugestao": self.gerar_hook(titulo, nicho)
                },
                "intro_5_30s": {
                    "tempo": "0:05-0:30",
                    "objetivo": "Estabelecer credibilidade e expectativa",
                    "elementos": [
                        "Quem é você (rápido)",
                        "O que viewer vai aprender",
                        "Por que deveria confiar em você",
                        "Preview do conteúdo"
                    ],
                    "sugestao": f"Eu sou [SEU NOME] e já ajudei [NÚMERO] pessoas a {nicho}. Nesse vídeo, vou te mostrar exatamente [PROMESSA]. Fica comigo até o final que tem [BÔNUS/SURPRESA]."
                },
                "conteudo_principal": {
                    "tempo": "0:30-8:00",
                    "objetivo": "Entregar valor máximo",
                    "estrutura_recomendada": "3-5 pontos principais",
                    "pontos": [
                        {
                            "ponto": 1,
                            "titulo": "Primeiro conceito/fundamento",
                            "tempo": "0:30-2:30",
                            "elementos": ["Explicação", "Exemplo prático", "Erro comum"]
                        },
                        {
                            "ponto": 2,
                            "titulo": "Segundo conceito/aplicação",
                            "tempo": "2:30-4:30",
                            "elementos": ["Explicação", "Demonstração", "Dica extra"]
                        },
                        {
                            "ponto": 3,
                            "titulo": "Terceiro conceito/avançado",
                            "tempo": "4:30-6:30",
                            "elementos": ["Explicação", "Case real", "Atalho/macete"]
                        },
                        {
                            "ponto": 4,
                            "titulo": "Quarto conceito/bônus",
                            "tempo": "6:30-8:00",
                            "elementos": ["Dica exclusiva", "Ferramenta recomendada", "Recurso extra"]
                        }
                    ],
                    "dicas_retengao": [
                        "Mude ângulo/cena a cada 15-30s",
                        "Use B-roll e gráficos",
                        "Insira mini-hooks entre seções",
                        "Adicione elementos visuais"
                    ]
                },
                "cta_medio": {
                    "tempo": "8:00-8:30",
                    "objetivo": "Engajamento sem prejudicar retenção",
                    "sugestao": "Se você está curtindo esse conteúdo, já deixa o like e se inscreve no canal. Tem muito mais vídeo como esse por vir!",
                    "dica": "Inserir após entregar valor significativo"
                },
                "conclusao": {
                    "tempo": "8:30-9:30",
                    "objetivo": "Resumo e próximo passo",
                    "elementos": [
                        "Recapitulação rápida dos pontos",
                        "Próximo passo prático",
                        "Convite para ação"
                    ],
                    "sugestao": "Então é isso! Recapitulando: [PONTO 1], [PONTO 2], [PONTO 3]. Agora é sua vez de colocar em prática."
                },
                "cta_final": {
                    "tempo": "9:30-10:00",
                    "objetivo": "Direcionar para próximo vídeo/ação",
                    "sugestao": "Se você quer se aprofundar mais em [TÓPICO], clica nesse vídeo aqui que eu fiz sobre [TÓPICO RELACIONADO]. E me conta nos comentários: qual foi sua maior dificuldade com [NICH]? Vou responder todo mundo!",
                    "elementos_obrigatorios": [
                        "End screen com 2-3 elementos",
                        "Card para vídeo relacionado",
                        "Botão de inscrição"
                    ]
                }
            },
            "metadata": {
                "titulo_sugestoes": self.gerar_variacoes_titulo(titulo),
                "thumbnail_sugestoes": self.gerar_sugestoes_thumbnail(titulo, nicho),
                "tags_sugestoes": self.gerar_tags(titulo, nicho),
                "descricao_template": self.gerar_template_descricao(titulo, nicho)
            }
        }
        
        return estrutura
    
    def gerar_variacoes_titulo(self, titulo_base: str) -> list:
        """Gera variações de título otimizadas para CTR"""
        return [
            f"Como {titulo_base} (Guia Completo 2026)",
            f"{titulo_base} em 10 Minutos",
            f"O Segredo de {titulo_base} Que Ninguém Te Conta",
            f"7 Passos Para {titulo_base}",
            f"{titulo_base}: Erros Que Você Precisa Evitar"
        ]
    
    def gerar_sugestoes_thumbnail(self, titulo: str, nicho: str) -> list:
        """Sugere elementos para thumbnail"""
        return [
            "Rosto com expressão forte (surpresa, empolgação)",
            "Texto grande e legível (3-5 palavras máximo)",
            "Alto contraste de cores",
            "Seta ou círculo destacando elemento",
            "Antes/Depois (se aplicável)",
            "Número grande (ex: '7 PASSOS')"
        ]
    
    def gerar_tags(self, titulo: str, nicho: str) -> list:
        """Gera tags otimizadas para SEO"""
        tags_base = [
            nicho.lower(),
            f"como {nicho.lower()}",
            f"{nicho} para iniciantes",
            f"{nicho} 2026",
            f"tutorial de {nicho}",
            f"dicas de {nicho}",
            f"guia completo {nicho}"
        ]
        return tags_base
    
    def gerar_template_descricao(self, titulo: str, nicho: str) -> str:
        """Gera template de descrição otimizada"""
        return f"""
{titulo}

Nesse vídeo eu vou te mostrar exatamente como {titulo.lower()}. Se você é iniciante em {nicho} ou já tem experiência, esse conteúdo vai te ajudar a [RESULTADO].

⏰ TIMESTAMPS:
0:00 - Introdução
0:30 - [Ponto 1]
2:30 - [Ponto 2]
4:30 - [Ponto 3]
6:30 - [Ponto 4]
8:30 - Conclusão

🔗 LINKS MENCIONADOS:
[Link 1]
[Link 2]

📱 ME SIGA NAS REDES:
Instagram: @[SEU_INSTA]
Twitter: @[SEU_TWITTER]

👍 SE INSCREVA NO CANAL!
https://youtube.com/[SEU_CANAL]?sub_confirmation=1

#Hashtags:
#{nicho.replace(' ', '')}
#Como{nicho.replace(' ', '')}
#{nicho.replace(' ', '')}ParaIniciantes
        """.strip()
    
    def salvar_roteiro(self, estrutura: Dict) -> str:
        """Salva roteiro em arquivo"""
        nome_arquivo = f"roteiro_{estrutura['titulo'].replace(' ', '_').lower()[:50]}.json"
        caminho = os.path.join(self.output_dir, nome_arquivo)
        
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(estrutura, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Roteiro salvo: {caminho}")
        return caminho
    
    def gerar_roteiro_completo(self, titulo: str, nicho: str) -> Dict:
        """Gera roteiro completo e salva"""
        print(f"\n{'='*60}")
        print(f"  GERADOR DE ROTEIROS YOUTUBE")
        print(f"  Título: {titulo}")
        print(f"  Nicho: {nicho}")
        print(f"{'='*60}\n")
        
        estrutura = self.gerar_estrutura_roteiro(titulo, nicho)
        caminho = self.salvar_roteiro(estrutura)
        
        # Imprimir resumo
        print(f"\n📝 ESTRUTURA DO ROTEIRO:")
        print(f"  Hook (0-5s): {estrutura['estrutura']['hook_0_5s']['sugestao'][:100]}...")
        print(f"  Intro (5-30s): {estrutura['estrutura']['intro_5_30s']['sugestao'][:100]}...")
        print(f"\n📊 METADATA SUGERIDA:")
        print(f"  Títulos: {len(estrutura['metadata']['titulo_sugestoes'])} opções")
        print(f"  Tags: {len(estrutura['metadata']['tags_sugestoes'])} tags")
        print(f"\n✅ Roteiro completo em: {caminho}")
        
        return estrutura

def main():
    """Função principal"""
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python3 gerar_roteiro_youtube.py \"TÍTULO DO VÍDEO\" [NICHO]")
        print("Exemplo: python3 gerar_roteiro_youtube.py \"Como Investir na Bolsa\" finanças")
        sys.exit(1)
    
    titulo = sys.argv[1]
    nicho = sys.argv[2] if len(sys.argv) > 2 else "geral"
    
    gerador = GeradorRoteiroYouTube()
    roteiro = gerador.gerar_roteiro_completo(titulo, nicho)

if __name__ == "__main__":
    main()
