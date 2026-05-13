# Sistema de Controle de Prazos e Processos

Este diretório contém os scripts e modelos para controle de prazos e processos jurídicos.

## Scripts Disponíveis

- `criar_registro_processo.sh` - Script para criar um novo registro de processo
- `criar_anotacao_processo.sh` - Script para adicionar anotações a um processo existente
- `buscar_anotacoes.sh` - Script para buscar termos nas anotações de processos
- `ocr_analise_juridica.py` - Script para OCR e análise jurídica automatizada de documentos
- `sistema_lembretes.py` - Sistema de lembretes processuais baseados em prazos identificados
- `classificador_documentos.py` - Sistema de classificação automática de documentos jurídicos
- `sistema_precedentes.py` - Sistema de precedentes jurídicos para consulta e análise
- `gerador_relatorios.py` - Sistema de geração automatizada de relatórios jurídicos
- `enviar_relatorios_email.py` - Sistema de envio automático de relatórios por e-mail e WhatsApp
- `extrator_partes.py` - Sistema de extração automatizada de partes envolvidas em processos
- `sistema_conformidade.py` - Sistema de conformidade regulatória para verificação de normas
- `analise_preditiva.py` - Sistema de análise preditiva de riscos jurídicos
- `integracao_tribunal.py` - Sistema de integração com sistemas de tribunal para consulta de processos
- `integracao_google_drive_analise.py` - Script para integração com Google Drive para análise de documentos
- `integracao_internet_pesquisa_juridica.py` - Script para integração com internet para pesquisa jurídica
- `configurar_internet_pesquisa.sh` - Script de configuração para integração com internet
- `configurar_email.sh` - Script de configuração para envio de e-mails
- `modelo-controle-processos.md` - Modelo de arquivo de controle de processo
- `otimizador_tokens.py` - Sistema de otimização de uso de tokens para IA
- `integracao_discord.py` - Sistema de integração com Discord para comunicação
- `configurar_discord.sh` - Script de configuração para integração com Discord
- `integracao_agentmail.md` - Documentação para integração com AgentMail
- `demo_internet_pesquisa.py` - Demonstração da funcionalidade de internet para pesquisa jurídica
- `refly_skills_integration_plan.md` - Plano de integração do Refly com o sistema jurídico
- `examples/refly_juridical_ocr_skill.md` - Exemplo de skill do Refly para OCR jurídico
- `demo_refly_integration.py` - Demonstração de integração com Refly
- `configurar_refly.sh` - Script de configuração para instalação do Refly
- `implementar_primeiras_skills_refly.py` - Script para implementação das primeiras skills do Refly
- `demo_funcionamento_refly.py` - Demonstração de funcionamento das skills do Refly
- `refly-skills/` - Diretório com as skills do Refly implementadas

## Estrutura de Anotações

Cada processo agora inclui uma pasta `anotacoes` com modelos para:

- Análise inicial
- Estratégia de defesa/ataque
- Notas de pesquisa jurídica
- Rascunhos de peças processuais

## Sistema de Análise Jurídica Automatizada

### Estratégia de OCR
- 1ª tentativa: Tesseract OCR (gratuito e local)
- 2ª tentativa: Qwen-VL OCR (via API, já integrado ao sistema)
- Análise jurídica automatizada do conteúdo extraído

### Componentes
- OCR especializado em documentos jurídicos
- Análise jurídica automatizada
- Identificação de prazos, pontos críticos e partes envolvidas
- Geração de anotações detalhadas
- Integração com Google Drive
- Sistema de lembretes processuais
- Classificação automática de documentos
- Otimização de tokens para redução de custos
- Integração com internet para pesquisa jurídica
- Integração com Refly para padronização de skills

## Sistema de Lembretes Processuais

O sistema de lembretes cria automaticamente alertas baseados nos prazos identificados durante a análise jurídica. Os lembretes são criados com antecedência para garantir que nenhum prazo importante seja perdido.

### Uso do sistema de lembretes
```bash
python3 sistema_lembretes.py criar "arquivo_analise.json" "/caminho/pasta/processo"
python3 sistema_lembretes.py verificar  # Verifica lembretes para hoje
```

