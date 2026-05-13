#!/usr/bin/env python3
"""
YouTube Post-Production Agent
Automated video editing, thumbnail generation, and YouTube upload
"""

import os
import json
import random
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any

from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip
from moviepy.video.fx import fadein, fadeout
from PIL import Image, ImageDraw, ImageFont
import numpy as np


class YouTubePostAgent:
    """
    Complete post-production pipeline for YouTube videos.
    
    Features:
    - Automatic video editing (cuts, transitions, music)
    - Thumbnail generation (optimized for YouTube)
    - YouTube upload with SEO optimization
    """
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def process(
        self,
        input_video: str,
        output_title: str,
        description: str = "",
        tags: List[str] = None,
        music_track: Optional[str] = None,
        max_duration: int = 60,  # Max clips duration in seconds
        num_short_clips: int = 3,
        thumbnail_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Full post-production pipeline.
        
        Args:
            input_video: Path to raw video file
            output_title: YouTube video title
            description: Video description
            tags: List of tags
            music_track: Optional background music
            max_duration: Duration per clip segment
            num_short_clips: Number of short clips to generate
            thumbnail_text: Text for thumbnail (default: title)
        
        Returns:
            Dictionary with paths to edited video, thumbnail, and upload info
        """
        input_path = Path(input_video)
        if not input_path.exists():
            raise FileNotFoundError(f"Input video not found: {input_video}")
        
        # Step 1: Analyze and split video
        print("📊 Analyzing video...")
        clips = self._split_video(input_path, max_duration)
        
        # Step 2: Add transitions and music
        print("✂️ Editing video with transitions...")
        edited_video = self._edit_video(clips, music_track)
        
        # Step 3: Generate thumbnail
        print("🎨 Generating thumbnail...")
        thumbnail_path = self._generate_thumbnail(
            input_path, 
            thumbnail_text or output_title
        )
        
        # Step 4: Save edited video
        output_video = self.output_dir / f"edited_{input_path.stem}.mp4"
        print(f"💾 Saving edited video to {output_video}...")
        edited_video.write_videofile(
            str(output_video),
            codec="libx264",
            audio_codec="aac",
            fps=30,
            threads=4
        )
        
        # Step 5: Prepare SEO metadata
        seo_data = self._generate_seo_metadata(output_title, description, tags)
        
        return {
            "edited_video": str(output_video),
            "thumbnail": str(thumbnail_path),
            "seo": seo_data,
            "ready_for_upload": True
        }
    
    def _split_video(self, video_path: Path, max_duration: int) -> List[Path]:
        """Split video into segments and extract exciting parts."""
        clip = VideoFileClip(str(video_path))
        duration = clip.duration
        clip.close()
        
        segments = []
        segment_duration = min(max_duration, duration / 3)
        
        # Extract 3 interesting segments
        timestamps = []
        if duration > segment_duration * 2:
            timestamps = [0, duration // 2 - segment_duration // 2, duration - segment_duration]
        else:
            timestamps = [0]
        
        for i, start in enumerate(timestamps):
            end = min(start + segment_duration, duration)
            segment_path = self.output_dir / f"segment_{i}.mp4"
            
            subprocess.run([
                "ffmpeg", "-y", "-i", str(video_path),
                "-ss", str(start), "-to", str(end),
                "-c:v", "libx264", "-c:a", "aac",
                str(segment_path)
            ], capture_output=True)
            
            segments.append(segment_path)
        
        return segments
    
    def _edit_video(self, segments: List[Path], music_track: Optional[str] = None) -> VideoFileClip:
        """Apply transitions, cuts, and add background music."""
        clips = [VideoFileClip(str(s)) for s in segments]
        
        # Add crossfade transitions
        final_clips = []
        for i, clip in enumerate(clips):
            final_clips.append(clip.fadein(0.5))
            if i > 0:
                final_clips[-2] = final_clips[-2].fadeout(0.5)
        
        # Concatenate with overlap for crossfade effect
        final_video = concatenate_videoclips(final_clips, method="compose")
        
        # Add background music if provided
        if music_track and Path(music_track).exists():
            audio = AudioFileClip(music_track)
            audio = audio.volumex(0.3)  # Lower volume
            audio = audio.set_duration(final_video.duration)
            final_video = final_video.set_audio(
                CompositeAudioClip([final_video.audio, audio]) if final_video.audio else audio
            )
        
        return final_video
    
    def _generate_thumbnail(self, video_path: Path, text: str) -> Path:
        """Generate YouTube-optimized thumbnail."""
        # Extract frame from video
        clip = VideoFileClip(str(video_path))
        frame_time = min(1.0, clip.duration / 3)
        frame = clip.get_frame(frame_time)
        clip.close()
        
        # Create image
        img = Image.fromarray(frame)
        img = img.resize((1280, 720))  # YouTube thumbnail size
        
        # Add overlay gradient
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Gradient overlay (dark at bottom)
        for y in range(img.size[1] - 200, img.size[1]):
            alpha = int(255 * (y - (img.size[1] - 200)) / 200)
            draw.line([(0, y), (img.size[0], y)], fill=(0, 0, 0, alpha))
        
        # Add text
        img = Image.alpha_composite(img.convert('RGBA'), overlay)
        draw = ImageDraw.Draw(img)
        
        # Try to use a bold font, fallback to default
        try:
            font = ImageFont.truetype("arialbd.ttf", 80)
            small_font = ImageFont.truetype("arialbd.ttf", 40)
        except:
            font = ImageFont.load_default()
            small_font = font
        
        # Multi-line text
        words = text.split()
        lines = []
        current_line = []
        for word in words[:6]:  # Max 6 words
            current_line.append(word)
            if len(current_line) >= 2:
                lines.append(" ".join(current_line))
                current_line = []
        if current_line:
            lines.append(" ".join(current_line))
        
        # Draw text with outline
        y_text = img.size[1] - 180
        for line in lines[-2:]:  # Max 2 lines
            # Outline
            draw.text((52, y_text), line, font=font, fill="black")
            draw.text((48, y_text), line, font=font, fill="white")
            draw.text((50, y_text + 2), line, font=font, fill="white")
            draw.text((50, y_text - 2), line, font=font, fill="white")
            draw.text((50, y_text), line, font=font, fill="yellow")
            y_text += 90
        
        # Save
        thumbnail_path = self.output_dir / f"thumbnail_{video_path.stem}.jpg"
        img.convert('RGB').save(thumbnail_path, quality=95)
        
        return thumbnail_path
    
    def _generate_seo_metadata(self, title: str, description: str, tags: List[str] = None) -> Dict:
        """Generate YouTube SEO optimized metadata."""
        # Extract keywords from title
        keywords = title.lower().replace("-", " ").replace("|", " ").split()
        keywords = [k for k in keywords if len(k) > 3]
        
        # Default tags with trending keywords
        default_tags = ["shorts", "trending", "viral", "youtube"]
        all_tags = (tags or []) + keywords + default_tags
        
        # Generate hashtags
        hashtags = " ".join([f"#{tag}" for tag in keywords[:3]])
        
        return {
            "title": title,
            "description": f"{description}\n\n{hashtags}\n\n#shorts #viral #youtube",
            "tags": list(set(all_tags))[:15],  # YouTube limit
            "has_part_of_series": False,
            "made_for_kids": False
        }
    
    def upload_to_youtube(
        self,
        video_path: str,
        thumbnail_path: str,
        title: str,
        description: str,
        tags: List[str] = None,
        credentials_file: str = "client_secret.json"
    ) -> Dict[str, Any]:
        """
        Upload video to YouTube.
        
        Requires Google API credentials (client_secret.json).
        First run will require OAuth authentication.
        """
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        
        SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
        
        flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
        credentials = flow.run_local_server(port=0)
        youtube = build("youtube", "v3", credentials=credentials)
        
        # Prepare upload
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or [],
                "categoryId": "22"  # People & Blogs
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        }
        
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media
        )
        
        print("🚀 Uploading to YouTube...")
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"   Uploaded {int(status.progress() * 100)}%")
        
        video_id = response["id"]
        
        # Upload thumbnail
        if Path(thumbnail_path).exists():
            youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            ).execute()
        
        return {
            "video_id": video_id,
            "url": f"https://youtube.com/watch?v={video_id}",
            "status": "uploaded"
        }


def main():
    """CLI interface for the agent."""
    import argparse
    
    parser = argparse.ArgumentParser(description="YouTube Post-Production Agent")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("--title", required=True, help="Video title")
    parser.add_argument("--description", default="", help="Video description")
    parser.add_argument("--tags", nargs="*", help="Video tags")
    parser.add_argument("--music", help="Background music file")
    
    args = parser.parse_args()
    
    agent = YouTubePostAgent()
    result = agent.process(
        input_video=args.input,
        output_title=args.title,
        description=args.description,
        tags=args.tags,
        music_track=args.music
    )
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()