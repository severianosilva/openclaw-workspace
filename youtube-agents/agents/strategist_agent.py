"""Agente Estrategista - Otimiza canal para monetizacao maxima"""

import json
import os
from datetime import datetime
from typing import Dict, List

class StrategistAgent:
    def __init__(self, memory_path: str):
        self.memory_path = memory_path
        os.makedirs(os.path.dirname(memory_path), exist_ok=True)
        
    def optimize_for_monetization(self, channel: Dict, topics: List[Dict]) -> Dict:
        """Cria estrategia completa de monetizacao"""
        
        strategy = {
            "channel_id": channel.get("id"),
            "phase": self._determine_phase(channel),
            "content_calendar": self._create_content_calendar(topics),
            "monetization_tactics": self._monetization_tactics(channel),
            "audience_growth": self._growth_strategy(),
            "revenue_projections": self._project_revenue(topics),
            "sprint_plan": self._sprint_plan()
        }
        
        self._save_strategy(strategy)
        return strategy
    
    def _determine_phase(self, channel: Dict) -> str:
        return "growth"
    
    def _create_content_calendar(self, topics: List[Dict]) -> Dict:
        calendar = {"monday": None, "wednesday": None, "friday": None}
        
        for i, topic in enumerate(topics[:3]):
            days = ["monday", "wednesday", "friday"]
            calendar[days[i]] = {
                "topic": topic.get("title"),
                "type": "main" if i % 2 == 0 else "shorts",
                "status": "planned"
            }
        
        return calendar
    
    def _monetization_tactics(self, channel: Dict) -> List[str]:
        return [
            "Focar em CPM alto (financas, negocios)",
            "Criar Shorts diarios para crescimento rapido",
            "Adicionar links de afiliado na descricao",
            "Fazer videos de antes/depois (alto engajamento)",
            "Usar titulos com numeros (7, 10, 5)",
            "Publicar no horario de pico (18h)"
        ]
    
    def _growth_strategy(self) -> List[str]:
        return [
            "Primeira semana: Shorts diarios",
            "Semana 2-3: Videos longos 2x por semana",
            "Semana 4+: Consistente 3x por semana",
            "Engajar em comunidades do niche",
            "Responder todos os comentarios"
        ]
    
    def _project_revenue(self, topics: List[Dict]) -> Dict:
        total_views = sum(t.get("potential_views", 0) for t in topics[:10])
        rpm = 15.0
        
        return {
            "month_1": round(total_views * 0.3 / 1000 * rpm, 2),
            "month_3": round(total_views * 0.7 / 1000 * rpm, 2),
            "month_6": round(total_views / 1000 * rpm, 2),
            "break_even_months": 3
        }
    
    def _sprint_plan(self) -> Dict:
        return {
            "sprint_1": "Setup + 5 shorts + 2 videos",
            "goal": "1000 subscribers",
            "tactics": "Shorts virais + SEO",
            "kpi": "CTR > 5%, Retencao > 50%"
        }
    
    def _save_strategy(self, strategy: Dict):
        filename = os.path.join(os.path.dirname(self.memory_path), "strategy.json")
        with open(filename, 'w') as f:
            json.dump(strategy, f, indent=2)