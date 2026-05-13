# Exemplo de Skill do Refly: OCR Jurídico

Este é um exemplo prático de como seria uma skill do Refly para o sistema de OCR especializado em documentos jurídicos.

## Definição da Skill

### SKILL.md
```yaml
---
name: juridical-ocr-processor
description: Processa documentos jurídicos com OCR especializado para extração de texto
author: Sistema Jurídico Automatizado
version: 1.0.0
category: document-processing
tags: [ocr, legal, document-analysis, text-extraction]
---

# Processador de OCR Jurídico

Esta skill aplica OCR especializado em documentos jurídicos usando múltiplas estratégias para máxima precisão.

## Funcionalidades

- Extração de texto de documentos PDF jurídicos
- Aplicação de OCR usando Tesseract como primeira tentativa
- Fallback para Qwen-VL OCR quando necessário
- Análise de confiança do OCR
- Formatação de texto para análise jurídica subsequente

## Configuração

A skill requer acesso aos seguintes recursos:

- Motor OCR Tesseract instalado
- Acesso à API Qwen-VL (quando configurada)
- Permissões de leitura para arquivos de entrada
- Permissões de escrita para arquivos de saída

## Uso

A skill pode ser invocada diretamente ou como parte de fluxos maiores de análise jurídica.
```

### Implementação da Skill (exemplo conceptual)

```javascript
// Este é um exemplo conceitual da implementação da skill
// Em uma implementação real, usaria a linguagem DSL do Refly

async function juridicalOCRProcessor(input) {
  const { documentPath, preferredEngine = 'tesseract' } = input;
  
  let extractedText = '';
  let confidenceScore = 0;
  let processingSteps = [];
  
  // Validação de entrada
  if (!documentPath) {
    throw new Error('Caminho do documento é obrigatório');
  }
  
  // Etapa 1: Tentativa de extração de texto direto do PDF
  try {
    const directText = await extractDirectTextFromPDF(documentPath);
    if (directText.length > 100) {
      // Texto direto é suficientemente longo, provavelmente não precisa de OCR
      extractedText = directText;
      confidenceScore = 0.95;
      processingSteps.push({
        step: 'direct_extraction',
        status: 'success',
        confidence: 0.95
      });
    } else {
      // Texto direto é curto, provavelmente precisa de OCR
      processingSteps.push({
        step: 'direct_extraction',
        status: 'insufficient_content',
        confidence: 0.1
      });
      
      // Etapa 2: Aplicar OCR com o motor preferido
      if (preferredEngine === 'tesseract' || !preferredEngine) {
        try {
          extractedText = await applyTesseractOCR(documentPath);
          confidenceScore = 0.85;
          processingSteps.push({
            step: 'tesseract_ocr',
            status: 'success',
            confidence: 0.85
          });
        } catch (error) {
          processingSteps.push({
            step: 'tesseract_ocr',
            status: 'failed',
            error: error.message
          });
          
          // Fallback para Qwen-VL OCR
          try {
            extractedText = await applyQwenVLOCR(documentPath);
            confidenceScore = 0.90;
            processingSteps.push({
              step: 'qwen_vl_ocr',
              status: 'success',
              confidence: 0.90
            });
          } catch (fallbackError) {
            processingSteps.push({
              step: 'qwen_vl_ocr',
              status: 'failed',
              error: fallbackError.message
            });
            throw new Error(`Falha em todos os métodos de OCR: ${error.message}, ${fallbackError.message}`);
          }
        }
      }
    }
  } catch (error) {
    processingSteps.push({
      step: 'overall_processing',
      status: 'failed',
      error: error.message
    });
    throw error;
  }
  
  // Pós-processamento para formatação jurídica
  const formattedText = formatLegalText(extractedText);
  
  return {
    extractedText: formattedText,
    confidenceScore,
    processingSteps,
    processingTime: Date.now() - startTime
  };
}

// Funções auxiliares (implementação simplificada)
async function extractDirectTextFromPDF(filePath) {
  // Implementação real usaria biblioteca como pdfjs ou PyPDF2
  // Esta é apenas uma representação conceitual
  const fs = require('fs');
  // Em implementação real, usaria uma biblioteca apropriada
  return "Texto extraído diretamente do PDF";
}

async function applyTesseractOCR(filePath) {
  // Implementação real chamaria o Tesseract OCR
  return "Texto extraído com Tesseract OCR";
}

async function applyQwenVLOCR(filePath) {
  // Implementação real chamaria a API Qwen-VL
  return "Texto extraído com Qwen-VL OCR";
}

function formatLegalText(text) {
  // Formatação específica para textos jurídicos
  // Remover espaços extras, padronizar formatação, etc.
  return text.replace(/\s+/g, ' ').trim();
}
```

## Exemplo de Uso em um Fluxo Jurídico

```yaml
# workflow.yaml - Exemplo de uso da skill em um fluxo
name: legal-document-analysis-flow
description: Fluxo completo de análise de documentos jurídicos
steps:
  - id: ocr-processing
    skill: juridical-ocr-processor
    inputs:
      documentPath: "{{ inputs.documentPath }}"
      preferredEngine: "tesseract"
    outputs:
      extractedText: "{{ steps.ocr-processing.outputs.extractedText }}"
      confidence: "{{ steps.ocr-processing.outputs.confidenceScore }}"

  - id: legal-analysis
    skill: juridical-document-analysis
    inputs:
      documentContent: "{{ steps.ocr-processing.outputs.extractedText }}"
      documentType: "{{ inputs.documentType }}"
    condition: "{{ steps.ocr-processing.outputs.confidence > 0.7 }}"
    outputs:
      analysisResults: "{{ steps.legal-analysis.outputs.analysisResults }}"

  - id: low-confidence-alert
    skill: notification-sender
    inputs:
      message: "Documento com baixa confiança de OCR detectado. Confiança: {{ steps.ocr-processing.outputs.confidence }}"
      recipients: ["legal-team@example.com"]
    condition: "{{ steps.ocr-processing.outputs.confidence <= 0.7 }}"
```

## Benefícios da Abordagem com Refly

1. **Reusabilidade**: A mesma skill de OCR pode ser usada em diferentes fluxos jurídicos
2. **Versionamento**: Atualizações no OCR não afetam outros componentes
3. **Testabilidade**: Cada skill pode ser testada isoladamente
4. **Monitoramento**: Métricas de desempenho por skill
5. **Governança**: Controle centralizado sobre todas as operações de OCR

## Considerações para Implementação Real

1. **Performance**: Otimizar o pipeline de OCR para tempos de resposta rápidos
2. **Escalabilidade**: Permitir processamento paralelo de múltiplos documentos
3. **Recuperação de Falhas**: Mecanismos robustos para lidar com falhas de OCR
4. **Segurança**: Proteger documentos jurídicos sensíveis durante o processamento
5. **Auditoria**: Manter logs detalhados de todas as operações de OCR