"""Agente Planejador - Decompõe requisições em tarefas executáveis"""

from typing import List, Dict
from datetime import datetime

class PlannerAgent:
    def __init__(self, memory_path: str):
        self.memory_path = memory_path
    
    def analyze_request(self, request: str) -> Dict:
        """Analisa requisição e cria plano"""
        return {
            "request": request,
            "complexity": self._assess_complexity(request),
            "estimated_time": self._estimate_time(request),
            "required_skills": self._identify_skills(request)
        }
    
    def _assess_complexity(self, request: str) -> str:
        keywords = {"API": 3, "database": 4, "auth": 3, "simple": 1}
        score = sum(v for k, v in keywords.items() if k.lower() in request.lower())
        if score >= 6: return "alta"
        if score >= 3: return "média"
        return "baixa"
    
    def _estimate_time(self, request: str) -> int:
        # minutos estimados
        return 30 if "API" in request else 15
    
    def _identify_skills(self, request: str) -> List[str]:
        skills = []
        if "API" in request: skills.append("backend")
        if "database" in request.lower(): skills.append("database")
        if "frontend" in request.lower() or "React" in request: skills.append("frontend")
        return skills or ["general"]