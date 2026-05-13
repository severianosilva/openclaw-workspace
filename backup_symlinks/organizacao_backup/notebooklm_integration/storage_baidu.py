#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baidu Yun Pan (百度网盘) Integration
2 TB Grátis - https://pan.baidu.com/

⚠️ 注意：Interface em chinês. Requer VPN/proxy se estiver fora da China.

Uso:
    from storage_baidu import BaiduStorage
    
    baidu = BaiduStorage(access_token="xxx")
    baidu.upload("arquivo_grande.zip")
    link = baidu.compartilhar("arquivo_grande.zip")
"""

import os
import json
import requests
import hashlib
import base64
from typing import Optional, Dict, List
from datetime import datetime

class BaiduStorage:
    """Cliente para Baidu Yun Pan (2TB grátis)"""
    
    def __init__(self, access_token: str = None, api_key: str = None, secret_key: str = None):
        """
        Inicializa cliente Baidu
        
        Args:
            access_token: Baidu Access Token (OAuth)
            api_key: Baidu API Key
            secret_key: Baidu Secret Key
        """
        self.access_token = access_token or os.getenv("BAIDU_ACCESS_TOKEN")
        self.api_key = api_key or os.getenv("BAIDU_API_KEY")
        self.secret_key = secret_key or os.getenv("BAIDU_SECRET_KEY")
        
        self.base_url = "https://pan.baidu.com/rest/2.0/xpan"
        self.headers = {
            "User-Agent": "pan.baidu.com"
        }
        
        if not self.access_token:
            print("⚠️  Configure BAIDU_ACCESS_TOKEN no .env")
            print("📝 Obter token: https://pan.baidu.com/union/console")
    
    def autenticar(self, code: str = None) -> Optional[str]:
        """
        Autenticação OAuth (primeira vez)
        
        Para obter código:
        1. Acesse: https://openapi.baidu.com/oauth/2.0/authorize
           ?response_type=code
           &client_key=SEU_API_KEY
           &redirect_uri=SEU_REDIRECT_URI
           &scope=basic,netdisk
        2. Usuário autoriza
        3. Redireciona com code
        4. Usa este método para trocar por access_token
        """
        if not code:
            print("❌ Precisa do código OAuth")
            return None
        
        url = "https://openapi.baidu.com/oauth/2.0/token"
        params = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.api_key,
            "client_secret": self.secret_key,
            "redirect_uri": "oob"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if "access_token" in data:
                self.access_token = data["access_token"]
                print(f"✅ Token obtido! Expires em: {data.get('expires_in', 0)}s")
                return self.access_token
            else:
                print(f"❌ Erro: {data}")
                return None
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def _get_params(self) -> Dict:
        """Parâmetros comuns para API"""
        return {
            "access_token": self.access_token,
            "clienttype": "1",
            "app_id": "250528"  # App ID oficial Baidu
        }
    
    def upload(self, arquivo_path: str, remote_path: str = None) -> Optional[str]:
        """
        Upload de arquivo (2 etapas: init + upload)
        
        Args:
            arquivo_path: Caminho local
            remote_path: Caminho remoto (ex: /apps/openclaw/arquivo.zip)
            
        Returns:
            Path remoto se sucesso
        """
        if not os.path.exists(arquivo_path):
            print(f"❌ Arquivo não existe: {arquivo_path}")
            return None
        
        if not remote_path:
            remote_path = f"/apps/openclaw/{os.path.basename(arquivo_path)}"
        
        params = self._get_params()
        
        try:
            # Etapa 1: Pre-upload (inicializar)
            file_size = os.path.getsize(arquivo_path)
            file_md5 = self._calcular_md5(arquivo_path)
            
            url_init = f"{self.base_url}/file"
            params_init = {
                **params,
                "method": "precreate",
                "path": remote_path,
                "size": file_size,
                "content-md5": file_md5,
                "slice-md5": self._calcular_md5_slice(arquivo_path),
                "content-type": "application/octet-stream",
                "isdir": "0"
            }
            
            response = requests.post(url_init, params=params_init, timeout=30)
            result = response.json()
            
            if result.get("errno") == 0:
                upload_id = result.get("uploadid")
                
                # Etapa 2: Upload real (chunked para arquivos grandes)
                return self._upload_chunks(arquivo_path, remote_path, upload_id, params)
            else:
                print(f"❌ Erro pre-upload: {result}")
                return None
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def _upload_chunks(self, arquivo_path: str, remote_path: str, upload_id: str, params: Dict, chunk_size: int = 4*1024*1024) -> Optional[str]:
        """Upload em chunks (para arquivos grandes)"""
        
        url_upload = f"{self.base_url}/file"
        partseq = 0
        part_list = []
        
        with open(arquivo_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                params_upload = {
                    **params,
                    "method": "upload",
                    "type": "tmpfile",
                    "path": remote_path,
                    "uploadid": upload_id,
                    "partseq": partseq
                }
                
                try:
                    response = requests.post(
                        url_upload,
                        params=params_upload,
                        data=chunk,
                        headers=self.headers,
                        timeout=300
                    )
                    
                    result = response.json()
                    
                    if result.get("errno") == 0:
                        part_list.append(result["md5"])
                        progresso = (partseq + 1) * chunk_size / os.path.getsize(arquivo_path) * 100
                        print(f"📤 Upload: {progresso:.1f}%")
                        partseq += 1
                    else:
                        print(f"❌ Erro chunk {partseq}: {result}")
                        return None
                        
                except Exception as e:
                    print(f"❌ Erro chunk: {e}")
                    return None
        
        # Etapa 3: Criar arquivo final
        return self._create_file(remote_path, upload_id, part_list, params)
    
    def _create_file(self, remote_path: str, upload_id: str, part_list: List[str], params: Dict) -> Optional[str]:
        """Cria arquivo final após upload de chunks"""
        
        url_create = f"{self.base_url}/file"
        params_create = {
            **params,
            "method": "create",
            "path": remote_path,
            "size": 0,  # Será calculado automaticamente
            "isdir": "0",
            "rtype": "3",
            "uploadid": upload_id,
            "block_list": json.dumps(part_list)
        }
        
        try:
            response = requests.post(url_create, params=params_create, timeout=30)
            result = response.json()
            
            if result.get("errno") == 0:
                print(f"✅ Upload concluído: {remote_path}")
                return remote_path
            else:
                print(f"❌ Erro criar arquivo: {result}")
                return None
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def _calcular_md5(self, arquivo_path: str) -> str:
        """Calcula MD5 do arquivo completo"""
        md5 = hashlib.md5()
        with open(arquivo_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                md5.update(chunk)
        return md5.hexdigest()
    
    def _calcular_md5_slice(self, arquivo_path: str, slice_size: int = 256*1024) -> str:
        """Calcula MD5 do primeiro slice (256KB)"""
        md5 = hashlib.md5()
        with open(arquivo_path, 'rb') as f:
            chunk = f.read(slice_size)
            md5.update(chunk)
        return md5.hexdigest()
    
    def download(self, remote_path: str, destino_path: str = None) -> Optional[str]:
        """Download de arquivo"""
        
        if not destino_path:
            destino_path = os.path.basename(remote_path)
        
        params = {
            **self._get_params(),
            "method": "filedownload",
            "path": remote_path
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/file",
                params=params,
                stream=True,
                timeout=600
            )
            
            if response.status_code == 200:
                with open(destino_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"⬇️ Download: {destino_path}")
                return destino_path
            else:
                print(f"❌ Erro download: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def listar_arquivos(self, path: str = "/apps/openclaw") -> List[Dict]:
        """Lista arquivos em uma pasta"""
        
        params = {
            **self._get_params(),
            "method": "list",
            "dir": path,
            "order": "time",
            "limit": "100"
        }
        
        try:
            response = requests.get(f"{self.base_url}/file", params=params, timeout=30)
            result = response.json()
            
            if result.get("errno") == 0:
                return result.get("list", [])
            else:
                print(f"❌ Erro listar: {result}")
                return []
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return []
    
    def compartilhar(self, remote_path: str, senha: str = None, periodo: int = 7) -> Optional[Dict]:
        """
        Gera link de compartilhamento
        
        Args:
            remote_path: Caminho do arquivo
            senha: Senha de 4 dígitos (opcional)
            periodo: Dias de validade (0=permanente, 1, 3, 7, 30)
            
        Returns:
            Dict com link e senha
        """
        
        params = {
            **self._get_params(),
            "method": "share",
            "paths": json.dumps([remote_path]),
            "pwd": senha or "",
            "period": periodo
        }
        
        try:
            response = requests.post(f"{self.base_url}/share", params=params, timeout=30)
            result = response.json()
            
            if result.get("errno") == 0:
                share_info = {
                    "link": f"https://pan.baidu.com/s/{result['shareid']}",
                    "senha": senha or "Sem senha",
                    "periodo": periodo
                }
                print(f"🔗 Link: {share_info['link']}")
                print(f"🔑 Senha: {share_info['senha']}")
                return share_info
            else:
                print(f"❌ Erro compartilhar: {result}")
                return None
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def espaco_usado(self) -> Dict:
        """Retorna espaço usado/disponível"""
        
        params = {
            **self._get_params(),
            "method": "quota"
        }
        
        try:
            response = requests.get(f"{self.base_url}/quota", params=params, timeout=30)
            result = response.json()
            
            if result.get("errno") == 0:
                total_gb = result.get("quota", 0) / 1024 / 1024 / 1024
                usado_gb = (result.get("quota", 0) - result.get("free", 0)) / 1024 / 1024 / 1024
                disponivel_gb = result.get("free", 0) / 1024 / 1024 / 1024
                
                return {
                    "total": f"{total_gb:.1f} GB",
                    "usado": f"{usado_gb:.1f} GB",
                    "disponivel": f"{disponivel_gb:.1f} GB"
                }
            else:
                return {"erro": result.get("errno")}
                
        except Exception as e:
            return {"erro": str(e)}


# Funções utilitárias
def upload_para_baidu(arquivo: str, pasta: str = "/apps/openclaw") -> Optional[Dict]:
    """Função rápida para upload + compartilhar"""
    baidu = BaiduStorage()
    remote_path = baidu.upload(arquivo, f"{pasta}/{os.path.basename(arquivo)}")
    if remote_path:
        return baidu.compartilhar(remote_path, senha="1234")
    return None


if __name__ == "__main__":
    print("Teste Baidu Yun Pan")
    print("="*50)
    
    baidu = BaiduStorage()
    
    if baidu.access_token:
        print("\n✅ Token configurado!")
        
        # Verificar espaço
        espaco = baidu.espaco_usado()
        print(f"\n💾 Espaço: {espaco}")
        
        # Listar arquivos
        print("\n📁 Arquivos:")
        arquivos = baidu.listar_arquivos()
        for f in arquivos[:5]:
            print(f"  • {f.get('server_filename', 'N/A')} ({f.get('size', 0)/1024/1024:.1f} MB)")
    else:
        print("\n❌ Configure BAIDU_ACCESS_TOKEN no .env")
        print("\n📝 Como obter:")
        print("1. Acesse: https://pan.baidu.com/union/console")
        print("2. Crie um app")
        print("3. Obtenha API Key e Secret")
        print("4. Autorize via OAuth")
        print("5. Copie access_token")
