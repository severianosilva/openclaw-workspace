#!/usr/bin/env python3
"""YouTube Money Agents - Configuração CrewAI"""

from pathlib import Path
import json

BASE_DIR = Path(__file__).parent

# Configuração do CrewAI para YouTube
CREW_CONFIG = {
    "agents": [
        {
            "name": "Researcher",
            "role": "YouTube Topic Researcher",
            "goal": "Find high-CPM, trending topics for YouTube monetization",
            "backstory": "Expert in YouTube SEO and keyword research. Specializes in identifying profitable niches.",
            "tools": ["google_trends", "keyword_planner", "youtube_api"]
        },
        {
            "name": "Scriptwriter",
            "role": "YouTube Script Writer",
            "goal": "Create engaging, SEO-optimized video scripts",
            "backstory": "Professional content writer with 10+ years creating viral YouTube content.",
            "tools": ["gpt4", "seo_optimizer", "script_templates"]
        },
        {
            "name": "Designer",
            "role": "Visual Designer",
            "goal": "Create eye-catching thumbnails and channel branding",
            "backstory": "Graphic designer specializing in YouTube thumbnails with 5M+ views generated.",
            "tools": ["imagemagick", "canva_api", "color_palette"]
        },
        {
            "name": "VideoEditor",
            "role": "Video Editor",
            "goal": "Produce professional YouTube videos automatically",
            "backstory": "Video editing expert using FFmpeg and AI tools.",
            "tools": ["ffmpeg", "moviepy", "broll_library"]
        },
        {
            "name": "Publisher",
            "role": "YouTube Publisher",
            "goal": "Upload and optimize videos for maximum reach",
            "backstory": "YouTube automation specialist with proven growth strategies.",
            "tools": ["youtube_api", "seo_tools", "scheduler"]
        }
    ],
    "tasks": [
        {
            "agent": "Researcher",
            "description": "Research 10 profitable topics in the finance niche",
            "expected_output": "List of topics with CPM, search volume, and competition"
        },
        {
            "agent": "Scriptwriter",
            "description": "Write an 8-minute engaging script for the top topic",
            "expected_output": "Complete script with chapters, CTAs, and SEO metadata"
        },
        {
            "agent": "Designer",
            "description": "Create thumbnail and channel branding",
            "expected_output": "Thumbnail PNG and branding assets"
        },
        {
            "agent": "VideoEditor",
            "description": "Assemble final video with intro, content, and outro",
            "expected_output": "MP4 video file ready for upload"
        },
        {
            "agent": "Publisher",
            "description": "Upload video with optimized title and description",
            "expected_output": "Published YouTube video URL"
        }
    ]
}

# Requerimentos
REQUIREMENTS = """
# YouTube Money Agents - CrewAI Edition
crewai>=0.22.0
langchain>=0.1.0
langchain-openai>=0.0.2
python-dotenv>=1.0.0
pillow>=10.0.0
moviepy>=1.0.3
ffmpeg-python>=0.2.0
google-api-python-client>=2.100.0
google-auth-httplib2>=0.2.0
google-auth-oauthlib>=1.2.0
"""

def create_crewai_setup():
    """Cria arquivos de configuração CrewAI"""
    
    # requirements.txt
    with open(BASE_DIR / "requirements.txt", 'w') as f:
        f.write(REQUIREMENTS.strip())
    
    # crew_config.json
    with open(BASE_DIR / "crew_config.json", 'w') as f:
        json.dump(CREW_CONFIG, f, indent=2)
    
    print("[OK] Configuração CrewAI criada")

if __name__ == "__main__":
    create_crewai_setup()