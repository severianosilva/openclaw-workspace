#!/usr/bin/env python3
"""
Sistema de Pesquisa de Jurisprudência e Súmulas Administrativas
Integração com fontes externas para pesquisa jurídica
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Adicionar pasta de controle-prazos ao path para importar módulos
sys.path.insert(0, '/home/severosa/organizacao/controle-prazos')

class PesquisadorJurisprudencia:
    """Classe para pesquisa de jurisprudência e súmulas"""
    
    def __init__(self):
        self.base_dados = Path('/home/severosa/organizacao/advocacia/processos-administrativos/jurisprudencia')
        self.base_dados.mkdir(parents=True, exist_ok=True)
        
        # Fontes de pesquisa disponíveis
        self.fontes = {
            'stf': 'https://portal.stf.jus.br/jurisprudencia/',
            'stj': 'https://scon.stj.jus.br/SCON/',
            'tju-mg': 'https://www.tjmg.jus.br/',
            'agu': 'https://www.gov.br/agu/pt-br',
            'tcu': 'https://portal.tcu.gov.br/',
            'cgf': 'https://www.gov.br/cgu/pt-br'
        }
    
    def pesquisar_jurisprudencia(self, termos, orgao='todos', limite=10):
        """
        Pesquisar jurisprudência por termos
        
        Args:
            termos: Lista de termos para pesquisa
            orgao: Órgão específico (stf, stj, tju-mg, etc.) ou 'todos'
            limite: Número máximo de resultados
        
        Returns:
            Lista de resultados da pesquisa
        """
        print(f"\n🔍 Pesquisando jurisprudência...")
        print(f"Termos: {', '.join(termos)}")
        print(f"Órgão: {orgao}")
        
        resultados = []
        
        # Se tiver integração com internet, usar web_search
        try:
            from integracao_internet_pesquisa_juridica import PesquisadorJuridico
            pesquisador = PesquisadorJuridico()
            
            query = ' '.join(termos)
            if orgao != 'todos':
                query = f"{query} site:{self.fontes.get(orgao, '')}"
            
            resultados = pesquisador.pesquisar(query, limite=limite)
            
        except ImportError:
            print("⚠️  Integração com internet não disponível")
            print("📝 Pesquisa manual necessária nas fontes:")
            for fonte, url in self.fontes.items():
                if orgao == 'todos' or fonte == orgao:
                    print(f"  - {fonte.upper()}: {url}")
        
        return resultados
    
    def pesquisar_smulas(self, tema, orgao='todos'):
        """
        Pesquisar súmulas por tema
        
        Args:
            tema: Tema da súmula
            orgao: Órgão específico ou 'todos'
        
        Returns:
            Lista de súmulas encontradas
        """
        print(f"\n📚 Pesquisando súmulas sobre: {tema}")
        
        smulas = []
        
        # Súmulas vinculantes do STF
        smulas_vinculantes = {
            '5': 'Necessidade de defesa técnica em processo administrativo disciplinar',
            '14': 'Direito de acesso a informações no processo administrativo',
            '17': 'Proibição de nepotismo na administração pública',
            '21': 'Exigência de concurso público para investidura em cargo público',
            '24': 'Inconstitucionalidade de lei que trata de matéria reservada a lei complementar',
            '35': 'Direito à motivação das decisões administrativas',
        }
        
        # Súmulas do STJ sobre direito administrativo
        smulas_stj = {
            '13': 'A administração pública pode declarar a nulidade de seus próprios atos',
            '18': 'É vedada a majoração de tributo, em lei posterior à ocorrência do fato imponível',
            '43': 'Prescrição no processo administrativo disciplinar',
            '67': 'Ação disciplinar contra servidor público',
        }
        
        # Filtrar por tema (busca simples por palavras-chave)
        termos_tema = tema.lower().split()
        
        for num, ementa in smulas_vinculantes.items():
            if any(termo in ementa.lower() for termo in termos_tema):
                smulas.append({
                    'numero': f'SV {num}',
                    'orgao': 'STF',
                    'ementa': ementa,
                    'tipo': 'Vinculante'
                })
        
        for num, ementa in smulas_stj.items():
            if any(termo in ementa.lower() for termo in termos_tema):
                smulas.append({
                    'numero': f'Súmula {num}',
                    'orgao': 'STJ',
                    'ementa': ementa,
                    'tipo': 'STJ'
                })
        
        if smulas:
            print(f"\n✅ {len(smulas)} súmula(s) encontrada(s):")
            for smula in smulas:
                print(f"\n  {smula['numero']} ({smula['orgao']}):")
                print(f"  {smula['ementa']}")
        else:
            print("⚠️  Nenhuma súmula encontrada com os termos informados")
        
        return smulas
    
    def salvar_pesquisa(self, termos, resultados, tipo='jurisprudencia'):
        """Salvar resultados da pesquisa para consulta futura"""
        arquivo = self.base_dados / f"pesquisa_{tipo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        dados = {
            'data': datetime.now().isoformat(),
            'termos': termos,
            'tipo': tipo,
            'resultados': resultados
        }
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Pesquisa salva em: {arquivo}")
        return arquivo
    
    def gerar_relatorio_pesquisa(self, processo_numero, termos, jurisprudencia, smulas):
        """Gerar relatório de pesquisa para anexar ao processo"""
        pasta_processo = Path(f'/home/severosa/organizacao/advocacia/processos-administrativos/ativos/{processo_numero}')
        pasta_processo.mkdir(parents=True, exist_ok=True)
        
        relatorio = pasta_processo / 'pesquisa-jurisprudencial.md'
        
        conteudo = f"""# Pesquisa Jurisprudencial

