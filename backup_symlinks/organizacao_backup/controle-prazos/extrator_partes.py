#!/usr/bin/env python3
"""
Sistema de extração automatizada de partes envolvidas em processos
"""

import os
import sys
import json
import re
from datetime import datetime
from typing import Dict, List, Tuple
import spacy
from pathlib import Path

def carregar_modelo_nlp():
    """Carrega modelo de processamento de linguagem natural para português"""
    try:
        # Tenta carregar modelo do spaCy para português
        nlp = spacy.load("pt_core_news_sm")
        return nlp
    except OSError:
        print("Modelo 'pt_core_news_sm' do spaCy não encontrado.")
        print("Instale com: python -m spacy download pt_core_news_sm")
        print("Usando expressões regulares como fallback.")
        return None

def extrair_partes_regex(texto: str) -> Dict[str, List[str]]:
    """
    Extrai partes envolvidas usando expressões regulares
    """
    partes = {
        "autores": [],
        "reus": [],
        "advogados": [],
        "juizes": [],
        "outros": []
    }
    
    # Converter para minúsculas para comparação
    texto_lower = texto.lower()
    
    # Padrões para identificar partes
    padroes = {
        "autores": [
            r"autos?\s+de\s+([^,\.\n]+?)\s+(?:vs\.?|versus|contra)",
            r"(?:exmo\.?\s+sr\.?|excelentíssimo\s+sr\.?)\s+dr\.?\s+([^,\.\n]+?)\s+autos?\s+de",
            r"requer(?:ente|ido)\s+:?\s*([^,\.\n]+?)(?:\s+(?:cpf|cnpj|oab))?"
        ],
        "reus": [
            r"vs\.?\s+([^,\.\n]+?)(?:\s+(?:cpf|cnpj|oab))?",
            r"versus\s+([^,\.\n]+?)(?:\s+(?:cpf|cnpj|oab))?",
            r"contra\s+([^,\.\n]+?)(?:\s+(?:cpf|cnpj|oab))?",
            r"requerido\s+:?\s*([^,\.\n]+?)(?:\s+(?:cpf|cnpj|oab))?"
        ],
        "advogados": [
            r"(?:adv\.?|advogad[oa]s?)\s+([^,\.\n]+?)(?:\s+nº?\s+\d+)?",
            r"oab\s+n[oº]?\s*(\d+)[^,\.\n]*?-\s*([^,\.\n]+?)",
            r"inscrito\s+na\s+oab\s+[^,\.\n]*?-\s*([^,\.\n]+?)",
            r"representa(?:do)?\s+pelo\s+(?:adv\.?|advogad[oa])\s+([^,\.\n]+?)"
        ],
        "juizes": [
            r"(?:exmo\.?\s+sr\.?|excelentíssimo\s+sr\.?)\s+(?:dr\.?|dra\.?)\s+([^,\.\n]+?)\s+(?:juiz|desembargador|ministro)",
            r"(?:juiz|desembargador|ministro)\s+([^,\.\n]+?)(?:\s+(?:dra\.?|dr\.?))?",
            r"vossa\s+excelência\s+([^,\.\n]+?)\s+(?:juiz|desembargador|ministro)"
        ]
    }
    
    # Extrair usando cada padrão
    for categoria, lista_padroes in padroes.items():
        for padrao in lista_padroes:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    # Se for um grupo múltiplo, pegar o primeiro grupo significativo
                    match = next((m for m in match if m.strip()), "").strip()
                else:
                    match = match.strip()
                
                if match and len(match) > 2:  # Filtrar strings muito curtas
                    # Remover possíveis números e caracteres especiais extras
                    match = re.sub(r'\s+', ' ', match).strip()
                    
                    # Adicionar apenas se não for duplicado
                    if match not in partes[categoria]:
                        partes[categoria].append(match)
    
    # Extração mais genérica de nomes próprios
    # Procurar por padrões de nomes: "Sr./Sra. Nome Sobrenome"
    nomes_padrao = r"(?:sr[aº]?\s+|dr[aº]?\s+|exmo\.?\s+sr[aº]?\s+)([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]*)*)"
    nomes_matches = re.findall(nomes_padrao, texto)
    
    for nome in nomes_matches:
        nome = nome.strip()
        if nome and len(nome) > 5:  # Filtrar nomes muito curtos
            # Verificar se já está em alguma categoria
            ja_adicionado = False
            for categoria in partes.values():
                if nome in categoria:
                    ja_adicionado = True
                    break
            
            if not ja_adicionado:
                partes["outros"].append(nome)
    
    return partes

