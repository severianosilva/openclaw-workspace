"""Agente de Design - Cria thumbnails, banners e elementos visuais"""

import json
import os
from datetime import datetime
from typing import Dict, List

class DesignAgent:
    def __init__(self, workspace_path: str):
        self.workspace = workspace_path
        os.makedirs(workspace_path, exist_ok=True)
        
    def create_channel_branding(self, channel: Dict) -> Dict:
        """Cria identidade visual do canal"""
        
        branding = {
            "channel_id": channel.get("id"),
            "logo": self._generate_logo_prompt(channel),
            "banner": self._generate_banner_prompt(channel),
            "color_palette": self._define_colors(channel.get("niche", "")),
            "fonts": self._select_fonts(),
            "thumbnail_template": self._create_thumbnail_template(channel)
        }
        
        filename = f"branding_{channel['id']}.json"
        with open(os.path.join(self.workspace, filename), 'w', encoding='utf-8') as f:
            json.dump(branding, f, indent=2, ensure_ascii=False)
        
        return branding
    
    def _generate_logo_prompt(self, channel: Dict) -> Dict:
        return {
            "prompt": f"minimalist logo for {channel.get('name')}, modern, professional, blue gradient, simple icon",
            "style": "flat design",
            "colors": "blue, white, dark gray",
            "size": "800x800"
        }
    
    def _generate_banner_prompt(self, channel: Dict) -> Dict:
        return {
            "prompt": f"YouTube banner for {channel.get('name')}, {channel.get('niche')} theme, professional, clean layout, 2560x1440",
            "elements": ["channel name", "tagline", "brand colors"],
            "text_spacing": "safe area on right"
        }
    
    def _define_colors(self, niche: str) -> Dict:
        colors = {
            "financas": {"primary": "#1a73e8", "secondary": "#4285f4", "accent": "#34a853"},
            "negocios": {"primary": "#34a853", "secondary": "#1a73e8", "accent": "#fbbc05"},
            "tecnologia": {"primary": "#ea4335", "secondary": "#4285f4", "accent": "#fbab00"},
            "saude": {"primary": "#4285f4", "secondary": "#34a853", "accent": "#fbbc05"}
        }
        return colors.get(niche, colors["tecnologia"])
    
    def _select_fonts(self) -> Dict:
        return {
            "title": "Roboto Bold",
            "body": "Roboto Regular",
            "thumbnail": "Anton, Oswald"
        }
    
    def _create_thumbnail_template(self, channel: Dict) -> Dict:
        return {
            "layout": "face on left, text on right",
            "colors": self._define_colors(channel.get("niche", "")),
            "elements": [
                "close-up face reaction (shock/surprise)",
                "large bold text (4-6 words)",
                "number badge (optional)",
                "brand color background"
            ],
            "dimensions": "1280x720",
            "safe_zone": "center 80%"
        }
    
    def create_thumbnail(self, script: Dict) -> Dict:
        """Gera prompt para thumbnail"""
        title_words = script.get("title", "").split()[:5]
        
        return {
            "prompt": f"YouTube thumbnail, dramatic face expression, text '{title_words[0]} {title_words[1]}', bold colors, high contrast",
            "text": " ".join(title_words[:4]).upper(),
            "hook": "Facial expression showing shock or surprise",
            "colors": "vibrant orange/red background"
        }