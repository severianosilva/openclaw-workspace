# YouTube Post-Production Agent

Automated video editing, thumbnail generation, and YouTube upload with SEO optimization.

## Features
- ✅ Automatic video editing (cuts, transitions, music)
- ✅ Thumbnail generation (optimized for YouTube)
- ✅ YouTube upload with SEO optimization
- ✅ Free APIs/tools only

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from youtube_post_agent import YouTubePostAgent

agent = YouTubePostAgent()
result = agent.process(
    input_video="raw_video.mp4",
    output_title="My Video Title",
    description="Video description",
    tags=["tag1", "tag2"],
    music_track="background_music.mp3"  # optional
)
```

## Free Tools Used
- **FFmpeg** - Video processing
- **MoviePy** - Python video editing
- **PIL/Pillow** - Thumbnail generation
- **Google API Python Client** - YouTube Data API v3
- **Whisper** - Auto transcription for SEO keywords