# Skills do Refly para o Sistema Jurídico Automatizado

Este diretório contém as skills do Refly que fazem parte do sistema jurídico automatizado.

## Estrutura

- `skills/` - Diretório contendo as skills individuais
- `data/` - Diretório para dados persistentes
- `refly.config.json` - Configuração do ambiente Refly

## Skills Implementadas

### juridical-ocr-processor
Processa documentos jurídicos com OCR especializado para extração de texto.

### Próximas Skills a Serem Implementadas
- juridical-document-analyzer
- juridical-reminder-creator
- juridical-document-classifier
- juridical-precedents-search
- juridical-report-generator

## Instalação

1. Certifique-se de que o CLI do Refly está instalado:
   ```bash
   npm install -g @powerformer/refly-cli
   ```

2. Navegue até este diretório e instale as dependências:
   ```bash
   cd /caminho/para/refly-skills
   npm install
   ```

3. Para desenvolvimento, inicie o servidor de desenvolvimento:
   ```bash
   refly dev
   ```

## Uso

As skills podem ser chamadas diretamente ou compostas em fluxos de trabalho mais complexos.
