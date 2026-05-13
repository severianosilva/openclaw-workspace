#!/usr/bin/env python3
"""
Sistema de conformidade regulatória para processos jurídicos
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import subprocess

class SistemaConformidade:
    def __init__(self):
        self.normas_regulatorias = self.carregar_normas_basicas()
    
    def carregar_normas_basicas(self) -> Dict:
        """
        Carrega normas regulatórias básicas para verificação de conformidade
        """
        return {
            "codigo_civil": {
                "descricao": "Código Civil Brasileiro",
                "artigos_principais": ["artigo 1", "artigo 2", "artigo 3", "artigo 4", "artigo 5"],
                "verificacoes": ["capacidade_civil", "personalidade_juridica", "bem_sujeito_ao_direito"]
            },
            "codigo_processo_civil": {
                "descricao": "Código de Processo Civil",
                "artigos_principais": [
                    "artigo 10", "artigo 11", "artigo 12", "artigo 13", "artigo 14",
                    "artigo 238", "artigo 239", "artigo 240", "artigo 347", "artigo 1041"
                ],
                "verificacoes": [
                    "prazo_recursal", "formalizacao_peticao", "intimacao_partes",
                    "cumprimento_sentenca", "procedimento_comum"
                ]
            },
            "codigo_penal": {
                "descricao": "Código Penal Brasileiro",
                "artigos_principais": ["artigo 1", "artigo 2", "artigo 3", "artigo 4"],
                "verificacoes": ["tipicidade", "ilicitude", "culpabilidade", "punibilidade"]
            },
            "lei_9504_97": {
                "descricao": "Lei das Eleições",
                "artigos_principais": ["artigo 73", "artigo 74", "artigo 75"],
                "verificacoes": ["propaganda_eleitoral", "conduta_vedada", "abuso_poder"]
            },
            "regimento_interno": {
                "descricao": "Regimento Interno do Tribunal",
                "artigos_principais": ["normas_procedimentais", "prazos_regimentais", "distribuicao_processos"],
                "verificacoes": ["competencia", "prazos", "procedimentos"]
            }
        }
    
    def verificar_conformidade_documento(self, texto_documento: str) -> Dict:
        """
        Verifica a conformidade do documento com as normas regulatórias
        """
        resultados = {
            "normas_verificadas": [],
            "possiveis_inconformidades": [],
            "recomendacoes": [],
            "nivel_conformidade": 0.0,
            "detalhes_verificacao": {}
        }
        
        # Análise de conformidade com base em palavras-chave e padrões
        for nome_norma, dados_norma in self.normas_regulatorias.items():
            verificacoes_norma = {
                "nome": nome_norma,
                "descricao": dados_norma["descricao"],
                "artigos_mencionados": [],
                "verificacoes_realizadas": {},
                "pontos_positivos": [],
                "pontos_negativos": []
            }
            
            # Verificar menções a artigos específicos
            for artigo in dados_norma["artigos_principais"]:
                if artigo in texto_documento.lower():
                    verificacoes_norma["artigos_mencionados"].append(artigo)
            
            # Verificar verificações específicas
            for verificacao in dados_norma["verificacoes"]:
                verificacao_resultado = self.verificar_item_especifico(texto_documento, verificacao)
                verificacoes_norma["verificacoes_realizadas"][verificacao] = verificacao_resultado
                
                if verificacao_resultado["conforme"]:
                    verificacoes_norma["pontos_positivos"].append(verificacao)
                else:
                    verificacoes_norma["pontos_negativos"].append({
                        "item": verificacao,
                        "descricao": verificacao_resultado["descricao"],
                        "sugestao": verificacao_resultado["sugestao"]
                    })
            
            resultados["normas_verificadas"].append(verificacoes_norma)
        
        # Calcular nível de conformidade
        total_itens = 0
        itens_conformes = 0
        
        for norma in resultados["normas_verificadas"]:
            for verificacao, resultado in norma["verificacoes_realizadas"].items():
                total_itens += 1
                if resultado["conforme"]:
                    itens_conformes += 1
        
        if total_itens > 0:
            resultados["nivel_conformidade"] = itens_conformes / total_itens
        else:
            resultados["nivel_conformidade"] = 1.0  # 100% se não houver itens para verificar
        
        # Gerar possíveis inconformidades
        for norma in resultados["normas_verificadas"]:
            for ponto_negativo in norma["pontos_negativos"]:
                resultados["possiveis_inconformidades"].append({
                    "norma": norma["descricao"],
                    "item": ponto_negativo["item"],
                    "descricao": ponto_negativo["descricao"],
                    "sugestao": ponto_negativo["sugestao"]
                })
        
        # Gerar recomendações
        if resultados["possiveis_inconformidades"]:
            resultados["recomendacoes"].append("Revisar itens com possíveis inconformidades")
            resultados["recomendacoes"].append("Consultar normas específicas para ajustes")
        else:
            resultados["recomendacoes"].append("Documento aparentemente em conformidade")
            resultados["recomendacoes"].append("Manter acompanhamento regulatório")
        
        return resultados
    
    def verificar_item_especifico(self, texto_documento: str, item_verificacao: str) -> Dict:
        """
        Verifica um item específico de conformidade
        """
        verificacoes_especificas = {
            "prazo_recursal": {
                "padroes": [r"(\d+)\s+dias\s+uteis?", r"(\d+)\s+dias\s+civis?"],
                "descricao": "Prazo recursal não identificado ou fora do padrão",
                "sugestao": "Verificar prazo recursal conforme CPC art. 1041 e seguintes"
            },
            "formalizacao_peticao": {
                "padroes": [r"nome.*?advogad", r"oab", r"procuracao", r"inicial.*?requer", r"peticao.*?inicial"],
                "descricao": "Formalização da petição inicial incompleta",
                "sugestao": "Verificar requisitos do art. 319 do CPC"
            },
            "intimacao_partes": {
                "padroes": [r"intimacao", r"ciencia", r"publicacao", r"juntada.*?provas"],
                "descricao": "Intimações não devidamente processadas",
                "sugestao": "Verificar cumprimento de intimacões conforme normas processuais"
            },
            "cumprimento_sentenca": {
                "padroes": [r"cumprimento", r"execucao", r"satisfacao.*?credito", r"quantia.*?devida"],
                "descricao": "Sentença não devidamente cumprida",
                "sugestao": "Verificar cumprimento de sentença conforme CPC art. 537 e seguintes"
            },
            "capacidade_civil": {
                "padroes": [r"maioridade", r"incapacidade", r"representacao", r"assistencia"],
                "descricao": "Capacidade civil não devidamente verificada",
                "sugestao": "Verificar capacidade conforme CC art. 1 e seguintes"
            },
            "personalidade_juridica": {
                "padroes": [r"cnpj", r"registro.*?empresa", r"atos.*?constituicao"],
                "descricao": "Personalidade jurídica não devidamente comprovada",
                "sugestao": "Verificar constituição e registro da pessoa jurídica"
            },
            "tipicidade": {
                "padroes": [r"conduta", r"resultado", r"nexo.*?causal", r"ilicito"],
                "descricao": "Tipicidade do crime não devidamente demonstrada",
                "sugestao": "Verificar elementos do tipo penal"
            },
            "propaganda_eleitoral": {
                "padroes": [r"propaganda", r"eleitoral", r"campanha", r"vedado"],
                "descricao": "Possível propaganda eleitoral irregular",
                "sugestao": "Verificar Lei 9.504/97"
            }
        }
        
        if item_verificacao in verificacoes_especificas:
            dados_verificacao = verificacoes_especificas[item_verificacao]
            
            # Verificar se algum dos padrões está presente no documento
            encontrado = False
            for padrao in dados_verificacao["padroes"]:
                if re.search(padrao, texto_documento, re.IGNORECASE):
                    encontrado = True
                    break
            
            return {
                "conforme": encontrado,
                "descricao": dados_verificacao["descricao"],
                "sugestao": dados_verificacao["sugestao"]
            }
        
        # Caso padrão - assume conformidade se não tiver regra específica
        return {
            "conforme": True,
            "descricao": f"Item {item_verificacao} não verificado de forma específica",
            "sugestao": "Verificação manual recomendada"
        }
    
    def gerar_relatorio_conformidade(self, resultados: Dict, processo_path: str, nome_documento: str) -> str:
        """
        Gera um relatório de conformidade
        """
        print("Gerando relatório de conformidade...")
        
        # Criar pasta de anotações se não existir
        anotacoes_dir = os.path.join(processo_path, "anotacoes")
        os.makedirs(anotacoes_dir, exist_ok=True)
        
        # Gerar nome de arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorio_conformidade_{timestamp}.md"
        caminho_arquivo = os.path.join(anotacoes_dir, nome_arquivo)
        
        # Criar conteúdo do relatório
        conteudo = f"""# Relatório de Conformidade Regulatória

