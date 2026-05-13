#!/usr/bin/env python3
"""
Script auxiliar para envio de relatórios por WhatsApp
"""

import sys
import os

def enviar_relatorio_whatsapp(destinatario, caminho_relatorio, tipo_relatorio):
    """
    Envia relatório por WhatsApp
    """
    print(f"Enviando relatório {tipo_relatorio} por WhatsApp para {destinatario}")
    
    # Ler o conteúdo do relatório
    with open(caminho_relatorio, 'r', encoding='utf-8') as f:
        conteudo_relatorio = f.read()
    
    # Limitar o tamanho do conteúdo para envio via WhatsApp
    if len(conteudo_relatorio) > 10000:  # 10KB
        conteudo_resumido = conteudo_relatorio[:10000] + "\n\n[...conteúdo truncado...]"
    else:
        conteudo_resumido = conteudo_relatorio
    
    # Enviar mensagem via OpenClaw
    try:
        mensagem = f"Relatório {tipo_relatorio} gerado automaticamente:\n\n{conteudo_resumido}"
        
        # Importar e usar a função message
        from openclaw.tools import message
        result = message({
            "action": "send",
            "to": destinatario,
            "message": mensagem,
            "channel": "whatsapp"
        })
        
        if result and "error" not in result:
            print(f"Relatório enviado por WhatsApp para {destinatario}")
            return True
        else:
            print(f"Erro ao enviar via WhatsApp: {result.get('error', 'Erro desconhecido')}")
            return False
    except ImportError:
        # Se não conseguir importar, tentar via subprocess
        import subprocess
        result = subprocess.run([
            "python3", "-c", 
            f"from openclaw.tools import message; "
            f"result = message({{'action': 'send', 'to': '{destinatario}', "
            f"'message': '''{mensagem[:1000]}''', 'channel': 'whatsapp'}}); "
            f"print('success' if result and 'error' not in result else 'fail')"
        ], capture_output=True, text=True)
        
        success = "success" in result.stdout
        if success:
            print(f"Relatório enviado por WhatsApp para {destinatario}")
        else:
            print(f"Erro ao enviar via WhatsApp")
        
        return success
    except Exception as e:
        print(f"Erro ao enviar via WhatsApp: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python enviar_whatsapp.py <destinatario> <caminho_relatorio> <tipo_relatorio>")
        sys.exit(1)
    
    destinatario = sys.argv[1]
    caminho_relatorio = sys.argv[2]
    tipo_relatorio = sys.argv[3]
    
    sucesso = enviar_relatorio_whatsapp(destinatario, caminho_relatorio, tipo_relatorio)
    sys.exit(0 if sucesso else 1)