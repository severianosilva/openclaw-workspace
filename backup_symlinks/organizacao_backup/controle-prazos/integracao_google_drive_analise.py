#!/usr/bin/env python3
"""
Script para integração com Google Drive para análise jurídica automatizada
"""

import os
import pickle
import json
from datetime import datetime
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import subprocess
import tempfile
import mimetypes

# Escopos necessários para acessar Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

def autenticar_google_drive():
    """Autentica com a API do Google Drive"""
    creds = None
    # O token.pickle armazena os tokens de acesso e atualização
    if os.path.exists('token_drive.pickle'):
        with open('token_drive.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # Se não houver credenciais válidas, solicita autenticação
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Aqui usamos as credenciais já configuradas no sistema
            flow = InstalledAppFlow.from_client_config(
                get_client_config(), SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Salva as credenciais para a próxima execução
        with open('token_drive.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('drive', 'v3', credentials=creds)

def get_client_config():
    """Retorna a configuração do cliente do Google"""
    # Esta função deve retornar as credenciais OAuth do Google
    # que já estão configuradas no sistema
    client_config = {
        "installed": {
            "client_id": os.getenv('GOOGLE_CLIENT_ID', ''),
            "project_id": os.getenv('GOOGLE_PROJECT_ID', ''),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": os.getenv('GOOGLE_CLIENT_SECRET', ''),
            "redirect_uris": ["http://localhost"]
        }
    }
    return client_config

def encontrar_novo_pdf(service, pasta_alvo="Processos-Juridicos/PDFs-Brutos"):
    """Procura por novos PDFs na pasta especificada"""
    print(f"Procurando por novos PDFs em '{pasta_alvo}'...")
    
    # Primeiro, encontrar a pasta
    query = f"name='{pasta_alvo.split('/')[-1]}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    
    if not items:
        print(f"Pasta '{pasta_alvo}' não encontrada no Google Drive")
        return None
    
    pasta_id = items[0]['id']
    
    # Agora procurar por PDFs recentes na pasta
    pdf_query = f"'{pasta_id}' in parents and mimeType='application/pdf' and trashed=false"
    pdf_results = service.files().list(
        q=pdf_query, 
        orderBy='createdTime desc',
        fields="files(id, name, createdTime)"
    ).execute()
    
    pdfs = pdf_results.get('files', [])
    
    if not pdfs:
        print("Nenhum PDF encontrado na pasta")
        return None
    
    # Retorna o PDF mais recente
    return pdfs[0]

def baixar_pdf(service, file_id, destino):
    """Baixa um PDF do Google Drive"""
    print(f"Baixando PDF (ID: {file_id}) para {destino}...")
    
    import io
    from googleapiclient.http import MediaIoBaseDownload
    
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")
    
    with open(destino, 'wb') as f:
        f.write(fh.getvalue())

def encontrar_pasta_processo(nome_processo):
    """Encontra a pasta correspondente ao processo no sistema local"""
    # Procura em ambas as pastas (advocacia e servidor público)
    pastas_base = [
        os.path.expanduser("~/organizacao/advocacia/ativos"),
        os.path.expanduser("~/organizacao/servidor-publico/ativos")
    ]
    
    for pasta_base in pastas_base:
        if os.path.exists(pasta_base):
            for pasta_nome in os.listdir(pasta_base):
                caminho_pasta = os.path.join(pasta_base, pasta_nome)
                if os.path.isdir(caminho_pasta):
                    # Verifica se o nome do processo está contido no nome da pasta
                    if nome_processo.lower() in pasta_nome.lower():
                        return caminho_pasta
    
    print(f"Nenhuma pasta de processo encontrada para: {nome_processo}")
    return None

def extrair_nome_processo(nome_arquivo):
    """Extrai o nome do processo do nome do arquivo PDF"""
    # Remove extensão e caracteres especiais
    nome_sem_ext = os.path.splitext(nome_arquivo)[0]
    # Pode conter números de processo, nomes de clientes, etc.
    return nome_sem_ext.replace('_', ' ').replace('-', ' ')

def executar_analise_juridica(caminho_pdf, processo_path):
    """Executa a análise jurídica usando o script criado"""
    script_path = os.path.join(os.path.dirname(__file__), "ocr_analise_juridica.py")
    
    cmd = ["python3", script_path, caminho_pdf, processo_path]
    print(f"Executando análise jurídica: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Erro na análise jurídica: {result.stderr}")
        return False
    
    print("Análise jurídica concluída com sucesso")
    return True

def main():
    """Função principal de integração com Google Drive"""
    print("Iniciando integração com Google Drive para análise jurídica...")
    
    try:
        # Autenticar com Google Drive
        service = autenticar_google_drive()
        
        # Encontrar novo PDF
        pdf_info = encontrar_novo_pdf(service)
        
        if not pdf_info:
            print("Nenhum novo PDF encontrado para análise")
            return
        
        print(f"Novo PDF encontrado: {pdf_info['name']}")
        
        # Criar pasta temporária para download
        temp_dir = tempfile.mkdtemp()
        caminho_temp_pdf = os.path.join(temp_dir, pdf_info['name'])
        
        # Baixar PDF
        baixar_pdf(service, pdf_info['id'], caminho_temp_pdf)
        
        # Extrair nome do processo do nome do arquivo
        nome_processo = extrair_nome_processo(pdf_info['name'])
        
        # Encontrar pasta correspondente ao processo
        processo_path = encontrar_pasta_processo(nome_processo)
        
        if not processo_path:
            print(f"Não foi possível encontrar pasta de processo para: {nome_processo}")
            # Criar pasta temporária para análise
            processo_path = tempfile.mkdtemp()
            print(f"Usando pasta temporária: {processo_path}")
        
        # Executar análise jurídica
        sucesso = executar_analise_juridica(caminho_temp_pdf, processo_path)
        
        if sucesso:
            print("Análise jurídica completada com sucesso")
        else:
            print("Falha na análise jurídica")
        
        # Limpar arquivos temporários
        import shutil
        shutil.rmtree(temp_dir)
        
    except Exception as e:
        print(f"Erro na integração com Google Drive: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()