#!/usr/bin/env python3
"""
Sistema de Análise de Processo Administrativo
Integra análise jurídica, pesquisa de jurisprudência e geração de peças
"""

import os
import sys
import shutil
from datetime import datetime, timedelta
from pathlib import Path

# Adicionar paths
sys.path.insert(0, '/home/severosa/organizacao/controle-prazos')
sys.path.insert(0, '/home/severosa/organizacao/advocacia/processos-administrativos')

class AnalisadorProcessoAdministrativo:
    """Sistema completo de análise de processo administrativo"""
    
    def __init__(self):
        self.base_advocacia = Path('/home/severosa/organizacao/advocacia/processos-administrativos')
        self.base_ativos = self.base_advocacia / 'ativos'
        self.base_arquivados = self.base_advocacia / 'arquivados'
        
        # Garantir existência das pastas
        self.base_ativos.mkdir(parents=True, exist_ok=True)
        self.base_arquivados.mkdir(parents=True, exist_ok=True)
        
        # Importar pesquisador de jurisprudência
        from pesquisador_jurisprudencia import PesquisadorJurisprudencia
        self.pesquisador = PesquisadorJurisprudencia()
    
    def criar_processo(self, numero, orgao, assunto, interessado):
        """
        Criar novo processo administrativo
        
        Args:
            numero: Número do processo
            orgao: Órgão/Entidade
            assunto: Assunto do processo
            interessado: Nome do interessado
        """
        print(f"\n📁 Criando processo administrativo: {numero}")
        
        # Criar pasta do processo
        pasta_processo = self.base_ativos / numero
        pasta_processo.mkdir(parents=True, exist_ok=True)
        
        # Criar subpastas
        (pasta_processo / 'documentos').mkdir(exist_ok=True)
        (pasta_processo / 'pecas').mkdir(exist_ok=True)
        (pasta_processo / 'decisoes').mkdir(exist_ok=True)
        (pasta_processo / 'pesquisas').mkdir(exist_ok=True)
        
        # Copiar modelo de controle
        modelo = self.base_advocacia / 'modelo-controle' / 'modelo-processo-administrativo.md'
        controle = pasta_processo / 'controle-processo.md'
        
        if modelo.exists():
            shutil.copy(modelo, controle)
            
            # Atualizar informações básicas
            with open(controle, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            conteudo = conteudo.replace('**Número do Processo:** ', f'**Número do Processo:** {numero}\n')
            conteudo = conteudo.replace('**Órgão/Entidade:** ', f'**Órgão/Entidade:** {orgao}\n')
            conteudo = conteudo.replace('**Assunto:** ', f'**Assunto:** {assunto}\n')
            conteudo = conteudo.replace('**Interessado:** ', f'**Interessado:** {interessado}\n')
            conteudo = conteudo.replace('**Data de Abertura:** ', f'**Data de Abertura:** {datetime.now().strftime("%d/%m/%Y")}\n')
            
            with open(controle, 'w', encoding='utf-8') as f:
                f.write(conteudo)
        
        # Criar arquivo de anotações
        anotacoes = pasta_processo / 'anotacoes.md'
        with open(anotacoes, 'w', encoding='utf-8') as f:
            f.write(f"# Anotações - Processo {numero}\n\n")
            f.write(f"**Órgão:** {orgao}\n")
            f.write(f"**Assunto:** {assunto}\n\n")
            f.write("---\n\n")
        
        print(f"✅ Processo criado em: {pasta_processo}")
        print(f"📄 Controle: {controle}")
        
        return pasta_processo
    
    def analisar_processo(self, numero, fatos, questoes_dirito, termos_pesquisa):
        """
        Analisar processo administrativo com pesquisa de jurisprudência
        
        Args:
            numero: Número do processo
            fatos: Descrição dos fatos
            questoes_dirito: Questões de direito envolvidas
            termos_pesquisa: Termos para pesquisa de jurisprudência
        """
        print(f"\n⚖️  Analisando processo: {numero}")
        
        pasta_processo = self.base_ativos / numero
        
        if not pasta_processo.exists():
            print(f"❌ Processo não encontrado: {numero}")
            return None
        
        # 1. Pesquisa de jurisprudência
        print("\n🔍 Realizando pesquisa de jurisprudência...")
        jurisprudencia = self.pesquisador.pesquisar_jurisprudencia(
            termos_pesquisa, 
            orgao='todos', 
            limite=10
        )
        
        # 2. Pesquisa de súmulas
        print("\n📚 Pesquisando súmulas aplicáveis...")
        smulas = self.pesquisador.pesquisar_smulas(questoes_dirito)
        
        # 3. Gerar relatório de pesquisa
        relatorio = self.pesquisador.gerar_relatorio_pesquisa(
            numero, 
            termos_pesquisa, 
            jurisprudencia, 
            smulas
        )
        
        # 4. Criar análise jurídica consolidada
        analise = pasta_processo / 'analise-juridica.md'
        
        conteudo = f"""# Análise Jurídica - Processo {numero}

**Data da Análise:** {datetime.now().strftime('%d/%m/%Y %H:%M')}

---

## 1. Resumo dos Fatos

{fatos}

---

## 2. Questões de Direito

{questoes_dirito}

---

## 3. Jurisprudência Aplicável

"""
        
        if jurisprudencia:
            for i, resultado in enumerate(jurisprudencia, 1):
                conteudo += f"\n### {i}. {resultado.get('titulo', 'Sem título')}\n"
                conteudo += f"- **Órgão:** {resultado.get('orgao', 'Não informado')}\n"
                conteudo += f"- **Data:** {resultado.get('data', 'Não informada')}\n"
                conteudo += f"\n**Ementa:**\n{resultado.get('ementa', 'Não informada')}\n"
        else:
            conteudo += "*Pesquisa de jurisprudência em andamento*\n"
        
        conteudo += f"\n---\n\n## 4. Súmulas Aplicáveis\n\n"
        
        if smulas:
            for smula in smulas:
                conteudo += f"\n### {smula['numero']} ({smula['orgao']})\n"
                conteudo += f"{smula['ementa']}\n"
        else:
            conteudo += "*Nenhuma súmula identificada*\n"
        
        conteudo += f"""
---

## 5. Estratégia Recomendada

<!-- Inserir estratégia baseada na análise -->

## 6. Peças Necessárias

- [ ] Manifestação/Defesa
- [ ] Requerimento de Diligência
- [ ] Recurso Administrativo
- [ ] Outras: _______________

## 7. Prazos a Observar

<!-- Inserir prazos críticos -->

---

*Análise realizada em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*
"""
        
        with open(analise, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        
        print(f"\n✅ Análise jurídica gerada: {analise}")
        print(f"📄 Relatório de pesquisa: {relatorio}")
        
        return {
            'pasta': pasta_processo,
            'analise': analise,
            'relatorio': relatorio,
            'jurisprudencia': len(jurisprudencia),
            'smulas': len(smulas)
        }
    
    def gerar_peca(self, numero, tipo_peca, conteudo_base):
        """
        Gerar peça processual
        
        Args:
            numero: Número do processo
            tipo_peca: Tipo da peça (defesa, recurso, manifestação, etc.)
            conteudo_base: Conteúdo base da peça
        """
        pasta_processo = self.base_ativos / numero
        
        if not pasta_processo.exists():
            print(f"❌ Processo não encontrado: {numero}")
            return None
        
        pasta_pecas = pasta_processo / 'pecas'
        pasta_pecas.mkdir(exist_ok=True)
        
        nome_arquivo = f"{tipo_peca.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        arquivo_peca = pasta_pecas / nome_arquivo
        
        with open(arquivo_peca, 'w', encoding='utf-8') as f:
            f.write(f"# {tipo_peca}\n\n")
            f.write(f"**Processo:** {numero}\n")
            f.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y')}\n\n")
            f.write("---\n\n")
            f.write(conteudo_base)
        
        print(f"\n✅ Peça gerada: {arquivo_peca}")
        return arquivo_peca
    
    def listar_processos(self, status='todos'):
        """Listar processos administrativos"""
        print("\n📋 Processos Administrativos")
        print("="*60)
        
        if not self.base_ativos.exists():
            print("Nenhum processo encontrado")
            return []
        
        processos = []
        for pasta in self.base_ativos.iterdir():
            if pasta.is_dir():
                controle = pasta / 'controle-processo.md'
                if controle.exists():
                    processos.append({
                        'numero': pasta.name,
                        'pasta': pasta,
                        'status': 'Ativo'
                    })
        
        if processos:
            for i, proc in enumerate(processos, 1):
                print(f"\n{i}. {proc['numero']}")
                print(f"   Pasta: {proc['pasta']}")
                print(f"   Status: {proc['status']}")
        else:
            print("Nenhum processo ativo encontrado")
        
        return processos


def main():
    """Função principal para teste"""
    analisador = AnalisadorProcessoAdministrativo()
    
    print("="*60)
    print("SISTEMA DE ANÁLISE DE PROCESSO ADMINISTRATIVO")
    print("="*60)
    
    # Listar processos existentes
    analisador.listar_processos()
    
    print("\n" + "="*60)
    print("Sistema pronto para uso!")
    print("="*60)
    print("\nComandos disponíveis:")
    print("  1. Criar processo: analisador.criar_processo(numero, orgao, assunto, interessado)")
    print("  2. Analisar processo: analisador.analisar_processo(numero, fatos, questoes_dirito, termos_pesquisa)")
    print("  3. Gerar peça: analisador.gerar_peca(numero, tipo_peca, conteudo)")
    print("  4. Listar processos: analisador.listar_processos()")
    print("="*60)


if __name__ == '__main__':
    main()
