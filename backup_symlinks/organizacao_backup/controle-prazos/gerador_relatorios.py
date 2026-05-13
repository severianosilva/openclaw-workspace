#!/usr/bin/env python3
"""
Sistema de geração automatizada de relatórios jurídicos
"""

import os
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List
import subprocess

def gerar_relatorio_diario():
    """Gera relatório diário com status dos processos"""
    print("Gerando relatório diário...")
    
    data_hoje = datetime.now()
    data_formatada = data_hoje.strftime("%d/%m/%Y")
    
    # Conteúdo do relatório
    conteudo = f"# Relatório Diário - {data_formatada}\n\n"
    conteudo += f"**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
    
    # Incluir informações sobre prazos próximos
    conteudo += "## Prazos Próximos\n\n"
    prazos_proximos = verificar_prazos_proximos()
    if prazos_proximos:
        for prazo in prazos_proximos:
            conteudo += f"- **{prazo['descricao']}** - {prazo['data']} - Processo: {prazo['processo']}\n"
    else:
        conteudo += "*Nenhum prazo próximo identificado*\n\n"
    
    # Incluir informações sobre novos documentos
    conteudo += "## Atividades Recentes\n\n"
    atividades = verificar_atividades_recentes()
    if atividades:
        for atividade in atividades:
            conteudo += f"- **{atividade['tipo']}** - {atividade['data']} - {atividade['descricao']}\n"
    else:
        conteudo += "*Nenhuma atividade recente*\n\n"
    
    # Incluir lembretes do dia
    conteudo += "## Lembretes para Hoje\n\n"
    lembretes = verificar_lembretes_hoje()
    if lembretes:
        for lembrete in lembretes:
            conteudo += f"- {lembrete['mensagem']} - Processo: {lembrete['processo']}\n"
    else:
        conteudo += "*Nenhum lembrete para hoje*\n\n"
    
    # Salvar relatório
    pasta_relatorios = os.path.expanduser("~/organizacao/controle-prazos/relatorios")
    os.makedirs(pasta_relatorios, exist_ok=True)
    
    nome_arquivo = f"relatorio_{data_hoje.strftime('%Y%m%d')}.md"
    caminho_arquivo = os.path.join(pasta_relatorios, nome_arquivo)
    
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"Relatório diário gerado: {caminho_arquivo}")
    return caminho_arquivo

def verificar_prazos_proximos(dias: int = 7) -> List[Dict]:
    """Verifica prazos que vencem nos próximos dias"""
    prazos = []
    
    # Procurar em todas as pastas de processo
    pastas_base = [
        os.path.expanduser("~/organizacao/advocacia/ativos"),
        os.path.expanduser("~/organizacao/servidor-publico/ativos")
    ]
    
    data_limite = datetime.now() + timedelta(days=dias)
    
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
                                
                                # Comparar data do vencimento com limite
                                try:
                                    data_vencimento = datetime.strptime(lembrete['data_vencimento'], "%Y-%m-%d")
                                    if datetime.now() <= data_vencimento <= data_limite:
                                        prazos.append({
                                            "descricao": lembrete['descricao'],
                                            "data": lembrete['data_vencimento'],
                                            "processo": pasta_nome,
                                            "mensagem": lembrete['mensagem']
                                        })
                                except ValueError:
                                    # Tentar outro formato de data
                                    try:
                                        data_vencimento = datetime.strptime(lembrete['data_vencimento'], "%d/%m/%Y")
                                        if datetime.now() <= data_vencimento <= data_limite:
                                            prazos.append({
                                                "descricao": lembrete['descricao'],
                                                "data": lembrete['data_vencimento'],
                                                "processo": pasta_nome,
                                                "mensagem": lembrete['mensagem']
                                            })
                                    except ValueError:
                                        continue
    
    # Ordenar por data
    prazos.sort(key=lambda x: x['data'])
    return prazos

