#!/bin/bash
# Demonstração do Sistema de Análise de Processo Administrativo

echo "============================================================"
echo "SISTEMA DE ANÁLISE DE PROCESSO ADMINISTRATIVO"
echo "============================================================"
echo ""

# Criar processo de exemplo
echo "📁 1. Criando processo administrativo de exemplo..."
python3 << 'EOF'
from pathlib import Path
import sys
sys.path.insert(0, '/home/severosa/organizacao/advocacia/processos-administrativos')

from analise_processo_administrativo import AnalisadorProcessoAdministrativo

analisador = AnalisadorProcessoAdministrativo()

# Criar processo exemplo
pasta = analisador.criar_processo(
    numero='ADM-2026-001',
    orgao='Secretaria Municipal de Administração',
    assunto='Processo Administrativo Disciplinar - Servidor Público',
    interessado='João da Silva'
)

print(f"\n✅ Processo criado com sucesso!")
EOF

echo ""
echo "🔍 2. Realizando análise jurídica com pesquisa de jurisprudência..."
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/severosa/organizacao/advocacia/processos-administrativos')

from analise_processo_administrativo import AnalisadorProcessoAdministrativo

analisador = AnalisadorProcessoAdministrativo()

# Analisar processo
resultado = analisador.analisar_processo(
    numero='ADM-2026-001',
    fatos='''
O servidor público João da Silva está sendo investigado por suposta infração 
administrativa consistente em abandono de cargo. A administração alega que o 
servidor faltou por mais de 30 dias consecutivos sem justificativa.

O servidor alega que as faltas foram justificadas por motivo de saúde, com 
apresentação de atestados médicos, mas que estes não foram devidamente 
considerados pela administração.
''',
    questoes_dirito='''
1. Legalidade do processo administrativo disciplinar
2. Direito à ampla defesa e ao contraditório
3. Validade dos atestados médicos apresentados
4. Configuração ou não de abandono de cargo
5. Prazos processuais
''',
    termos_pesquisa=['processo administrativo disciplinar', 'abandono de cargo', 'atestado médico', 'servidor público']
)

print(f"\n✅ Análise concluída!")
print(f"   - Jurisprudências encontradas: {resultado['jurisprudencia']}")
print(f"   - Súmulas encontradas: {resultado['smulas']}")
EOF

echo ""
echo "📄 3. Gerando peça de defesa..."
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/severosa/organizacao/advocacia/processos-administrativos')

from analise_processo_administrativo import AnalisadorProcessoAdministrativo

analisador = AnalisadorProcessoAdministrativo()

conteudo_defesa = '''
## Preliminares

1. **Direito à Ampla Defesa** - Assegurado pelo art. 5º, LV, da Constituição Federal
2. **Necessidade de Produção de Provas** - Requer-se a oitiva de testemunhas e juntada de documentos

## Do Mérito

### Das Faltas Alegadas

As faltas apontadas pela administração foram devidamente justificadas por atestados médicos, 
conforme documentação já apresentada nos autos.

### Da Inexistência de Abandono de Cargo

O abandono de cargo requer dolo específico, ou seja, a intenção deliberada de abandonar 
as funções. No caso, as ausências foram motivadas por questões de saúde, devidamente comprovadas.

## Dos Pedidos

Diante do exposto, requer-se:

a) O recebimento da presente defesa;
b) A produção de todas as provas admitidas;
c) Ao final, o arquivamento do processo por inexistência de infração;
d) Subsidiariamente, a aplicação de penalidade branda, caso entendida a responsabilidade.

Nestes termos,
Pede deferimento.

Belo Horizonte, __ de __________ de 2026.

_________________________________
Advogado
OAB/MG _______
'''

peca = analisador.gerar_peca(
    numero='ADM-2026-001',
    tipo_peca='Defesa Prévia',
    conteudo_base=conteudo_defesa
)

print(f"\n✅ Defesa gerada com sucesso!")
EOF

echo ""
echo "📋 4. Listando processos ativos..."
python3 << 'EOF'
import sys
sys.path.insert(0, '/home/severosa/organizacao/advocacia/processos-administrativos')

from analise_processo_administrativo import AnalisadorProcessoAdministrativo

analisador = AnalisadorProcessoAdministrativo()
analisador.listar_processos()
EOF

echo ""
echo "============================================================"
echo "DEMONSTRAÇÃO CONCLUÍDA!"
echo "============================================================"
echo ""
echo "📂 Localização dos arquivos:"
echo "   Processos: /home/severosa/organizacao/advocacia/processos-administrativos/ativos/"
echo ""
echo "📚 Documentação:"
echo "   - LEIA-ME.md (guia completo de uso)"
echo "   - Modelo de controle: modelo-controle/modelo-processo-administrativo.md"
echo ""
echo "🔧 Scripts disponíveis:"
echo "   - analise_processo_administrativo.py (sistema principal)"
echo "   - pesquisador_jurisprudencia.py (pesquisa de jurisprudência)"
echo "   - demo_sistema_administrativo.sh (esta demonstração)"
echo ""
echo "============================================================"
