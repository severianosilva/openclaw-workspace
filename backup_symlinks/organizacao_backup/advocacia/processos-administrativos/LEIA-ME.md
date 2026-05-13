# Sistema de Análise de Processo Administrativo

## 🎯 Visão Geral

Sistema completo para gestão e análise de processos administrativos, com integração para pesquisa de jurisprudência, súmulas e geração automatizada de peças processuais.

## 📁 Estrutura de Pastas

```
processos-administrativos/
├── ativos/                    # Processos em andamento
│   └── NUMERO_PROCESSO/
│       ├── controle-processo.md
│       ├── anotacoes.md
│       ├── analise-juridica.md
│       ├── documentos/
│       ├── pecas/
│       ├── decisoes/
│       └── pesquisas/
├── arquivados/                # Processos encerrados
├── modelo-controle/
│   └── modelo-processo-administrativo.md
├── jurisprudencia/            # Pesquisas salvas
├── analise_processo_administrativo.py
├── pesquisador_jurisprudencia.py
└── demo_sistema_administrativo.sh
```

## 🚀 Funcionalidades

### 1. Criação de Processos
- Estrutura automática de pastas
- Modelo de controle preenchido
- Sistema de anotações integrado

### 2. Análise Jurídica
- Pesquisa automática de jurisprudência
- Identificação de súmulas aplicáveis
- Geração de relatório consolidado

### 3. Pesquisa de Jurisprudência
- Integração com múltiplas fontes (STF, STJ, TJ-MG, AGU, TCU, CGU)
- Busca por termos específicos
- Salvamento automático das pesquisas

### 4. Geração de Peças
- Modelos personalizáveis
- Estrutura padronizada
- Armazenamento organizado

## 📖 Como Usar

### Criar Novo Processo

```python
from analise_processo_administrativo import AnalisadorProcessoAdministrativo

analisador = AnalisadorProcessoAdministrativo()

pasta = analisador.criar_processo(
    numero='ADM-2026-001',
    orgao='Secretaria Municipal de Administração',
    assunto='Processo Administrativo Disciplinar',
    interessado='João da Silva'
)
```

### Analisar Processo com Jurisprudência

```python
resultado = analisador.analisar_processo(
    numero='ADM-2026-001',
    fatos='Descrição detalhada dos fatos...',
    questoes_dirito='Questões de direito envolvidas...',
    termos_pesquisa=[
        'processo administrativo disciplinar',
        'ampla defesa',
        'servidor público'
    ]
)

print(f"Jurisprudências: {resultado['jurisprudencia']}")
print(f"Súmulas: {resultado['smulas']}")
```

### Gerar Peça Processual

```python
peca = analisador.gerar_peca(
    numero='ADM-2026-001',
    tipo_peca='Defesa Prévia',
    conteudo_base='''
## Preliminares
...

## Do Mérito
...

## Dos Pedidos
...
'''
)
```

### Listar Processos

```python
processos = analisador.listar_processos(status='todos')
```

## 🔍 Fontes de Pesquisa

### Jurisprudência
- **STF** - Supremo Tribunal Federal
- **STJ** - Superior Tribunal de Justiça
- **TJ-MG** - Tribunal de Justiça de Minas Gerais
- **AGU** - Advocacia-Geral da União
- **TCU** - Tribunal de Contas da União
- **CGU** - Controladoria-Geral da União

### Súmulas
- Súmulas Vinculantes do STF
- Súmulas do STJ
- Súmulas administrativas específicas

## 📊 Modelo de Controle

O modelo de controle inclui:

- ✅ Informações básicas do processo
- ✅ Partes envolvidas
- ✅ Histórico de movimentações
- ✅ Prazos críticos
- ✅ Checklist de documentação
- ✅ Análise jurídica estruturada
- ✅ Estratégia de atuação
- ✅ Peças elaboradas
- ✅ Decisões e recursos

## 🧪 Testar o Sistema

Execute a demonstração:

```bash
cd /home/severosa/organizacao/advocacia/processos-administrativos
bash demo_sistema_administrativo.sh
```

## 🔗 Integrações

### Internet para Pesquisa
O sistema usa o módulo `integracao_internet_pesquisa_juridica.py` para pesquisas online.

Certifique-se de que a integração com internet esteja configurada:

```bash
# Verificar configuração
ls -la /home/severosa/organizacao/controle-prazos/integracao_internet_pesquisa_juridica.py
```

### WhatsApp
Relatórios podem ser enviados via WhatsApp usando a integração do OpenClaw.

## 📝 Exemplo de Uso Completo

```python
from analise_processo_administrativo import AnalisadorProcessoAdministrativo

# 1. Criar processo
analisador = AnalisadorProcessoAdministrativo()

processo = analisador.criar_processo(
    numero='PAD-2026-005',
    orgao='Comissão de Ética',
    assunto='Apuração de conduta irregular',
    interessado='Maria Santos'
)

# 2. Analisar com jurisprudência
analisador.analisar_processo(
    numero='PAD-2026-005',
    fatos='Servidora alegadamente violou código de ética...',
    questoes_dirito='1. Competência da comissão\n2. Prazos\n3. Penalidades',
    termos_pesquisa=['comissão de ética', 'processo disciplinar', 'penalidade']
)

# 3. Gerar peça
analisador.gerar_peca(
    numero='PAD-2026-005',
    tipo_peca='Manifestação',
    conteudo_base='...'
)
```

## ⚙️ Configuração

### Dependências Python
```bash
pip install requests beautifulsoup4
```

### Permissões
```bash
chmod +x demo_sistema_administrativo.sh
chmod +x *.py
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação em `/home/severosa/organizacao/controle-prazos/LEIA-ME.md`
2. Consulte os logs em `/home/severosa/.openclaw/workspace/memory/`
3. Execute `demo_sistema_administrativo.sh` para testar funcionalidades

---

**Última atualização:** Fevereiro/2026
**Versão:** 1.0
**Status:** ✅ Operacional