def extrair_partes_nlp(texto: str, nlp_model) -> Dict[str, List[str]]:
    """
    Extrai partes envolvidas usando NLP (spaCy)
    """
    if not nlp_model:
        return extrair_partes_regex(texto)
    
    doc = nlp_model(texto)
    
    partes = {
        "autores": [],
        "reus": [],
        "advogados": [],
        "juizes": [],
        "outros": []
    }
    
    # Extrair entidades nomeadas
    nomes_pessoas = []
    for ent in doc.ents:
        if ent.label_ == "PER" or ent.text.lower() in ["autor", "réu", "advogado", "juiz"]:
            nomes_pessoas.append(ent.text)
    
    # Usar também a abordagem regex como complemento
    partes_regex = extrair_partes_regex(texto)
    
    # Combinar resultados
    for categoria in partes:
        partes[categoria] = list(set(partes_regex[categoria]))  # Usar regex como base
    
    return partes

def salvar_partes_extraidas(processo_path: str, partes: Dict[str, List[str]], nome_arquivo_original: str = ""):
    """
    Salva as partes extraídas no sistema de anotações do processo
    """
    print(f"Salvando partes extraídas para o processo: {processo_path}")
    
    # Criar pasta de anotações se não existir
    anotacoes_dir = os.path.join(processo_path, "anotacoes")
    os.makedirs(anotacoes_dir, exist_ok=True)
    
    # Gerar nome de arquivo baseado no original
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"partes_envolvidas_{timestamp}.json"
    caminho_arquivo = os.path.join(anotacoes_dir, nome_arquivo)
    
    # Adicionar metadados
    dados_partes = {
        "fonte_documento": nome_arquivo_original,
        "data_extracao": datetime.now().isoformat(),
        "partes_identificadas": partes
    }
    
    # Salvar o arquivo
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados_partes, f, ensure_ascii=False, indent=2)
    
    print(f"Partes salvas em: {caminho_arquivo}")
    
    # Também criar versão em Markdown para fácil leitura
    md_path = os.path.join(anotacoes_dir, f"partes_envolvidas_{timestamp}.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# Partes Envolvidas no Processo\n\n")
        f.write(f"*Extraído de: {nome_arquivo_original}*\n")
        f.write(f"*Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*\n\n")
        
        for categoria, lista_partes in partes.items():
            if lista_partes:
                f.write(f"## {categoria.replace('_', ' ').title()}\n\n")
                for parte in lista_partes:
                    f.write(f"- {parte}\n")
                f.write("\n")
    
    print(f"Resumo em Markdown salvo em: {md_path}")
    return caminho_arquivo

def atualizar_catalogo_geral(partes: Dict[str, List[str]], processo_path: str):
    """
    Atualiza o catálogo geral de partes envolvidas em todos os processos
    """
    # Obter nome do processo
    nome_processo = os.path.basename(processo_path)
    
    # Caminho para o catálogo geral
    catalogo_path = os.path.expanduser("~/organizacao/controle-prazos/catalogo_partes_geral.json")
    
    # Carregar catálogo existente ou criar novo
    if os.path.exists(catalogo_path):
        with open(catalogo_path, 'r', encoding='utf-8') as f:
            catalogo = json.load(f)
    else:
        catalogo = {
            "ultima_atualizacao": datetime.now().isoformat(),
            "processos": {}
        }
    
    # Atualizar informações do processo
    catalogo["processos"][nome_processo] = {
        "path": processo_path,
        "partes": partes,
        "ultima_atualizacao": datetime.now().isoformat()
    }
    
    # Atualizar timestamp
    catalogo["ultima_atualizacao"] = datetime.now().isoformat()
    
    # Salvar catálogo atualizado
    with open(catalogo_path, 'w', encoding='utf-8') as f:
        json.dump(catalogo, f, ensure_ascii=False, indent=2)
    
    print(f"Catálogo geral de partes atualizado: {catalogo_path}")

