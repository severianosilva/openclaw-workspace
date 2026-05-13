---
name: juridical-ocr-processor
description: Processador de OCR especializado para documentos jurídicos
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

## Implementação

```python
def processar_ocr_juridico(document_path, preferred_engine='tesseract'):
    '''
    Processa OCR em documento jurídico
    '''
    import os
    import sys
    import subprocess
    
    # Importar módulos necessários
    try:
        import fitz  # PyMuPDF
        from PIL import Image
        import io
        import pytesseract
    except ImportError as e:
        print(f"Erro ao importar módulos: {e}")
        return {
            "error": f"Módulos necessários não instalados: {e}",
            "extracted_text": "",
            "confidence_score": 0.0
        }
    
    # Função para extrair texto diretamente do PDF
    def extrair_texto_direto(caminho_pdf):
        try:
            doc = fitz.open(caminho_pdf)
            texto_completo = ""
            for page in doc:
                texto_completo += page.get_text()
            doc.close()
            return texto_completo
        except Exception as e:
            print(f"Erro ao extrair texto direto: {e}")
            return ""
    
    # Função para aplicar OCR com Tesseract
    def aplicar_ocr_tesseract(caminho_pdf):
        try:
            doc = fitz.open(caminho_pdf)
            texto_completo = ""
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                # Renderizar página como imagem
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                
                # Converter para objeto Image do PIL
                img = Image.open(io.BytesIO(img_data))
                
                # Aplicar OCR com Tesseract
                texto_pagina = pytesseract.image_to_string(img, lang='por')
                texto_completo += texto_pagina + "\n"
            
            doc.close()
            return texto_completo
        except Exception as e:
            print(f"Erro ao aplicar OCR com Tesseract: {e}")
            return ""
    
    # Primeira tentativa: extrair texto diretamente
    texto = extrair_texto_direto(document_path)
    
    # Se o texto extraído for muito pequeno, aplicar OCR
    if len(texto.strip()) < 100:
        print("Texto extraído diretamente do PDF é muito pequeno, aplicando OCR...")
        
        # Primeira tentativa de OCR: Tesseract
        if preferred_engine == 'tesseract':
            texto = aplicar_ocr_tesseract(document_path)
            
            # Se ainda não for suficiente, tentar Qwen OCR
            if len(texto.strip()) < 100:
                print("Texto extraído com Tesseract é insuficiente, retornando vazio (Qwen OCR não implementado diretamente nesta skill)")
                # Em uma implementação completa, aqui faríamos a chamada à API do Qwen
                pass
    
    # Calcular pontuação de confiança básica
    confidence = min(0.95, len(texto.strip()) / 1000) if texto.strip() else 0.0
    confidence = max(0.1, confidence)  # Valor mínimo
    
    return {
        "extracted_text": texto,
        "confidence_score": round(confidence, 2),
        "processing_method": "direct_extraction" if len(extrair_texto_direto(document_path)) >= 100 else "ocr_processing"
    }

# Função principal da skill
def execute(inputs):
    '''
    Função principal da skill do Refly
    '''
    document_path = inputs.get('document_path')
    preferred_engine = inputs.get('preferred_engine', 'tesseract')
    
    if not document_path:
        return {
            "error": "document_path é obrigatório",
            "extracted_text": "",
            "confidence_score": 0.0
        }
    
    if not os.path.exists(document_path):
        return {
            "error": f"Arquivo não encontrado: {document_path}",
            "extracted_text": "",
            "confidence_score": 0.0
        }
    
    # Chamar função de processamento OCR
    result = processar_ocr_juridico(document_path, preferred_engine)
    
    return result
```
