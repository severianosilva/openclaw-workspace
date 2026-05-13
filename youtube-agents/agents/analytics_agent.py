"""Agente de Analytics - Monitora desempenho do canal"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List

class AnalyticsAgent:
    def __init__(self, memory_path: str):
        self.memory_path = memory_path
        os.makedirs(os.path.dirname(memory_path), exist_ok=True)
        
    def analyze_performance(self, channel_data: Dict) -> Dict:
        """Analisa desempenho e sugere otimizações"""
        
        report = {
            "timestamp": str(datetime.now()),
            "channel_id": channel_data.get("id"),
            "metrics": self._get_current_metrics(),
            "growth_rate": self._calculate_growth(),
            "revenue_potential": self._calculate_revenue(),
            "recommendations": self._generate_recommendations()
        }
        
        self._save_report(report)
        return report
    
    def _get_current_metrics(self) -> Dict:
        """Simula métricas atuais do canal"""
        import random
        return {
            "subscribers": random.randint(100, 10000),
            "total_views": random.randint(1000, 100000),
            "avg_watch_time": "4:30",
            "ctr": f"{random.uniform(2.5, 8.5):.1f}%",
            "rpm": round(random.uniform(5.0, 25.0), 2)
        }
    
    def _calculate_growth(self) -> Dict:
        """Calcula taxa de crescimento"""
        import random
        return {
            "daily_growth": f"{random.uniform(1.0, 5.0):.1f}%",
            "weekly_growth": f"{random.uniform(5.0, 15.0):.1f}%",
            "subscriber_velocity": random.randint(10, 200)
        }
    
    def _calculate_revenue(self) -> Dict:
        """Calcula potencial de receita"""
        return {
            "monthly_estimate": 300.00,
            "break_even_views": 10000,
            "projected_months_to_monetize": 3
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Gera recomendações baseadas em analytics"""
        return [
            "Aumentar frequência de uploads para 4x por semana",
            "Focar em Shorts para ganhar subs mais rápido",
            "Melhorar thumbnails com rostos e cores vibrantes",
            "Criar playlist por tema para aumentar watch time",
            "Fazer collab com canais similares"
        ]
    
    def optimize_for_revenue(self, script: Dict) -> Dict:
        """Otimiza roteiro para monetização"""
        optimizations = {
            "title": f"[URGENTE] {script['title']} - Você Precisa Ver Isso!",
            "description_addition": "\n\n💰 Ganhe dinheiro com este método - afiliado!",
            "tags_addition": ["2024", "grátis", "rápido"],
            "cta_timing": "Adicionar CTA nos primeiros 30 segundos"
        }
        return optimizations
    
    def _save_report(self, report: Dict):
        report_file = os.path.join(os.path.dirname(self.memory_path), "analytics.json")
        
        reports = []
        if os.path.exists(report_file):
            with open(report_file, 'r') as f:
                reports = json.load(f)
        
        reports.append(report)
        with open(report_file, 'w') as f:
            json.dump(reports[-10:], f, indent=2)  # Keep last 10 reports