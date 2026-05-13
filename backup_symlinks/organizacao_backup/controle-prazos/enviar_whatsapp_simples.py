#!/usr/bin/env python3
"""
Script simples para envio de relatórios por WhatsApp
"""

import sys
import os

def main():
    if len(sys.argv) != 4:
        print("Uso: python enviar_whatsapp_simples.py <destinatario> <caminho_relatorio> <tipo_relatorio>")
        sys.exit(1)
    
    destinatario = sys.argv[1]
    caminho_relatorio = sys.argv[2]
    tipo_relatorio = sys.argv[3]
    
    print(f"Enviando relatório {tipo_relatorio} por WhatsApp para {destinatario}")
    
    # Ler o conteúdo do relatório
    with open(caminho_relatorio, 'r', encoding='utf-8') as f:
        conteudo_relatorio = f.read()
    
    # Limitar o tamanho do conteúdo para envio via WhatsApp
    if len(conteudo_relatorio) > 10000:  # 10KB
        conteudo_resumido = conteudo_relatorio[:10000] + "\n\n[...conteúdo truncado...]"
    else:
        conteudo_resumido = conteudo_relatorio
    
    # Obter apenas o nome do arquivo do relatório
    nome_arquivo = os.path.basename(caminho_relatorio)
    mensagem = f"Relatório {tipo_relatorio} gerado automaticamente. Arquivo: {nome_arquivo}\n\n{conteudo_resumido[:500]}..."  # Primeiros 500 caracteres
    
    # Agora vamos usar a função message diretamente no ambiente do OpenClaw
    try:
        # Importar a função message do ambiente do OpenClaw
        import importlib.util
        import sys
        
        # Caminho para o módulo de mensagem
        spec = importlib.util.spec_from_file_location("message", "/home/severosa/.openclaw/workspace/message.py")
        if spec is not None:
            message_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(message_module)
            send_message = message_module.message
        else:
            # Se não encontrar, tentar usar o sistema de mensagens do OpenClaw
            from openclaw.tools.message import message as send_message
        
        result = send_message({
            "action": "send",
            "channel": "whatsapp",
            "to": destinatario,
            "message": mensagem
        })
        
        if result and "error" not in result:
            print(f"Relatório enviado por WhatsApp para {destinatario}")
            sys.exit(0)
        else:
            print(f"Erro ao enviar via WhatsApp: {result.get('error', 'Erro desconhecido')}")
            sys.exit(1)
    except Exception as e:
        print(f"Erro ao enviar via WhatsApp: {str(e)}")
        
        # Vamos tentar uma abordagem alternativa: usar a função message diretamente
        try:
            # Tente usar o sistema de mensagens do OpenClaw via subprocess
            import subprocess
            cmd = [
                "python3", "-c",
                f'''
import sys
sys.path.append("/home/severosa/.npm-global/lib/node_modules/openclaw/tools")
from message import message
result = message({{
    "action": "send",
    "channel": "whatsapp",
    "to": "{destinatario}",
    "message": """{mensagem}"""
}})
print("SUCCESS" if result and "error" not in result else f"ERROR: {{result}}")
'''
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if "SUCCESS" in result.stdout:
                print(f"Relatório enviado por WhatsApp para {destinatario}")
                sys.exit(0)
            else:
                print(f"Erro final ao enviar via WhatsApp: {result.stdout} {result.stderr}")
                sys.exit(1)
        except Exception as e2:
            print(f"Falha total ao enviar via WhatsApp: {str(e2)}")
            sys.exit(1)

if __name__ == "__main__":
    main()