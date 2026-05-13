#!/usr/bin/env python3
"""
Sistema de classificação automática de documentos jurídicos
"""

import os
import sys
import json
import re
from datetime import datetime
from typing import Dict, List, Tuple
import shutil

def identificar_tipo_documento(texto: str) -> Tuple[str, float]:
    """
    Identifica o tipo de documento jurídico com base em palavras-chave
    Retorna o tipo e a confiança (0-1)
    """
    texto_lower = texto.lower()
    
    # Tipos de documentos e palavras-chave associadas
    tipos_documentos = {
        "peticao_inicial": {
            "palavras_chave": ["ação", "ajuizar", "ajuizamento", "inicial", "réu", "autor", "cumprimento", "pedido"],
            "peso": 1.0
        },
        "contestacao": {
            "palavras_chave": ["contestar", "contestação", "réplica", "impugnar", "objeções", "descumprimento"],
            "peso": 1.0
        },
        "sentenca": {
            "palavras_chave": ["sentença", "julgamento", "provido", "negado", "provido", "extinto", "mérito"],
            "peso": 1.0
        },
        "despacho": {
            "palavras_chave": ["despacho", "determino", "deferimento", "indeferimento", "diligências", "juntada"],
            "peso": 1.0
        },
        "acordao": {
            "palavras_chave": ["acórdão", "relator", "vistos", "provido", "negado", "votante", "unânime"],
            "peso": 1.0
        },
        "intimacao": {
            "palavras_chave": ["intimação", "ciência", "publicação", "certidão", "intimado", "comparecimento"],
            "peso": 1.0
        },
        "recurso": {
            "palavras_chave": ["apelação", "agravo", "recurso", "interpor", "interposição", "reexame", "necessário"],
            "peso": 1.0
        },
        "parecer": {
            "palavras_chave": ["parecer", "jurídico", "análise", "fundamentação", "opinião", "técnico"],
            "peso": 1.0
        },
        "contrato": {
            "palavras_chave": ["contrato", "cláusula", "partes", "obrigação", "objeto", "prestação", "recíproca"],
            "peso": 1.0
        }
    }
    
    melhor_tipo = "outros"
    melhor_pontuacao = 0
    
    for tipo, info in tipos_documentos.items():
        pontuacao = 0
        for palavra in info["palavras_chave"]:
            if palavra in texto_lower:
                # Dar peso maior para ocorrências mais frequentes
                ocorrencias = len(re.findall(r'\b' + re.escape(palavra) + r'\b', texto_lower))
                pontuacao += ocorrencias
        
        if pontuacao > melhor_pontuacao:
            melhor_pontuacao = pontuacao
            melhor_tipo = tipo
    
    # Calcular confiança baseada na pontuação
    confianca = min(melhor_pontuacao / 10.0, 1.0)  # Normalizar para 0-1
    
    return melhor_tipo, confianca

def organizar_documento(origem: str, destino_base: str, tipo_documento: str):
    """
    Organiza o documento movendo-o para a pasta apropriada
    """
    print(f"Organizando documento como: {tipo_documento}")
    
    # Criar pasta de destino baseada no tipo de documento
    pasta_destino = os.path.join(destino_base, "documentos_classificados", tipo_documento)
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Copiar o arquivo para a pasta de destino
    nome_arquivo = os.path.basename(origem)
    caminho_destino = os.path.join(pasta_destino, nome_arquivo)
    
    # Se já existir, adicionar timestamp
    if os.path.exists(caminho_destino):
        nome_base, ext = os.path.splitext(nome_arquivo)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        novo_nome = f"{nome_base}_{timestamp}{ext}"
        caminho_destino = os.path.join(pasta_destino, novo_nome)
    
    shutil.copy2(origem, caminho_destino)
    print(f"Documento copiado para: {caminho_destino}")
    
    return caminho_destino