def processar_documento_partes(caminho_documento: str, processo_path: str):
    """
    Processa um documento e extrai as partes envolvidas
    """
    print(f"Processando documento para extração de partes: {caminho_documento}")
    
    # Ler conteúdo do documento
    try:
        with open(caminho_documento, 'r', encoding='utf-8') as f:
            texto = f.read()
    except UnicodeDecodeError:
        # Tentar com outro encoding
        with open(caminho_documento, 'r', encoding='latin-1') as f:
            texto = f.read()
    
    # Carregar modelo NLP
    nlp_model = carregar_modelo_nlp()
    
    # Extrair partes
    partes = extrair_partes_nlp(texto, nlp_model)
    
    # Salvar resultados
    nome_arquivo = os.path.basename(caminho_documento)
    salvar_partes_extraidas(processo_path, partes, nome_arquivo)
    
    # Atualizar catálogo geral
    atualizar_catalogo_geral(partes, processo_path)
    
    # Imprimir resumo
    print("\nResumo das partes identificadas:")
    for categoria, lista_partes in partes.items():
        if lista_partes:
            print(f"  {categoria.replace('_', ' ').title()}: {len(lista_partes)} encontradas")
            for parte in lista_partes[:3]:  # Mostrar apenas as 3 primeiras
                print(f"    - {parte}")
            if len(lista_partes) > 3:
                print(f"    ... e mais {len(lista_partes) - 3}")
    
    return partes

def buscar_partes(nome_parcial: str) -> List[Dict]:
    """
    Busca por partes em todos os processos usando nome parcial
    """
    catalogo_path = os.path.expanduser("~/organizacao/controle-prazos/catalogo_partes_geral.json")
    
    if not os.path.exists(catalogo_path):
        print("Catálogo de partes não encontrado. Execute a extração primeiro.")
        return []
    
    with open(catalogo_path, 'r', encoding='utf-8') as f:
        catalogo = json.load(f)
    
    resultados = []
    nome_parcial_lower = nome_parcial.lower()
    
    for processo_nome, dados_processo in catalogo.get("processos", {}).items():
        for categoria, lista_partes in dados_processo.get("partes", {}).items():
            for parte in lista_partes:
                if nome_parcial_lower in parte.lower():
                    resultados.append({
                        "processo": processo_nome,
                        "parte": parte,
                        "categoria": categoria,
                        "path": dados_processo.get("path", "")
                    })
    
    return resultados

def main():
    if len(sys.argv) < 3:
        print("Uso:")
        print("  python extrator_partes.py <caminho_documento> <pasta_processo>")
        print("  python extrator_partes.py buscar <nome_parcial>  # Busca por nome")
        sys.exit(1)
    
    comando = sys.argv[1]
    
    if comando == "buscar":
        if len(sys.argv) < 3:
            print("Uso: python extrator_partes.py buscar <nome_parcial>")
            sys.exit(1)
        
        nome_parcial = sys.argv[2]
        resultados = buscar_partes(nome_parcial)
        
        if resultados:
            print(f"\nResultados para '{nome_parcial}':")
            print("="*50)
            
            for resultado in resultados:
                print(f"Processo: {resultado['processo']}")
                print(f"Parte: {resultado['parte']}")
                print(f"Categoria: {resultado['categoria']}")
                print("-" * 30)
        else:
            print(f"Nenhuma parte encontrada com o nome '{nome_parcial}'")
    
    else:
        caminho_documento = sys.argv[1]
        pasta_processo = sys.argv[2]
        
        if not os.path.exists(caminho_documento):
            print(f"Documento não encontrado: {caminho_documento}")
            sys.exit(1)
        
        if not os.path.exists(pasta_processo):
            print(f"Pasta do processo não encontrada: {pasta_processo}")
            sys.exit(1)
        
        processar_documento_partes(caminho_documento, pasta_processo)

if __name__ == "__main__":
    main()