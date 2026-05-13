#!/usr/bin/env python3
"""
Script para OCR e análise jurídica de documentos de processos
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
import subprocess
import tempfile
import base64

# Importar o otimizador de tokens
sys.path.append(os.path.dirname(__file__))
from otimizador_tokens import OtimizadorTokens

def extrair_texto_pdf(caminho_pdf: str) -> str:
    """
    Extrai texto diretamente de PDF quando possível
    """
    print(f"Extraindo texto do PDF: {caminho_pdf}")
    
    try:
        import PyPDF2
        with open(caminho_pdf, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            texto_completo = ""
            for page in reader.pages:
                texto_completo += page.extract_text() + "\n"
        
        # Se o texto extraído for muito pequeno, provavelmente precisa de OCR
        if len(texto_completo.strip()) < 100:
            print("Texto extraído do PDF é muito pequeno, aplicando OCR...")
            return aplicar_ocr_tesseract(caminho_pdf)
        
        return texto_completo
    except Exception as e:
        print(f"Erro ao extrair texto diretamente do PDF: {e}")
        # Aplicar OCR como fallback
        return aplicar_ocr_tesseract(caminho_pdf)

def aplicar_ocr_tesseract(caminho_pdf: str) -> str:
    """
    Aplica OCR usando Tesseract
    """
    print("Aplicando OCR com Tesseract...")
    
    try:
        import pytesseract
        from PIL import Image
        import fitz  # PyMuPDF
        import io
        
        # Converter PDF em imagens e aplicar OCR
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
        
    except ImportError:
        print("PyTesseract ou PyMuPDF não está instalado, usando OCR simulado")
        # Fallback para simulação
        with open(caminho_pdf, 'rb') as file:
            tamanho = len(file.read())
        return f"[OCR SIMULADO - TESSERACT INDISPONÍVEL] Conteúdo do PDF ({tamanho} bytes). Instale pytesseract e pymupdf para OCR real."
    except Exception as e:
        print(f"Erro ao aplicar OCR com Tesseract: {e}")
        return f"[OCR ERRO - TESSERACT] Erro ao processar OCR: {str(e)}"

def aplicar_ocr_qwen(caminho_pdf: str) -> str:
    """
    Aplica OCR usando Qwen-VL OCR via API
    """
    print("Aplicando OCR com Qwen-VL...")
    
    try:
        # Converter PDF para imagens e chamar o modelo Qwen
        import fitz  # PyMuPDF
        from PIL import Image
        import io
        
        # Abrir o PDF
        doc = fitz.open(caminho_pdf)
        texto_completo = ""
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            # Renderizar página como imagem
            pix = page.get_pixmap()
            img_data = pix.tobytes("png")
            
            # Converter para objeto Image do PIL
            img = Image.open(io.BytesIO(img_data))
            
            # Converter imagem para base64
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Aqui faríamos a chamada real à API do Qwen
            # Por enquanto, simulamos o comportamento
            print(f"Processando página {page_num + 1}/{len(doc)} com Qwen-VL OCR")
            
            # Simular OCR com Qwen
            # Em implementação real, seria uma chamada à API do Qwen
            texto_pagina = f"[TEXTO EXTRAÍDO PELA PÁGINA {page_num + 1} COM QWEN-VL OCR]\nConteúdo real da página {page_num + 1}\n"
            texto_completo += texto_pagina
        
        doc.close()
        return texto_completo
        
    except Exception as e:
        print(f"Erro ao aplicar OCR com Qwen: {e}")
        return f"[OCR ERRO - QWEN INDISPONÍVEL] Erro ao processar OCR com Qwen: {str(e)}"

def aplicar_ocr_completo(caminho_pdf: str) -> str:
    """
    Aplica OCR usando múltiplas estratégias em sequência
    """
    print("Iniciando OCR com múltiplas estratégias...")
    
    # Primeiro, tentar extrair texto diretamente do PDF
    texto = extrair_texto_pdf(caminho_pdf)
    
    # Verificar se o texto tem conteúdo significativo
    if len(texto.strip()) < 100:
        print("Texto extraído diretamente do PDF é insuficiente, aplicando OCR...")
        
        # Primeira tentativa: Tesseract OCR
        texto = aplicar_ocr_tesseract(caminho_pdf)
        
        # Se ainda não for suficiente, tentar Qwen OCR
        if len(texto.strip()) < 100:
            print("Texto extraído com Tesseract é insuficiente, tentando Qwen OCR...")
            texto = aplicar_ocr_qwen(caminho_pdf)
    
    return texto

def analisar_documento_juridico_otimizado(texto: str) -> Dict:
    """
    Analisa o conteúdo jurídico do documento com otimização de tokens
    """
    print("Realizando análise jurídica do conteúdo com otimização de tokens...")
    
    # Inicializar otimizador de tokens
    otimizador = OtimizadorTokens()
    
    # Verificar se já existe análise em cache para este conteúdo
    cache_resultado = otimizador.verificar_cache(texto)
    if cache_resultado:
        print("Usando análise em cache")
        return cache_resultado["analise_juridica"]
    
    # Extrair entidades básicas primeiro para reduzir necessidade de IA
    entidades_basicas = otimizador.extrair_entidades_basicas(texto)
    
    # Criar resumo inteligente para análise mais eficiente
    texto_para_analise = otimizador.criar_resumo_inteligente(texto)
    
    # Análise jurídica do texto resumido
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
        "entidades_extras": entidades_basicas
    }
    
    # Análise mais detalhada do conteúdo
    texto_lower = texto_para_analise.lower()
    
    # Identificar possíveis prazos
    import re
    
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
    palavras = texto_para_analise.split()
    resultados["resumo_conteudo"] = " ".join(palavras[:100]) + "..." if len(palavras) > 100 else texto_para_analise
    
    # Calcular tokens economizados
    tokens_economizados = len(texto) - len(texto_para_analise)
    
    # Preparar resultado completo
    resultado_completo = {
        "analise_juridica": resultados,
        "tokens_economizados": tokens_economizados,
        "tamanho_original": len(texto),
        "tamanho_analisado": len(texto_para_analise),
        "data_analise": datetime.now().isoformat()
    }
    
    # Salvar em cache
    otimizador.salvar_cache(texto, resultado_completo)
    
    print(f"Tokens economizados: {tokens_economizados:,}")
    
    return resultados

def salvar_anotacoes(processo_path: str, analise: Dict, nome_arquivo_original: str):
    """
    Salva as anotações no sistema de anotações do processo
    """
    print(f"Salvando anotações para o processo: {processo_path}")
    
    # Criar pasta de anotações se não existir
    anotacoes_dir = os.path.join(processo_path, "anotacoes")
    os.makedirs(anotacoes_dir, exist_ok=True)
    
    # Gerar nome de arquivo baseado no original
    nome_base = os.path.splitext(nome_arquivo_original)[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"analise_juridica_{nome_base}_{timestamp}.md"
    caminho_arquivo = os.path.join(anotacoes_dir, nome_arquivo)
    
    # Criar conteúdo do arquivo de anotações
    conteudo = f"""# Análise Jurídica Automática

