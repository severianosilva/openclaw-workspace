# Exemplo de Uso do Sistema de Anotações (Notebook LN)

Este documento demonstra como utilizar o sistema de anotações integrado ao nosso sistema de controle e análise processual.

## Criação de Processo com Anotações

Ao criar um novo processo, o sistema automaticamente:

1. Cria a estrutura de pastas:
   - documentos/
   - andamentos/
   - anotacoes/

2. Adiciona modelos de anotações:
   - analise_inicial.md
   - estrategia_defesa.md
   - notas_pesquisa_juridica.md
   - rascunhos_peca.md

## Adicionando Anotações Específicas

Para adicionar uma anotação específica a um processo existente:

```bash
./criar_anotacao_processo.sh "/home/severosa/organizacao/advocacia/ativos/Nome do Processo" "tipo_de_anotacao"
```

Tipos disponíveis:
- analise_inicial
- estrategia_defesa
- notas_pesquisa_juridica
- rascunhos_peca
- personalizado "nome_arquivo"

## Busca de Informações

Para buscar termos específicos nas anotações:

```bash
./buscar_anotacoes.sh "termo_pesquisado"
```

O sistema retornará todos os arquivos que contenham o termo pesquisado, mostrando o contexto em torno do termo.

## Exemplo Prático

Suponha que você deseje adicionar uma anotação sobre aspectos constitucionais de um caso:

```bash
./criar_anotacao_processo.sh "/home/severosa/organizacao/advocacia/ativos/Caso Exemplo 001" "personalizado" "analise_constitucional"
```

Depois, ao trabalhar em outro caso semelhante, você pode buscar por anotações anteriores sobre temas constitucionais:

```bash
./buscar_anotacoes.sh "constitucional"
```

## Integração com Análise Processual

O sistema de anotações se integra perfeitamente com a análise processual:

1. Anotações de pesquisa jurídica alimentam a estratégia de defesa
2. Rascunhos de peças podem se referenciar a análises anteriores
3. Buscas permitem reaproveitar conteúdo e estratégias de casos anteriores

## Benefícios do Sistema

- Centralização de conhecimento jurídico
- Reutilização de análises e estratégias
- Histórico de raciocínio jurídico
- Apoio à tomada de decisão
- Facilitação na redação de peças processuais