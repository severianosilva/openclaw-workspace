#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRANSFERÊNCIA PARA GOOGLE DRIVE - PYTHON
Usa API Google Drive para transferir arquivos sem RClone
"""

import os
import pickle
import glob
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# Configurações
SCOPES = ['https://www.googleapis.com/auth/drive']
BACKUP_DIR = "/home/severosa/organizacao/backup"
MEDIA_DIR = "/home/severosa/.openclaw/media/inbound"
TOKEN_FILE = "/home/severosa/.openclaw/token_drive.pickle"
CREDENTIALS_FILE = "/home/severosa/.openclaw/credentials.json"

def get_drive_service():
    """Autentica e retorna serviço do Google Drive"""
    creds = None
    
    # Carregar credenciais salvas
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # Refresh se expirado
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif os.path.exists(CREDENTIALS_FILE):
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        else:
            print(f"ERRO: Arquivo {CREDENTIALS_FILE} não encontrado!")
            print("Crie em: https://console.cloud.google.com/apis/credentials")
            return None
        
        # Salvar token
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('drive', 'v3', credentials=creds)

def get_or_create_folder(service, folder_name, parent_id=None):
    """Cria ou retorna pasta no Drive"""
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    query += " and trashed=false"
    
    results = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    
    if items:
        return items[0]['id']
    
    # Criar pasta
    metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id] if parent_id else []
    }
    folder = service.files().create(body=metadata, fields='id').execute()
    return folder['id']

def upload_file(service, file_path, folder_id):
    """Faz upload de arquivo"""
    file_name = os.path.basename(file_path)
    
    # Verificar se já existe
    query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields='files(id)').execute()
    
    if results.get('files'):
        print(f"   ⚠️  {file_name} já existe no Drive (pulando)")
        return True
    
    # Upload
    media = MediaFileUpload(file_path, resumable=True)
    metadata = {'name': file_name, 'parents': [folder_id]}
    
    try:
        file = service.files().create(body=metadata, media_body=media, fields='id').execute()
        print(f"   ✅ {file_name} → Drive")
        return True
    except HttpError as e:
        print(f"   ❌ Erro: {e}")
        return False

def clean_old_files(directory, days=30, extensions=None):
    """Lista arquivos antigos para transferência"""
    cutoff = datetime.now() - timedelta(days=days)
    files = []
    
    for ext in (extensions or ['*']):
        pattern = os.path.join(directory, f"**/*.{ext}") if ext != '*' else os.path.join(directory, '*')
        for file_path in glob.glob(pattern, recursive=True):
            if os.path.isfile(file_path):
                mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if mtime < cutoff:
                    files.append(file_path)
    
    return sorted(files, key=os.path.getmtime, reverse=True)

def main():
    print("=" * 60)
    print("  TRANSFERÊNCIA PARA GOOGLE DRIVE")
    print("=" * 60)
    print()
    
    # Conectar ao Drive
    print("🔐 Conectando ao Google Drive...")
    service = get_drive_service()
    if not service:
        print()
        print("❌ Falha na autenticação!")
        print("Execute com credenciais configuradas:")
        print("  python3 transferir_drive.py")
        return
    
    # Criar estrutura de pastas
    print("📁 Criando estrutura...")
    root_id = get_or_create_folder(service, "OpenClaw-Offload")
    backups_id = get_or_create_folder(service, "backups-antigos", root_id)
    audio_id = get_or_create_folder(service, "media-audio", root_id)
    trans_id = get_or_create_folder(service, "transcricoes", root_id)
    
    stats = {'backups': 0, 'audio': 0, 'trans': 0, 'bytes': 0}
    
    # 1. Backups antigos
    print("\n🗂️  PROCESSANDO BACKUPS...")
    backups = clean_old_files(BACKUP_DIR, days=30, extensions=['tar.gz'])
    # Manter os 2 mais recentes
    backups_to_move = backups[2:] if len(backups) > 2 else []
    
    for file_path in backups_to_move[:5]:  # Limitar a 5 por vez
        size = os.path.getsize(file_path)
        if upload_file(service, file_path, backups_id):
            os.remove(file_path)  # Deletar local após upload
            stats['backups'] += 1
            stats['bytes'] += size
            print(f"   💾 Espaço: {size / 1024 / 1024:.1f} MB")
    
    # 2. Áudios antigos
    print("\n🎵 PROCESSANDO ÁUDIOS...")
    audios = clean_old_files(MEDIA_DIR, days=7, extensions=['ogg', 'mp3', 'wav'])
    
    for file_path in audios[:10]:  # Limitar a 10 por vez
        size = os.path.getsize(file_path)
        if upload_file(service, file_path, audio_id):
            os.remove(file_path)
            stats['audio'] += 1
            stats['bytes'] += size
            print(f"   💾 Espaço: {size / 1024 / 1024:.1f} MB")
    
    # 3. Transcrições antigas
    print("\n📝 PROCESSANDO TRANSCRIÇÕES...")
    trans = clean_old_files(MEDIA_DIR, days=14, extensions=['txt'])
    trans = [t for t in trans if 'transcricao' in os.path.basename(t).lower()]
    
    for file_path in trans[:20]:
        size = os.path.getsize(file_path)
        if upload_file(service, file_path, trans_id):
            os.remove(file_path)
            stats['trans'] += 1
            stats['bytes'] += size
    
    # Resumo
    print("\n" + "=" * 60)
    print("  ✅ TRANSFERÊNCIA CONCLUÍDA")
    print("=" * 60)
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Backups: {stats['backups']}")
    print(f"   Áudios: {stats['audio']}")
    print(f"   Transcrições: {stats['trans']}")
    print(f"   TOTAL: {stats['backups'] + stats['audio'] + stats['trans']} arquivos")
    print(f"   💾 ESPAÇO LIBERADO: {stats['bytes'] / 1024 / 1024:.1f} MB")
    print(f"\n📁 Pasta no Drive: OpenClaw-Offload/")
    
    # Espaço local
    print("\n💾 ESPAÇO LOCAL ATUAL:")
    os.system("df -h /home/severosa")

if __name__ == '__main__':
    main()
