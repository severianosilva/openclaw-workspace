#!/usr/bin/env python3
"""
🧪 Exemplo de uso do YouTube Video Agent
Demonstra o fluxo completo de geração de vídeo
"""

import json
import os
from pathlib import Path

# Importar o agente
from agente_video_youtube import YouTubeVideoAgent

def main():
    print("🧪 EXEMPLO DE USO - YouTube Video Agent\n")
    
    # Configurações
    roteiro_exemplo = {
        "titulo": "Como Aprender Inglês Rápido em 2026",
        "nicho": "educacao",
        "duracao_alvo": "10min",
        "data_geracao": "2026-05-11T21:30:00",
        "estrutura": {
            "hook_0_5s": {
                "tempo": "0:00-0:05",
                "sugestao": "Você já se pegou pensando como aprender inglês rápido em 2026? Pois é, eu também. E hoje vou te mostrar exatamente como fazer isso."
            },
            "intro_5_30s": {
                "tempo": "0:05-0:30",
                "sugestao": "Eu sou Professor Expert e já ajudei milhares de pessoas a aprender inglês. Nesse vídeo, vou te mostrar exatamente os 4 métodos mais eficazes. Fica comigo até o final!"
            },
            "conteudo_principal": {
                "tempo": "0:30-8:00",
                "pontos": [
                    {
                        "ponto": 1,
                        "titulo": "Método 1: Imersão Diária",
                        "elementos": ["Explicação", "Exemplo prático", "Erro comum"]
                    },
                    {
                        "ponto": 2,
                        "titulo": "Método 2: Técnica Pomodoro",
                        "elementos": ["Explicação", "Demonstração", "Dica extra"]
                    },
                    {
                        "ponto": 3,
                        "titulo": "Método 3: Shadowing",
                        "elementos": ["Explicação", "Case real", "Atalho"]
                    },
                    {
                        "ponto": 4,
                        "titulo": "Método 4: Anki Cards",
                        "elementos": ["Dica exclusiva", "Ferramenta", "Recurso"]
                    }
                ]
            },
            "conclusao": {
                "tempo": "8:30-9:30",
                "sugestao": "Então é isso! Recapitulando: imersão diária, pomodoro, shadowing e anki. Comece hoje mesmo!"
            },
            "cta_final": {
                "tempo": "9:30-10:00",
                "sugestao": "Se quiser mais dicas, clica aqui. Comenta qual método você vai usar primeiro!"
            }
        }
    }
    
    # Criar diretório de teste
    test_dir = Path("./test_output")
    test_dir.mkdir(exist_ok=True)
    
    # Salvar roteiro exemplo
    roteiro_path = test_dir / "roteiro_teste.json"
    with open(roteiro_path, 'w', encoding='utf-8') as f:
        json.dump(roteiro_exemplo, f, ensure_ascii=False, indent=2)
    
    print(f"📄 Roteiro de teste criado: {roteiro_path}")
    
    # Inicializar agente
    agent = YouTubeVideoAgent(output_dir=str(test_dir / "production"))
    
    # Processar (apenas demonstração - não gera áudio real sem gtts instalado)
    print("\n" + "="*60)
    print("  PROCESSANDO ROTEIRO DE TESTE")
    print("="*60)
    
    try:
        # Carregar roteiro
        script = agent.load_script(str(roteiro_path))
        
        # Gerar texto de narração
        narration = agent.generate_narration_script(script)
        print(f"\n📝 Texto de narração ({len(narration)} caracteres):")
        print(f"  {narration[:200]}...")
        
        # Tentar gerar áudio (pode falhar se gtts não estiver instalado)
        print("\n🔊 Tentando gerar áudio TTS...")
        try:
            audio_path = agent.generate_tts_audio(
                narration[:500],  # Texto curto para teste
                "teste_audio"
            )
            print(f"✅ Áudio gerado: {audio_path}")
        except Exception as e:
            print(f"⚠️ TTS não disponível: {e}")
            print("   (Instale com: pip install gtts)")
        
        # Gerar imagens de teste
        print("\n🖼️ Gerando imagens de teste...")
        images = agent.generate_scene_images(script)
        print(f"✅ {len(images)} imagens geradas")
        
        # Salvar resultado
        result = {
            "script": script,
            "images": images,
            "output_dir": str(agent.output_dir)
        }
        
        result_path = test_dir / "resultado_teste.json"
        with open(result_path, 'w') as f:
            # Converter para JSON serializável
            result_json = {
                "script_titulo": result["script"]["titulo"],
                "num_imagens": len(result["images"]),
                "output_dir": result["output_dir"]
            }
            json.dump(result_json, f, indent=2)
        
        print(f"\n💾 Resultado salvo: {result_path}")
        
    except Exception as e:
        print(f"\n❌ Erro no processamento: {e}")
    
    print("\n" + "="*60)
    print("  TESTE CONCLUÍDO")
    print("="*60)
    print(f"\n📁 Arquivos em: {test_dir}")
    print("\nPróximo passo: Instale as dependências e execute no Colab!")

if __name__ == "__main__":
    main()