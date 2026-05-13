#!/usr/bin/env python3
"""
Script para envio assíncrono de relatórios por WhatsApp
"""

import sys
import os
import asyncio
import subprocess

async def enviar_relatorio_whatsapp_async(destinatario, caminho_relatorio, tipo_relatorio):
    """
    Envia relatório por WhatsApp de forma assíncrona
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
    
    try:
        # Usar asyncio para chamar o comando openclaw
        proc = await asyncio.create_subprocess_exec(
            'openclaw', 'message', 'send',
            '--channel', 'whatsapp',
            '--to', destinatario,
            '--message', mensagem,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await proc.communicate()
        
        if proc.returncode == 0:
            print(f"Relatório enviado por WhatsApp para {destinatario}")
            return True
        else:
            print(f"Erro ao enviar via WhatsApp: {stderr.decode()}")
            return False
    except Exception as e:
        print(f"Erro ao enviar via WhatsApp: {str(e)}")
        return False

def main():
    if len(sys.argv) != 4:
        print("Uso: python enviar_whatsapp_async.py <destinatario> <caminho_relatorio> <tipo_relatorio>")
        sys.exit(1)
    
    destinatario = sys.argv[1]
    caminho_relatorio = sys.argv[2]
    tipo_relatorio = sys.argv[3]
    
    # Executar a função assíncrona
    resultado = asyncio.run(enviar_relatorio_whatsapp_async(destinatario, caminho_relatorio, tipo_relatorio))
    
    sys.exit(0 if resultado else 1)

if __name__ == "__main__":
    main()