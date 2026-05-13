"""Agente de Pesquisa - Encontra temas lucrativos"""

import json
import os
import random
from datetime import datetime
from typing import List, Dict

HIGH_CPM_CATEGORIES = {
    "financas": {"cpms": 25.50, "keywords": ["investimento", "cripto", "renda passiva"]},
    "negocios": {"cpms": 22.30, "keywords": ["empreendedorismo", "gestao", "marketing"]},
    "tecnologia": {"cpms": 18.75, "keywords": ["IA", "programacao", "gadgets"]},
    "saude": {"cpms": 15.20, "keywords": ["fitness", "nutricao", "bem-estar"]},
    "educacao": {"cpms": 12.80, "keywords": ["curso", "tutorial", "ensino"]}
}

class ResearchAgent:
    def __init__(self, memory_path: str):
        self.memory_path = memory_path
        
    def find_profitable_topics(self, niche: str = None, count: int = 5) -> List[Dict]:
        if niche and niche in HIGH_CPM_CATEGORIES:
            categories = {niche: HIGH_CPM_CATEGORIES[niche]}
        else:
            categories = HIGH_CPM_CATEGORIES
            
        topics = []
        for category, data in categories.items():
            for i in range(count // len(categories)):
                topic = {
                    "id": f"topic_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}",
                    "title": self._generate_topic_title(category, data["keywords"]),
                    "category": category,
                    "estimated_cpm": data["cpms"],
                    "keywords": data["keywords"][:3],
                    "competition": self._estimate_competition(category),
                    "potential_views": self._estimate_views(category),
                    "timestamp": str(datetime.now())
                }
                topics.append(topic)
        
        self._save_research(topics)
        return topics
    
    def _generate_topic_title(self, category: str, keywords: List) -> str:
        prefixes = ["Como ", "Guia Completo de ", "10 Dicas de ", "Curso de ", "Tudo sobre "]
        prefix = prefixes[random.randint(0, len(prefixes)-1)]
        keyword = keywords[random.randint(0, len(keywords)-1)]
        return f"{prefix}{keyword.title()} em 2024"
    
    def _estimate_competition(self, category: str) -> str:
        comp = {"financas": "alta", "negocios": "alta", "tecnologia": "média-alta", "saude": "média", "educacao": "média-baixa"}
        return comp.get(category, "média")
    
    def _estimate_views(self, category: str) -> int:
        ranges = {"financas": 50000, "negocios": 45000, "tecnologia": 60000, "saude": 35000, "educacao": 30000}
        return ranges.get(category, 25000)
    
    def _save_research(self, topics: List[Dict]):
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        research_file = os.path.join(os.path.dirname(self.memory_path), "research.json")
        
        existing = []
        if os.path.exists(research_file):
            try:
                with open(research_file, 'r') as f:
                    data = json.load(f)
                    existing = data if isinstance(data, list) else []
            except:
                existing = []
        
        existing.extend(topics)
        with open(research_file, 'w') as f:
            json.dump(existing, f, indent=2)