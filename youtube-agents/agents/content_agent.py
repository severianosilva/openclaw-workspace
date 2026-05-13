"""Agente de Conteúdo - Cria roteiros otimizados para YouTube"""

import json
import os
from datetime import datetime
from typing import Dict, List

class ContentAgent:
    def __init__(self, workspace_path: str):
        self.workspace = workspace_path
        os.makedirs(workspace_path, exist_ok=True)
        
    def create_script(self, topic: Dict, duration: int = 8) -> Dict:
        """Cria roteiro otimizado para engajamento"""
        
        script = {
            "id": f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "topic_id": topic.get("id"),
            "title": topic.get("title"),
            "duration_minutes": duration,
            "seo_title": self._optimize_title(topic.get("title", "")),
            "description": self._create_description(topic),
            "tags": self._generate_tags(topic),
            "chapters": self._create_chapters(topic, duration),
            "call_to_action": [
                "Inscreva-se para mais conteúdo",
                "Deixe seu like se foi útil",
                "Comente sua dúvida"
            ],
            "estimated_revenue": self._estimate_revenue(topic, duration)
        }
        
        filename = f"script_{topic['id']}.json"
        with open(os.path.join(self.workspace, filename), 'w', encoding='utf-8') as f:
            json.dump(script, f, indent=2, ensure_ascii=False)
        
        return script
    
    def _optimize_title(self, title: str) -> str:
        prefixes = ["COMO FAZER", "APRENDA", "GUIA DEFINITIVO"]
        return f"{prefixes[0]}: {title.upper()}"
    
    def _create_description(self, topic: Dict) -> str:
        keywords = ", ".join(topic.get("keywords", []))
        return f"""
📌 {topic.get('title')}

🔍 Neste vídeo você vai aprender sobre {keywords}

⏰ Timestamps:
00:00 Introdução
01:30 Conteúdo principal
{datetime.now().strftime('%M:%S')} Conclusão

👉 INSCREVA-SE: /channel/UC_example

#shorts #youtube #brasil
"""
    
    def _generate_tags(self, topic: Dict) -> List[str]:
        base_tags = ["educacional", "tutorial", "como fazer"]
        base_tags.extend(topic.get("keywords", []))
        return base_tags[:15]
    
    def _create_chapters(self, topic: Dict, duration: int) -> List[Dict]:
        return [
            {"time": "00:00", "title": "Introdução", "hook": True},
            {"time": "00:30", "title": f"O que é {topic.get('category', 'topic')}", "content": True},
            {"time": "02:00", "title": "Passo a passo prático", "content": True},
            {"time": "05:00", "title": "Dicas e truques", "content": True},
            {"time": f"{duration-2:02d}:00", "title": "Conclusão e CTA", "cta": True}
        ]
    
    def _estimate_revenue(self, topic: Dict, duration: int) -> Dict:
        cpm = topic.get("estimated_cpm", 15)
        views = topic.get("potential_views", 25000)
        revenue = (views / 1000) * cpm * 0.6
        return {
            "estimated_views": views,
            "estimated_revenue": round(revenue, 2),
            "break_even_days": 30
        }