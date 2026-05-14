---
name: colab-wan-executor
description: Execute Wan 2.1 text-to-video generation autonomously in Google Colab without manual intervention
allowed-tools: []
---

# Wan 2.1 Colab Executor

Automatiza a execução completa do processo de geração de vídeo Wan 2.1 no Google Colab.

## Uso

1. Execute no Colab:
```python
exec(requests.get('https://raw.githubusercontent.com/severianosilva/openclaw-workspace/master/wan_2_1_colab.ipynb').text)
```

2. Configure a API key:
```python
import os
os.environ['INFERENCE_API_KEY'] = 'your_key_here'
```

3. Execute:
```python
!python wan_executor.py
```

## Arquivo wan_executor.py

```python
import requests, os, json, time

API_KEY = os.environ.get('INFERENCE_API_KEY')
if not API_KEY:
    print("ERROR: Set INFERENCE_API_KEY")
    exit(1)

response = requests.post(
    'https://api.inference.sh/v1/apps/run',
    headers={'Authorization': f'Bearer {API_KEY}'},
    json={'app': 'pruna/wan-t2v', 'input': {'prompt': 'winter fox sunset'}}
).json()

print(json.dumps(response, indent=2))
```