#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lark Cloud Storage Integration
200 GB Grátis - https://www.larksuite.com/

Uso:
    from storage_lark import LarkStorage
    
    lark = LarkStorage(app_id="xxx", app_secret="yyy")
    lark.upload("arquivo.mp4", folder="youtube/videos")
    link = lark.compartilhar("arquivo.mp4")
"""

import os
import json
import requests
from typing import Optional, Dict, List
from datetime import datetime

class LarkStorage:
    """Cliente para Lark Cloud Storage (200GB grátis)"""
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        """
        Inicializa cliente Lark
        
        Args:
            app_id: Lark App ID (obter em https://open.larksuite.com/)
            app_secret: Lark App Secret
        """
        self.app_id = app_id or os.getenv("LARK_APP_ID")
        self.app_secret = app_secret or os.getenv("LARK_APP_SECRET")
        self.base_url = "https://open.larksuite.com/open-apis/drive/v1"
        self.access_token = None
        self.token_expires = None
        
        if not self.app_id or not self.app_secret:
            print("⚠️  Configure LARK_APP_ID e LARK_APP_SECRET no .env")
        
    def autenticar(self) -> bool:
        """Obtém access token"""
        url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
        
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            data = response.json()
            
            if data.get("code") == 0:
                self.access_token = data["tenant_access_token"]
                self.token_expires = datetime.now().timestamp() + data.get("expire", 7200)
                print("✅ Autenticado no Lark")
                return True
            else:
                print(f"❌ Erro autenticação: {data}")
                return False
                
        except Exception as e:
            print(f"❌ Erro conexão: {e}")
            return False
    
    def _get_token(self) -> Optional[str]:
        """Garante token válido"""
        if not self.access_token or datetime.now().timestamp() > self.token_expires:
            self.autenticar()
        return self.access_token
    
    def upload(self, arquivo_path: str, folder: str = "root", parent_file_token: str = None) -> Optional[str]:
        """
        Upload de arquivo
        
        Args:
            arquivo_path: Caminho local do arquivo
            folder: Nome da pasta no Lark
            parent_file_token: Token da pasta pai
            
        Returns:
            File token se sucesso, None se erro
        """
        token = self._get_token()
        if not token:
            return None
        
        if not os.path.exists(arquivo_path):
            print(f"❌ Arquivo não existe: {arquivo_path}")
            return None
        
        # 1. Criar pasta se não existir
        if folder != "root" and not parent_file_token:
            parent_file_token = self.criar_pasta(folder)
        
        # 2. Upload do arquivo
        url = f"{self.base_url}/files"
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        try:
            with open(arquivo_path, 'rb') as f:
                files = {'file': (os.path.basename(arquivo_path), f)}
                data = {
                    'folder_token': parent_file_token or 'root',
                    'file_name': os.path.basename(arquivo_path)
                }
                
                response = requests.post(url, headers=headers, files=files, data=data, timeout=300)
                result = response.json()
                
                if result.get("code") == 0:
                    file_token = result["data"]["file_token"]
                    file_size = os.path.getsize(arquivo_path)
                    print(f"✅ Upload: {os.path.basename(arquivo_path)} ({file_size/1024/1024:.1f} MB)")
                    return file_token
                else:
                    print(f"❌ Erro upload: {result}")
                    return None
                    
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def criar_pasta(self, nome_pasta: str, parent_token: str = "root") -> Optional[str]:
        """Cria pasta no Lark Drive"""
        token = self._get_token()
        if not token:
            return None
        
        url = f"{self.base_url}/folders"
        headers = {"Authorization": f"Bearer {token}"}
        
        payload = {
            "folder_name": nome_pasta,
            "parent_file_token": parent_token
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                folder_token = result["data"]["file_token"]
                print(f"📁 Pasta criada: {nome_pasta}")
                return folder_token
            else:
                print(f"❌ Erro criar pasta: {result}")
                return None
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def listar_arquivos(self, folder_token: str = "root") -> List[Dict]:
        """Lista arquivos em uma pasta"""
        token = self._get_token()
        if not token:
            return []
        
        url = f"{self.base_url}/files/search"
        headers = {"Authorization": f"Bearer {token}"}
        params = {"folder_token": folder_token}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                return result.get("data", {}).get("items", [])
            else:
                print(f"❌ Erro listar: {result}")
                return []
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []
    
    def compartilhar(self, file_token: str, permissao: str = "anyone_with_link") -> Optional[str]:
        """
        Gera link de compartilhamento
        
        Args:
            file_token: Token do arquivo
            permissao: "anyone_with_link", "organization", "private"
            
        Returns:
            URL de compartilhamento
        """
        token = self._get_token()
        if not token:
            return None
        
        url = f"{self.base_url}/files/{file_token}/share"
        headers = {"Authorization": f"Bearer {token}"}
        
        payload = {
            "type": permissao
        }
        
        try:
            response = requests.put(url, json=payload, headers=headers, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                share_url = result["data"]["share_url"]
                print(f"🔗 Link: {share_url}")
                return share_url
            else:
                print(f"❌ Erro compartilhar: {result}")
                return None
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def download(self, file_token: str, destino_path: str = None) -> Optional[str]:
        """Download de arquivo"""
        token = self._get_token()
        if not token:
            return None
        
        url = f"{self.base_url}/files/{file_token}/download"
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = requests.get(url, headers=headers, timeout=300)
            
            if response.status_code == 200:
                if not destino_path:
                    destino_path = f"lark_download_{file_token}"
                
                with open(destino_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"⬇️ Download: {destino_path}")
                return destino_path
            else:
                print(f"❌ Erro download: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def espaco_usado(self) -> Dict:
        """Retorna espaço usado/disponível"""
        # Lark não fornece API pública para quota no momento
        # Retorna estimativa
        return {
            "usado": "Desconhecido",
            "total": "200 GB",
            "disponivel": "~200 GB (estimado)"
        }


# Funções utilitárias
def upload_para_lark(arquivo: str, pasta: str = "openclaw") -> Optional[str]:
    """Função rápida para upload"""
    lark = LarkStorage()
    token = lark.upload(arquivo, folder=pasta)
    if token:
        return lark.compartilhar(token)
    return None


if __name__ == "__main__":
    print("Teste Lark Storage")
    print("="*50)
    
    # Testar (precisa de credenciais configuradas)
    lark = LarkStorage()
    
    if lark.autenticar():
        print("\n✅ Autenticação bem-sucedida!")
        
        # Criar pasta de teste
        folder_token = lark.criar_pasta("OpenClaw_Testes")
        
        if folder_token:
            # Upload de teste
            print("\n📤 Upload de teste...")
            # lark.upload("arquivo_teste.txt", parent_file_token=folder_token)
    else:
        print("\n❌ Configure suas credenciais no .env")