def verificar_atividades_recentes(dias: int = 1) -> List[Dict]:
    """Verifica atividades recentes nos processos"""
    atividades = []
    
    # Procurar em todas as pastas de processo
    pastas_base = [
        os.path.expanduser("~/organizacao/advocacia/ativos"),
        os.path.expanduser("~/organizacao/servidor-publico/ativos")
    ]
    
    data_limite = datetime.now() - timedelta(days=dias)
    
    for pasta_base in pastas_base:
        if os.path.exists(pasta_base):
            for pasta_nome in os.listdir(pasta_base):
                processo_path = os.path.join(pasta_base, pasta_nome)
                if os.path.isdir(processo_path):
                    # Verificar arquivos modificados recentemente
                    for root, dirs, files in os.walk(processo_path):
                        for file in files:
                            caminho_arquivo = os.path.join(root, file)
                            data_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho_arquivo))
                            
                            if data_modificacao >= data_limite:
                                atividades.append({
                                    "tipo": "Arquivo modificado",
                                    "data": data_modificacao.strftime("%d/%m/%Y %H:%M"),
                                    "descricao": f"{file} em {pasta_nome}",
                                    "caminho": caminho_arquivo
                                })
    
    # Ordenar por data
    atividades.sort(key=lambda x: x['data'], reverse=True)
    return atividades[:10]  # Limitar a 10 atividades

def verificar_lembretes_hoje():
    """Verifica lembretes para o dia atual"""
    # Importar função do sistema de lembretes
    sys.path.append(os.path.dirname(__file__))
    from sistema_lembretes import verificar_lembretes_hoje as verificar
    return verificar()

def gerar_relatorio_semanal():
    """Gera relatório semanal com análise de tendências"""
    print("Gerando relatório semanal...")
    
    data_inicio = datetime.now() - timedelta(days=7)
    data_fim = datetime.now()
    
    data_inicio_fmt = data_inicio.strftime("%d/%m/%Y")
    data_fim_fmt = data_fim.strftime("%d/%m/%Y")
    
    # Conteúdo do relatório
    conteudo = f"# Relatório Semanal - {data_inicio_fmt} a {data_fim_fmt}\n\n"
    conteudo += f"**Período:** {data_inicio_fmt} a {data_fim_fmt}\n"
    conteudo += f"**Gerado em:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
    
    # Análise de prazos
    conteudo += "## Análise de Prazos\n\n"
    prazos_semana = verificar_prazos_proximos(7)
    prazos_vencidos = verificar_prazos_vencidos(7)
    
    conteudo += f"- Prazos vencidos na semana: {len(prazos_vencidos)}\n"
    conteudo += f"- Prazos próximos (até 7 dias): {len(prazos_semana)}\n\n"
    
    if prazos_vencidos:
        conteudo += "### Prazos Vencidos\n"
        for prazo in prazos_vencidos:
            conteudo += f"- {prazo['mensagem']} - Processo: {prazo['processo']}\n"
        conteudo += "\n"
    
    # Atividades da semana
    conteudo += "## Atividades da Semana\n\n"
    atividades_semana = verificar_atividades_recentes(7)
    conteudo += f"- Atividades registradas: {len(atividades_semana)}\n\n"
    
    # Processos mais ativos
    processos_ativos = {}
    for atividade in atividades_semana:
        processo = atividade['descricao'].split(' ')[-1]  # Pegar nome do processo
        if processo in processos_ativos:
            processos_ativos[processo] += 1
        else:
            processos_ativos[processo] = 1
    
    if processos_ativos:
        conteudo += "### Processos Mais Ativos\n"
        for processo, count in sorted(processos_ativos.items(), key=lambda x: x[1], reverse=True)[:5]:
            conteudo += f"- {processo}: {count} atividades\n"
        conteudo += "\n"
    
    # Salvar relatório
    pasta_relatorios = os.path.expanduser("~/organizacao/controle-prazos/relatorios")
    os.makedirs(pasta_relatorios, exist_ok=True)
    
    nome_arquivo = f"relatorio_semanal_{data_inicio.strftime('%Y%m%d')}_{data_fim.strftime('%Y%m%d')}.md"
    caminho_arquivo = os.path.join(pasta_relatorios, nome_arquivo)
    
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"Relatório semanal gerado: {caminho_arquivo}")
    return caminho_arquivo

