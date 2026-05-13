#!/usr/bin/env python3
"""Demonstração completa do sistema YouTube Money Agents"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agents.research_agent import ResearchAgent
from agents.content_agent import ContentAgent
from agents.channel_agent import ChannelAgent
from agents.analytics_agent import AnalyticsAgent
from agents.monetization_agent import MonetizationAgent

BASE_DIR = Path(__file__).parent
MEMORY_FILE = BASE_DIR / "memory" / "demo.json"

def run_demo():
    """Executa demonstração completa"""
    print("=" * 60)
    print("YOUTUBE MONEY AGENTS - DEMO COMPLETA")
    print("=" * 60)
    
    # 1. Criar Canal
    print("\n[1] Criando canal de finanças...")
    channel_agent = ChannelAgent(str(MEMORY_FILE))
    channel = channel_agent.create_channel("finanças", "Money Master BR")
    print(f"   Canal: {channel['name']}")
    print(f"   Estratégia: {channel['content_strategy']['upload_frequency']}")
    
    # 2. Pesquisar Temas
    print("\n[2] Pesquisando temas lucrativos...")
    research_agent = ResearchAgent(str(MEMORY_FILE))
    topics = research_agent.find_profitable_topics("finanças", count=3)
    print(f"   Encontrados {len(topics)} temas")
    for t in topics:
        print(f"   - {t['title']} (CPM: R$ {t['estimated_cpm']})")
    
    # 3. Criar Roteiros
    print("\n[3] Criando roteiros...")
    content_agent = ContentAgent(str(BASE_DIR / "workspace"))
    scripts = []
    for topic in topics[:2]:
        script = content_agent.create_script(topic)
        scripts.append(script)
        print(f"   Roteiro: {script['title'][:40]}...")
        print(f"   Receita estimada: R$ {script['estimated_revenue']['estimated_revenue']}")
    
    # 4. Analisar Performance
    print("\n[4] Analisando performance...")
    analytics = AnalyticsAgent(str(MEMORY_FILE))
    report = analytics.analyze_performance(channel)
    print(f"   Subscribers estimados: {report['metrics']['subscribers']}")
    print(f"   RPM: R$ {report['metrics']['rpm']}")
    
    # 5. Monetização
    print("\n[5] Plano de monetização...")
    monetization = MonetizationAgent()
    monetization_plan = monetization.optimize_for_max_revenue(channel, topics)
    print(f"   Receita mensal estimada: R$ {monetization_plan['estimated_monthly_revenue']['estimated_revenue']}")
    print(f"   Afiliados recomendados: {', '.join(monetization_plan['affiliate_opportunities'][:3])}")
    
    print("\n" + "=" * 60)
    print("DEMO CONCLUÍDA - Arquivos em workspace/")
    print("=" * 60)

if __name__ == "__main__":
    run_demo()