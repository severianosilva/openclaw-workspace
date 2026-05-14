import requests
import json
import os

# Use environment variable for API key
HF_KEY = os.environ.get('HF_API_KEY', '')
PROMPT = 'winter fox sunset'

print("Wan 2.1 Executor")
print("Set HF_API_KEY environment variable")

if not HF_KEY:
    print("ERROR: Set HF_API_KEY")
else:
    # Available free models for video
    models = [
        'stabilityai/stable-video-diffusion-img2vid-xt',
        'cerspense/zeroscope_v2_576w'
    ]
    
    for model in models:
        try:
            print(f"Trying {model}...")
            r = requests.post(
                f'https://api-inference.huggingface.co/models/{model}',
                headers={'Authorization': f'Bearer {HF_KEY}'},
                json={'inputs': PROMPT},
                timeout=60
            )
            if r.status_code == 200:
                with open('output.mp4', 'wb') as f:
                    f.write(r.content)
                print(f"SUCCESS! Saved output.mp4")
                break
            else:
                print(f"  Status {r.status_code}")
        except Exception as e:
            print(f"  Error: {e}")