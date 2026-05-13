#!/usr/bin/env python3
"""
Sistema de precedentes jurídicos para consulta e análise
"""

import os
import json
import sqlite3
import sys
from datetime import datetime
from typing import Dict, List, Tuple
import re

class BancoPrecedentes:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.expanduser("~/organizacao/controle-prazos/precedentes.db")
        
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Criar tabela de precedentes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS precedentes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                tribunal TEXT,
                numero_processo TEXT,
                data_decisao DATE,
                ementa TEXT,
                decisao TEXT,
                legislacao_aplicavel TEXT,
                jurisprudencia_similar TEXT,
                areas_direito TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Criar índice para busca
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_areas_direito ON precedentes(areas_direito)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags ON precedentes(tags)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tribunal ON precedentes(tribunal)')
        
        conn.commit()
        conn.close()
    
    def adicionar_precedente(self, precedente: Dict):
        """Adiciona um novo precedente ao banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO precedentes 
            (titulo, tribunal, numero_processo, data_decisao, ementa, decisao, 
             legislacao_aplicavel, jurisprudencia_similar, areas_direito, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            precedente.get('titulo'),
            precedente.get('tribunal'),
            precedente.get('numero_processo'),
            precedente.get('data_decisao'),
            precedente.get('ementa'),
            precedente.get('decisao'),
            precedente.get('legislacao_aplicavel'),
            precedente.get('jurisprudencia_similar'),
            ','.join(precedente.get('areas_direito', [])),
            ','.join(precedente.get('tags', []))
        ))
        
        conn.commit()
        conn.close()
        
        print(f"Precedente adicionado: {precedente.get('titulo')}")
    
    def buscar_precedentes(self, termos: str = "", areas_direito: List[str] = None, tribunal: str = None, limite: int = 10) -> List[Dict]:
        """Busca precedentes com base em critérios"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Montar consulta SQL
        query = "SELECT * FROM precedentes WHERE 1=1"
        params = []
        
        if termos:
            query += " AND (titulo LIKE ? OR ementa LIKE ? OR decisao LIKE ?)"
            termo_busca = f"%{termos}%"
            params.extend([termo_busca, termo_busca, termo_busca])
        
        if areas_direito:
            areas_str = ','.join(areas_direito)
            query += " AND areas_direito LIKE ?"
            params.append(f"%{areas_str}%")
        
        if tribunal:
            query += " AND tribunal LIKE ?"
            params.append(f"%{tribunal}%")
        
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limite)
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        
        # Obter nomes das colunas
        colunas = [description[0] for description in cursor.description]
        
        # Converter resultados para dicionários
        precedentes = []
        for row in resultados:
            precedente = dict(zip(colunas, row))
            # Converter áreas do formato string de volta para lista
            if precedente['areas_direito']:
                precedente['areas_direito'] = precedente['areas_direito'].split(',')
            else:
                precedente['areas_direito'] = []
            
            if precedente['tags']:
                precedente['tags'] = precedente['tags'].split(',')
            else:
                precedente['tags'] = []
            
            precedentes.append(precedente)
        
        conn.close()
        return precedentes
    
    def buscar_por_similaridade(self, texto_referencia: str, limite: int = 5) -> List[Tuple[Dict, float]]:
        """Busca precedentes por similaridade com um texto de referência"""
        # Obter todos os precedentes
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM precedentes")
        resultados = cursor.fetchall()
        colunas = [description[0] for description in cursor.description]
        conn.close()
        
        precedentes_completos = []
        for row in resultados:
            precedente = dict(zip(colunas, row))
            if precedente['areas_direito']:
                precedente['areas_direito'] = precedente['areas_direito'].split(',')
            else:
                precedente['areas_direito'] = []
            
            if precedente['tags']:
                precedente['tags'] = precedente['tags'].split(',')
            else:
                precedente['tags'] = []
            
            precedentes_completos.append(precedente)
        
        # Calcular similaridade simples baseada em palavras-chave
        similaridades = []
        texto_ref_lower = texto_referencia.lower()
        
        for precedente in precedentes_completos:
            # Calcular pontuação de similaridade
            pontuacao = 0
            
            # Verificar em títulos
            if precedente['titulo'] and texto_ref_lower in precedente['titulo'].lower():
                pontuacao += 3
            
            # Verificar em ementa
            if precedente['ementa'] and texto_ref_lower in precedente['ementa'].lower():
                pontuacao += 2
            
            # Verificar em decisão
            if precedente['decisao'] and texto_ref_lower in precedente['decisao'].lower():
                pontuacao += 2
            
            # Verificar áreas do direito
            for area in precedente['areas_direito']:
                if area.lower() in texto_ref_lower:
                    pontuacao += 1
            
            # Verificar tags
            for tag in precedente['tags']:
                if tag.lower() in texto_ref_lower:
                    pontuacao += 1
            
            if pontuacao > 0:
                similaridades.append((precedente, pontuacao))
        
        # Ordenar por pontuação (similaridade) e retornar os melhores
        similaridades.sort(key=lambda x: x[1], reverse=True)
        return similaridades[:limite]

