#!/usr/bin/env python3
"""
Sistema de integração com sistemas de consulta de processos dos tribunais
"""

import os
import sys
import json
import re
import requests
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urlencode
import time

class IntegracaoTribunal:
    def __init__(self):
        self.tribunais_suportados = {
            "stf": {
                "nome": "Supremo Tribunal Federal",
                "url_consulta": "https://portal.stf.gov.br/portal-pje/consultas/consulta-pje",
                "metodo": "pje",
                "formato_numero": r"^\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}$"  # Ex: 0000000-00.0000.0.00.0000
            },
            "stj": {
                "nome": "Superior Tribunal de Justiça",
                "url_consulta": "https://portal.stj.gov.br/servicos/djf/consultarprocessoexterno",
                "metodo": "stj",
                "formato_numero": r"^\d{12}$"  # Ex: 000000000000
            },
            "tjmg": {
                "nome": "Tribunal de Justiça de Minas Gerais",
                "url_consulta": "https://consultas2.tjmg.jus.br/consultaprocessos/",
                "metodo": "tjmg",
                "formato_numero": r"^\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}$"
            },
            "trt3": {
                "nome": "Tribunal Regional do Trabalho - 3ª Região",
                "url_consulta": "https://pje.trt3.jus.br/consultapublica/ConsultaPublica/listView.seam",
                "metodo": "pje",
                "formato_numero": r"^\d{7}-\d{2}\.\d{4}\.\d{2}\.\d{3}\.\d{4}$"
            }
        }
    
    def validar_numero_processo(self, numero_processo: str, tribunal_sigla: str) -> bool:
        """
        Valida o número do processo com base no formato esperado do tribunal
        """
        if tribunal_sigla not in self.tribunais_suportados:
            return False
        
        formato = self.tribunais_suportados[tribunal_sigla]["formato_numero"]
        return bool(re.match(formato, numero_processo))
    
    def extrair_numero_processo(self, texto_documento: str) -> List[str]:
        """
        Extrai números de processos do texto do documento
        """
        # Padrão para número de processo no formato CNJ
        padrao_cnj = r'\b\d{7}-\d{2}\.\d{4}\.\d{1,2}\.\d{2}\.\d{4}\b'
        numeros = re.findall(padrao_cnj, texto_documento)
        
        # Padrão para número de processo mais antigo (STJ)
        padrao_antigo = r'\b\d{12}\b'
        numeros.extend(re.findall(padrao_antigo, texto_documento))
        
        # Remover duplicados
        return list(set(numeros))
    
    def consultar_processo_stf(self, numero_processo: str) -> Optional[Dict]:
        """
        Consulta processo no STF (simulado)
        """
        print(f"Consultando processo no STF: {numero_processo}")
        
        # Simulação de consulta - em implementação real, faria requisição HTTP
        # Para fins de demonstração, retornamos dados simulados
        return {
            "numero_processo": numero_processo,
            "tribunal": "STF",
            "classe": "ADI",
            "assunto": "AÇÃO DIRETA DE INCONSTITUCIONALIDADE",
            "data_distribuicao": "2023-01-15",
            "situacao_atual": "Em Trâmite",
            "ultima_movimentacao": "2023-12-01",
            "movimentos": [
                {"data": "2023-01-15", "evento": "Distribuído"},
                {"data": "2023-02-10", "evento": "Juntada de Petição"},
                {"data": "2023-12-01", "evento": "Publicação em DJ"}
            ],
            "partes": [
                {"nome": "REQUERENTE", "tipo": "Autor"},
                {"nome": "REQUERIDO", "tipo": "Réu"}
            ]
        }
    
    def consultar_processo_stj(self, numero_processo: str) -> Optional[Dict]:
        """
        Consulta processo no STJ (simulado)
        """
        print(f"Consultando processo no STJ: {numero_processo}")
        
        # Simulação de consulta
        return {
            "numero_processo": numero_processo,
            "tribunal": "STJ",
            "classe": "REsp",
            "assunto": "RECURSO ESPECIAL",
            "data_distribuicao": "2023-03-20",
            "situacao_atual": "Em Trâmite",
            "ultima_movimentacao": "2023-11-15",
            "movimentos": [
                {"data": "2023-03-20", "evento": "Distribuído"},
                {"data": "2023-04-05", "evento": "Juntada de Contrarrazões"},
                {"data": "2023-11-15", "evento": "Certidão de Inclusão em Mesa"}
            ],
            "partes": [
                {"nome": "RECORRENTE", "tipo": "Apelante"},
                {"nome": "RECORRIDO", "tipo": "Apelado"}
            ]
        }
    
    def consultar_processo_tjmg(self, numero_processo: str) -> Optional[Dict]:
        """
        Consulta processo no TJMG (simulado)
        """
        print(f"Consultando processo no TJMG: {numero_processo}")
        
        # Simulação de consulta
        return {
            "numero_processo": numero_processo,
            "tribunal": "TJMG",
            "classe": "Proc. Cível",
            "assunto": "COBRANÇA",
            "data_distribuicao": "2023-05-10",
            "situacao_atual": "Em Trâmite",
            "ultima_movimentacao": "2023-10-22",
            "movimentos": [
                {"data": "2023-05-10", "evento": "Distribuído"},
                {"data": "2023-05-15", "evento": "Citação"},
                {"data": "2023-06-20", "evento": "Contestação"},
                {"data": "2023-10-22", "evento": "Juntada de Provas"}
            ],
            "partes": [
                {"nome": "AUTOR", "tipo": "Requerente"},
                {"nome": "RÉU", "tipo": "Requerido"}
            ]
        }
    
    def consultar_processo_trt3(self, numero_processo: str) -> Optional[Dict]:
        """
        Consulta processo no TRT3 (simulado)
        """
        print(f"Consultando processo no TRT3: {numero_processo}")
        
        # Simulação de consulta
        return {
            "numero_processo": numero_processo,
            "tribunal": "TRT3",
            "classe": "RO",
            "assunto": "RECLAMAÇÃO TRABALHISTA",
            "data_distribuicao": "2023-04-18",
            "situacao_atual": "Concluído",
            "ultima_movimentacao": "2023-09-30",
            "movimentos": [
                {"data": "2023-04-18", "evento": "Distribuído"},
                {"data": "2023-04-25", "evento": "Citação"},
                {"data": "2023-05-30", "evento": "Resposta do Réu"},
                {"data": "2023-09-30", "evento": "Sentença - PROCEDENTE"}
            ],
            "partes": [
                {"nome": "RECLAMANTE", "tipo": "Autor"},
                {"nome": "RECLAMADO", "tipo": "Réu"}
            ]
        }
    
    def consultar_processo(self, numero_processo: str, tribunal_sigla: str) -> Optional[Dict]:
        """
        Consulta processo em tribunal específico
        """
        if tribunal_sigla not in self.tribunais_suportados:
            print(f"Tribunal {tribunal_sigla} não suportado")
            return None
        
        # Validar número do processo
        if not self.validar_numero_processo(numero_processo, tribunal_sigla):
            print(f"Número de processo {numero_processo} inválido para o tribunal {tribunal_sigla}")
            return None
        
        # Mapear método de consulta
        metodos_consulta = {
            "stf": self.consultar_processo_stf,
            "stj": self.consultar_processo_stj,
            "tjmg": self.consultar_processo_tjmg,
            "trt3": self.consultar_processo_trt3
        }
        
        metodo = metodos_consulta.get(tribunal_sigla)
        if metodo:
            return metodo(numero_processo)
        else:
            print(f"Método de consulta não implementado para {tribunal_sigla}")
            return None
    
    def consultar_documento(self, texto_documento: str) -> List[Dict]:
        """
        Consulta processos mencionados no documento
        """
        print("Extrair e consultar processos mencionados no documento...")
        
        numeros_processo = self.extrair_numero_processo(texto_documento)
        resultados = []
        
        for numero in numeros_processo:
            # Tentar identificar o tribunal pelo número (últimos 4 dígitos do órgão judiciário)
            tribunal = self.identificar_tribunal_por_numero(numero)
            
            if tribunal:
                print(f"Identificado tribunal {tribunal} para o processo {numero}")
                resultado = self.consultar_processo(numero, tribunal)
                if resultado:
                    resultados.append(resultado)
            else:
                print(f"Não foi possível identificar o tribunal para o processo {numero}")
        
        return resultados
    
    def identificar_tribunal_por_numero(self, numero_processo: str) -> Optional[str]:
        """
        Identifica o tribunal com base no número do processo (padrão CNJ)
        """
        if len(numero_processo) >= 20:  # Formato CNJ completo
            # Os dígitos 14-16 representam o órgão judiciário
            try:
                orgao = numero_processo[13:16]
                
                # Mapeamento simplificado de órgãos judiciários
                orgaos_map = {
                    "000": "stf",  # Supremo Tribunal Federal
                    "010": "stj",  # Superior Tribunal de Justiça
                    "020": "tjmg",  # Exemplo para TJMG
                    "022": "trt3"   # Exemplo para TRT3
                }
                
                return orgaos_map.get(orgao, None)
            except:
                return None
        
        # Tentar identificar por comprimento e outros critérios
        if len(numero_processo) == 12:  # Formato antigo STJ
            return "stj"
        
        return None
    
    def salvar_atualizacoes_processo(self, resultados: List[Dict], processo_path: str):
        """
        Salva as atualizações dos processos consultados
        """
        print("Salvando atualizações dos processos consultados...")
        
        # Criar pasta de atualizacoes se não existir
        atualizacoes_dir = os.path.join(processo_path, "atualizacoes_tribunal")
        os.makedirs(atualizacoes_dir, exist_ok=True)
        
        # Gerar nome de arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"atualizacoes_tribunal_{timestamp}.json"
        caminho_arquivo = os.path.join(atualizacoes_dir, nome_arquivo)
        
        # Salvar os resultados
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"Atualizações salvas em: {caminho_arquivo}")
        
        # Criar versão em Markdown para fácil leitura
        md_path = os.path.join(atualizacoes_dir, f"atualizacoes_tribunal_{timestamp}.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write("# Atualizações de Processos nos Tribunais\n\n")
            f.write(f"*Consulta realizada em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*\n\n")
            
            for resultado in resultados:
                f.write(f"## Processo: {resultado['numero_processo']}\n")
                f.write(f"- **Tribunal:** {resultado['tribunal']}\n")
                f.write(f"- **Classe:** {resultado['classe']}\n")
                f.write(f"- **Assunto:** {resultado['assunto']}\n")
                f.write(f"- **Situação:** {resultado['situacao_atual']}\n")
                f.write(f"- **Última Movimentação:** {resultado['ultima_movimentacao']}\n\n")
                
                f.write("### Movimentações Recentes:\n")
                for movimento in resultado['movimentos'][-5:]:  # Últimas 5 movimentações
                    f.write(f"- **{movimento['data']}**: {movimento['evento']}\n")
                
                f.write("\n### Partes Envolvidas:\n")
                for parte in resultado['partes']:
                    f.write(f"- **{parte['tipo']}**: {parte['nome']}\n")
                
                f.write("---\n\n")
        
        print(f"Resumo em Markdown salvo em: {md_path}")
        return caminho_arquivo
    
    def executar_consulta_documento(self, caminho_documento: str, processo_path: str):
        """
        Executa a consulta de processos mencionados em um documento
        """
        print(f"Executando consulta de processos: {caminho_documento}")
        
        # Ler conteúdo do documento
        try:
            with open(caminho_documento, 'r', encoding='utf-8') as f:
                texto_documento = f.read()
        except UnicodeDecodeError:
            # Tentar com outro encoding
            with open(caminho_documento, 'r', encoding='latin-1') as f:
                texto_documento = f.read()
        
        # Consultar processos mencionados
        resultados = self.consultar_documento(texto_documento)
        
        if resultados:
            print(f"Foram encontrados e consultados {len(resultados)} processos")
            
            # Salvar atualizações
            caminho_salvo = self.salvar_atualizacoes_processo(resultados, processo_path)
            
            # Exibir resumo
            print("\nResumo das consultas realizadas:")
            for resultado in resultados:
                print(f"- Processo {resultado['numero_processo']} no {resultado['tribunal']}")
                print(f"  Situação: {resultado['situacao_atual']}")
                print(f"  Última movimentação: {resultado['ultima_movimentacao']}")
        else:
            print("Nenhum processo identificado ou consultado com sucesso")
        
        return resultados

def main():
    if len(sys.argv) < 3:
        print("Uso:")
        print("  python integracao_tribunal.py <caminho_documento> <pasta_processo>")
        print("  python integracao_tribunal.py <numero_processo> <tribunal_sigla>  # Consulta direta")
        sys.exit(1)
    
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    
    integracao = IntegracaoTribunal()
    
    # Verificar se os argumentos são um número de processo e tribunal
    if re.match(r'^\d{7}-\d{2}\.\d{4}\.\d{1,2}\.\d{2}\.\d{4}$|^\d{12}$', arg1) and arg2 in integracao.tribunais_suportados:
        # Consulta direta de processo
        numero_processo = arg1
        tribunal_sigla = arg2
        
        resultado = integracao.consultar_processo(numero_processo, tribunal_sigla)
        if resultado:
            print(json.dumps(resultado, indent=2, ensure_ascii=False, default=str))
        else:
            print("Falha na consulta do processo")
            sys.exit(1)
    else:
        # Consulta a partir de documento
        caminho_documento = arg1
        pasta_processo = arg2
        
        if not os.path.exists(caminho_documento):
            print(f"Documento não encontrado: {caminho_documento}")
            sys.exit(1)
        
        if not os.path.exists(pasta_processo):
            print(f"Pasta do processo não encontrada: {pasta_processo}")
            sys.exit(1)
        
        integracao.executar_consulta_documento(caminho_documento, pasta_processo)

if __name__ == "__main__":
    main()