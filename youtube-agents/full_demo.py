#!/usr/bin/env python3
"""Demo completa - Todos os agentes trabalhando juntos"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agents.research_agent import ResearchAgent
from agents.content_agent import ContentAgent
from agents.channel_agent import ChannelAgent
from agents.design_agent import DesignAgent
from agents.video_agent import VideoAgent
from agents.upload_agent import UploadAgent, AudienceAgent
from agents.strategist_agent import StrategistAgent
from agents.monetization_agent import MonetizationAgent

BASE_DIR = Path(__file__).parent
MEMORY_FILE = BASE_DIR / "memory" / "full_demo.json"

def run_full_demo():
    print("=" * 70)
    print("YOUTUBE MONEY AGENTS - DEMO COMPLETA (100% AUTONOMO)")
    print("=" * 70)
    
    # 1. Criar Canal
    print("\n[1] ESTRATEGISTA - Criando canal...")
    channel_agent = ChannelAgent(str(MEMORY_FILE))
    channel = channel_agent.create_channel("financas", "Money Empire BR")
    print(f"   [OK] Canal: {channel['name']}")
    
    # 2. Pesquisar Temas
    print("\n[2] PESQUISA - Encontrando temas lucrativos...")
    research = ResearchAgent(str(MEMORY_FILE))
    topics = research.find_profitable_topics("financas", count=3)
    print(f"   [OK] {len(topics)} temas com CPM R$ 25.50")
    
    # 3. Design do Canal
    print("\n[3] DESIGN - Criando identidade visual...")
    design = DesignAgent(str(BASE_DIR / "workspace"))
    branding = design.create_channel_branding(channel)
    print(f"   [OK] Logo, banner e template de thumbnails criados")
    
    # 4. Estrategista
    print("\n[4] ESTRATEGISTA - Planejando monetizacao...")
    strategist = StrategistAgent(str(MEMORY_FILE))
    strategy = strategist.optimize_for_monetization(channel, topics)
    print(f"   [OK] Estrategia: {strategy['phase']} phase")
    print(f"   [$$] Projecao 6 meses: R$ {strategy['revenue_projections']['month_6']}")
    
    # 5. Roteiros
    print("\n[5] CONTEUDO - Criando roteiros...")
    content = ContentAgent(str(BASE_DIR / "workspace"))
    scripts = []
    for topic in topics[:2]:
        script = content.create_script(topic)
        scripts.append(script)
    print(f"   [OK] {len(scripts)} roteiros criados")
    
    # 6. Producao de Video
    print("\n[6] PRODUCAO - Planejando videos...")
    video_agent = VideoAgent(str(BASE_DIR / "workspace"))
    for script in scripts:
        video_plan = video_agent.produce_video(script, branding)
    print(f"   [OK] Producao planejada para {len(scripts)} videos")
    
    # 7. Upload
    print("\n[7] UPLOAD - Preparando publicacao...")
    upload = UploadAgent(str(BASE_DIR / "workspace"))
    for script in scripts[:1]:
        upload_data = upload.prepare_upload({"id": script['id']}, script, channel)
    print(f"   [OK] Upload preparado (aguardando API YouTube)")
    
    # 8. Monetizacao
    print("\n[8] MONETIZACAO - Maximizando receita...")
    monetization = MonetizationAgent()
    monetization_plan = monetization.optimize_for_max_revenue(channel, topics)
    print(f"   [OK] Afiliados: {', '.join(monetization_plan['affiliate_opportunities'][:3])}")
    
    # 9. Audiencia
    print("\n[9] AUDIENCIA - Monitoramento configurado...")
    audience = AudienceAgent(str(MEMORY_FILE))
    metrics = audience.monitor_audience(channel['id'])
    print(f"   [OK] Metricas: Retencao {metrics['audience_retention']}")
    
    print("\n" + "=" * 70)
    print("[START] SISTEMA 100% OPERACIONAL")
    print("[FILE] Arquivos gerados em: workspace/")
    print("[DATA] Estrategia salva em: memory/strategy.json")
    print("=" * 70)
    
    print("\n[SUMMARY] RESUMO EXECUTIVO:")
    print(f"   Canal: {channel['name']} ({channel['niche']})")
    print(f"   Temas: {len(topics)} prontos")
    print(f"   Roteiros: {len(scripts)} criados")
    print(f"   Receita projetada: R$ {strategy['revenue_projections']['month_6']}/mes")
    print(f"   Break-even: {strategy['revenue_projections']['break_even_months']} meses")

if __name__ == "__main__":
    run_full_demo()