**Processo:** {processo_numero}
**Data da Pesquisa:** {datetime.now().strftime('%d/%m/%Y %H:%M')}
**Termos Pesquisados:** {', '.join(termos)}

---

## Jurisprudência Encontrada

"""
        
        if jurisprudencia:
            for i, resultado in enumerate(jurisprudencia, 1):
                conteudo += f"\n### {i}. {resultado.get('titulo', 'Sem título')}\n"
                conteudo += f"- **Órgão:** {resultado.get('orgao', 'Não informado')}\n"
                conteudo += f"- **Data:** {resultado.get('data', 'Não informada')}\n"
                conteudo += f"- **Relator:** {resultado.get('relator', 'Não informado')}\n"
                conteudo += f"\n**Ementa:**\n{resultado.get('ementa', 'Não informada')}\n"
                
                if resultado.get('url'):
                    conteudo += f"\n**Link:** {resultado['url']}\n"
        else:
            conteudo += "*Nenhuma jurisprudência encontrada*\n"
        
        conteudo += "\n---\n\n## Súmulas Aplicáveis\n\n"
        
        if smulas:
            for smula in smulas:
                conteudo += f"\n### {smula['numero']} ({smula['orgao']})\n"
                conteudo += f"**Tipo:** {smula['tipo']}\n\n"
                conteudo += f"{smula['ementa']}\n"
        else:
            conteudo += "*Nenhuma súmula encontrada*\n"
        
        conteudo += f"\n---\n\n*Pesquisa realizada em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*\n"
        
        with open(relatorio, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        
        print(f"\n📄 Relatório gerado: {relatorio}")
        return relatorio


def main():
    """Função principal para teste"""
    pesquisador = PesquisadorJurisprudencia()
    
    print("="*60)
    print("SISTEMA DE PESQUISA DE JURISPRUDÊNCIA E SÚMULAS")
    print("="*60)
    
    # Exemplo de pesquisa
    termos = ['processo administrativo', 'defesa', 'prazo']
    jurisprudencia = pesquisador.pesquisar_jurisprudencia(termos, orgao='todos', limite=5)
    
    smulas = pesquisador.pesquisar_smulas('processo administrativo disciplinar')
    
    # Salvar pesquisa
    if jurisprudencia or smulas:
        pesquisador.salvar_pesquisa(termos, {
            'jurisprudencia': jurisprudencia,
            'smulas': smulas
        })
    
    print("\n" + "="*60)
    print("Pesquisa concluída!")
    print("="*60)


if __name__ == '__main__':
    main()
