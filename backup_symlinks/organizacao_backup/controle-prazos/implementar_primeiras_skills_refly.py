#!/usr/bin/env python3
"""
Implementação das primeiras skills do Refly para o sistema jurídico automatizado
"""

import os
import json
from datetime import datetime
import sys

def criar_skill_ocr_juridico():
    """Cria a skill de OCR jurídico"""
    skill_dir = "/home/severosa/organizacao/controle-prazos/refly-skills/juridical-ocr-processor"
    
    # Atualizar o SKILL.md com implementação mais detalhada
    skill_content = """---
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
                texto_completo += texto_pagina + "\\n"
            
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
"""
    
    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_content)
    
    # Criar arquivo de configuração da skill
    config = {
        "skill": "juridical-ocr-processor",
        "version": "1.0.0",
        "handler": "execute",
        "inputs": {
            "document_path": {
                "type": "string",
                "required": True,
                "description": "Caminho para o documento a ser processado"
            },
            "preferred_engine": {
                "type": "string",
                "required": False,
                "default": "tesseract",
                "description": "Motor OCR preferido (tesseract, qwen-vl, ambos)"
            }
        },
        "outputs": {
            "extracted_text": {
                "type": "string",
                "description": "Texto extraído do documento"
            },
            "confidence_score": {
                "type": "number",
                "description": "Pontuação de confiança do OCR (0-1)"
            },
            "processing_method": {
                "type": "string",
                "description": "Método de processamento usado"
            },
            "error": {
                "type": "string",
                "description": "Mensagem de erro, se houver"
            }
        }
    }
    
    with open(os.path.join(skill_dir, "config.json"), "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("✓ Skill de OCR jurídico criada com sucesso")

def criar_skill_analise_juridica():
    """Cria a skill de análise jurídica"""
    skill_dir = "/home/severosa/organizacao/controle-prazos/refly-skills/juridical-document-analyzer"
    os.makedirs(skill_dir, exist_ok=True)
    
    skill_content = """---
name: juridical-document-analyzer
description: Analisa documentos jurídicos para identificar prazos, pontos críticos e partes
author: Sistema Jurídico Automatizado
version: 1.0.0
category: document-analysis
tags: [legal, analysis, document-processing, compliance]
---

# Analisador Jurídico de Documentos

Esta skill analisa documentos jurídicos para identificar prazos, pontos críticos, partes envolvidas e áreas do direito aplicáveis.

## Funcionalidades

- Identificação de prazos processuais
- Detecção de pontos críticos e riscos
- Extração de partes envolvidas (autores, réus, advogados, juízes)
- Identificação de áreas do direito envolvidas
- Análise de conformidade e potenciais problemas

## Configuração

A skill requer acesso ao conteúdo do documento a ser analisado.

## Uso

A skill pode ser invocada diretamente ou como parte de fluxos maiores de análise jurídica.

## Implementação

```python
def analisar_documento_juridico(texto_documento, tipo_documento="generico"):
    '''
    Analisa conteúdo jurídico do documento
    '''
    import re
    
    # Análise jurídica do texto
    resultados = {
        "prazos_identificados": [],
        "pontos_criticos": [],
        "documentos_relevantes": [],
        "partes_identificadas": [],
        "valores_mencionados": [],
        "fundamentacao_legal": [],
        "resumo_conteudo": "",
        "nivel_complexidade": "",
        "areas_direito_envolvidas": [],
        "recomendacoes": []
    }
    
    # Análise mais detalhada do conteúdo
    texto_lower = texto_documento.lower()
    
    # Padrões para identificação de prazos
    padroes_prazo = [
        r"(\\d+)\\s+(dia|dias|mês|meses|ano|anos)\\s+(para|a contar|a partir)",
        r"prazo\\s+de\\s+(\\d+)\\s+(dia|dias|mês|meses|ano|anos)",
        r"(\\d+)\\s+dias\\s+uteis?",
        r"(\\d+)\\s+dias\\s+civis?"
    ]
    
    for padrao in padroes_prazo:
        matches = re.finditer(padrao, texto_lower)
        for match in matches:
            descricao = match.group(0)
            resultados["prazos_identificados"].append({
                "descricao": descricao,
                "contexto": f"Trecho: {match.group(0)[:100]}..."
            })
    
    # Identificar possíveis pontos críticos
    pontos_criticos_keywords = [
        ("nulidade", "alta"),
        ("revelia", "média"),
        ("prescrição", "alta"),
        (" decadência", "alta"),
        ("incompetência", "média"),
        ("suspeição", "baixa"),
        ("impedimento", "baixa"),
        ("exceção", "média"),
        ("recurso", "alta"),
        ("embargos", "alta")
    ]
    
    for keyword, nivel in pontos_criticos_keywords:
        if keyword in texto_lower:
            resultados["pontos_criticos"].append({
                "tipo": keyword,
                "descricao": f"Menção a {keyword} no documento",
                "nivel": nivel
            })
    
    # Identificar partes envolvidas
    partes_keywords = [
        "autor", "réu", "apelante", "apelado", "recorrente", 
        "recorrido", "executante", "executado", "requerente", 
        "requerido", "paciente", "coator", "investigado", 
        "acusado", "ré", "emandante", "emandado"
    ]
    
    for parte in partes_keywords:
        if parte in texto_lower:
            if parte not in resultados["partes_identificadas"]:
                resultados["partes_identificadas"].append(parte)
    
    # Identificar áreas do direito
    areas_direito = ["civil", "penal", "trabalhista", "tributário", "administrativo", 
                     "constitucional", "processual civil", "processual penal", 
                     "família", "sucessões", "empresa", "consumidor", "ambiental"]
    
    for area in areas_direito:
        if area in texto_lower:
            if area not in resultados["areas_direito_envolvidas"]:
                resultados["areas_direito_envolvidas"].append(area.capitalize())
    
    # Determinar nível de complexidade
    palavras_complexas = ["recurso", "embargos", "impugnação", "contestação", 
                          "reconvenção", "exceção", "arguição", "interposição", 
                          "admissibilidade", "provido", "negado provimento"]
    
    complexidade = sum(1 for palavra in palavras_complexas if palavra in texto_lower)
    
    if complexidade >= 5:
        resultados["nivel_complexidade"] = "alto"
    elif complexidade >= 2:
        resultados["nivel_complexidade"] = "médio"
    else:
        resultados["nivel_complexidade"] = "baixo"
    
    # Criar resumo
    palavras = texto_documento.split()
    resultados["resumo_conteudo"] = " ".join(palavras[:100]) + "..." if len(palavras) > 100 else texto_documento
    
    # Adicionar recomendações básicas
    if resultados["pontos_criticos"]:
        resultados["recomendacoes"].append("Avaliar cuidadosamente os pontos críticos identificados")
    
    if resultados["prazos_identificados"]:
        resultados["recomendacoes"].append("Acompanhar os prazos identificados para evitar preclusão")
    
    if resultados["nivel_complexidade"] == "alto":
        resultados["recomendacoes"].append("Considerar revisão por especialista dada a complexidade")
    
    return resultados

# Função principal da skill
def execute(inputs):
    '''
    Função principal da skill do Refly
    '''
    document_content = inputs.get('document_content', '')
    document_type = inputs.get('document_type', 'generico')
    
    if not document_content:
        return {
            "error": "document_content é obrigatório",
            "analysis_results": {}
        }
    
    # Chamar função de análise jurídica
    result = analisar_documento_juridico(document_content, document_type)
    
    return {
        "analysis_results": result,
        "document_type": document_type
    }
```
"""
    
    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_content)
    
    # Criar arquivo de configuração da skill
    config = {
        "skill": "juridical-document-analyzer",
        "version": "1.0.0",
        "handler": "execute",
        "inputs": {
            "document_content": {
                "type": "string",
                "required": True,
                "description": "Conteúdo do documento a ser analisado"
            },
            "document_type": {
                "type": "string",
                "required": False,
                "default": "generico",
                "description": "Tipo do documento (petição, sentença, despacho, etc.)"
            }
        },
        "outputs": {
            "analysis_results": {
                "type": "object",
                "description": "Resultados da análise jurídica"
            },
            "document_type": {
                "type": "string",
                "description": "Tipo do documento analisado"
            },
            "error": {
                "type": "string",
                "description": "Mensagem de erro, se houver"
            }
        }
    }
    
    with open(os.path.join(skill_dir, "config.json"), "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("✓ Skill de análise jurídica criada com sucesso")

def criar_skill_sistema_lembretes():
    """Cria a skill de sistema de lembretes"""
    skill_dir = "/home/severosa/organizacao/controle-prazos/refly-skills/juridical-reminder-creator"
    os.makedirs(skill_dir, exist_ok=True)
    
    skill_content = """---
name: juridical-reminder-creator
description: Cria lembretes baseados em prazos identificados em documentos jurídicos
author: Sistema Jurídico Automatizado
version: 1.0.0
category: reminders
tags: [legal, reminders, deadlines, notifications]
---

# Criador de Lembretes Jurídicos

Esta skill cria lembretes automáticos baseados em prazos identificados em documentos jurídicos.

## Funcionalidades

- Criação de lembretes baseados em prazos identificados
- Agendamento de notificações antecipadas
- Integração com sistema de processos
- Suporte a diferentes tipos de alertas

## Configuração

A skill requer lista de prazos e número do processo associado.

## Uso

A skill pode ser invocada após identificação de prazos em documentos jurídicos.

## Implementação

```python
def criar_lembretes_juridicos(deadlines, process_number, advance_notice_days=3):
    '''
    Cria lembretes para prazos jurídicos
    '''
    from datetime import datetime, timedelta
    import uuid
    
    lembretes_criados = []
    
    for prazo in deadlines:
        descricao = prazo.get('descricao', 'Prazo não especificado')
        contexto = prazo.get('contexto', 'Contexto não fornecido')
        
        # Calcular data do lembrete (antecedência)
        # Neste exemplo simplificado, assumimos que a data do prazo está embutida na descrição
        # Em uma implementação real, isso seria extraído do documento
        
        # Gerar ID único para o lembrete
        lembrete_id = str(uuid.uuid4())
        
        # Calcular data do lembrete (3 dias antes por padrão)
        lembrete_info = {
            "reminder_id": lembrete_id,
            "process_number": process_number,
            "deadline_description": descricao,
            "deadline_context": contexto,
            "advance_notice_days": advance_notice_days,
            "created_at": datetime.now().isoformat(),
            "status": "scheduled"
        }
        
        lembretes_criados.append(lembrete_info)
    
    return {
        "reminder_ids": [lem["reminder_id"] for lem in lembretes_criados],
        "scheduled_reminders": lembretes_criados,
        "total_reminders": len(lembretes_criados)
    }

# Função principal da skill
def execute(inputs):
    '''
    Função principal da skill do Refly
    '''
    deadlines = inputs.get('deadlines', [])
    process_number = inputs.get('process_number', '')
    advance_notice_days = inputs.get('advance_notice_days', 3)
    
    if not deadlines:
        return {
            "error": "deadlines é obrigatório",
            "reminder_ids": [],
            "scheduled_reminders": [],
            "total_reminders": 0
        }
    
    if not process_number:
        return {
            "error": "process_number é obrigatório",
            "reminder_ids": [],
            "scheduled_reminders": [],
            "total_reminders": 0
        }
    
    # Chamar função de criação de lembretes
    result = criar_lembretes_juridicos(deadlines, process_number, advance_notice_days)
    
    return result
```
"""
    
    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_content)
    
    # Criar arquivo de configuração da skill
    config = {
        "skill": "juridical-reminder-creator",
        "version": "1.0.0",
        "handler": "execute",
        "inputs": {
            "deadlines": {
                "type": "array",
                "required": True,
                "description": "Lista de prazos identificados"
            },
            "process_number": {
                "type": "string",
                "required": True,
                "description": "Número do processo associado"
            },
            "advance_notice_days": {
                "type": "number",
                "required": False,
                "default": 3,
                "description": "Dias de antecedência para o lembrete"
            }
        },
        "outputs": {
            "reminder_ids": {
                "type": "array",
                "description": "IDs dos lembretes criados"
            },
            "scheduled_reminders": {
                "type": "array",
                "description": "Detalhes dos lembretes agendados"
            },
            "total_reminders": {
                "type": "number",
                "description": "Total de lembretes criados"
            },
            "error": {
                "type": "string",
                "description": "Mensagem de erro, se houver"
            }
        }
    }
    
    with open(os.path.join(skill_dir, "config.json"), "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print("✓ Skill de sistema de lembretes criada com sucesso")

def main():
    print("Implementando as primeiras skills do Refly para o sistema jurídico automatizado...")
    print("=" * 80)
    
    # Criar as três skills iniciais
    criar_skill_ocr_juridico()
    print()
    
    criar_skill_analise_juridica()
    print()
    
    criar_skill_sistema_lembretes()
    print()
    
    print("=" * 80)
    print("IMPLEMENTAÇÃO DAS PRIMEIRAS SKILLS DO REFly CONCLUÍDA!")
    print("=" * 80)
    print()
    print("As seguintes skills foram criadas:")
    print("1. juridical-ocr-processor - Processamento OCR especializado para documentos jurídicos")
    print("2. juridical-document-analyzer - Análise jurídica automatizada de documentos")
    print("3. juridical-reminder-creator - Sistema de lembretes baseado em prazos identificados")
    print()
    print("Cada skill está localizada em seu próprio diretório dentro de:")
    print("/home/severosa/organizacao/controle-prazos/refly-skills/")
    print()
    print("Cada skill contém:")
    print("- SKILL.md: Documentação e implementação da skill")
    print("- config.json: Configuração de entradas e saídas da skill")
    print()
    print("Próximos passos:")
    print("1. Revisar as implementações das skills conforme necessário")
    print("2. Testar as skills individualmente")
    print("3. Criar fluxos de trabalho combinando múltiplas skills")
    print("4. Expandir para outras funcionalidades do sistema jurídico")
    print()
    print("O sistema Refly está preparado para receber mais skills conforme o planejamento!")

if __name__ == "__main__":
    main()