#!/usr/bin/env python3
"""
Wan 2.1 Text-to-Video Autonomous Executor
Supports: inference.sh, Replicate (free credits), HuggingFace
"""
import requests
import os
import json
import sys

def run_replicate(prompt, api_key):
    """Use Replicate API with Wan 2.1"""
    print("Using Replicate API...")
    headers = {
        'Authorization': f'Token {api_key}',
        'Content-Type': 'application/json'
    }
    # Replicate Wan 2.1 model
    response = requests.post(
        'https://api.replicate.com/v1/models/wavespeedai/wan-2.1-t2v-720p/predictions',
        headers=headers,
        json={'input': {'prompt': prompt}},
        timeout=30
    )
    return response.json()

def run_inference_sh(prompt, api_key):
    """Use inference.sh API"""
    print("Using inference.sh API...")
    response = requests.post(
        'https://api.inference.sh/apps/run',
        headers={'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'},
        json={'app': 'pruna/wan-t2v', 'input': {'prompt': prompt}},
        timeout=30
    )
    return response.json()

def main():
    print("=== Wan 2.1 Autonomous Executor ===")
    
    PROMPT = "a fox moving quickly in a beautiful winter scenery nature trees sunset tracking camera"
    print(f"Prompt: {PROMPT}")
    
    # Try inference.sh first
    API_KEY = os.environ.get('INFERENCE_API_KEY', '')
    if API_KEY:
        result = run_inference_sh(PROMPT, API_KEY)
        if result.get('success'):
            print("\n=== VIDEO READY ===")
            print(json.dumps(result, indent=2))
            return
        print(f"Failed: {result}")
    
    # Try Replicate
    REPLICATE_KEY = os.environ.get('REPLICATE_API_TOKEN', '')
    if REPLICATE_KEY:
        result = run_replicate(PROMPT, REPLICATE_KEY)
        print("\n=== RESULT ===")
        print(json.dumps(result, indent=2))
        if 'urls' in result:
            print(f"\nVideo URL: {result['urls'].get('get')}")
        return
    
    print("\nNo API keys found. Set either:")
    print("- INFERENCE_API_KEY")
    print("- REPLICATE_API_TOKEN")

if __name__ == "__main__":
    main()