#!/usr/bin/env python3
"""Extrair e organizar backups do OpenClaw"""
import tarfile, zipfile
from pathlib import Path
import shutil

tar_file = Path("D:/OpenClaw Backup/organizacao_backup.tar")
destino = Path("D:/OpenClaw_Backup_Recuperado")

print(f"Extraindo {tar_file.name}...")
with tarfile.open(tar_file, 'r') as tar:
    # Extrair apenas diretórios principais
    members = [m for m in tar.getmembers() if m.islnk() or (m.isfile() and m.name.count('/') <= 3)]
    tar.extractall(destino, members=members)

print("Extração concluída!")
print(f"Conteúdo: {list((destino / 'organizacao').glob('*'))}")