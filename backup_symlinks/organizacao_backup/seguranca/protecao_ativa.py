#!/usr/bin/env python3
"""
SISTEMA DE PROTEÇÃO ATIVA - Firewall de Aplicação
Monitora e bloqueia atividades suspeitas em tempo real
"""

import os
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

class ActiveProtection:
    def __init__(self):
        self.whitelist_numbers = ["+5531982436396"]
        self.suspicious_patterns = [
            "device-list-*",  # Padrão de arquivos de dispositivo
        ]
        self.blocked_ips = set()
        self.last_check = None
        self.alert_threshold = 3  # Alertar após 3 falhas
        
        # Arquivos de controle
        self.blocklist_file = "/home/severosa/organizacao/seguranca/bloqueados.json"
        self.alert_log = "/home/severosa/organizacao/seguranca/logs/proteacao_ativa.log"
        
        # Carregar lista de bloqueados
        self.load_blocklist()
    
    def log(self, level, message):
        """Registrar log de proteção"""
        timestamp = datetime.now().isoformat()
        entry = f"[{timestamp}] [{level}] {message}"
        print(entry)
        
        with open(self.alert_log, "a") as f:
            f.write(entry + "\n")
    
    def load_blocklist(self):
        """Carregar lista de IPs/dispositivos bloqueados"""
        if os.path.exists(self.blocklist_file):
            with open(self.blocklist_file, "r") as f:
                data = json.load(f)
                self.blocked_ips = set(data.get("blocked", []))
    
    def save_blocklist(self):
        """Salvar lista de bloqueados"""
        with open(self.blocklist_file, "w") as f:
            json.dump({
                "blocked": list(self.blocked_ips),
                "updated": datetime.now().isoformat()
            }, f, indent=2)
    
    def check_whatsapp_devices(self):
        """Verificar dispositivos WhatsApp e bloquear suspeitos"""
        whatsapp_path = "/home/severosa/.openclaw/credentials/whatsapp/default"
        
        if not os.path.exists(whatsapp_path):
            return
        
        device_files = [f for f in os.listdir(whatsapp_path) if f.startswith("device-list-")]
        
        for device_file in device_files:
            device_id = device_file.replace("device-list-", "").replace(".json", "")
            
            if device_id not in self.whitelist_numbers:
                self.log("BLOCK", f"Dispositivo não autorizado bloqueado: {device_id}")
                self.quarantine_device(device_file, whatsapp_path)
    
    def quarantine_device(self, filename, source_path):
        """Mover dispositivo suspeito para quarentena"""
        quarantine_dir = "/home/severosa/organizacao/seguranca/quarentena"
        os.makedirs(quarantine_dir, exist_ok=True)
        
        # Mover arquivo
        source = os.path.join(source_path, filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = os.path.join(quarantine_dir, f"SUSPECT_{timestamp}_{filename}")
        
        try:
            os.rename(source, dest)
            self.log("ACTION", f"Dispositivo movido para quarentena: {dest}")
        except Exception as e:
            self.log("ERROR", f"Falha ao mover para quarentena: {e}")
    
    def monitor_file_changes(self):
        """Monitorar alterações em arquivos críticos"""
        critical_files = [
            "/home/severosa/.openclaw/openclaw.json",
        ]
        
        for file_path in critical_files:
            if os.path.exists(file_path):
                stat = os.stat(file_path)
                current_modified = stat.st_mtime
                
                # Verificar se foi modificado recentemente (últimos 5 minutos)
                if self.last_check and (current_modified > self.last_check.timestamp()):
                    self.log("ALERT", f"Arquivo crítico modificado: {file_path}")
    
    def run_protection_loop(self):
        """Loop principal de proteção"""
        self.log("INFO", "🛡️  Sistema de Proteção Ativa iniciado")
        self.log("INFO", f"Whitelist: {self.whitelist_numbers}")
        
        while True:
            try:
                self.last_check = datetime.now()
                
                # Verificar dispositivos
                self.check_whatsapp_devices()
                
                # Monitorar alterações
                self.monitor_file_changes()
                
                # Aguardar próxima verificação (a cada 30 segundos)
                time.sleep(30)
                
            except KeyboardInterrupt:
                self.log("INFO", "Proteção interrompida pelo usuário")
                break
            except Exception as e:
                self.log("ERROR", f"Erro no loop de proteção: {e}")
                time.sleep(5)

if __name__ == "__main__":
    protection = ActiveProtection()
    protection.run_protection_loop()
