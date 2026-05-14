#!/usr/bin/env python3
"""Wan 2.1 Text-to-Video Autonomous Executor"""
import requests
import os
import json

PROMPT = "winter fox sunset tracking shot"
API_KEY = os.environ.get('INFERENCE_API_KEY', '')

if not API_KEY:
    print("Set INFERENCE_API_KEY environment variable")
else:
    print("Generating video...")
    r = requests.post('https://api.inference.sh/apps/run',
        headers={'Authorization': f'Bearer {API_KEY}'},
        json={'app': 'pruna/wan-t2v', 'input': {'prompt': PROMPT}})
    print(json.dumps(r.json(), indent=2))