**Documento Analisado:** {nome_documento}
**Data da Análise:** {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
**Sistema de Conformidade Regulatória Automatizado**

## Nível Geral de Conformidade
- **Percentual:** {resultados['nivel_conformidade']*100:.2f}%
- **Status:** {"Conforme" if resultados['nivel_conformidade'] >= 0.8 else "Parcialmente Conforme" if resultados['nivel_conformidade'] >= 0.5 else "Não Conforme"}

## Normas Verificadas

"""
        
        for norma in resultados["normas_verificadas"]:
            conteudo += f"### {norma['descricao']}\n"
            conteudo += f"- **Artigos mencionados:** {', '.join(norma['artigos_mencionados']) if norma['artigos_mencionados'] else 'Nenhum'}\n"
            conteudo += f"- **Itens verificados:** {len(norma['verificacoes_realizadas'])}\n"
            conteudo += f"- **Conformes:** {len(norma['pontos_positivos'])}\n"
            conteudo += f"- **Ajustes necessários:** {len(norma['pontos_negativos'])}\n\n"
        
        if resultados["possiveis_inconformidades"]:
            conteudo += "## Possíveis Inconformidades\n\n"
            for inconformidade in resultados["possiveis_inconformidades"]:
                conteudo += f"- **Norma:** {inconformidade['norma']}\n"
                conteudo += f"  - **Item:** {inconformidade['item']}\n"
                conteudo += f"  - **Descrição:** {inconformidade['descricao']}\n"
                conteudo += f"  - **Sugestão:** {inconformidade['sugestao']}\n\n"
        
        conteudo += "## Recomendações\n\n"
        for recomendacao in resultados["recomendacoes"]:
            conteudo += f"- {recomendacao}\n"
        
        conteudo += f"\n## Detalhes Técnicos\n"
        conteudo += f"- **Total de itens verificados:** {sum(len(norma['verificacoes_realizadas']) for norma in resultados['normas_verificadas'])}\n"
        conteudo += f"- **Itens conformes:** {sum(1 for norma in resultados['normas_verificadas'] for verif in norma['verificacoes_realizadas'].values() if verif['conforme'])}\n"
        conteudo += f"- **Itens não conformes:** {len(resultados['possiveis_inconformidades'])}\n\n"
        
        conteudo += f"*Este relatório foi gerado automaticamente pelo sistema de conformidade regulatória.*\n"
        
        # Salvar o arquivo
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        
        print(f"Relatório de conformidade salvo em: {caminho_arquivo}")
        return caminho_arquivo
    
    def verificar_conformidade_processo(self, caminho_documento: str, processo_path: str):
        """
        Verifica a conformidade de um documento em relação ao processo
        """
        print(f"Verificando conformidade regulatória: {caminho_documento}")
        
        # Ler conteúdo do documento
        try:
            with open(caminho_documento, 'r', encoding='utf-8') as f:
                texto_documento = f.read()
        except UnicodeDecodeError:
            # Tentar com outro encoding
            with open(caminho_documento, 'r', encoding='latin-1') as f:
                texto_documento = f.read()
        
        # Verificar conformidade
        resultados = self.verificar_conformidade_documento(texto_documento)
        
        # Gerar relatório
        nome_documento = os.path.basename(caminho_documento)
        caminho_relatorio = self.gerar_relatorio_conformidade(resultados, processo_path, nome_documento)
        
        # Exibir resumo
        print(f"\nResumo da verificação de conformidade:")
        print(f"- Nível de conformidade: {resultados['nivel_conformidade']*100:.2f}%")
        print(f"- Normas verificadas: {len(resultados['normas_verificadas'])}")
        print(f"- Possíveis inconformidades: {len(resultados['possiveis_inconformidades'])}")
        
        if resultados['possiveis_inconformidades']:
            print(f"\nAtenção: Foram identificadas {len(resultados['possiveis_inconformidades'])} possíveis inconformidades")
            print("Recomenda-se revisão cuidadosa dos itens identificados.")
        else:
            print("\nNenhuma inconformidade crítica identificada.")
        
        return resultados, caminho_relatorio

def main():
    if len(sys.argv) < 3:
        print("Uso:")
        print("  python sistema_conformidade.py <caminho_documento> <pasta_processo>")
        sys.exit(1)
    
    caminho_documento = sys.argv[1]
    pasta_processo = sys.argv[2]
    
    if not os.path.exists(caminho_documento):
        print(f"Documento não encontrado: {caminho_documento}")
        sys.exit(1)
    
    if not os.path.exists(pasta_processo):
        print(f"Pasta do processo não encontrada: {pasta_processo}")
        sys.exit(1)
    
    sistema = SistemaConformidade()
    sistema.verificar_conformidade_processo(caminho_documento, pasta_processo)

if __name__ == "__main__":
    main()