def verificar_prazos_vencidos(dias_atraso: int = 7) -> List[Dict]:
    """Verifica prazos que venceram nos últimos dias"""
    prazos = []
    
    # Procurar em todas as pastas de processo
    pastas_base = [
        os.path.expanduser("~/organizacao/advocacia/ativos"),
        os.path.expanduser("~/organizacao/servidor-publico/ativos")
    ]
    
    data_limite = datetime.now() - timedelta(days=dias_atraso)
    
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
                                
                                # Comparar data do vencimento com limite
                                try:
                                    data_vencimento = datetime.strptime(lembrete['data_vencimento'], "%Y-%m-%d")
                                    if data_limite <= data_vencimento < datetime.now():
                                        prazos.append({
                                            "descricao": lembrete['descricao'],
                                            "data": lembrete['data_vencimento'],
                                            "processo": pasta_nome,
                                            "mensagem": lembrete['mensagem']
                                        })
                                except ValueError:
                                    # Tentar outro formato de data
                                    try:
                                        data_vencimento = datetime.strptime(lembrete['data_vencimento'], "%d/%m/%Y")
                                        if data_limite <= data_vencimento < datetime.now():
                                            prazos.append({
                                                "descricao": lembrete['descricao'],
                                                "data": lembrete['data_vencimento'],
                                                "processo": pasta_nome,
                                                "mensagem": lembrete['mensagem']
                                            })
                                    except ValueError:
                                        continue
    
    # Ordenar por data
    prazos.sort(key=lambda x: x['data'], reverse=True)
    return prazos

def gerar_relatorio_executivo():
    """Gera relatório executivo com visão geral"""
    print("Gerando relatório executivo...")
    
    data_atual = datetime.now()
    
    # Conteúdo do relatório
    conteudo = f"# Relatório Executivo - Visão Geral\n\n"
    conteudo += f"**Data:** {data_atual.strftime('%d/%m/%Y %H:%M:%S')}\n\n"
    
    # Contadores
    total_processos = contar_processos()
    prazos_hoje = len(verificar_lembretes_hoje())
    prazos_proximos = len(verificar_prazos_proximos(7))
    prazos_vencidos = len(verificar_prazos_vencidos(30))
    
    conteudo += "## Indicadores Gerais\n\n"
    conteudo += f"- Total de processos ativos: {total_processos}\n"
    conteudo += f"- Prazos para hoje: {prazos_hoje}\n"
    conteudo += f"- Prazos nos próximos 7 dias: {prazos_proximos}\n"
    conteudo += f"- Prazos vencidos (últimos 30 dias): {prazos_vencidos}\n\n"
    
    # Alertas
    conteudo += "## Alertas\n\n"
    if prazos_vencidos > 0:
        conteudo += f"⚠️ **{prazos_vencidos} prazos vencidos** - Atenção necessária\n"
    if prazos_hoje > 5:
        conteudo += f"📅 **{prazos_hoje} prazos para hoje** - Dia crítico\n"
    
    if prazos_vencidos == 0 and prazos_hoje <= 5:
        conteudo += "✅ Situação sob controle\n"
    
    conteudo += "\n## Recomendações\n\n"
    if prazos_vencidos > 0:
        conteudo += "- Priorizar regularização de prazos vencidos\n"
    if prazos_hoje > 0:
        conteudo += "- Verificar prazos para hoje\n"
    if prazos_proximos > 10:
        conteudo += "- Planejar agenda para próximos dias\n"
    
    # Salvar relatório
    pasta_relatorios = os.path.expanduser("~/organizacao/controle-prazos/relatorios")
    os.makedirs(pasta_relatorios, exist_ok=True)
    
    nome_arquivo = f"relatorio_executivo_{data_atual.strftime('%Y%m%d_%H%M')}.md"
    caminho_arquivo = os.path.join(pasta_relatorios, nome_arquivo)
    
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"Relatório executivo gerado: {caminho_arquivo}")
    return caminho_arquivo

def contar_processos():
    """Conta o número total de processos ativos"""
    total = 0
    
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
                    total += 1
    
    return total

def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python gerador_relatorios.py diario      # Gera relatório diário")
        print("  python gerador_relatorios.py semanal     # Gera relatório semanal")
        print("  python gerador_relatorios.py executivo   # Gera relatório executivo")
        sys.exit(1)
    
    tipo_relatorio = sys.argv[1]
    
    if tipo_relatorio == "diario":
        gerar_relatorio_diario()
    elif tipo_relatorio == "semanal":
        gerar_relatorio_semanal()
    elif tipo_relatorio == "executivo":
        gerar_relatorio_executivo()
    else:
        print("Tipo de relatório inválido. Use 'diario', 'semanal' ou 'executivo'.")
        sys.exit(1)

if __name__ == "__main__":
    main()