def classificar_documento(caminho_documento: str, pasta_processo: str, texto_documento: str = None):
    """
    Classifica um documento e organiza-o automaticamente
    """
    print(f"Classificando documento: {caminho_documento}")
    
    # Se não foi fornecido texto, ler do arquivo
    if texto_documento is None:
        try:
            with open(caminho_documento, 'r', encoding='utf-8') as f:
                texto_documento = f.read()
        except UnicodeDecodeError:
            # Tentar com outro encoding
            with open(caminho_documento, 'r', encoding='latin-1') as f:
                texto_documento = f.read()
    
    # Identificar tipo de documento
    tipo_documento, confianca = identificar_tipo_documento(texto_documento)
    
    print(f"Tipo identificado: {tipo_documento} (confiança: {confianca:.2f})")
    
    # Só organizar se a confiança for razoável
    if confianca > 0.3:
        caminho_organizado = organizar_documento(caminho_documento, pasta_processo, tipo_documento)
        
        # Registrar classificação
        registrar_classificacao(caminho_documento, tipo_documento, confianca, caminho_organizado)
        
        return tipo_documento, confianca
    else:
        print(f"Confiança muito baixa ({confianca:.2f}), mantendo documento original")
        return "outros", confianca

def registrar_classificacao(origem: str, tipo: str, confianca: float, destino: str):
    """
    Registra a classificação em um arquivo de log
    """
    pasta_origem = os.path.dirname(origem)
    log_dir = os.path.join(pasta_origem, "logs_classificacao")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"classificacao_{datetime.now().strftime('%Y%m')}.json")
    
    registro = {
        "timestamp": datetime.now().isoformat(),
        "documento_origem": origem,
        "documento_destino": destino,
        "tipo_classificado": tipo,
        "confianca": confianca
    }
    
    # Ler registros anteriores se existirem
    registros_existentes = []
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                registros_existentes = json.load(f)
        except:
            registros_existentes = []
    
    registros_existentes.append(registro)
    
    # Salvar registros atualizados
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(registros_existentes, f, ensure_ascii=False, indent=2)

def processar_pasta_documentos(pasta_origem: str, pasta_processo: str):
    """
    Processa todos os documentos em uma pasta e classifica-os
    """
    print(f"Processando documentos em: {pasta_origem}")
    
    documentos_processados = 0
    
    for arquivo in os.listdir(pasta_origem):
        caminho_completo = os.path.join(pasta_origem, arquivo)
        
        # Processar apenas arquivos de texto ou PDFs que já foram convertidos
        if arquivo.lower().endswith(('.txt', '.md')):
            print(f"Processando: {arquivo}")
            
            with open(caminho_completo, 'r', encoding='utf-8') as f:
                texto = f.read()
            
            classificar_documento(caminho_completo, pasta_processo, texto)
            documentos_processados += 1
    
    print(f"Processamento concluído. {documentos_processados} documentos processados.")

def main():
    if len(sys.argv) < 3:
        print("Uso:")
        print("  python classificador_documentos.py <caminho_documento> <pasta_processo>")
        print("  python classificador_documentos.py <pasta_documentos> <pasta_processo>  # Para processar toda a pasta")
        sys.exit(1)
    
    caminho_entrada = sys.argv[1]
    pasta_processo = sys.argv[2]
    
    if not os.path.exists(caminho_entrada):
        print(f"Caminho não encontrado: {caminho_entrada}")
        sys.exit(1)
    
    if not os.path.exists(pasta_processo):
        print(f"Pasta do processo não encontrada: {pasta_processo}")
        sys.exit(1)
    
    if os.path.isfile(caminho_entrada):
        # Processar arquivo individual
        classificar_documento(caminho_entrada, pasta_processo)
    elif os.path.isdir(caminho_entrada):
        # Processar toda a pasta
        processar_pasta_documentos(caminho_entrada, pasta_processo)
    else:
        print("Entrada inválida. Deve ser um arquivo ou diretório.")
        sys.exit(1)

if __name__ == "__main__":
    main()