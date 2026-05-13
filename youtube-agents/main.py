#!/usr/bin/env python3
"""YouTube Money Agents - Sistema de Canais Rentáveis"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agents.research_agent import ResearchAgent
from agents.content_agent import ContentAgent
from agents.channel_agent import ChannelAgent
from agents.analytics_agent import AnalyticsAgent

BASE_DIR = Path(__file__).parent
MEMORY_FILE = BASE_DIR / "memory" / "research.json"
WORKSPACE = BASE_DIR / "workspace"

def init_system():
    """Inicializa sistema"""
    os.makedirs(BASE_DIR / "memory", exist_ok=True)
    os.makedirs(WORKSPACE, exist_ok=True)

def start_system():
    """Inicia sistema interativo"""
    init_system()
    print("[YOUTUBE AGENTS] Sistema Iniciado")
    print("Comandos: /new-channel <niche>, /research, /status, exit")
    
    current_channel = None
    
    while True:
        cmd = input("\n> ").strip()
        if cmd in ['exit', 'quit', 'q']:
            print("[END] Sistema encerrado")
            break
        elif cmd.startswith('/new-channel '):
            niche = cmd[13:]
            current_channel = create_channel(niche)
        elif cmd == '/research':
            topics = research_topics()
            show_topics(topics)
        elif cmd == '/status':
            show_status()
        elif cmd.startswith('/optimize '):
            if current_channel:
                optimize_channel(current_channel)
            else:
                print("Crie um canal primeiro com /new-channel")
        elif cmd == '/help':
            print("Comandos: /new-channel, /research, /optimize, /status, exit")
        elif cmd:
            print("Comando desconhecido. Digite /help")

def create_channel(niche: str) -> dict:
    """Cria novo canal"""
    print(f"\n[CHANNEL] Criando canal de {niche}...")
    
    channel_agent = ChannelAgent(str(MEMORY_FILE))
    channel = channel_agent.create_channel(niche)
    
    print(f"[OK] Canal criado: {channel['name']}")
    return channel

def research_topics(niche: str = None) -> list:
    """Pesquisa temas lucrativos"""
    print("\n[RESEARCH] Pesquisando temas...")
    
    research_agent = ResearchAgent(str(MEMORY_FILE))
    topics = research_agent.find_profitable_topics(niche or "finanças", count=5)
    
    return topics

def show_topics(topics: list):
    """Mostra temas pesquisados"""
    print("\n[TOPICS] Temas com potencial:")
    for t in topics:
        print(f"  - {t['title']}")
        print(f"    CPM: R$ {t['estimated_cpm']}, Views: {t['potential_views']}")

def optimize_channel(channel: dict):
    """Otimiza canal para monetização"""
    print("\n[OPTIMIZE] Analisando desempenho...")
    
    analytics = AnalyticsAgent(str(MEMORY_FILE))
    report = analytics.analyze_performance(channel)
    
    print(f"\n[ANALYTICS]")
    print(f"  Subscribers: {report['metrics']['subscribers']}")
    print(f"  RPM: R$ {report['metrics']['rpm']}")
    print(f"  Receita estimada: R$ {report['revenue_potential']['monthly_estimate']}")
    
    print("\n[RECOMMENDATIONS]")
    for rec in report['recommendations'][:3]:
        print(f"  - {rec}")

def show_status():
    """Mostra status do sistema"""
    print("\n[STATUS] YouTube Money Agents")
    print(f"  Workspace: {WORKSPACE}")
    print(f"  Memory: {MEMORY_FILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Money Agents")
    parser.add_argument("--start", action="store_true")
    parser.add_argument("--new-channel", help="Criar canal no nicho")
    parser.add_argument("--niche", help="Nicho para pesquisa")
    
    args = parser.parse_args()
    
    if args.start:
        start_system()
    elif args.new_channel:
        init_system()
        create_channel(args.new_channel)
        topics = research_topics(args.new_channel)
        show_topics(topics)
    elif args.niche:
        init_system()
        research_topics(args.niche)
    else:
        print("Uso: python main.py --start")
        print("     python main.py --new-channel 'finanças'")