## Sistema de Classificação Automática de Documentos

O classificador automático identifica o tipo de documento jurídico (petição, sentença, despacho, etc.) e organiza automaticamente na pasta apropriada.

### Uso do classificador
```bash
python3 classificador_documentos.py "caminho/documento.txt" "/caminho/pasta/processo"
```

## Otimização de Tokens

O sistema inclui um otimizador de tokens que:

- Cria cache de análises para evitar reprocessamento
- Extrai entidades antes de chamar IA
- Gera resumos inteligentes de documentos longos
- Processa por partes em vez de todo o conteúdo de uma vez
- Reduz significativamente o consumo de tokens

## Integração com Internet para Pesquisa Jurídica

O sistema inclui integração com internet para:

- Pesquisa de jurisprudência em tribunais superiores
- Consulta a bases de dados jurídicas (STF, STJ, Jusbrasil, LexML)
- Verificação de atualizações legislativas
- Busca de precedentes similares
- Consulta a legislação atualizada

### Configuração
Para usar a API de pesquisa avançada:
1. Obtenha uma chave gratuita da API da Brave Search em: https://brave.com/search/api/
2. Execute o script de configuração: `./configurar_internet_pesquisa.sh`
3. Cole sua chave da API quando solicitado

### Uso
```bash
python3 integracao_internet_pesquisa_juridica.py "termo de pesquisa"
python3 integracao_internet_pesquisa_juridica.py --teste  # Modo de teste
```

## Integração com Refly

O sistema agora inclui integração com o Refly, uma plataforma open-source para construção de "agent skills" (habilidades de agentes) estáveis, atômicas e versionadas. Esta integração permite:

- Transformar componentes do sistema em skills padronizadas
- Versionamento independente de diferentes funcionalidades
- Reutilização de skills em diferentes contextos
- Governança centralizada das habilidades jurídicas
- Exportação para diferentes plataformas e agentes

### Skills já implementadas:
- `juridical-ocr-processor`: Processamento OCR jurídico especializado
- `juridical-document-analyzer`: Análise jurídica automatizada
- `juridical-reminder-creator`: Sistema de lembretes baseado em prazos

### Benefícios:
- Maior modularidade e manutenibilidade
- Melhor governança e controle
- Redução de custos com otimização de tokens
- Integração mais fácil com outros sistemas
- Escalabilidade para novas funcionalidades

## Integração com Discord

O sistema inclui integração com Discord para:

- Comunicação via bot
- Comandos para verificar status do sistema
- Notificações em tempo real
- Comandos: !status, !processos, !lembretes

## Integração com AgentMail

O sistema inclui integração com AgentMail para:

- Roteamento de notificações via email
- Sistema de alertas configuráveis
- Integração com serviços de automação

## Uso

### Criar novo processo
```bash
./criar_registro_processo.sh
```

### Adicionar anotação a processo existente
```bash
./criar_anotacao_processo.sh "/caminho/para/processo" "tipo_de_anotacao"
```

### Buscar termos nas anotações
```bash
./buscar_anotacoes.sh "termo_a_buscar"
```

### Análise jurídica automatizada
```bash
python3 ocr_analise_juridica.py "caminho/do/arquivo.pdf" "caminho/pasta/processo"
```

### Integração com Google Drive
```bash
python3 integracao_google_drive_analise.py
```

### Integração com Internet para Pesquisa Jurídica
```bash
python3 integracao_internet_pesquisa_juridica.py "termo de pesquisa"
```

### Demonstração de Integração com Refly
```bash
python3 demo_refly_integration.py
python3 demo_funcionamento_refly.py
```

### Integração com Discord
```bash
python3 integracao_discord.py SEU_TOKEN_DO_BOT
```

## Modelos de Anotações

- `modelos-anotacoes/modelo-analise-inicial.md` - Modelo para análise inicial do caso
- `modelos-anotacoes/modelo-estrategia-defesa.md` - Modelo para estratégia de defesa/ataque
- `modelos-anotacoes/modelo-pesquisa-juridica.md` - Modelo para pesquisa jurídica
- `modelos-anotacoes/modelo-rascunho-peca.md` - Modelo para rascunho de peças processuais