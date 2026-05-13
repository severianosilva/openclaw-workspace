# YouTube Post-Production Agent

## Quick Setup

### 1. Install Python Dependencies (Optional for advanced features)

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

**Minimum required:** FFmpeg (already installed on your system)

### 2. Google API Credentials (for YouTube upload)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable **YouTube Data API v3**
4. Create OAuth 2.0 credentials
5. Download `client_secret.json` to the agent directory

### 3. Basic Usage

**Simple version (FFmpeg only):**
```bash
python youtube_post_agent_simple.py input_video.mp4 "My Video Title"
```

**Full version (with MoviePy):**
```python
from youtube_post_agent import YouTubePostAgent

agent = YouTubePostAgent()
result = agent.process(
    input_video="raw.mp4",
    output_title="My Video",
    description="Description here",
    music_track="background.mp3"
)
```

## Features

| Feature | Status | Requirements |
|---------|--------|--------------|
| Video cutting/trimming | ✅ | FFmpeg |
| Transitions/fade effects | ✅ | FFmpeg |
| Background music | ✅ | FFmpeg |
| Thumbnail generation | ✅ | FFmpeg |
| YouTube upload | ✅ | Google API |
| SEO metadata | ✅ | Built-in |

## Output

```json
{
  "edited_video": "output/edited_video.mp4",
  "thumbnail": "output/thumbnail_video.jpg",
  "seo": {
    "title": "My Video",
    "description": "...",
    "tags": ["shorts", "trending", ...],
    "hashtags": "#my #video"
  },
  "ready_for_upload": true
}
```

## YouTube API Setup

For upload functionality:

1. **Create credentials file** (`client_secret.json`) from Google Cloud Console
2. **Run upload** (first run will open browser for auth):
   ```python
   result = agent.upload_to_youtube(
       video_path=result["edited_video"],
       thumbnail_path=result["thumbnail"],
       title="My Video",
       description="...",
       tags=["shorts", "viral"]
   )
   ```

## Directory Structure

```
youtube_post_agent/
├── youtube_post_agent.py         # Full version (MoviePy)
├── youtube_post_agent_simple.py  # FFmpeg-only version
├── requirements.txt
├── config.json
└── output/                       # Generated files
```