def adicionar_precedente_manual():
    """Função para adicionar precedente manualmente"""
    print("Adicionando precedente manualmente...")
    
    titulo = input("Título do precedente: ").strip()
    tribunal = input("Tribunal (opcional): ").strip()
    numero_processo = input("Número do processo (opcional): ").strip()
    data_decisao = input("Data da decisão (AAAA-MM-DD, opcional): ").strip()
    ementa = input("Ementa (resumo da decisão): ").strip()
    decisao = input("Decisão completa (opcional): ").strip()
    legislacao_aplicavel = input("Legislação aplicável (opcional): ").strip()
    jurisprudencia_similar = input("Jurisprudência similar (opcional): ").strip()
    
    areas_input = input("Áreas do direito (separadas por vírgula): ").strip()
    areas_direito = [area.strip() for area in areas_input.split(',')] if areas_input else []
    
    tags_input = input("Tags (separadas por vírgula): ").strip()
    tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
    
    precedente = {
        'titulo': titulo,
        'tribunal': tribunal,
        'numero_processo': numero_processo,
        'data_decisao': data_decisao,
        'ementa': ementa,
        'decisao': decisao,
        'legislacao_aplicavel': legislacao_aplicavel,
        'jurisprudencia_similar': jurisprudencia_similar,
        'areas_direito': areas_direito,
        'tags': tags
    }
    
    banco = BancoPrecedentes()
    banco.adicionar_precedente(precedente)
    print("Precedente adicionado com sucesso!")

def buscar_precedentes_interativo():
    """Função para busca interativa de precedentes"""
    print("Buscando precedentes...")
    
    termos = input("Termos para busca (opcional): ").strip()
    areas_input = input("Áreas do direito (separadas por vírgula, opcional): ").strip()
    tribunal = input("Tribunal (opcional): ").strip()
    
    areas_direito = [area.strip() for area in areas_input.split(',')] if areas_input else []
    
    banco = BancoPrecedentes()
    resultados = banco.buscar_precedentes(
        termos=termos,
        areas_direito=areas_direito,
        tribunal=tribunal,
        limite=10
    )
    
    if resultados:
        print(f"\nEncontrados {len(resultados)} precedentes:")
        print("="*50)
        
        for i, precedente in enumerate(resultados, 1):
            print(f"{i}. {precedente['titulo']}")
            print(f"   Tribunal: {precedente['tribunal']}")
            print(f"   Processo: {precedente['numero_processo']}")
            print(f"   Data: {precedente['data_decisao']}")
            print(f"   Áreas: {', '.join(precedente['areas_direito'])}")
            print(f"   Tags: {', '.join(precedente['tags'])}")
            print(f"   Ementa: {precedente['ementa'][:100]}...")
            print("-" * 50)
    else:
        print("Nenhum precedente encontrado.")

def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python sistema_precedentes.py adicionar     # Adiciona precedente manualmente")
        print("  python sistema_precedentes.py buscar        # Busca precedentes")
        print("  python sistema_precedentes.py buscar_similar <texto>  # Busca por similaridade")
        sys.exit(1)
    
    comando = sys.argv[1]
    
    if comando == "adicionar":
        adicionar_precedente_manual()
    elif comando == "buscar":
        buscar_precedentes_interativo()
    elif comando == "buscar_similar":
        if len(sys.argv) < 3:
            print("Uso: python sistema_precedentes.py buscar_similar <texto_referencia>")
            sys.exit(1)
        
        texto_referencia = ' '.join(sys.argv[2:])
        banco = BancoPrecedentes()
        resultados = banco.buscar_por_similaridade(texto_referencia, limite=5)
        
        if resultados:
            print(f"\nEncontrados {len(resultados)} precedentes similares:")
            print("="*50)
            
            for i, (precedente, pontuacao) in enumerate(resultados, 1):
                print(f"{i}. {precedente['titulo']} (Similaridade: {pontuacao})")
                print(f"   Tribunal: {precedente['tribunal']}")
                print(f"   Ementa: {precedente['ementa'][:100]}...")
                print("-" * 50)
        else:
            print("Nenhum precedente similar encontrado.")
    else:
        print("Comando inválido. Use 'adicionar', 'buscar' ou 'buscar_similar'.")
        sys.exit(1)

if __name__ == "__main__":
    main()