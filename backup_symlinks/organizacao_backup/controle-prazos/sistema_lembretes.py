#!/usr/bin/env python3
"""
Sistema de lembretes processuais baseado nos prazos identificados
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List
import subprocess

def criar_lembrete(prazo_descricao: str, data_vencimento: str, processo_path: str, dias_antecedencia: int = 3):
    """
    Cria um lembrete para um prazo processual
    """
    print(f"Criando lembrete para: {prazo_descricao}")
    print(f"Vencimento: {data_vencimento}")
    
    # Converter string de data para objeto datetime
    try:
        data_vencimento_dt = datetime.strptime(data_vencimento, "%Y-%m-%d")
    except ValueError:
        # Tentar outros formatos comuns
        try:
            data_vencimento_dt = datetime.strptime(data_vencimento, "%d/%m/%Y")
        except ValueError:
            print(f"Formato de data inválido: {data_vencimento}")
            return None
    
    # Calcular data do lembrete (dias antes do vencimento)
    data_lembrete = data_vencimento_dt - timedelta(days=dias_antecedencia)
    
    # Criar mensagem de lembrete
    mensagem_lembrete = f"Lembrete: {prazo_descricao} no processo. Vence em {data_vencimento}"
    
    # Criar nome de arquivo para o lembrete
    nome_arquivo = f"lembrete_{data_lembrete.strftime('%Y%m%d')}_{data_vencimento}.txt"
    caminho_lembrete = os.path.join(processo_path, "lembretes", nome_arquivo)
    
    # Criar diretório de lembretes se não existir
    os.makedirs(os.path.join(processo_path, "lembretes"), exist_ok=True)
    
    # Salvar informações do lembrete
    lembrete_info = {
        "descricao": prazo_descricao,
        "data_vencimento": data_vencimento,
        "data_lembrete": data_lembrete.isoformat(),
        "mensagem": mensagem_lembrete,
        "processo_path": processo_path,
        "dias_antecedencia": dias_antecedencia
    }
    
    with open(caminho_lembrete, 'w', encoding='utf-8') as f:
        json.dump(lembrete_info, f, ensure_ascii=False, indent=2)
    
    print(f"Lembrete criado: {caminho_lembrete}")
    return caminho_lembrete

def processar_prazos_para_lembretes(analise_file: str, processo_path: str):
    """
    Processa um arquivo de análise jurídica para criar lembretes dos prazos identificados
    """
    print(f"Processando prazos para lembretes em: {analise_file}")
    
    with open(analise_file, 'r', encoding='utf-8') as f:
        analise = json.load(f)
    
    prazos = analise.get('prazos_identificados', [])
    
    if not prazos:
        print("Nenhum prazo identificado para criar lembretes")
        return
    
    for i, prazo in enumerate(prazos):
        descricao = prazo.get('descricao', f'Prazo genérico {i+1}')
        contexto = prazo.get('contexto', '')
        
        # Tentar extrair data do contexto ou descrição
        import re
        
        # Padrões comuns de datas
        padroes_data = [
            r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
            r'(\d{2}/\d{2}/\d{4})',  # DD/MM/YYYY
            r'(\d{2}-\d{2}-\d{4})',  # DD-MM-YYYY
        ]
        
        data_encontrada = None
        for padrao in padroes_data:
            matches = re.search(padrao, contexto + " " + descricao)
            if matches:
                data_encontrada = matches.group(1)
                break
        
        if data_encontrada:
            criar_lembrete(descricao, data_encontrada, processo_path)
        else:
            print(f"Não foi possível extrair data para o prazo: {descricao}")

def verificar_lembretes_hoje():
    """
    Verifica se há lembretes para hoje em todos os processos
    """
    print("Verificando lembretes para hoje...")
    
    hoje = datetime.now().date()
    lembretes_hoje = []
    
    # Procurar em todas as pastas de processo
    pastas_base = [
        os.path.expanduser("~/organizacao/advocacia/ativos"),
        os.path.expanduser("~/organizacao/servidor-publico/ativos")
    ]
    
    for pasta_base in pastas_base:
        if os.path.exists(pasta_base):
            for pasta_nome in os.listdir(pasta_base):
                processo_path = os.path.join(pasta_base, pasta_nome)
                if os.path.isdir(processo_path):
                    lembretes_dir = os.path.join(processo_path, "lembretes")
                    if os.path.exists(lembretes_dir):
                        for lembrete_nome in os.listdir(lembretes_dir):
                            if lembrete_nome.startswith("lembrete_") and lembrete_nome.endswith(".txt"):
                                caminho_lembrete = os.path.join(lembretes_dir, lembrete_nome)
                                
                                with open(caminho_lembrete, 'r', encoding='utf-8') as f:
                                    lembrete = json.load(f)
                                
                                # Comparar data do lembrete com hoje
                                data_lembrete = datetime.fromisoformat(lembrete['data_lembrete']).date()
                                
                                if data_lembrete == hoje:
                                    lembretes_hoje.append({
                                        "mensagem": lembrete['mensagem'],
                                        "processo": pasta_nome,
                                        "caminho": caminho_lembrete
                                    })
    
    if lembretes_hoje:
        print(f"Encontrados {len(lembretes_hoje)} lembretes para hoje:")
        for lembrete in lembretes_hoje:
            print(f"- {lembrete['mensagem']} (Processo: {lembrete['processo']})")
    else:
        print("Nenhum lembrete para hoje")
    
    return lembretes_hoje

def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python sistema_lembretes.py criar <arquivo_analise> <pasta_processo>  # Cria lembretes a partir de análise")
        print("  python sistema_lembretes.py verificar                           # Verifica lembretes para hoje")
        sys.exit(1)
    
    comando = sys.argv[1]
    
    if comando == "criar":
        if len(sys.argv) != 4:
            print("Uso: python sistema_lembretes.py criar <arquivo_analise> <pasta_processo>")
            sys.exit(1)
        
        analise_file = sys.argv[2]
        processo_path = sys.argv[3]
        
        if not os.path.exists(analise_file):
            print(f"Arquivo de análise não encontrado: {analise_file}")
            sys.exit(1)
        
        if not os.path.exists(processo_path):
            print(f"Pasta do processo não encontrada: {processo_path}")
            sys.exit(1)
        
        processar_prazos_para_lembretes(analise_file, processo_path)
        
    elif comando == "verificar":
        lembretes_hoje = verificar_lembretes_hoje()
        
        # Se houver lembretes para hoje, podemos enviar notificação
        if lembretes_hoje:
            print("\nNOTIFICAÇÃO: Você tem prazos importantes vencendo em breve!")
            for lembrete in lembretes_hoje:
                print(f"  - {lembrete['mensagem']}")
    
    else:
        print("Comando inválido. Use 'criar' ou 'verificar'.")
        sys.exit(1)

if __name__ == "__main__":
    main()