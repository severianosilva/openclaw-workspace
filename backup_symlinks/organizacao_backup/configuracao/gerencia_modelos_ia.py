#!/usr/bin/env python3
"""
Sistema de Troca Automática de Modelos de IA
Monitora uso e alterna entre modelos quando atinge limites
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

class GerenciadorModelosIA:
    """Gerencia troca automática de modelos de IA baseado em uso"""
    
    def __init__(self):
        self.config_path = Path('/home/severosa/.openclaw/openclaw.json')
        self.usage_path = Path('/home/severosa/.openclaw/usage_modelos.json')
        self.config = self.carregar_config()
        self.usage = self.carregar_usage()
        
        # Limites de uso por modelo (em requisições)
        self.limites = {
            'qwen-portal/coder-model': 100,      # 100 requisições
            'qwen-portal/vision-model': 50,       # 50 requisições
            'openrouter/auto': 200,               # 200 requisições
            'minimax-portal/MiniMax-M2.1': 150,   # 150 requisições
            'minimax-portal/MiniMax-M2.1-lightning': 300,  # 300 requisições
            'google/gemini-3-pro-preview': 100,   # 100 requisições
            'synthetic/hf:MiniMaxAI/MiniMax-M2.1': 250,  # 250 requisições
        }
        
        # Ordem de fallback
        self.fallback_order = [
            'qwen-portal/coder-model',
            'minimax-portal/MiniMax-M2.1-lightning',
            'minimax-portal/MiniMax-M2.1',
            'synthetic/hf:MiniMaxAI/MiniMax-M2.1',
            'openrouter/auto',
            'google/gemini-3-pro-preview',
            'qwen-portal/vision-model'
        ]
    
    def carregar_config(self):
        """Carregar configuração do OpenClaw"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar config: {e}")
            return {}
    
    def carregar_usage(self):
        """Carregar histórico de uso"""
        try:
            if self.usage_path.exists():
                with open(self.usage_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar usage: {e}")
        
        # Estrutura inicial
        return {
            'modelos': {},
            'modelo_atual': 'qwen-portal/coder-model',
            'ultima_troca': None,
            'historico_trocas': []
        }
    
    def salvar_usage(self):
        """Salvar histórico de uso"""
        with open(self.usage_path, 'w', encoding='utf-8') as f:
            json.dump(self.usage, f, indent=2, ensure_ascii=False)
    
    def registrar_uso(self, modelo_id):
        """Registrar uso de um modelo"""
        hoje = datetime.now().strftime('%Y-%m-%d')
        
        if modelo_id not in self.usage['modelos']:
            self.usage['modelos'][modelo_id] = {
                'total': 0,
                'hoje': 0,
                'ultima_data': hoje
            }
        
        dados = self.usage['modelos'][modelo_id]
        
        # Resetar contagem se mudou o dia
        if dados['ultima_data'] != hoje:
            dados['hoje'] = 0
            dados['ultima_data'] = hoje
        
        dados['total'] += 1
        dados['hoje'] += 1
        
        self.salvar_usage()
        
        # Verificar se precisa trocar
        self.verificar_e_trocar_modelo()
    
    def verificar_e_trocar_modelo(self):
        """Verifica se modelo atual atingiu limite e troca se necessário"""
        modelo_atual = self.usage['modelo_atual']
        limite = self.limites.get(modelo_atual, 100)
        uso_hoje = self.usage['modelos'].get(modelo_atual, {}).get('hoje', 0)
        
        print(f"\n📊 Verificando modelo: {modelo_atual}")
        print(f"   Uso hoje: {uso_hoje}/{limite}")
        
        if uso_hoje >= limite:
            print(f"   ⚠️  Limite atingido! Trocando modelo...")
            self.trocar_modelo()
    
    def trocar_modelo(self, motivo='limite_atingido'):
        """Trocar para o próximo modelo disponível"""
        modelo_atual = self.usage['modelo_atual']
        
        # Encontrar próximo modelo disponível
        novo_modelo = None
        for modelo in self.fallback_order:
            if modelo == modelo_atual:
                continue
            
            # Verificar se este modelo tem limite e se já atingiu
            limite = self.limites.get(modelo, 100)
            uso_hoje = self.usage['modelos'].get(modelo, {}).get('hoje', 0)
            
            if uso_hoje < limite:
                novo_modelo = modelo
                break
        
        if not novo_modelo:
            # Todos atingiram limite, usar o primeiro como fallback
            novo_modelo = self.fallback_order[0]
            print(f"   ⚠️  Todos modelos no limite. Resetando contagem.")
            self.resetar_contagens()
        
        # Registrar troca
        troca = {
            'data': datetime.now().isoformat(),
            'de': modelo_atual,
            'para': novo_modelo,
            'motivo': motivo
        }
        
        self.usage['modelo_atual'] = novo_modelo
        self.usage['ultima_troca'] = troca['data']
        self.usage['historico_trocas'].append(troca)
        
        # Manter apenas últimas 50 trocas
        self.usage['historico_trocas'] = self.usage['historico_trocas'][-50:]
        
        self.salvar_usage()
        
        print(f"   ✅ Modelo trocado: {modelo_atual} → {novo_modelo}")
        
        # Atualizar configuração do OpenClaw
        self.atualizar_config_modelo(novo_modelo)
        
        return novo_modelo
    
    def resetar_contagens(self):
        """Resetar contagem de uso de todos os modelos"""
        hoje = datetime.now().strftime('%Y-%m-%d')
        
        for modelo in self.usage['modelos']:
            self.usage['modelos'][modelo]['hoje'] = 0
            self.usage['modelos'][modelo]['ultima_data'] = hoje
        
        self.salvar_usage()
        print("   🔄 Contagens resetadas")
    
    def atualizar_config_modelo(self, novo_modelo):
        """Atualizar configuração do OpenClaw com novo modelo"""
        try:
            self.config['agents']['defaults']['model']['primary'] = novo_modelo
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            print(f"   📝 Configuração atualizada")
            
            # Reiniciar gateway para aplicar mudanças
            self.reiniciar_gateway()
            
        except Exception as e:
            print(f"   ❌ Erro ao atualizar config: {e}")
    
    def reiniciar_gateway(self):
        """Reiniciar gateway do OpenClaw"""
        import subprocess
        try:
            print("   🔄 Reiniciando gateway...")
            subprocess.run(['openclaw', 'gateway', 'restart'], 
                         capture_output=True, timeout=30)
            print("   ✅ Gateway reiniciado")
        except Exception as e:
            print(f"   ⚠️  Erro ao reiniciar gateway: {e}")
            print("   Reinicie manualmente: openclaw gateway restart")
    
    def status(self):
        """Mostrar status atual dos modelos"""
        print("\n" + "="*60)
        print("STATUS DOS MODELOS DE IA")
        print("="*60)
        
        modelo_atual = self.usage['modelo_atual']
        print(f"\n🎯 Modelo Atual: {modelo_atual}")
        
        if self.usage['ultima_troca']:
            print(f"🕒 Última Troca: {self.usage['ultima_troca']}")
        
        print("\n📊 Uso por Modelo:")
        print("-"*60)
        
        for modelo in self.fallback_order:
            limite = self.limites.get(modelo, 100)
            uso = self.usage['modelos'].get(modelo, {}).get('hoje', 0)
            total = self.usage['modelos'].get(modelo, {}).get('total', 0)
            
            status = "✅" if uso < limite else "⚠️  LIMITE"
            atual = "🎯" if modelo == modelo_atual else "  "
            
            porcentagem = (uso / limite) * 100 if limite > 0 else 0
            barra = "█" * int(porcentagem / 10) + "░" * (10 - int(porcentagem / 10))
            
            print(f"{atual} {status} {modelo[:40]:<40} [{barra}] {uso}/{limite} (total: {total})")
        
        print("\n📜 Histórico Recente de Trocas:")
        print("-"*60)
        
        for troca in self.usage['historico_trocas'][-5:]:
            data = troca['data'][:16].replace('T', ' ')
            print(f"  {data} | {troca['de'][:30]:<30} → {troca['para'][:30]:<30} ({troca['motivo']})")
        
        print("\n" + "="*60)
    
    def configurar_limites(self, modelo_id, novo_limite):
        """Configurar limite personalizado para um modelo"""
        self.limites[modelo_id] = novo_limite
        print(f"✅ Limite de {modelo_id} atualizado para {novo_limite} requisições")
        
        # Salvar limites personalizados
        limites_path = Path('/home/severosa/.openclaw/limites_modelos.json')
        with open(limites_path, 'w', encoding='utf-8') as f:
            json.dump(self.limites, f, indent=2, ensure_ascii=False)


def main():
    """Função principal"""
    gerenciador = GerenciadorModelosIA()
    
    if len(sys.argv) < 2:
        print("Uso: python3 gerencia_modelos_ia.py <comando>")
        print("\nComandos disponíveis:")
        print("  status          - Mostrar status dos modelos")
        print("  uso <modelo>    - Registrar uso de um modelo")
        print("  trocar [motivo] - Trocar modelo manualmente")
        print("  limite <modelo> <novo_limite> - Configurar limite")
        print("  reset           - Resetar todas as contagens")
        return
    
    comando = sys.argv[1]
    
    if comando == 'status':
        gerenciador.status()
    
    elif comando == 'uso':
        if len(sys.argv) < 3:
            modelo = gerenciador.usage['modelo_atual']
        else:
            modelo = sys.argv[2]
        gerenciador.registrar_uso(modelo)
        print(f"✅ Uso registrado para {modelo}")
    
    elif comando == 'trocar':
        motivo = sys.argv[2] if len(sys.argv) > 2 else 'manual'
        gerenciador.trocar_modelo(motivo)
    
    elif comando == 'limite':
        if len(sys.argv) < 4:
            print("Uso: limite <modelo_id> <novo_limite>")
            return
        modelo = sys.argv[2]
        limite = int(sys.argv[3])
        gerenciador.configurar_limites(modelo, limite)
    
    elif comando == 'reset':
        gerenciador.resetar_contagens()
        print("✅ Contagens resetadas")
    
    else:
        print(f"Comando desconhecido: {comando}")


if __name__ == '__main__':
    main()
