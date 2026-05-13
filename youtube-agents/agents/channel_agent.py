"""Agente do Canal - Gerencia canal YouTube"""

import json
import os
from datetime import datetime
from typing import Dict

class ChannelAgent:
    def __init__(self, memory_path: str):
        self.memory_path = memory_path
        self.channel_data = self._load_or_create_channel()
        
    def create_channel(self, niche: str, name: str = None) -> Dict:
        """Cria configuração de canal"""
        
        channel = {
            "id": f"channel_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "name": name or f"{niche.title()} Master",
            "niche": niche,
            "created_at": str(datetime.now()),
            "branding": self._generate_branding(niche),
            "content_strategy": self._define_strategy(niche),
            "posting_schedule": self._create_schedule()
        }
        
        self.channel_data = channel
        self._save_channel()
        return channel
    
    def _generate_branding(self, niche: str) -> Dict:
        colors = {
            "financas": {"primary": "#1a73e8", "secondary": "#4285f4"},
            "negocios": {"primary": "#34a853", "secondary": "#1a73e8"},
            "tecnologia": {"primary": "#ea4335", "secondary": "#fbab00"},
            "saude": {"primary": "#4285f4", "secondary": "#34a853"}
        }
        
        return {
            "logo_prompt": f"Modern minimalist logo for {niche} channel, professional, blue colors",
            "banner_prompt": f"Professional banner for {niche} YouTube channel, clean design",
            "colors": colors.get(niche, colors["tecnologia"])
        }
    
    def _define_strategy(self, niche: str) -> Dict:
        return {
            "content_type": ["educational", "tutorial", "listicle"],
            "target_audience": "18-35 years old",
            "upload_frequency": "3 videos per week",
            "best_times": ["18:00", "20:00"],
            "shorts_ratio": 0.3
        }
    
    def _create_schedule(self) -> Dict:
        return {
            "monday": "main_video",
            "wednesday": "shorts",
            "friday": "main_video",
            "weekends": "community_posts"
        }
    
    def _load_or_create_channel(self) -> Dict:
        if os.path.exists(self.memory_path):
            with open(self.memory_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_channel(self):
        with open(self.memory_path, 'w') as f:
            json.dump(self.channel_data, f, indent=2)