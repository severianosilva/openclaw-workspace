# YouTube Post-Production Agent

## Overview

Automated post-production pipeline for YouTube videos. Receives raw footage from upstream agents and outputs YouTube-ready videos with optimized thumbnails and SEO metadata.

## Usage

### Quick Start (FFmpeg-only, no dependencies)

```bash
python youtube_post_agent_simple.py raw_video.mp4 "My Video Title"
```

### Full Version (with advanced editing)

```python
from youtube_post_agent import YouTubePostAgent

agent = YouTubePostAgent()
result = agent.process(
    input_video="raw_footage.mp4",
    output_title="Amazing Shorts - Must Watch!",
    description="Check out this incredible moment!",
    tags=["shorts", "trending", "viral"],
    music_track="background_music.mp3"
)
```

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

## Features

| Feature | Status |
|---------|--------|
| Video cutting/trimming | ✅ FFmpeg |
| Transitions/fade effects | ✅ FFmpeg |
| Background music mixing | ✅ FFmpeg |
| Thumbnail generation | ✅ FFmpeg |
| YouTube upload | ✅ Google API |
| SEO metadata generation | ✅ Built-in |

## YouTube API Setup (for upload)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Enable YouTube Data API v3
3. Create OAuth 2.0 credentials
4. Save `client_secret.json` in the agent directory
5. First upload will open browser for authentication

## Integration with Other Agents

This agent fits into the content creation pipeline:

```
[Content Idea] → [Raw Recording] → [YouTubePostAgent] → YouTube
                    ↓
              raw_video.mp4
```

## Requirements

- FFmpeg (installed)
- Python 3.x
- Optional: Google API credentials for upload