#!/usr/bin/env python3
"""
MONITOR DE SAÚDE DO SISTEMA
Verifica se o sistema está respondendo corretamente
"""

import subprocess
import json
import time
from datetime import datetime

class HealthMonitor:
    def __init__(self):
        self.status_file = "/home/severosa/.openclaw/health_status.json"
        self.check_interval = 300  # 5 minutos
    
    def check_gateway(self):
        """Verificar se gateway está rodando"""
        try:
            result = subprocess.run(["pgrep", "-f", "openclaw-gateway"], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def check_whatsapp(self):
        """Verificar conexão WhatsApp"""
        try:
            # Verificar arquivos de credenciais
            import os
            whatsapp_path = "/home/severosa/.openclaw/credentials/whatsapp/default"
            if os.path.exists(whatsapp_path):
                files = os.listdir(whatsapp_path)
                return any(f.startswith("creds.json") for f in files)
            return False
        except:
            return False
    
    def check_telegram(self):
        """Verificar conexão Telegram"""
        try:
            # Verificar se token existe na config
            with open("/home/severosa/.openclaw/openclaw.json", "r") as f:
                config = json.load(f)
                return config.get("channels", {}).get("telegram", {}).get("enabled", False)
        except:
            return False
    
    def run_check(self):
        """Executar verificação completa"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "gateway": self.check_gateway(),
            "whatsapp_connected": self.check_whatsapp(),
            "telegram_enabled": self.check_telegram(),
            "status": "OK" if all([
                self.check_gateway(),
                self.check_whatsapp(),
                self.check_telegram()
            ]) else "WARNING"
        }
        
        # Salvar status
        with open(self.status_file, "w") as f:
            json.dump(status, f, indent=2)
        
        return status
    
    def log_status(self, status):
        """Registrar status"""
        log_file = "/home/severosa/.openclaw/health.log"
        with open(log_file, "a") as f:
            f.write(f"{status['timestamp']} - {status['status']}\n")

if __name__ == "__main__":
    monitor = HealthMonitor()
    status = monitor.run_check()
    monitor.log_status(status)
    print(json.dumps(status, indent=2))
