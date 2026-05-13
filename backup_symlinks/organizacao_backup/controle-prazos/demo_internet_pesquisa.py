#!/usr/bin/env python3
"""
Demonstração da integração com internet para pesquisa jurídica
"""

import os
import sys
import json
from datetime import datetime

# Adicionar o diretório de controle de processos ao path
sys.path.append('/home/severosa/organizacao/controle-prazos')

from integracao_internet_pesquisa_juridica import integracao_pesquisa_juridica_completa

def demo_internet_pesquisa():
    """
    Demonstra as funcionalidades de integração com internet para pesquisa jurídica
    """
    print("==========================================")
    print("DEMONSTRAÇÃO: INTEGRAÇÃO COM INTERNET PARA PESQUISA JURÍDICA")
    print("==========================================")
    print("")
    
    print("Esta demonstração mostra como o sistema se conecta à internet")
    print("para realizar pesquisas jurídicas avançadas, consultando")
    print("jurisprudência, legislação e precedentes em tempo real.")
    print("")
    
    print("FUNCIONALIDADES DISPONÍVEIS:")
    print("============================")
    print("")
    print("1. PESQUISA DE JURISPRUDÊNCIA")
    print("   - Busca em tribunais superiores (STF, STJ)")
    print("   - Consulta a bases de dados jurídicas (Jusbrasil, LexML)")
    print("   - Filtragem por área do direito e tipo de processo")
    print("")
    print("2. CONSULTA A LEGISLAÇÃO ATUALIZADA")
    print("   - Acesso a leis, decretos e regulamentos")
    print("   - Verificação de vigência e alterações recentes")
    print("   - Integração com Planalto e sistemas legislativos")
    print("")
    print("3. BUSCA DE PRECEDENTES SIMILARES")
    print("   - Análise de documentos para encontrar casos semelhantes")
    print("   - Comparação com decisões anteriores")
    print("   - Identificação de padrões jurisprudenciais")
    print("")
    print("4. VERIFICAÇÃO DE ATUALIZAÇÕES LEGISLATIVAS")
    print("   - Monitoramento de novas leis e regulamentos")
    print("   - Alertas sobre mudanças que afetam processos")
    print("   - Integração com Congresso Nacional e Presidência")
    print("")
    
    print("TESTANDO INTEGRAÇÃO:")
    print("===================")
    print("")
    
    # Testar com um termo jurídico comum
    termo_teste = "danos morais"
    print(f"1. Pesquisando jurisprudência para: '{termo_teste}'")
    
    try:
        resultado_teste = integracao_pesquisa_juridica_completa(
            texto_documento=f"Documento sobre {termo_teste} e responsabilidade civil",
            termo_pesquisa=termo_teste
        )
        
        print(f"   ✓ Resultados obtidos:")
        print(f"     - Jurisprudência encontrada: {len(resultado_teste['pesquisa_jurisprudencia'])}")
        print(f"     - Precedentes similares: {len(resultado_teste['precedentes_similares'])}")
        print(f"     - Atualizações legislativas: {resultado_teste['atualizacoes_legislativas']['atualizacoes_encontradas']}")
        
        if resultado_teste['pesquisa_jurisprudencia']:
            print(f"     - Primeiro resultado: {resultado_teste['pesquisa_jurisprudencia'][0]['titulo'][:100]}...")
        
    except Exception as e:
        print(f"   ✗ Erro no teste: {str(e)}")
    
    print("")
    print("CONFIGURAÇÃO DA API:")
    print("===================")
    print("")
    
    # Verificar se a API da Brave Search está configurada
    chave_api = os.getenv('BRAVE_SEARCH_API_KEY')
    if chave_api:
        print("✓ API da Brave Search configurada")
        print("  - Permite pesquisas avançadas com maior precisão")
        print("  - Acesso a resultados mais relevantes e atualizados")
        print("  - Menos limitações de rate limiting")
    else:
        print("! API da Brave Search não configurada")
        print("  - O sistema usará métodos alternativos de pesquisa")
        print("  - Para configurar: obtenha uma chave gratuita em https://brave.com/search/api/")
        print("  - Execute: ~/organizacao/controle-prazos/configurar_internet_pesquisa.sh")
    
    print("")
    print("USO NA AUTOMAÇÃO JURÍDICA:")
    print("=========================")
    print("")
    print("A integração com internet é automaticamente utilizada por:")
    print("- Sistema de análise jurídica automatizada")
    print("- Gerador de precedentes e similaridades")
    print("- Sistema de conformidade regulatória")
    print("- Análise preditiva de riscos")
    print("- Consultas a tribunais e órgãos reguladores")
    print("")
    
    print("EXEMPLOS DE COMANDOS:")
    print("====================")
    print("# Pesquisa específica")
    print("python3 ~/organizacao/controle-prazos/integracao_internet_pesquisa_juridica.py 'recurso especial'")
    print("")
    print("# Teste completo")
    print("python3 ~/organizacao/controle-prazos/integracao_internet_pesquisa_juridica.py --teste")
    print("")
    print("# Com texto de documento")
    print("python3 ~/organizacao/controle-prazos/integracao_internet_pesquisa_juridica.py 'habeas corpus' 'documento com informações sobre processo'")
    print("")
    
    print("==========================================")
    print("FIM DA DEMONSTRAÇÃO")
    print("==========================================")

if __name__ == "__main__":
    demo_internet_pesquisa()