#!/usr/bin/env python3
"""
Script de autenticação inicial do Google Drive
Executar uma vez para obter o token de acesso
"""

import os
import sys
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Escopos necessários
SCOPES = ['https://www.googleapis.com/auth/drive']

def carregar_credenciais():
    """Carrega as credenciais do arquivo configurado"""
    credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH', 
                                 os.path.expanduser('~/.openclaw/credentials/google_credentials.json'))
    
    if not os.path.exists(credentials_path):
        print(f"❌ ERRO: Arquivo de credenciais não encontrado: {credentials_path}")
        print("\nExecute primeiro: ~/organizacao/configurar_credenciais_google.sh")
        sys.exit(1)
    
    return credentials_path

def autenticar():
    """Realiza a autenticação OAuth2 com Google Drive"""
    creds = None
    token_path = os.path.expanduser('~/.openclaw/credentials/token_drive.pickle')
    
    # Verificar se já existe token válido
    if os.path.exists(token_path):
        print("🔄 Token existente encontrado. Verificando validade...")
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # Se não houver credenciais válidas, solicitar autenticação
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Token expirado. Renovando...")
            creds.refresh(Request())
        else:
            print("\n" + "="*60)
            print("  AUTENTICAÇÃO GOOGLE DRIVE")
            print("="*60)
            print("\nUm navegador será aberto para você autorizar o acesso.")
            print("Por favor, faça login com a conta Google que tem acesso")
            print("ao Google Drive com os PDFs dos processos.\n")
            
            credentials_path = carregar_credenciais()
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                creds = flow.run_local_server(port=8888)
                print("\n✅ Autenticação bem-sucedida!")
            except Exception as e:
                print(f"\n❌ Erro na autenticação: {str(e)}")
                sys.exit(1)
        
        # Salvar token para próximas execuções
        os.makedirs(os.path.dirname(token_path), exist_ok=True)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
        print(f"💾 Token salvo em: {token_path}")
    
    return creds

def testar_acesso(creds):
    """Testa o acesso ao Google Drive"""
    print("\n🔄 Testando acesso ao Google Drive...")
    
    try:
        service = build('drive', 'v3', credentials=creds)
        
        # Listar os 5 arquivos mais recentes
        results = service.files().list(
            pageSize=5, 
            fields="nextPageToken, files(id, name, mimeType, modifiedTime)"
        ).execute()
        
        items = results.get('files', [])
        
        if not items:
            print("📂 Sua conta Drive está vazia ou sem acesso.")
        else:
            print("\n📂 Arquivos encontrados no seu Drive:")
            print("-" * 60)
            for item in items:
                print(f"  • {item['name']} ({item['mimeType']})")
            print("-" * 60)
        
        # Verificar pasta Processos-Juridicos
        query = "name='Processos-Juridicos' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        folders = results.get('files', [])
        
        if not folders:
            print("\n⚠️  Pasta 'Processos-Juridicos' não encontrada!")
            print("   Crie a pasta no seu Drive para habilitar o monitoramento automático.")
        else:
            print(f"\n✅ Pasta 'Processos-Juridicos' encontrada!")
            folder_id = folders[0]['id']
            
            # Verificar subpasta PDFs-Brutos
            subquery = f"'{folder_id}' in parents and name='PDFs-Brutos' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            subresults = service.files().list(q=subquery, fields="files(id, name)").execute()
            subfolders = subresults.get('files', [])
            
            if subfolders:
                print("✅ Subpasta 'PDFs-Brutos' encontrada!")
                
                # Verificar PDFs na pasta
                pdf_query = f"'{subfolders[0]['id']}' in parents and mimeType='application/pdf' and trashed=false"
                pdf_results = service.files().list(
                    q=pdf_query, 
                    orderBy='createdTime desc',
                    fields="files(id, name, createdTime)"
                ).execute()
                pdfs = pdf_results.get('files', [])
                
                if pdfs:
                    print(f"\n📄 {len(pdfs)} PDF(s) encontrado(s) na pasta PDFs-Brutos:")
                    for pdf in pdfs[:5]:  # mostrar apenas 5
                        print(f"  • {pdf['name']}")
                else:
                    print("\n📄 Nenhum PDF encontrado na pasta PDFs-Brutos ainda.")
            else:
                print("⚠️  Subpasta 'PDFs-Brutos' não encontrada.")
                print("   Crie: Processos-Juridicos > PDFs-Brutos")
        
        print("\n✅ Acesso ao Google Drive configurado com sucesso!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao testar acesso: {str(e)}")
        return False

def main():
    print("="*60)
    print("  CONFIGURAÇÃO DE ACESSO GOOGLE DRIVE")
    print("="*60)
    
    creds = autenticar()
    sucesso = testar_acesso(creds)
    
    if sucesso:
        print("\n" + "="*60)
        print(" PRÓXIMOS PASSOS:")
        print("="*60)
        print("1. Coloque seus PDFs na pasta PDFs-Brutos no Drive")
        print("2. Execute a análise com:")
        print("   python3 integracao_google_drive_analise.py")
        print("="*60)
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
