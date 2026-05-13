#!/usr/bin/env python3
"""Sistema de Agentes Autonomos para Desenvolvimento"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from agents.planner import PlannerAgent
from agents.coder import CoderAgent

BASE_DIR = Path(__file__).parent
MEMORY_FILE = BASE_DIR / "memory" / "agent_memory.json"
WORKSPACE = BASE_DIR / "workspace"

def init_memory():
    """Inicializa arquivo de memoria"""
    os.makedirs(BASE_DIR / "memory", exist_ok=True)
    os.makedirs(WORKSPACE, exist_ok=True)
    if not MEMORY_FILE.exists():
        with open(MEMORY_FILE, 'w') as f:
            json.dump({"tasks": [], "agents": {}, "created": str(datetime.now())}, f, indent=2)

def start_system():
    """Inicia o sistema de agentes"""
    init_memory()
    print("[START] Sistema de Agentes Autonomos Iniciado")
    print("Comandos: /req <tarefa>, /status, /help, exit")
    
    while True:
        cmd = input("\n> ").strip()
        if cmd in ['exit', 'quit', 'q']:
            print("[END] Sistema encerrado")
            break
        elif cmd.startswith('/req '):
            request = cmd[5:]
            process_request(request)
        elif cmd == '/status':
            show_status()
        elif cmd == '/help':
            print("Comandos: /req <tarefa>, /status, /help, exit")
        elif cmd:
            print("Comando desconhecido")

def process_request(request):
    """Processa requisicao usando agentes autonomos"""
    print(f"\n[PLAN] Processando: {request}")
    
    # Planner Agent
    planner = PlannerAgent(str(MEMORY_FILE))
    plan = planner.analyze_request(request)
    
    # Coder Agent
    coder = CoderAgent(str(WORKSPACE))
    filename = coder.generate_code(plan)
    
    # Salva historico
    save_task(request, plan, filename)
    
    print(f"[DONE] Codigo gerado: workspace/{filename}")
    print(f"[FILE] Abra o arquivo para ver o resultado")
    
def save_task(request, plan, filename):
    """Salva tarefa na memoria"""
    with open(MEMORY_FILE, 'r') as f:
        memory = json.load(f)
    memory["tasks"].append({
        "id": f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "request": request,
        "plan": plan,
        "output": filename,
        "timestamp": str(datetime.now())
    })
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)

def show_status():
    """Mostra status do sistema"""
    with open(MEMORY_FILE, 'r') as f:
        memory = json.load(f)
    
    print(f"\n[STATUS] Tarefas: {len(memory['tasks'])}")
    for t in memory['tasks'][-5:]:
        print(f"  - {t['id']}: {t['request'][:40]}...")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", action="store_true")
    parser.add_argument("--request", "-r")
    
    args = parser.parse_args()
    
    if args.start:
        start_system()
    elif args.request:
        init_memory()
        process_request(args.request)
    else:
        print("Uso: python main.py --start  ou  --request 'sua requisicao'")