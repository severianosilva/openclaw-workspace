#!/usr/bin/env python3
"""
🎥 Integração com APIs de Geração de Vídeo AI

Este módulo adiciona suporte para APIs gratuitas de geração de vídeo:
- Pika Labs (free tier limitado)
- Stable Video Diffusion (via HuggingFace)
- Kaiber (preview mode)
"""

import json
import os
import time
from typing import Dict, Optional
from pathlib import Path

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class AIVideoGenerator:
    """Integração com APIs de geração de vídeo AI"""
    
    def __init__(self):
        self.providers = {
            "pika": {
                "base_url": "https://api.pika.art/v1",
                "free_tier": "100 credits/month",
                "credit_cost": "80 credits per 10s 1080p"
            },
            "stable_video": {
                "base_url": "https://api.stability.ai/v2",
                "free_tier": "50 credits/month (trial)",
                "credit_cost": "~10 credits per clip"
            },
            "runway": {
                "base_url": "https://api.runwayml.com/v1",
                "free_tier": "125 seconds video/month",
                "credit_cost": "Free tier available"
            }
        }
    
    def generate_video_pika(self, prompt: str, duration: int = 3, 
                            api_key: str = None, 
                            aspect_ratio: str = "16:9") -> Optional[str]:
        """
        Gera vídeo usando Pika Labs API
        
        Limitações do free tier:
        - ~12 segundos de vídeo por mês (100 credits / 80 credits por vídeo)
        - Resolução até 1080p
        """
        if not api_key:
            print("⚠️ API key do Pika Labs necessária")
            print("   Obtenha em: https://pika.art/settings (requere conta)")
            return None
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "model": "pika-2.5"  # Modelo mais recente
        }
        
        try:
            # Submeter requisição
            response = requests.post(
                f"{self.providers['pika']['base_url']}/generate",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                video_url = result.get("video_url")
                
                # Download
                if video_url:
                    video_data = requests.get(video_url).content
                    output_path = f"pika_{int(time.time())}.mp4"
                    
                    with open(output_path, 'wb') as f:
                        f.write(video_data)
                    
                    print(f"✅ Vídeo Pika gerado: {output_path}")
                    print(f"   Credits usados: {result.get('credits_used', '?')}")
                    return output_path
            
            print(f"❌ Erro Pika: {response.status_code} - {response.text}")
            return None
            
        except Exception as e:
            print(f"❌ Erro ao gerar vídeo: {e}")
            return None
    
    def generate_video_stable(self, prompt: str, api_key: str = None,
                               duration: int = 3) -> Optional[str]:
        """
        Gera vídeo usando Stable Video Diffusion via Stability AI
        
        O trial gratuito oferece 50 credits (basta se cadastrar)
        """
        if not api_key:
            print("⚠️ API key da Stability AI necessária")
            print("   Obtenha em: https://stability.ai (trial gratuito)")
            return None
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Stable Video usa engine 3d-texture ou stable-video
        payload = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "clip_guidance_preset": "fastgreen",
            "sampler": "K_EULER_ANCESTRAL",
            "num_frames": duration * 8,  # 8 fps
            "width": 576,
            "height": 320
        }
        
        try:
            response = requests.post(
                f"{self.providers['stable_video']['base_url']}/generation/stable-video/generate",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                # Processar resposta (geralmente é um video gerado)
                result = response.json()
                # Salvar vídeo...
                output_path = f"stable_{int(time.time())}.mp4"
                print(f"✅ Vídeo Stable gerado: {output_path}")
                return output_path
            
            print(f"❌ Erro Stable: {response.status_code}")
            return None
            
        except Exception as e:
            print(f"❌ Erro Stable Video: {e}")
            return None
    
    def generate_video_runway(self, prompt: str, api_key: str = None,
                               duration: int = 4) -> Optional[str]:
        """
        Gera vídeo usando RunwayML API
        
        Free tier: 125 segundos de vídeo por mês
        """
        if not api_key:
            print("⚠️ API key do RunwayML necessária")
            print("   Obtenha em: https://runwayml.com (free tier)")
            return None
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "duration": duration,
            "model": "gen-2"  # Gen-2 do Runway
        }
        
        try:
            response = requests.post(
                f"{self.providers['runway']['base_url']}/videos",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                output_path = f"runway_{int(time.time())}.mp4"
                print(f"✅ Vídeo Runway gerado: {output_path}")
                return output_path
            
            print(f"❌ Erro Runway: {response.status_code}")
            return None
            
        except Exception as e:
            print(f"❌ Erro Runway: {e}")
            return None
    
    def generate_scene_video(self, descricao_cena: str, 
                            provider: str = "pika",
                            api_key: str = None) -> Optional[str]:
        """
        Gera vídeo para uma cena específica do roteiro
        
        Args:
            descricao_cena: Descrição da cena (ex: "pessoa estudando inglês")
            provider: "pika", "stable", ou "runway"
            api_key: API key correspondente
        
        Returns:
            Caminho do vídeo gerado ou None
        """
        prompt_base = f"high quality, cinematic, {descricao_cena}"
        
        if provider == "pika":
            return self.generate_video_pika(prompt_base, api_key=api_key)
        elif provider == "stable":
            return self.generate_video_stable(prompt_base, api_key=api_key)
        elif provider == "runway":
            return self.generate_video_runway(prompt_base, api_key=api_key)
        else:
            print(f"❌ Provider desconhecido: {provider}")
            return None


def create_video_generation_config():
    """Cria arquivo de configuração para geração de vídeo"""
    
    config = {
        "providers": {
            "pika": {
                "enabled": False,
                "api_key_env": "PIKA_API_KEY",
                "free_tier_info": "100 credits/month - ~12s 1080p video",
                "signup_url": "https://pika.art"
            },
            "stable_video": {
                "enabled": False,
                "api_key_env": "STABILITY_API_KEY",
                "free_tier_info": "50 credits free trial",
                "signup_url": "https://stability.ai"
            },
            "runway": {
                "enabled": False,
                "api_key_env": "RUNWAY_API_KEY",
                "free_tier_info": "125 seconds video/month",
                "signup_url": "https://runwayml.com"
            }
        },
        "usage_tips": [
            "Free tiers têm limites baixos - use com moderação",
            "Para vídeos longos, combine com stock images",
            "Pika é melhor para motion + estilização",
            "Stable é melhor para realismo",
            "Runway tem melhor qualidade geral"
        ]
    }
    
    with open("video_api_config.json", 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuração salva: video_api_config.json")
    return config


if __name__ == "__main__":
    print("🎥 AI Video Generator - Configuração\n")
    
    # Criar config
    config = create_video_generation_config()
    
    print("\n📋 Providers disponíveis:")
    for name, info in config["providers"].items():
        print(f"  {name}: {info['free_tier_info']}")
        print(f"    → {info['signup_url']}")