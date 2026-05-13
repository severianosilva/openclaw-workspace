#!/usr/bin/env python3
"""
Sistema de otimização de uso de tokens para o sistema jurídico automatizado
"""

import os
import json
from datetime import datetime, timedelta
import hashlib
from typing import Dict, List, Optional

class OtimizadorTokens:
    """
    Classe para otimizar o uso de tokens no sistema jurídico automatizado
    """
    
    def __init__(self):
        self.cache_dir = os.path.expanduser("~/organizacao/controle-prazos/cache")
        self.resumo_dir = os.path.expanduser("~/organizacao/controle-prazos/resumos")
        
        # Garantir que os diretórios existam
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.resumo_dir, exist_ok=True)
    
    def gerar_hash_conteudo(self, conteudo: str) -> str:
        """Gera hash do conteúdo para cache"""
        return hashlib.sha256(conteudo.encode('utf-8')).hexdigest()
    
    def verificar_cache(self, conteudo: str) -> Optional[dict]:
        """Verifica se já existe análise em cache para este conteúdo"""
        hash_conteudo = self.gerar_hash_conteudo(conteudo)
        caminho_cache = os.path.join(self.cache_dir, f"{hash_conteudo}.json")
        
        if os.path.exists(caminho_cache):
            # Verificar se o cache é recente (menos de 7 dias)
            data_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho_cache))
            if datetime.now() - data_modificacao < timedelta(days=7):
                try:
                    with open(caminho_cache, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except:
                    pass
        
        return None
    
    def salvar_cache(self, conteudo: str, resultado: dict):
        """Salva o resultado da análise em cache"""
        hash_conteudo = self.gerar_hash_conteudo(conteudo)
        caminho_cache = os.path.join(self.cache_dir, f"{hash_conteudo}.json")
        
        with open(caminho_cache, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    def extrair_entidades_basicas(self, texto: str) -> Dict[str, List[str]]:
        """
        Extrai entidades básicas usando métodos tradicionais antes de chamar IA
        """
        import re
        
        entidades = {
            'numeros_processo': [],
            'nomes_partes': [],
            'datas': [],
            'valores_monetarios': [],
            'trechos_principais': []
        }
        
        # Padrões regulares para extração
        padroes = {
            'numeros_processo': r'\b\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}\b|\b\d{20}\b|\b\d{7}\d{2}\d{4}\d{1}\d{2}\d{4}\b',
            'datas': r'\b\d{1,2}/\d{1,2}/\d{4}\b',
            'valores_monetarios': r'R\$[\s\d,.]+|[\d,.]+\s*R\$',
        }
        
        for tipo, padrao in padroes.items():
            matches = re.findall(padrao, texto)
            entidades[tipo] = list(set(matches))  # Remover duplicatas
        
        # Extrair trechos principais (cabeçalho, dispositivos finais, fundamentos)
        linhas = texto.split('\n')
        trechos_interessantes = []
        
        for i, linha in enumerate(linhas):
            if any(palavra in linha.lower() for palavra in 
                   ['vistos', 'relatados', 'fundamentados', 'decido', 'julgo', 'por unanimidade', 
                    'votação', 'acordam', 'negaram provimento', 'deram provimento', 
                    'cnpj', 'advogado', 'requerente', 'requerido']):
                # Incluir linhas antes e depois
                inicio = max(0, i-2)
                fim = min(len(linhas), i+8)
                trecho = '\n'.join(linhas[inicio:fim])
                trechos_interessantes.append(trecho.strip())
        
        entidades['trechos_principais'] = trechos_interessantes[:5]  # Limitar a 5 trechos
        
        return entidades
    
    def criar_resumo_inteligente(self, texto: str, max_tamanho: int = 4000) -> str:
        """
        Cria um resumo inteligente do documento, mantendo apenas as partes mais relevantes
        """
        if len(texto) <= max_tamanho:
            return texto
        
        # Dividir o texto em segmentos
        segmentos = texto.split('\n\n')
        
        # Priorizar segmentos com conteúdo jurídico relevante
        segmentos_prioritarios = []
        segmentos_normais = []
        
        for segmento in segmentos:
            if any(palavra in segmento.lower() for palavra in 
                   ['vistos', 'relatados', 'fundamentados', 'decido', 'julgo', 'por unanimidade', 
                    'votação', 'acordam', 'negaram provimento', 'deram provimento', 
                    'processo', 'petição', 'sentença', 'despacho', 'recurso', 
                    'cnpj', 'advogado', 'requerente', 'requerido', 'parte autora', 'ré']):
                segmentos_prioritarios.append(segmento)
            else:
                segmentos_normais.append(segmento)
        
        # Construir resumo mantendo prioridade
        resumo = []
        tamanho_atual = 0
        
        # Adicionar segmentos prioritários primeiro
        for segmento in segmentos_prioritarios:
            if tamanho_atual + len(segmento) <= max_tamanho:
                resumo.append(segmento)
                tamanho_atual += len(segmento)
            else:
                break
        
        # Completar com segmentos normais se houver espaço
        for segmento in segmentos_normais:
            if tamanho_atual + len(segmento) <= max_tamanho:
                resumo.append(segmento)
                tamanho_atual += len(segmento)
            else:
                break
        
        return '\n\n'.join(resumo)
    
    def processar_documento_otimizado(self, caminho_documento: str, tipo_documento: str = "juridico") -> Dict:
        """
        Processa documento com otimização de tokens
        """
        with open(caminho_documento, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # Verificar cache primeiro
        cache_resultado = self.verificar_cache(conteudo)
        if cache_resultado:
            print(f"Usando cache para documento: {caminho_documento}")
            return cache_resultado
        
        print(f"Processando documento com otimização de tokens: {caminho_documento}")
        
        # Extrair entidades básicas primeiro
        entidades = self.extrair_entidades_basicas(conteudo)
        
        # Criar resumo inteligente
        resumo_inteligente = self.criar_resumo_inteligente(conteudo)
        
        # Salvar resumo para referência futura
        nome_arquivo = os.path.basename(caminho_documento)
        caminho_resumo = os.path.join(self.resumo_dir, f"resumo_{nome_arquivo}")
        
        with open(caminho_resumo, 'w', encoding='utf-8') as f:
            f.write(f"Documento original: {caminho_documento}\n")
            f.write(f"Tipo: {tipo_documento}\n")
            f.write(f"Data do processamento: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("RESUMO INTELIGENTE:\n")
            f.write("=" * 50 + "\n")
            f.write(resumo_inteligente)
            f.write("\n\nENTIDADES EXTRAÍDAS:\n")
            f.write("=" * 50 + "\n")
            for chave, valor in entidades.items():
                f.write(f"{chave.upper()}:\n")
                for item in valor[:10]:  # Limitar a 10 itens por categoria
                    f.write(f"  - {item}\n")
                f.write("\n")
        
        # Preparar resultado otimizado
        resultado = {
            "documento_original": caminho_documento,
            "tipo_documento": tipo_documento,
            "tamanho_original": len(conteudo),
            "tamanho_resumo": len(resumo_inteligente),
            "resumo": resumo_inteligente,
            "entidades": entidades,
            "data_processamento": datetime.now().isoformat(),
            "tokens_economizados": len(conteudo) - len(resumo_inteligente)
        }
        
        # Salvar em cache
        self.salvar_cache(conteudo, resultado)
        
        print(f"Processamento otimizado concluído. Tokens economizados: {resultado['tokens_economizados']:,}")
        
        return resultado

    def processar_documento_otimizado_texto(self, texto: str, tipo_documento: str = "juridico") -> Dict:
        """
        Processa texto com otimização de tokens
        """
        # Verificar cache primeiro
        cache_resultado = self.verificar_cache(texto)
        if cache_resultado:
            print("Usando cache para texto")
            return cache_resultado
        
        print("Processando texto com otimização de tokens")
        
        # Extrair entidades básicas primeiro
        entidades = self.extrair_entidades_basicas(texto)
        
        # Criar resumo inteligente
        resumo_inteligente = self.criar_resumo_inteligente(texto)
        
        # Preparar resultado otimizado
        resultado = {
            "tipo_documento": tipo_documento,
            "tamanho_original": len(texto),
            "tamanho_resumo": len(resumo_inteligente),
            "resumo": resumo_inteligente,
            "entidades": entidades,
            "data_processamento": datetime.now().isoformat(),
            "tokens_economizados": len(texto) - len(resumo_inteligente)
        }
        
        # Salvar em cache
        self.salvar_cache(texto, resultado)
        
        print(f"Processamento otimizado concluído. Tokens economizados: {resultado['tokens_economizados']:,}")
        
        return resultado

def main():
    """
    Função principal para demonstrar a otimização de tokens
    """
    otimizador = OtimizadorTokens()
    
    print("Sistema de Otimização de Tokens - Demonstração")
    print("=" * 50)
    
    # Exemplo de uso com um documento hipotético
    # Na prática, isso seria chamado a partir dos outros scripts do sistema
    
    print("\nA otimização de tokens está configurada e pronta para uso.")
    print("Os principais benefícios são:")
    print("- Cache de análises para evitar reprocessamento")
    print("- Extração de entidades antes de chamar IA")
    print("- Resumos inteligentes de documentos longos")
    print("- Processamento por partes em vez de todo o conteúdo de uma vez")

if __name__ == "__main__":
    main()