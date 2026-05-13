"""Agente de Monetização - Maximiza receita do canal"""

from typing import Dict, List

class MonetizationAgent:
    def __init__(self):
        self.strategies = {
            "content": [],
            "audience": [],
            "revenue": []
        }
    
    def optimize_for_max_revenue(self, channel: Dict, topics: List[Dict]) -> Dict:
        """Gera plano de monetização"""
        
        plan = {
            "channel_name": channel.get("name"),
            "estimated_monthly_revenue": self._calculate_potential(topics),
            "optimization_plan": self._create_optimization_plan(channel, topics),
            "affiliate_opportunities": self._find_affiliates(topics),
            "sponsorship_targets": self._identify_sponsors(channel),
            "shorts_strategy": self._shorts_plan()
        }
        
        return plan
    
    def _calculate_potential(self, topics: List[Dict]) -> Dict:
        """Calcula potencial de receita"""
        monthly_views = sum(t.get("potential_views", 0) for t in topics[:10]) * 4
        rpm = 15.0
        monthly_revenue = (monthly_views / 1000) * rpm
        
        return {
            "monthly_views": monthly_views,
            "rpm": rpm,
            "estimated_revenue": round(monthly_revenue, 2),
            "break_even_views": 10000
        }
    
    def _create_optimization_plan(self, channel: Dict, topics: List[Dict]) -> List[str]:
        """Plano de otimização"""
        return [
            "Upload diario de Shorts para crescer rapidamente",
            "Focar em titulos com numeros (7, 10, 5)",
            "Adicionar ganchos em primeiros 5 segundos",
            "Criar playlists por sub-tema",
            "Usar hashtags trending #Shorts #Viral",
            "Publicar sempre no mesmo horario (18h)",
            "Responder comentarios para engagement"
        ]
    
    def _find_affiliates(self, topics: List[Dict]) -> List[str]:
        """Encontra programas de afiliados"""
        affiliates = {
            "financas": ["Hotmart", "Monetizze", "Eduzz", "Amazon Associados"],
            "negocios": ["Hotmart", "Monetizze", "ClickBank"],
            "tecnologia": ["Amazon", "AliExpress", "Programas OEM"],
            "saude": ["Hotmart", "Afiliado Livre"],
            "educacao": ["Udemy", "Hotmart", "Coursify"]
        }
        
        result = []
        for topic in topics[:3]:
            cat = topic.get("category", "")
            result.extend(affiliates.get(cat, ["Hotmart"]))
        
        return list(set(result))
    
    def _identify_sponsors(self, channel: Dict) -> List[str]:
        """Identifica patrocinadores ideais"""
        sponsors = {
            "financas": ["XP Investimentos", "Clear", "Inter", "PicPay"],
            "negocios": ["Shopee", "Mercado Livre", "Amazon"],
            "tecnologia": ["Samsung", "Apple", "Google"],
            "saude": ["Drogaria SP", "Raia Drogasil"],
            "educacao": ["Khan Academy", "Curso em Video"]
        }
        
        return sponsors.get(channel.get("niche", ""), ["Hotmart", "Amazon"])
    
    def _shorts_plan(self) -> Dict:
        """Plano para Shorts"""
        return {
            "frequency": "1 por dia",
            "format": "Antes/Depois, Dica rapida, Erro comum",
            "hooks": ["Você sabia?", "99% dos caras não sabem disso", "ISSO aqui muda tudo"],
            "revenue_boost": "2-5x mais rapido que videos longos"
        }