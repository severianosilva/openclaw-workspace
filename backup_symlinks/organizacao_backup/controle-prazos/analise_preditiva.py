#!/usr/bin/env python3
"""
Sistema de análise preditiva de riscos jurídicos
"""

import os
import sys
import json
import re
from datetime import datetime
from typing import Dict, List, Tuple
import math

class AnalisadorPreditivo:
    def __init__(self):
        self.base_precedentes = self.carregar_base_precedentes()
    
    def carregar_base_precedentes(self) -> Dict:
        """
        Carrega uma base de precedentes para análise preditiva
        """
        # Esta é uma base simplificada - em produção, viria de um banco de dados
        return {
            "areas_direito": {
                "civel": {
                    "taxa_sucesso": 0.65,
                    "media_prazo": 18,  # meses
                    "fatores_risco": ["valor_acima_1mi", "natureza_complexa", "litigiosidade"],
                    "fatores_favoraveis": ["prova_documental", "fumus_bonis_iuris", "periculum_in_morando"]
                },
                "trabalhista": {
                    "taxa_sucesso": 0.72,
                    "media_prazo": 12,
                    "fatores_risco": ["dissidio_coletivo", "parcelas_multiplicadas", "natureza_alta_complexidade"],
                    "fatores_favoraveis": ["parcelas_liquidas", "acordo_previo", "reconhecimento_empresa"]
                },
                "tributario": {
                    "taxa_sucesso": 0.45,
                    "media_prazo": 24,
                    "fatores_risco": ["sistemica", "constitucionalidade", "natureza_complexa"],
                    "fatores_favoraveis": ["sistemica_favoravel", "precedentes_favoraveis", "entendimento_superior_tribunal"]
                },
                "previdenciario": {
                    "taxa_sucesso": 0.58,
                    "media_prazo": 15,
                    "fatores_risco": ["carater_subjetivo", "prova_pericial", "controversia_jurisprudencial"],
                    "fatores_favoraveis": ["legislacao_favoravel", "precedentes_firmados", "direito_adquirido"]
                }
            },
            "fatores_gerais": {
                "valor_da_causa": {
                    "baixo": {"multiplicador": 1.0, "descricao": "Valor da causa baixo"},
                    "medio": {"multiplicador": 1.1, "descricao": "Valor da causa médio"},
                    "alto": {"multiplicador": 1.3, "descricao": "Valor da causa alto, maior exposição"}
                },
                "complexidade": {
                    "baixa": {"multiplicador": 0.8, "descricao": "Processo de baixa complexidade"},
                    "media": {"multiplicador": 1.0, "descricao": "Processo de complexidade média"},
                    "alta": {"multiplicador": 1.4, "descricao": "Processo de alta complexidade"}
                },
                "jurisprudencia": {
                    "favoravel": {"multiplicador": 0.7, "descricao": "Jurisprudência favorável"},
                    "contraria": {"multiplicador": 1.5, "descricao": "Jurisprudência contrária"},
                    "divergente": {"multiplicador": 1.2, "descricao": "Jurisprudência com divergência"}
                }
            }
        }
    
    def analisar_documento(self, texto_documento: str) -> Dict:
        """
        Analisa o documento e identifica fatores relevantes para análise preditiva
        """
        analise = {
            "area_direito": self.identificar_area_direito(texto_documento),
            "valor_da_causa": self.estimar_valor_causa(texto_documento),
            "complexidade": self.avaliar_complexidade(texto_documento),
            "jurisprudencia": self.analisar_jurisprudencia(texto_documento),
            "fatores_risco": [],
            "fatores_favoraveis": [],
            "indicadores_processuais": []
        }
        
        # Identificar fatores de risco e favoráveis com base na área do direito
        area_info = self.base_precedentes["areas_direito"].get(analise["area_direito"], {})
        if "fatores_risco" in area_info:
            for fator in area_info["fatores_risco"]:
                if self.verificar_presenca_fator(texto_documento, fator):
                    analise["fatores_risco"].append(fator)
        
        if "fatores_favoraveis" in area_info:
            for fator in area_info["fatores_favoraveis"]:
                if self.verificar_presenca_fator(texto_documento, fator):
                    analise["fatores_favoraveis"].append(fator)
        
        # Identificar indicadores processuais
        analise["indicadores_processuais"] = self.identificar_indicadores_processuais(texto_documento)
        
        return analise
    
    def identificar_area_direito(self, texto: str) -> str:
        """
        Identifica a área do direito com base no conteúdo do documento
        """
        texto_lower = texto.lower()
        
        areas_peso = {
            "civel": 0,
            "trabalhista": 0,
            "tributario": 0,
            "previdenciario": 0,
            "criminal": 0,
            "administrativo": 0
        }
        
        # Palavras-chave por área
        areas_palavras = {
            "civel": ["contrato", "indenizacao", "danos", "obrigacao", "responsabilidade", "direito civil"],
            "trabalhista": ["trabalhador", "empregador", "consignacao", "parcelas", "aviso previo", "fgts", "verbas"],
            "tributario": ["imposto", "isencao", "isenção", "isençao", "isençāo", "contribuicao", "contribuição", "constitucionalidade"],
            "previdenciario": ["aposentadoria", "auxilio", "auxílio", "beneficio", "benefício", "carência", "carencia", "carencia"],
            "criminal": ["acusacao", "acusação", "imputacao", "imputação", "crim", "pena", "flagrante"],
            "administrativo": ["licitacao", "licitação", "contrato administrativo", "concurso", "servidor", "pessoa juridica"]
        }
        
        for area, palavras in areas_palavras.items():
            for palavra in palavras:
                areas_peso[area] += texto_lower.count(palavra.lower())
        
        # Retornar a área com mais ocorrências
        area_principal = max(areas_peso, key=areas_peso.get)
        return area_principal if areas_peso[area_principal] > 0 else "civel"  # Padrão
    
    def estimar_valor_causa(self, texto: str) -> str:
        """
        Estima o valor da causa com base no documento
        """
        # Procurar por valores monetários no texto
        valores = re.findall(r'R\$\s*[\d.,]+|[\d.,]+\s*R\$', texto.replace('.', '').replace(',', '.'))
        
        if not valores:
            return "baixo"  # Valor padrão baixo
        
        # Converter valores para números
        valores_numericos = []
        for valor in valores:
            try:
                # Remover caracteres não numéricos exceto o ponto decimal
                valor_clean = re.sub(r'[^\d.]', '', valor)
                if valor_clean:
                    valores_numericos.append(float(valor_clean))
            except ValueError:
                continue
        
        if not valores_numericos:
            return "baixo"
        
        media_valores = sum(valores_numericos) / len(valores_numericos)
        
        if media_valores < 50000:  # Abaixo de 50 mil
            return "baixo"
        elif media_valores < 500000:  # Entre 50 mil e 500 mil
            return "medio"
        else:  # Acima de 500 mil
            return "alto"
    
    def avaliar_complexidade(self, texto: str) -> str:
        """
        Avalia a complexidade do processo
        """
        fatores_complexidade = [
            "prova pericial", "pericia", "perícia", "dissidio coletivo", "constitucionalidade",
            "repercussao geral", "repercussão geral", "questão federal", "matéria constitucional",
            "diversidade de litigantes", "partilha complexa", "liquidação de sentença",
            "cumprimento de sentença", "execução fiscal", "ação rescisória"
        ]
        
        score = 0
        texto_lower = texto.lower()
        
        for fator in fatores_complexidade:
            if fator in texto_lower:
                score += 1
        
        if score >= 3:
            return "alta"
        elif score >= 1:
            return "media"
        else:
            return "baixa"
    
    def analisar_jurisprudencia(self, texto: str) -> str:
        """
        Analisa a jurisprudência mencionada no documento
        """
        texto_lower = texto.lower()
        
        # Verificar menções a tribunais superiores
        mencoes_stf = texto_lower.count("stf") + texto_lower.count("supremo tribunal federal")
        mencoes_stj = texto_lower.count("stj") + texto_lower.count("superior tribunal de justiça")
        mencoes_tst = texto_lower.count("tst") + texto_lower.count("tribunal superior do trabalho")
        mencoes_tcu = texto_lower.count("tcu") + texto_lower.count("tribunal de contas da união")
        
        total_mencoes = mencoes_stf + mencoes_stj + mencoes_tst + mencoes_tcu
        
        if total_mencoes == 0:
            # Verificar menções a jurisprudência em geral
            if "jurisprudencia" in texto_lower or "jurisprudência" in texto_lower or "precedente" in texto_lower:
                return "divergente"  # Há menção mas não específica
            else:
                return "desconhecida"  # Sem menção
        
        # Determinar tendência com base nas menções
        if mencoes_stf > 0 or mencoes_stj > 0:
            # Menções a tribunais superiores normalmente indicam questões de interpretação
            if mencoes_stf > mencoes_stj:
                return "favoravel" if "favorável" in texto_lower else "divergente"
            else:
                return "favoravel" if "firmado" in texto_lower or "firmada" in texto_lower else "divergente"
        else:
            return "favoravel" if total_mencoes > 2 else "divergente"
    
    def verificar_presenca_fator(self, texto: str, fator: str) -> bool:
        """
        Verifica se um fator está presente no texto
        """
        # Mapeamento de fatores para palavras-chave
        mapeamento_fatores = {
            "valor_acima_1mi": ["acima de 1.000.000", "superior a 1 milhão", "valor elevado"],
            "natureza_complexa": ["complexidade", "complexo", "complicado", "dificil"],
            "litigiosidade": ["litigioso", "litigante de profissão", "multiplos processos"],
            "prova_documental": ["prova documental", "documento comprobatório", "documentação"],
            "fumus_bonis_iuris": ["fumus bonis iuris", "fumus boni iuris", "probabilidade"],
            "periculum_in_morando": ["perigo da demora", "perigo de dano", "irreparabilidade"],
            "parcelas_multiplicadas": ["parcelas elevadas", "múltiplas parcelas", "parcelas multiplicadas"],
            "sistemica": ["sistemica", "sistêmica", "generalizada", "massificada"],
            "constitucionalidade": ["constitucionalidade", "inconstitucionalidade", "constitucional"],
            "carater_subjetivo": ["subjetivo", "prova pericial", "livre convencimento"],
            "prova_pericial": ["perícia", "pericial", "laudo técnico"]
        }
        
        if fator in mapeamento_fatores:
            for palavra in mapeamento_fatores[fator]:
                if palavra in texto.lower():
                    return True
        
        # Caso genérico - verificar se o termo aparece no texto
        return fator.replace("_", " ") in texto.lower()
    
    def identificar_indicadores_processuais(self, texto: str) -> List[str]:
        """
        Identifica indicadores processuais relevantes
        """
        indicadores = []
        texto_lower = texto.lower()
        
        # Indicadores positivos
        if "prova documental" in texto_lower or "documentos comprobatórios" in texto_lower:
            indicadores.append("prova_documental_forte")
        
        if "jurisprudência favorável" in texto_lower or "precedentes favoráveis" in texto_lower:
            indicadores.append("jurisprudencia_favoravel")
        
        if "fumus bonis iuris" in texto_lower and "periculum in morando" in texto_lower:
            indicadores.append("requisitos_liminar_presentes")
        
        # Indicadores negativos
        if "controvérsia jurisprudencial" in texto_lower or "divergência jurisprudencial" in texto_lower:
            indicadores.append("jurisprudencia_divergente")
        
        if "complexidade técnica" in texto_lower or "prova pericial necessária" in texto_lower:
            indicadores.append("complexidade_tecnica_alta")
        
        if "matéria constitucional" in texto_lower or "constitucionalidade discutida" in texto_lower:
            indicadores.append("risco_constitucional")
        
        return indicadores
    
    def calcular_probabilidades(self, analise: Dict) -> Dict:
        """
        Calcula probabilidades e riscos com base na análise
        """
        area_info = self.base_precedentes["areas_direito"].get(analise["area_direito"], {})
        fatores_info = self.base_precedentes["fatores_gerais"]
        
        # Taxa base de sucesso
        taxa_base = area_info.get("taxa_sucesso", 0.5)
        
        # Modificadores
        modificador_valor = fatores_info["valor_da_causa"][analise["valor_da_causa"]] 
        modificador_complexidade = fatores_info["complexidade"][analise["complexidade"]]
        
        # Verificar jurisprudência
        modificador_jurisprudencia = 1.0
        if analise["jurisprudencia"] in fatores_info["jurisprudencia"]:
            modificador_jurisprudencia = fatores_info["jurisprudencia"][analise["jurisprudencia"]]["multiplicador"]
        
        # Calcular taxa final de sucesso
        taxa_sucesso = taxa_base
        taxa_sucesso *= modificador_valor["multiplicador"]
        taxa_sucesso *= modificador_complexidade["multiplicador"]
        taxa_sucesso /= modificador_jurisprudencia  # Dividir porque jurisprudência contrária aumenta risco
        
        # Limitar entre 0 e 1
        taxa_sucesso = max(0, min(1, taxa_sucesso))
        
        # Calcular risco
        risco = (1 - taxa_sucesso) * 100
        
        # Calcular prazo estimado
        prazo_estimado = area_info.get("media_prazo", 12)
        prazo_estimado *= modificador_complexidade["multiplicador"]
        
        # Análise de risco detalhada
        nivel_risco = "baixo" if risco < 30 else "moderado" if risco < 60 else "alto"
        
        return {
            "taxa_sucesso": taxa_sucesso,
            "risco": risco,
            "nivel_risco": nivel_risco,
            "prazo_estimado_meses": round(prazo_estimado),
            "confianca_analise": self.calcular_confianca(analise),
            "recomendacoes": self.gerar_recomendacoes(analise, taxa_sucesso, risco)
        }
    
    def calcular_confianca(self, analise: Dict) -> float:
        """
        Calcula a confiança da análise preditiva
        """
        # Baseado na quantidade de fatores identificados
        fatores_identificados = len(analise["fatores_risco"]) + len(analise["fatores_favoraveis"])
        indicadores_identificados = len(analise["indicadores_processuais"])
        
        # Pontuação baseada na cobertura
        pontuacao = min(1.0, (fatores_identificados + indicadores_identificados) / 10.0)
        
        return round(pontuacao * 100, 2)
    
    def gerar_recomendacoes(self, analise: Dict, taxa_sucesso: float, risco: float) -> List[str]:
        """
        Gera recomendações com base na análise
        """
        recomendacoes = []
        
        if risco > 70:
            recomendacoes.append("Avaliar a viabilidade do pleito considerando o alto risco")
            recomendacoes.append("Considerar transação ou acordo antes do processo")
        
        if risco > 50 and risco <= 70:
            recomendacoes.append("Procurar fortalecer os pontos fracos identificados")
            recomendacoes.append("Elaborar estratégia processual com foco nos fatores favoráveis")
        
        if taxa_sucesso > 0.7:
            recomendacoes.append("Aguardar desenvolvimento do processo com acompanhamento atento")
            recomendacoes.append("Preparar argumentos para fases recursais")
        
        if "complexidade_tecnica_alta" in analise["indicadores_processuais"]:
            recomendacoes.append("Contratar assistência técnica especializada")
        
        if "jurisprudencia_divergente" in analise["indicadores_processuais"]:
            recomendacoes.append("Aprofundar pesquisa jurisprudencial")
            recomendacoes.append("Buscar precedentes mais favoráveis")
        
        # Recomendações específicas por área
        if analise["area_direito"] == "trabalhista" and "parcelas_multiplicadas" in analise["fatores_risco"]:
            recomendacoes.append("Calcular parcelas com rigor para evitar nulidade")
        
        if analise["area_direito"] == "tributario" and "sistemica" in analise["fatores_risco"]:
            recomendacoes.append("Verificar existência de precedentes firmados sobre a matéria")
        
        return recomendacoes
    
    def gerar_relatorio_preditivo(self, analise: Dict, probabilidades: Dict, processo_path: str, nome_documento: str) -> str:
        """
        Gera um relatório com a análise preditiva
        """
        print("Gerando relatório de análise preditiva...")
        
        # Criar pasta de anotações se não existir
        anotacoes_dir = os.path.join(processo_path, "anotacoes")
        os.makedirs(anotacoes_dir, exist_ok=True)
        
        # Gerar nome de arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"analise_preditiva_{timestamp}.md"
        caminho_arquivo = os.path.join(anotacoes_dir, nome_arquivo)
        
        # Criar conteúdo do relatório
        conteudo = f"""# Análise Preditiva de Riscos Jurídicos

**Documento Analisado:** {nome_documento}
**Data da Análise:** {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
**Sistema de Análise Preditiva Automatizada**

## Resultados da Análise

### Área do Direito
- **Identificada:** {analise['area_direito'].title()}
- **Taxa Média de Sucesso:** {self.base_precedentes['areas_direito'].get(analise['area_direito'], {}).get('taxa_sucesso', 0.5)*100:.2f}%

### Probabilidades Estimadas
- **Taxa de Sucesso:** {probabilidades['taxa_sucesso']*100:.2f}%
- **Nível de Risco:** {probabilidades['nivel_risco'].title()} ({probabilidades['risco']:.2f}%)
- **Prazo Estimado:** {probabilidades['prazo_estimado_meses']} meses
- **Confiança da Análise:** {probabilidades['confianca_analise']}%

## Fatores Identificados

### Fatores de Risco
"""
        
        if analise['fatores_risco']:
            for fator in analise['fatores_risco']:
                conteudo += f"- {fator.replace('_', ' ').title()}\n"
        else:
            conteudo += "- Nenhum fator de risco identificado\n"
        
        conteudo += "\n### Fatores Favoráveis\n"
        if analise['fatores_favoraveis']:
            for fator in analise['fatores_favoraveis']:
                conteudo += f"- {fator.replace('_', ' ').title()}\n"
        else:
            conteudo += "- Nenhum fator favorável identificado\n"
        
        conteudo += "\n### Indicadores Processuais\n"
        if analise['indicadores_processuais']:
            for indicador in analise['indicadores_processuais']:
                conteudo += f"- {indicador.replace('_', ' ').title()}\n"
        else:
            conteudo += "- Nenhum indicador processual específico identificado\n"
        
        conteudo += "\n## Recomendações Estratégicas\n\n"
        for recomendacao in probabilidades['recomendacoes']:
            conteudo += f"- {recomendacao}\n"
        
        conteudo += f"\n## Considerações Finais\n"
        conteudo += f"- A análise preditiva é baseada em precedentes históricos e indicadores processuais\n"
        conteudo += f"- Recomenda-se acompanhamento constante e atualização da análise conforme o processo evolui\n"
        conteudo += f"- O resultado deve ser considerado como subsídio para tomada de decisão, não como certeza absoluta\n\n"
        
        conteudo += f"*Este relatório foi gerado automaticamente pelo sistema de análise preditiva de riscos jurídicos.*\n"
        
        # Salvar o arquivo
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        
        print(f"Relatório preditivo salvo em: {caminho_arquivo}")
        return caminho_arquivo
    
    def executar_analise_completa(self, caminho_documento: str, processo_path: str):
        """
        Executa a análise preditiva completa de um documento
        """
        print(f"Executando análise preditiva: {caminho_documento}")
        
        # Ler conteúdo do documento
        try:
            with open(caminho_documento, 'r', encoding='utf-8') as f:
                texto_documento = f.read()
        except UnicodeDecodeError:
            # Tentar com outro encoding
            with open(caminho_documento, 'r', encoding='latin-1') as f:
                texto_documento = f.read()
        
        # Analisar documento
        analise = self.analisar_documento(texto_documento)
        
        # Calcular probabilidades
        probabilidades = self.calcular_probabilidades(analise)
        
        # Gerar relatório
        nome_documento = os.path.basename(caminho_documento)
        caminho_relatorio = self.gerar_relatorio_preditivo(analise, probabilidades, processo_path, nome_documento)
        
        # Exibir resumo
        print(f"\nResumo da análise preditiva:")
        print(f"- Área do direito: {analise['area_direito']}")
        print(f"- Taxa de sucesso estimada: {probabilidades['taxa_sucesso']*100:.2f}%")
        print(f"- Nível de risco: {probabilidades['nivel_risco']}")
        print(f"- Prazo estimado: {probabilidades['prazo_estimado_meses']} meses")
        print(f"- Confiança da análise: {probabilidades['confianca_analise']}%")
        print(f"- Fatores de risco identificados: {len(analise['fatores_risco'])}")
        print(f"- Fatores favoráveis identificados: {len(analise['fatores_favoraveis'])}")
        
        return analise, probabilidades, caminho_relatorio

def main():
    if len(sys.argv) < 3:
        print("Uso:")
        print("  python analise_preditiva.py <caminho_documento> <pasta_processo>")
        sys.exit(1)
    
    caminho_documento = sys.argv[1]
    pasta_processo = sys.argv[2]
    
    if not os.path.exists(caminho_documento):
        print(f"Documento não encontrado: {caminho_documento}")
        sys.exit(1)
    
    if not os.path.exists(pasta_processo):
        print(f"Pasta do processo não encontrada: {pasta_processo}")
        sys.exit(1)
    
    analisador = AnalisadorPreditivo()
    analisador.executar_analise_completa(caminho_documento, pasta_processo)

if __name__ == "__main__":
    main()