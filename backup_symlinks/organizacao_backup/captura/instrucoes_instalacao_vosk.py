#!/usr/bin/env python3
"""
Script para verificar e instalar o modelo Vosk para português corretamente
"""

import os
import subprocess
import sys
from pathlib import Path

def verificar_instalacao_vosk():
    """Verifica se o Vosk está instalado e funcional"""
    try:
        import vosk
        print("✓ Vosk está instalado")
        
        # Verifica modelos disponíveis
        try:
            modelos = vosk.list_models()
            print(f"Modelos disponíveis: {modelos}")
        except AttributeError:
            print("? Não foi possível listar modelos diretamente com vosk.list_models()")
            
        return True
    except ImportError:
        print("✗ Vosk não está instalado")
        return False

def instalar_modelo_portugues():
    """Instala o modelo Vosk para português"""
    try:
        # Primeiro, vamos tentar encontrar onde os modelos são armazenados
        import vosk
        from vosk import Model
        
        # Caminho padrão onde o Vosk espera encontrar modelos
        home_dir = Path.home()
        model_paths = [
            home_dir / ".vosk",
            Path("/opt/vosk"),
            Path("./models"),
            Path("/tmp/vosk-models")
        ]
        
        # Criar diretório temporário para o modelo
        model_dir = Path("/tmp/vosk-model-small-pt-0.3")
        model_dir.mkdir(exist_ok=True)
        
        print(f"Tentando baixar modelo para: {model_dir}")
        
        # Baixar o modelo usando git-lfs ou wget
        import urllib.request
        import zipfile
        
        # URL alternativa para o modelo português
        urls_possiveis = [
            "https://github.com/alphacep/vosk-models/raw/main/vosk-model-small-pt-0.3.zip",
            "https://alphacephei.blob.core.windows.net/models/vosk-model-small-pt-0.3.zip",
            "https://github.com/alphacep/vosk-models/releases/download/dict-phone-based/vosk-model-small-pt-0.3.zip"
        ]
        
        modelo_baixado = False
        for url in urls_possiveis:
            try:
                print(f"Tentando baixar de: {url}")
                zip_path = model_dir / "model.zip"
                
                # Baixar o arquivo
                urllib.request.urlretrieve(url, str(zip_path))
                
                # Extrair o modelo
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(model_dir)
                
                # O modelo extraído geralmente está em uma subpasta
                extracted_dirs = [d for d in model_dir.iterdir() if d.is_dir()]
                if extracted_dirs:
                    model_subdir = extracted_dirs[0]
                    print(f"Modelo extraído para: {model_subdir}")
                    
                    # Verificar se é realmente um modelo Vosk
                    if (model_subdir / "am" / "final.mdl").exists() and (model_subdir / "graph" / "HCLG.fst").exists():
                        print("✓ Modelo Vosk válido encontrado!")
                        
                        # Agora tentar carregar o modelo
                        try:
                            model = Model(str(model_subdir))
                            print("✓ Modelo Vosk carregado com sucesso!")
                            
                            # Salvar o caminho do modelo para uso futuro
                            with open("/tmp/vosk_model_path.txt", "w") as f:
                                f.write(str(model_subdir))
                                
                            return str(model_subdir)
                        except Exception as e:
                            print(f"✗ Erro ao carregar modelo: {e}")
                    else:
                        print("✗ Pasta extraída não contém estrutura válida de modelo Vosk")
                
                modelo_baixado = True
                break
                
            except Exception as e:
                print(f"✗ Falha ao baixar de {url}: {e}")
                continue
        
        if not modelo_baixado:
            print("✗ Nenhum dos URLs de modelo funcionou")
            
    except Exception as e:
        print(f"Erro durante instalação do modelo: {e}")
    
    return None

def testar_modelo_salvo():
    """Testa o modelo Vosk salvo"""
    try:
        import vosk
        from vosk import Model, KaldiRecognizer
        import json
        
        # Verificar se temos um caminho de modelo salvo
        model_path_file = Path("/tmp/vosk_model_path.txt")
        if model_path_file.exists():
            with open(model_path_file, "r") as f:
                model_path = f.read().strip()
        else:
            print("? Nenhum modelo salvo encontrado")
            return False
        
        print(f"Tentando carregar modelo de: {model_path}")
        
        # Carregar modelo
        model = Model(model_path)
        print("✓ Modelo carregado com sucesso")
        
        # Testar com um áudio pequeno (exemplo simulado)
        # Na prática, você usaria um arquivo de áudio real
        rec = KaldiRecognizer(model, 16000)  # 16kHz sample rate
        
        print("✓ Reconhecedor criado com sucesso")
        return True
        
    except Exception as e:
        print(f"✗ Erro ao testar modelo salvo: {e}")
        return False

if __name__ == "__main__":
    print("=== Verificação e Instalação do Modelo Vosk ===")
    
    # Verificar instalação existente
    if verificar_instalacao_vosk():
        print("\n--- Testando modelo salvo ---")
        if not testar_modelo_salvo():
            print("\n--- Instalando novo modelo ---")
            model_path = instalar_modelo_portugues()
            if model_path:
                print(f"\n✓ Modelo instalado com sucesso em: {model_path}")
                print("Para usar este modelo, atualize seus scripts para apontar para este caminho")
            else:
                print("\n✗ Falha na instalação do modelo")
        else:
            print("\n✓ Modelo existente está funcionando corretamente")
    else:
        print("\n--- Instalando Vosk ---")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "vosk"])
            print("✓ Vosk instalado via pip")
            
            model_path = instalar_modelo_portugues()
            if model_path:
                print(f"\n✓ Modelo instalado com sucesso em: {model_path}")
            else:
                print("\n✗ Falha na instalação do modelo")
        except Exception as e:
            print(f"✗ Erro ao instalar Vosk: {e}")