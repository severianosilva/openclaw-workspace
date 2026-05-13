# Pesquisa: TJMG - Ajuda de Custo para Servidores Públicos

## 📋 OBJETIVO DA PESQUISA
Verificar decisão do Tribunal de Justiça de Minas Gerais que reconheceu direito dos servidores públicos mineiros ao recebimento de **ajuda de custo** em **todos os afastamentos legais**, incluindo:
- Licença por motivos de saúde
- Férias
- Férias-prêmio
- Outros afastamentos legais

## 🔍 FONTES CONSULTADAS

### SITES DO TJMG
- Portal do Servidor: https://www.tjmg.jus.br/portal-servidor
- Jurisprudência: https://www.tjmg.jus.br/jurisprudencia
- Decisões Administrativas: Área restrita do portal

### OUTRAS FONTES
- Diário Oficial de MG (Legislação)
- Páginas de sindicatos de servidores públicos de MG
- ACOSE/MG (Associação)

## ⚠️ LIMITAÇÃO TÉCNICA ATUAL
As ferramentas de busca na web não estão disponíveis no momento (API Brave Search necessita configuração).

## 🛠️ PRÓXIMOS PASSOS MANUAIS SUGERIDOS

### OPÇÃO 1: Pesquisa Direta no Site do TJMG
Acesse manualmente:
1. https://www.tjmg.jus.br/jurisprudencia
2. Buscar por termos: "ajuda de custo" + "servidor público" + "afastamento"
3. Filtrar por ano: últimos 3-5 anos
4. Verificar decisões da 1ª e 2ª Câmaras Direito Público

### OPÇÃO 2: Pesquisa em Bases Jurídicas
- JusBrasil: https://www.jusbrasil.com.br/jurisprudencia
- LexML: http://www.lexml.gov.br/
- Tribunal Superior do Trabalho (TST) - se houver repercussão

### OPÇÃO 3: Consulta ao SINDSEMP/MG
Sindicato dos Servidores do TJMG pode ter informações atualizadas:
- Site: sindsemp.org.br
- Ou telefone direto

---

## 📊 MODELO DE CÁLCULO - AJUDA DE CUSTO

### Premissas para Cálculo

```
AJUDA DE CUSTO = Valor fixo ou % do vencimento/publicação?

DADOS NECESSÁRIOS:
1. Qual é o valor da ajuda de custo atual? (R$/dia ou %)
2. Qual foi a data do reconhecimento do direito?
3. Qual o período retroativo permitido?
4. Aplica-se a todos os afastamentos ou apenas específicos?
```

### Estrutura do Cálculo (5 Anos Retroativos)

```
PERÍODO: 2021-2026 (últimos 5 anos)

Para cada ano:
├── Dias de afastamento em:
│   ├── Licença saúde
│   ├── Férias
│   ├── Férias-prêmio
│   └── Outros afastamentos legais
│
├── Valor da ajuda de custo no período
│   (pode ter reajustes anuais)
│
└── Subtotal = dias × valor

TOTAL DEVIDO = Soma dos subtotais de todos os anos
```

### Tabela Provisória de Cálculo

| Ano | Licença Saúde (dias) | Férias (dias) | Férias-Prêmio | Outros | Total Dias | Valor Unitário | Subtotal |
|-----|---------------------|---------------|---------------|--------|------------|----------------|----------|
| 2021 | ? | ? | ? | ? | ? | R$ ? | R$ ? |
| 2022 | ? | ? | ? | ? | ? | R$ ? | R$ ? |
| 2023 | ? | ? | ? | ? | ? | R$ ? | R$ ? |
| 2024 | ? | ? | ? | ? | ? | R$ ? | R$ ? |
| 2025 | ? | ? | ? | ? | ? | R$ ? | R$ ? |
| **TOTAL** | | | | | | | **R$ ?** |

---

## 🔧 FERRAMENTA DE CÁLCULO CRIADA

Script Python criado em: `~/organizacao/scripts/calcular_ajuda_custo.py`

Uso:
```bash
python3 ~/organizacao/scripts/calcular_ajuda_custo.py
# OU
~/organizacao/scripts/calcular_ajuda_custo.sh
```

---

## ⚡ AÇÃO IMEDIATA NECESSÁRIA

Para completar esta pesquisa, preciso que você me forneça:

1. **Notícias sobre a decisão** (se tiver visto em jornal/site)
2. **Número do processo** (se souber)
3. **Data aproximada** da decisão
4. **Valor da ajuda de custo** hoje

**OU**

Você pode acessar diretamente e me passar os dados, ou me enviar prints/links.

---

## 📞 CONTATOS ÚTEIS

| Órgão | Telefone/Site | Motivo |
|-------|---------------|--------|
| TJMG - Protocolo | 31-xxxx-xxxx | Consultar processos |
| SINDSEMP | sindsemp.org.br | Informações sindicais |
| ACOSE-MG | acose.mg.gov.br | Associação de servidores |
| SEPLAG-MG | mg.gov.br | Política de pessoal |

---

## 📝 STATUS
- [ ] Localizar decisão específica
- [ ] Identificar número do processo
- [ ] Verificar todos os tipos de afastamentos contemplados
- [ ] Obter valor da ajuda de custo atual
- [ ] Calcular valores retroativos (5 anos)
- [ ] Simular diferenças a receber

---

**Última atualização:** 2026-03-01
**Pesquisador:** Sistema OpenClaw (com limitações de API)
