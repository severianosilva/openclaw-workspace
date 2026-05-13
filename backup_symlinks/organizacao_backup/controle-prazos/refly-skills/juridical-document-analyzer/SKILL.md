---
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
        r"(\d+)\s+(dia|dias|mês|meses|ano|anos)\s+(para|a contar|a partir)",
        r"prazo\s+de\s+(\d+)\s+(dia|dias|mês|meses|ano|anos)",
        r"(\d+)\s+dias\s+uteis?",
        r"(\d+)\s+dias\s+civis?"
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
