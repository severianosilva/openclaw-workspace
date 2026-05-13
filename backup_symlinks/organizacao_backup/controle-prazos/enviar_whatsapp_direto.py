#!/usr/bin/env python3
"""
Script direto para envio de relatório por WhatsApp
"""

import sys
import os

def enviar_relatorio_whatsapp(destinatario, caminho_relatorio, tipo_relatorio):
    """
    Envia relatório por WhatsApp usando o sistema de mensagens do OpenClaw
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
    
    # Obter apenas o nome do arquivo do relatório
    nome_arquivo = os.path.basename(caminho_relatorio)
    mensagem = f"Relatório {tipo_relatorio} gerado automaticamente. Arquivo: {nome_arquivo}\n\n{conteudo_resumido[:500]}..."  # Primeiros 500 caracteres
    
    # Usar o sistema de mensagens do OpenClaw diretamente
    import subprocess
    import os
    
    # Obter o diretório do workspace
    workspace_dir = os.path.expanduser("~/.openclaw/workspace")
    
    # Criar um script temporário para enviar a mensagem
    script_content = f'''
import sys
sys.path.insert(0, "{workspace_dir}")

# Tente importar e usar a função message do sistema OpenClaw
try:
    # Primeiro tentar importar como módulo direto
    from openclaw.tools import message
    result = message.message({{
        "action": "send",
        "channel": "whatsapp",
        "to": "{destinatario}",
        "message": """{mensagem}"""
    }})
    print("SUCCESS" if result and "error" not in result else f"ERROR: {{result}}")
except ImportError:
    try:
        # Tentar importar diretamente do caminho do sistema
        import importlib.util
        spec = importlib.util.spec_from_file_location("message", "/home/severosa/.npm-global/lib/node_modules/openclaw/tools/message.js")
        # Como é um arquivo JS, tentar chamar o OpenClaw diretamente
        import subprocess
        cmd = ["openclaw", "message", "send", "--channel", "whatsapp", "--to", "{destinatario}", "--message", """{mensagem}"""]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print("SUCCESS" if result.returncode == 0 else f"ERROR: {{result.stderr}}")
    except Exception as e:
        print(f"ERROR: Não foi possível enviar mensagem: {{e}}")
except Exception as e:
    print(f"ERROR: {{e}}")
'''
    
    # Salvar script temporário
    with open('/tmp/enviar_msg_temp.py', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # Executar script temporário
    result = subprocess.run(['python3', '/tmp/enviar_msg_temp.py'], capture_output=True, text=True)
    
    # Limpar arquivo temporário
    try:
        os.remove('/tmp/enviar_msg_temp.py')
    except:
        pass
    
    if "SUCCESS" in result.stdout:
        print(f"Relatório enviado por WhatsApp com sucesso!")
        return True
    else:
        print(f"Erro: {result.stdout} {result.stderr}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python enviar_whatsapp_direto.py <destinatario> <caminho_relatorio> <tipo_relatorio>")
        sys.exit(1)
    
    destinatario = sys.argv[1]
    caminho_relatorio = sys.argv[2]
    tipo_relatorio = sys.argv[3]
    
    sucesso = enviar_relatorio_whatsapp(destinatario, caminho_relatorio, tipo_relatorio)
    sys.exit(0 if sucesso else 1)