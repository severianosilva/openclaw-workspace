"""Agente de Upload - Publica vídeos no YouTube"""

import json
import os
from datetime import datetime
from typing import Dict, List

class UploadAgent:
    def __init__(self, workspace_path: str):
        self.workspace = workspace_path
        os.makedirs(workspace_path, exist_ok=True)
        
    def prepare_upload(self, video_data: Dict, script: Dict, channel: Dict) -> Dict:
        """Prepara dados para upload"""
        
        upload_data = {
            "video_file": f"{script['id']}_final.mp4",
            "title": script.get("seo_title", script.get("title")),
            "description": self._create_description(script, channel),
            "tags": script.get("tags", []) + ["2024"],
            "category": "Education",
            "privacy": "public",
            "schedule": self._best_publish_time(),
            "thumbnail": f"thumb_{script['id']}.png",
            "playlist": self._suggest_playlist(script, channel),
            "end_screen": self._end_screen_elements()
        }
        
        filename = f"upload_{script['id']}.json"
        with open(os.path.join(self.workspace, filename), 'w', encoding='utf-8') as f:
            json.dump(upload_data, f, indent=2, ensure_ascii=False)
        
        return upload_data
    
    def _create_description(self, script: Dict, channel: Dict) -> str:
        keywords = ", ".join(script.get("tags", []))
        return f"""{script.get('title')}

🔔 INSCREVA-SE: /channel/UC_{channel.get('id', 'default')}

⏱️ Timestamps:
00:00 Introdução
01:30 Conteúdo
05:00 Dicas
07:00 Conclusão

👉 Palavras-chave: {keywords}

#shorts #youtube #brasil #{' #'.join(script.get('tags', [])[:3])}
"""
    
    def _best_publish_time(self) -> Dict:
        return {
            "day": "Tuesday",
            "time": "18:00",
            "timezone": "America/Sao_Paulo",
            "reason": "High engagement for target demographic"
        }
    
    def _suggest_playlist(self, script: Dict, channel: Dict) -> str:
        niche = channel.get("niche", "general")
        return f"{niche.title()} - Série Completa"
    
    def _end_screen_elements(self) -> List[str]:
        return [
            "Subscribe button (top right)",
            "Next video (bottom left)",
            "Playlist link (bottom right)"
        ]
    
    def execute_upload(self, upload_data: Dict) -> Dict:
        """Simula upload (na versão real, usa YouTube API)"""
        return {
            "status": "uploaded",
            "video_id": f"vid_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "url": "https://youtube.com/watch?v=demo",
            "scheduled": upload_data.get("schedule", {}).get("time")
        }

class AudienceAgent:
    """Monitora audiência e ajusta estratégias"""
    
    def __init__(self, memory_path: str):
        self.memory_path = memory_path
        
    def monitor_audience(self, channel_id: str) -> Dict:
        """Analisa audiência em tempo real"""
        return {
            "watch_time_avg": "4:32",
            "audience_retention": "65%",
            "top_demographics": {"age": "18-24", "gender": "male", "location": "Brazil"},
            "traffic_sources": {"search": 45, "suggested": 30, "external": 25},
            "engagement_rate": "8.2%"
        }
    
    def adjust_strategy(self, metrics: Dict, content_plan: Dict) -> Dict:
        """Ajusta estratégia baseado em performance"""
        adjustments = []
        
        if metrics.get("audience_retention", 0) < 50:
            adjustments.append("Melhorar ganchos nos primeiros 15 segundos")
        
        if metrics.get("engagement_rate", 0) < 5:
            adjustments.append("Adicionar CTA mais cedo")
        
        return {
            "adjustments": adjustments,
            "new_content_focus": self._focus_suggestion(metrics),
            "optimal_length": "8-12 minutes"
        }
    
    def _focus_suggestion(self, metrics: Dict) -> str:
        traffic = metrics.get("traffic_sources", {})
        if traffic.get("search", 0) > 40:
            return "SEO otimizado"
        elif traffic.get("suggested", 0) > 30:
            return "Colaborações com outros criadores"
        else:
            return "Conteúdo evergreen"