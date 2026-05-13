#!/usr/bin/env python3
"""
MONITOR DE INTRUSÃO - Detecta comportamentos suspeitos em tempo real
"""

import json
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class IntrusionDetector(FileSystemEventHandler):
    def __init__(self):
        self.protected_paths = [
            "/home/severosa/.openclaw/credentials",
            "/home/severosa/.openclaw/openclaw.json"
        ]
        self.suspicious_patterns = [
            "device-list-",  # Arquivos de dispositivo
        ]
        
    def on_modified(self, event):
        if event.is_directory:
            return
        
        check_suspicious_file(event.src_path)
    
    def on_created(self, event):
        if event.is_directory:
            return
        
        check_suspicious_file(event.src_path)

def check_suspicious_file(filepath):
    """Verificar se arquivo é suspeito"""
    filename = os.path.basename(filepath)
    
    # Verificar padrões suspeitos
    if "device-list-" in filename:
        device_id = filename.replace("device-list-", "").replace(".json", "")
        
        # Se não for o número autorizado, alertar
        if device_id != "5531982436396":
            print(f"🚨 ALERTA: Dispositivo suspeito detectado: {device_id}")
            print(f"   Arquivo: {filepath}")
            print(f"   Ação: Remover imediatamente!")
            
            # Log do evento
            log_file = "/home/severosa/organizacao/seguranca/logs/intrusion_$(date +%Y%m%d).log"
            with open(log_file, "a") as f:
                f.write(f"{time.time()} | INTRUSION | {device_id} | {filepath}\n")
            
            # Tentar remover automaticamente
            try:
                os.remove(filepath)
                print(f"   ✅ Arquivo removido automaticamente")
            except:
                print(f"   ⚠️ Não foi possível remover automaticamente")

def start_monitoring():
    """Iniciar monitoramento contínuo"""
    print("🔍 Iniciando monitor de intrusão...")
    print("Monitorando: /home/severosa/.openclaw/credentials")
    
    # Verificar dispositivos existentes
    whatsapp_path = "/home/severosa/.openclaw/credentials/whatsapp/default"
    
    if os.path.exists(whatsapp_path):
        for filename in os.listdir(whatsapp_path):
            if filename.startswith("device-list-"):
                filepath = os.path.join(whatsapp_path, filename)
                check_suspicious_file(filepath)
    
    print("✅ Verificação inicial concluída")
    print("Monitoramento passivo ativo")
    print("Pressione Ctrl+C para parar")
    
    try:
        while True:
            time.sleep(10)
            # Verificação periódica
            if os.path.exists(whatsapp_path):
                for filename in os.listdir(whatsapp_path):
                    if filename.startswith("device-list-"):
                        filepath = os.path.join(whatsapp_path, filename)
                        check_suspicious_file(filepath)
    except KeyboardInterrupt:
        print("\n🛑 Monitoramento encerrado")

if __name__ == "__main__":
    start_monitoring()