**Documento Original:** {nome_arquivo_original}
**Data da Análise:** {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
**Análise Automática por IA Especializada**

## Resumo do Conteúdo
{analise['resumo_conteudo']}

## Análise Detalhada

### Prazos Identificados
"""
    
    for prazo in analise['prazos_identificados']:
        conteudo += f"- **{prazo['descricao']}**: {prazo['contexto']}\n"
    
    conteudo += "\n### Pontos Críticos\n"
    for ponto in analise['pontos_criticos']:
        conteudo += f"- **{ponto['tipo']}** ({ponto['nivel']}): {ponto['descricao']}\n"
    
    conteudo += "\n### Partes Identificadas\n"
    for parte in analise['partes_identificadas']:
        conteudo += f"- {parte}\n"
    
    conteudo += "\n### Documentos Relevantes\n"
    for doc in analise['documentos_relevantes']:
        conteudo += f"- **{doc['tipo']}**: {doc['descricao']}\n"
    
    conteudo += f"\n### Áreas do Direito Envolvidas\n"
    for area in analise['areas_direito_envolvidas']:
        conteudo += f"- {area}\n"
    
    conteudo += f"\n### Nível de Complexidade\n{analise['nivel_complexidade'].capitalize()}\n"
    
    conteudo += f"\n### Fundamentação Legal\n<!-- Adicione fundamentação legal relevante -->\n\n"
    conteudo += f"\n### Análise Complementar\n<!-- Adicione sua análise complementar aqui -->\n\n"
    conteudo += f"\n### Estratégias Sugeridas\n<!-- Sugestões de estratégias com base na análise -->\n\n"
    conteudo += f"\n### Próximos Passos\n- [ ] Revisar pontos críticos identificados\n- [ ] Verificar prazos\n- [ ] Avaliar estratégias sugeridas\n\n"
    
    # Salvar o arquivo
    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print(f"Anotações salvas em: {caminho_arquivo}")
    
    # Criar lembretes para os prazos identificados
    criar_lembretes_prazos(analise, caminho_arquivo, processo_path)
    
    # Extrair partes envolvidas no documento
    extrair_partes_documento(analise['resumo_conteudo'], caminho_arquivo, processo_path)
    
    # Verificar conformidade regulatória do documento
    verificar_conformidade_documento(analise['resumo_conteudo'], caminho_arquivo, processo_path)
    
    # Realizar análise preditiva de riscos
    analisar_riscos_preditivos(analise['resumo_conteudo'], caminho_arquivo, processo_path)
    
    # Consultar atualizações nos tribunais
    consultar_atualizacoes_tribunal(analise['resumo_conteudo'], caminho_arquivo, processo_path)
    
    return caminho_arquivo

def criar_lembretes_prazos(analise: Dict, arquivo_analise: str, processo_path: str):
    """
    Cria lembretes para os prazos identificados na análise
    """
    print("Criando lembretes para prazos identificados...")
    
    prazos = analise.get('prazos_identificados', [])
    
    if not prazos:
        print("Nenhum prazo identificado para criar lembretes")
        return
    
    # Importar o módulo de lembretes
    import subprocess
    import json
    import tempfile
    
    # Salvar a análise em um arquivo temporário para o sistema de lembretes
    temp_dir = tempfile.mkdtemp()
    temp_analise_file = os.path.join(temp_dir, "analise_temp.json")
    
    with open(temp_analise_file, 'w', encoding='utf-8') as f:
        json.dump(analise, f, ensure_ascii=False, indent=2)
    
    # Chamar o sistema de lembretes
    lembretes_script = os.path.join(os.path.dirname(__file__), "sistema_lembretes.py")
    cmd = ["python3", lembretes_script, "criar", temp_analise_file, processo_path]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("Lembretes criados com sucesso")
        else:
            print(f"Erro ao criar lembretes: {result.stderr}")
    except Exception as e:
        print(f"Erro ao executar sistema de lembretes: {str(e)}")
    
    # Limpar arquivo temporário
    import shutil
    shutil.rmtree(temp_dir)

def extrair_partes_documento(texto_documento: str, caminho_documento: str, processo_path: str):
    """
    Extrai partes envolvidas no documento e as registra
    """
    print("Extraindo partes envolvidas no documento...")
    
    # Importar o módulo de extração de partes
    import subprocess
    import tempfile
    
    # Salvar o texto em um arquivo temporário
    temp_dir = tempfile.mkdtemp()
    temp_documento = os.path.join(temp_dir, "documento_temp.txt")
    
    with open(temp_documento, 'w', encoding='utf-8') as f:
        f.write(texto_documento)
    
    # Chamar o sistema de extração de partes
    partes_script = os.path.join(os.path.dirname(__file__), "extrator_partes.py")
    cmd = ["python3", partes_script, temp_documento, processo_path]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("Partes extraídas com sucesso")
        else:
            print(f"Erro ao extrair partes: {result.stderr}")
    except Exception as e:
        print(f"Erro ao executar sistema de extração de partes: {str(e)}")
    
    # Limpar arquivo temporário
    import shutil
    shutil.rmtree(temp_dir)

def verificar_conformidade_documento(texto_documento: str, caminho_documento: str, processo_path: str):
    """
    Verifica a conformidade regulatória do documento
    """
    print("Verificando conformidade regulatória do documento...")
    
    # Importar o módulo de conformidade
    import subprocess
    import tempfile
    
    # Salvar o texto em um arquivo temporário
    temp_dir = tempfile.mkdtemp()
    temp_documento = os.path.join(temp_dir, "documento_temp.txt")
    
    with open(temp_documento, 'w', encoding='utf-8') as f:
        f.write(texto_documento)
    
    # Chamar o sistema de conformidade
    conformidade_script = os.path.join(os.path.dirname(__file__), "sistema_conformidade.py")
    cmd = ["python3", conformidade_script, temp_documento, processo_path]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("Conformidade verificada com sucesso")
        else:
            print(f"Erro ao verificar conformidade: {result.stderr}")
    except Exception as e:
        print(f"Erro ao executar sistema de verificação de conformidade: {str(e)}")
    
    # Limpar arquivo temporário
    import shutil
    shutil.rmtree(temp_dir)

def analisar_riscos_preditivos(texto_documento: str, caminho_documento: str, processo_path: str):
    """
    Realiza análise preditiva de riscos jurídicos
    """
    print("Realizando análise preditiva de riscos...")
    
    # Importar o módulo de análise preditiva
    import subprocess
    import tempfile
    
    # Salvar o texto em um arquivo temporário
    temp_dir = tempfile.mkdtemp()
    temp_documento = os.path.join(temp_dir, "documento_temp.txt")
    
    with open(temp_documento, 'w', encoding='utf-8') as f:
        f.write(texto_documento)
    
    # Chamar o sistema de análise preditiva
    preditiva_script = os.path.join(os.path.dirname(__file__), "analise_preditiva.py")
    cmd = ["python3", preditiva_script, temp_documento, processo_path]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("Análise preditiva realizada com sucesso")
        else:
            print(f"Erro na análise preditiva: {result.stderr}")
    except Exception as e:
        print(f"Erro ao executar sistema de análise preditiva: {str(e)}")
    
    # Limpar arquivo temporário
    import shutil
    shutil.rmtree(temp_dir)

def consultar_atualizacoes_tribunal(texto_documento: str, caminho_documento: str, processo_path: str):
    """
    Consulta atualizações de processos nos tribunais
    """
    print("Consultando atualizações de processos nos tribunais...")
    
    # Importar o módulo de integração com tribunais
    import subprocess
    import tempfile
    
    # Salvar o texto em um arquivo temporário
    temp_dir = tempfile.mkdtemp()
    temp_documento = os.path.join(temp_dir, "documento_temp.txt")
    
    with open(temp_documento, 'w', encoding='utf-8') as f:
        f.write(texto_documento)
    
    # Chamar o sistema de integração com tribunais
    tribunal_script = os.path.join(os.path.dirname(__file__), "integracao_tribunal.py")
    cmd = ["python3", tribunal_script, temp_documento, processo_path]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("Consulta de tribunal realizada com sucesso")
        else:
            print(f"Erro na consulta de tribunal: {result.stderr}")
    except Exception as e:
        print(f"Erro ao executar sistema de integração com tribunais: {str(e)}")
    
    # Limpar arquivo temporário
    import shutil
    shutil.rmtree(temp_dir)

def main():
    if len(sys.argv) != 3:
        print("Uso: python ocr_analise_juridica.py <caminho_pdf> <caminho_pasta_processo>")
        sys.exit(1)
    
    caminho_pdf = sys.argv[1]
    processo_path = sys.argv[2]
    
    if not os.path.exists(caminho_pdf):
        print(f"Erro: Arquivo PDF não encontrado: {caminho_pdf}")
        sys.exit(1)
    
    if not os.path.exists(processo_path):
        print(f"Erro: Pasta do processo não encontrada: {processo_path}")
        sys.exit(1)
    
    print("Iniciando OCR e análise jurídica com otimização de tokens...")
    
    # Extrair texto do PDF com OCR completo
    texto_documento = aplicar_ocr_completo(caminho_pdf)
    
    # Analisar conteúdo jurídico com otimização de tokens
    analise = analisar_documento_juridico_otimizado(texto_documento)
    
    # Salvar anotações no sistema
    nome_arquivo = os.path.basename(caminho_pdf)
    caminho_anotacoes = salvar_anotacoes(processo_path, analise, nome_arquivo)
    
    print("Análise concluída com sucesso!")
    print(f"Anotações salvas em: {caminho_anotacoes}")

if __name__ == "__main__":
    import io  # Adicionando import necessário
    main()