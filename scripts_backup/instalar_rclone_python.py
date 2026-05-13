#!/usr/bin/env python3
"""
Instalador do rclone usando Python (sem dependências externas)
"""

import os
import sys
import urllib.request
import zipfile
import tarfile
import shutil

def instalar_rclone():
    """Instala rclone no diretório local do usuário"""
    
    print("="*60)
    print("  INSTALADOR RCLONE - PYTHON")
    print("="*60)
    print()
    
    # Diretórios
    home = os.path.expanduser("~")
    local_bin = os.path.join(home, ".local", "bin")
    os.makedirs(local_bin, exist_ok=True)
    
    rclone_path = os.path.join(local_bin, "rclone")
    
    # Verificar se já existe
    if os.path.exists(rclone_path):
        print(f"✅ rclone já instalado em: {rclone_path}")
        version = os.popen(f"{rclone_path} version 2>/dev/null | head -1").read().strip()
        print(f"   Versão: {version}")
        return True
    
    # Detectar arquitetura
    import platform
    machine = platform.machine().lower()
    system = platform.system().lower()
    
    if "x86_64" in machine or "amd64" in machine:
        arch = "amd64"
    elif "arm64" in machine or "aarch64" in machine:
        arch = "arm64"
    elif "arm" in machine:
        arch = "arm"
    else:
        arch = "amd64"  # default
    
    if system == "linux":
        os_name = "linux"
        ext = "zip"
    elif system == "darwin":
        os_name = "osx"
        ext = "zip"
    else:
        print(f"❌ Sistema não suportado: {system}")
        return False
    
    print(f"📥 Baixando rclone para {os_name}-{arch}...")
    
    # URL de download
    version = "1.65.2"  # versão estável
    url = f"https://downloads.rclone.org/v{version}/rclone-v{version}-{os_name}-{arch}.{ext}"
    
    # Arquivo temporário
    temp_dir = "/tmp/rclone_install"
    os.makedirs(temp_dir, exist_ok=True)
    download_file = os.path.join(temp_dir, f"rclone.{ext}")
    
    try:
        # Download
        print(f"   URL: {url}")
        urllib.request.urlretrieve(url, download_file)
        print(f"   ✓ Download concluído: {os.path.getsize(download_file) / 1024:.1f} KB")
        
        # Extrair
        print("📦 Extraindo...")
        if ext == "zip":
            with zipfile.ZipFile(download_file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
        else:
            with tarfile.open(download_file, 'r:gz') as tar_ref:
                tar_ref.extractall(temp_dir)
        
        # Encontrar binário extraído
        extracted_dir = None
        for item in os.listdir(temp_dir):
            if item.startswith("rclone-") and os.path.isdir(os.path.join(temp_dir, item)):
                extracted_dir = os.path.join(temp_dir, item)
                break
        
        if not extracted_dir:
            print("❌ Diretório extraído não encontrado")
            return False
        
        # Copiar binário
        source = os.path.join(extracted_dir, "rclone")
        if not os.path.exists(source):
            # Procurar em subdiretórios
            for root, dirs, files in os.walk(temp_dir):
                if "rclone" in files:
                    source = os.path.join(root, "rclone")
                    break
        
        shutil.copy2(source, rclone_path)
        os.chmod(rclone_path, 0o755)
        
        print(f"✅ rclone instalado em: {rclone_path}")
        
        # Atualizar PATH se necessário
        bashrc = os.path.join(home, ".bashrc")
        path_line = f'export PATH="$HOME/.local/bin:$PATH"'
        
        if os.path.exists(bashrc):
            with open(bashrc, 'r') as f:
                content = f.read()
            
            if ".local/bin" not in content:
                with open(bashrc, 'a') as f:
                    f.write(f"\n# RClone\n{path_line}\n")
                print(f"   ✓ PATH atualizado em {bashrc}")
        
        # Testar
        version = os.popen(f"{rclone_path} version 2>/dev/null | head -1").read().strip()
        print(f"   Versão: {version}")
        
        # Limpar temp
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        print()
        print("="*60)
        print("  INSTALAÇÃO CONCLUÍDA!")
        print("="*60)
        print()
        print("Para usar rclone:")
        print(f"  {rclone_path} version")
        print()
        print("Para configurar:")
        print(f"  {rclone_path} config")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na instalação: {e}")
        return False

if __name__ == "__main__":
    sucesso = instalar_rclone()
    sys.exit(0 if sucesso else 1)
