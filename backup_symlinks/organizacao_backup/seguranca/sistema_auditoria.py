#!/usr/bin/env python3
"""
SISTEMA DE AUDITORIA E SEGURANÇA - OpenClaw
Monitoramento contínuo para prevenir invasões e anomalias
"""

import json
import os
import hashlib
import datetime
import subprocess
from pathlib import Path

class SecurityAuditor:
    def __init__(self):
        self.config_path = "/home/severosa/.openclaw/openclaw.json"
        self.credentials_path = "/home/severosa/.openclaw/credentials"
        self.log_path = "/home/severosa/organizacao/seguranca/logs"
        self.whitelist_devices = ["+553182436396", "553182436396"]  # Seu número (com e sem +)
        self.known_hashes = {}
        
        # Criar diretório de logs
        os.makedirs(self.log_path, exist_ok=True)
    
    def log_event(self, level, message, details=None):
        """Registrar evento de segurança"""
        timestamp = datetime.datetime.now().isoformat()
        event = {
            "timestamp": timestamp,
            "level": level,
            "message": message,
            "details": details or {}
        }
        
        log_file = os.path.join(self.log_path, f"security_{datetime.date.today()}.log")
        with open(log_file, "a") as f:
            f.write(json.dumps(event) + "\n")
        
        # Alertas críticos
        if level == "CRITICAL":
            self.send_alert(event)
        
        return event
    
    def send_alert(self, event):
        """Enviar alerta para canais de comunicação"""
        alert_msg = f"🚨 ALERTA DE SEGURANÇA\n\n{event['message']}\n\nTimestamp: {event['timestamp']}"
        print(alert_msg)
    
    def check_whatsapp_credentials(self):
        """Verificar credenciais do WhatsApp"""
        whatsapp_path = os.path.join(self.credentials_path, "whatsapp", "default")
        
        if not os.path.exists(whatsapp_path):
            self.log_event("WARNING", "Diretório de credenciais WhatsApp não existe")
            return False
        
        # Verificar arquivos de dispositivo
        device_files = [f for f in os.listdir(whatsapp_path) if f.startswith("device-list-")]
        
        suspicious_devices = []
        for device_file in device_files:
            # Extrair número do arquivo
            device_id = device_file.replace("device-list-", "").replace(".json", "")
            
            # Normalizar (adicionar + se não tiver)
            if not device_id.startswith("+"):
                device_id_normalized = "+" + device_id
            else:
                device_id_normalized = device_id
            
            # Verificar se é dispositivo autorizado
            if device_id not in self.whitelist_devices:
                suspicious_devices.append(device_id)
                self.log_event("CRITICAL", 
                    f"Dispositivo não autorizado detectado: {device_id}",
                    {"file": device_file, "action": "REMOVER_IMEDIATAMENTE"})
        
        if suspicious_devices:
            return False
        
        self.log_event("INFO", f"Credenciais WhatsApp verificadas: {len(device_files)} dispositivo(s) autorizado(s)")
        return True
    
    def check_config_integrity(self):
        """Verificar integridade do arquivo de configuração"""
        if not os.path.exists(self.config_path):
            self.log_event("CRITICAL", "Arquivo de configuração não encontrado!")
            return False
        
        # Calcular hash atual
        with open(self.config_path, "rb") as f:
            current_hash = hashlib.sha256(f.read()).hexdigest()
        
        # Verificar contra hash conhecido
        hash_file = os.path.join(self.log_path, "config_hash.json")
        
        if os.path.exists(hash_file):
            with open(hash_file, "r") as f:
                known_hashes = json.load(f)
        else:
            known_hashes = {}
        
        if known_hashes.get("last_known") and known_hashes["last_known"] != current_hash:
            self.log_event("WARNING", 
                "Arquivo de configuração foi modificado",
                {"previous": known_hashes["last_known"][:16], "current": current_hash[:16]})
        
        # Atualizar hash conhecido
        known_hashes["last_known"] = current_hash
        known_hashes["last_check"] = datetime.datetime.now().isoformat()
        
        with open(hash_file, "w") as f:
            json.dump(known_hashes, f, indent=2)
        
        self.log_event("INFO", "Integridade da configuração verificada")
        return True
    
    def check_active_sessions(self):
        """Verificar sessões ativas"""
        sessions_path = "/home/severosa/.openclaw/agents/main/sessions"
        
        if not os.path.exists(sessions_path):
            return True
        
        session_files = [f for f in os.listdir(sessions_path) if f.endswith(".jsonl")]
        
        self.log_event("INFO", f"Sessões ativas: {len(session_files)}")
        return True
    
    def check_gateway_process(self):
        """Verificar se o gateway está rodando"""
        try:
            result = subprocess.run(["pgrep", "-f", "openclaw-gateway"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                pids = result.stdout.strip().split("\n")
                self.log_event("INFO", f"Gateway rodando com {len(pids)} processo(s)")
                return True
            else:
                self.log_event("WARNING", "Gateway não está rodando!")
                return False
        except Exception as e:
            self.log_event("ERROR", f"Erro ao verificar gateway: {str(e)}")
            return False
    
    def run_full_audit(self):
        """Executar auditoria completa"""
        self.log_event("INFO", "=== INICIANDO AUDITORIA DE SEGURANÇA ===")
        
        checks = {
            "whatsapp_credentials": self.check_whatsapp_credentials(),
            "config_integrity": self.check_config_integrity(),
            "active_sessions": self.check_active_sessions(),
            "gateway_process": self.check_gateway_process()
        }
        
        all_passed = all(checks.values())
        
        if all_passed:
            self.log_event("INFO", "✅ Todas as verificações de segurança passaram")
        else:
            failed = [k for k, v in checks.items() if not v]
            self.log_event("WARNING", f"⚠️ Verificações falharam: {', '.join(failed)}")
        
        self.log_event("INFO", "=== AUDITORIA CONCLUÍDA ===")
        
        return all_passed

if __name__ == "__main__":
    auditor = SecurityAuditor()
    auditor.run_full_audit()
