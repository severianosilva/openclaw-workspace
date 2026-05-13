#!/usr/bin/env python3
"""
🔐 YouTube Authenticator - Uma execução para autenticar
"""

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import os

SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube'
]

def authenticate_youtube():
    """Autentica YouTube API e salva token"""
    
    creds_dir = r"C:\Users\User\.openclaw\workspace\credentials"
    client_secret = os.path.join(creds_dir, "client_secret.json")
    token_file = os.path.join(creds_dir, "youtube_token.pickle")
    
    print("="*50)
    print("AUTENTICANDO YOUTUBE API")
    print("="*50)
    
    flow = InstalledAppFlow.from_client_secrets_file(client_secret, SCOPES)
    creds = flow.run_local_server(port=0)
    
    # Salvar token
    with open(token_file, 'wb') as f:
        pickle.dump(creds, f)
    
    print(f"[OK] Token salvo: {token_file}")
    
    # Testar API
    youtube = build('youtube', 'v3', credentials=creds)
    channels = youtube.channels().list(mine=True, part='snippet').execute()
    
    if 'items' in channels:
        channel = channels['items'][0]
        print(f"[OK] Autenticado como: {channel['snippet']['title']}")
    
    return creds

if __name__ == "__main__":
    authenticate_youtube()