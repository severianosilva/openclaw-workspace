#!/usr/bin/env python3
"""
Script para baixar e configurar o modelo Vosk para português
"""

import os
import requests
import zipfile
import shutil
from pathlib import Path

def baixar_modelo_vosk():
    """
    Baixa o modelo Vosk para português de um repositório oficial
    """
    # URLs alternativas para o modelo português
    urls_modelos = [
        {
            'url': 'https://alphacephei.blob.core.windows.net/models/vosk-model-small-pt-0.3.zip',
            'nome': 'vosk-model-small-pt-0.3'
        },
        {
            'url': 'https://github.com/alphacep/vosk-models/releases/download/v0.3.2/vosk-model-small-pt-0.3.zip',
            'nome': 'vosk-model-small-pt-0.3'
        }
    ]
    
    # Diretório onde vamos armazenar o modelo
    model_dir = Path.home() / '.local' / 'share' / 'vosk'
    model_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Diretório de modelos: {model_dir}")
    
    for modelo_info in urls_modelos:
        url = modelo_info['url']
        nome_modelo = modelo_info['nome']
        
        print(f"Tentando baixar modelo: {nome_modelo}")
        print(f"URL: {url}")
        
        try:
            # Fazer o download do modelo
            print("Baixando modelo...")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            zip_path = model_dir / f"{nome_modelo}.zip"
            
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Download concluído: {zip_path}")
            
            # Extrair o modelo
            extract_dir = model_dir / nome_modelo
            print(f"Extraindo para: {extract_dir}")
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Verificar se a extração foi bem-sucedida
            if (extract_dir / "am" / "final.mdl").exists():
                print(f"✓ Modelo extraído com sucesso em: {extract_dir}")
                
                # Verificar estrutura do modelo
                print("Estrutura do modelo:")
                for item in extract_dir.rglob("*"):
                    if item.is_file():
                        print(f"  {item.relative_to(extract_dir)}")
                
                # Apagar o arquivo ZIP após extração
                zip_path.unlink()
                
                print(f"\nModelo pronto para uso!")
                print(f"Caminho: {extract_dir}")
                
                # Testar o modelo
                testar_modelo(extract_dir)
                
                return str(extract_dir)
            else:
                print("✗ Estrutura do modelo inválida após extração")
                # Remover diretório de extração se inválido
                shutil.rmtree(extract_dir)
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Erro de rede ao baixar: {e}")
        except zipfile.BadZipFile:
            print("✗ Arquivo ZIP corrompido")
        except Exception as e:
            print(f"✗ Erro ao processar modelo: {e}")
    
    print("\n✗ Não foi possível baixar nenhum modelo")
    return None

def testar_modelo(model_path):
    """
    Testa se o modelo pode ser carregado corretamente
    """
    try:
        from vosk import Model
        
        print(f"\nTestando modelo em: {model_path}")
        model = Model(model_path)
        print("✓ Modelo carregado com sucesso!")
        
        # Salvar o caminho do modelo para uso futuro
        config_file = Path.home() / '.config' / 'vosk_model_path.txt'
        config_file.parent.mkdir(exist_ok=True)
        
        with open(config_file, 'w') as f:
            f.write(model_path)
        
        print(f"Caminho do modelo salvo em: {config_file}")
        
    except ImportError:
        print("✗ Vosk não está instalado")
    except Exception as e:
        print(f"✗ Erro ao testar modelo: {e}")

if __name__ == "__main__":
    print("Baixando modelo Vosk para português...")
    model_path = baixar_modelo_vosk()
    
    if model_path:
        print(f"\n✓ Modelo instalado com sucesso em: {model_path}")
    else:
        print("\n✗ Falha na instalação do modelo")
        print("Tente alternativas manuais ou verifique sua conexão com a internet")