#!/usr/bin/env python3
"""
Example workflow for YouTube Post-Production Agent

This demonstrates the complete pipeline from raw video to YouTube-ready package.
"""

import json
from pathlib import Path

# Import the agent
from youtube_post_agent_simple import YouTubePostAgentFFmpeg


def example_workflow():
    """Example: Process a raw video and prepare for upload."""
    
    # Configuration
    RAW_VIDEO = "raw_footage.mp4"      # Input from previous agent
    OUTPUT_TITLE = "Amazing Shorts - Must Watch!"
    DESCRIPTION = "Check out this incredible moment! Don't forget to like and subscribe."
    MUSIC_FILE = "background_music.mp3"  # Optional
    
    # Initialize agent
    agent = YouTubePostAgentFFmpeg(output_dir="youtube_output")
    
    # Process video
    print("🎬 Processing video...")
    result = agent.process(
        input_video=RAW_VIDEO,
        output_title=OUTPUT_TITLE,
        description=DESCRIPTION,
        tags=["shorts", "trending", "viral"],
        music_track=MUSIC_FILE if Path(MUSIC_FILE).exists() else None
    )
    
    # Display results
    print("\n✅ Processing complete!")
    print(f"   Edited video: {result['edited_video']}")
    print(f"   Thumbnail: {result['thumbnail']}")
    print(f"   SEO tags: {result['seo']['tags']}")
    
    # Save package info
    package_file = Path("youtube_output/package.json")
    with open(package_file, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\n📦 Package saved to {package_file}")
    print("\n📋 Next steps:")
    print("1. Review edited video and thumbnail")
    print("2. Set up YouTube API credentials (client_secret.json)")
    print("3. Run upload script")


def batch_process():
    """Process multiple videos at once."""
    
    videos = [
        {"input": "video1.mp4", "title": "First Video"},
        {"input": "video2.mp4", "title": "Second Video"},
    ]
    
    agent = YouTubePostAgentFFmpeg()
    
    for video in videos:
        if Path(video["input"]).exists():
            result = agent.process(
                input_video=video["input"],
                output_title=video["title"]
            )
            print(f"✓ Processed: {video['input']}")


if __name__ == "__main__":
    # Check if example video exists
    test_video = "test_input.mp4"
    
    if Path(test_video).exists():
        agent = YouTubePostAgentFFmpeg()
        result = agent.process(test_video, "Test Video - Shorts")
        print(json.dumps(result, indent=2))
    else:
        print("No test video found. Run with a video file as argument:")
        print("  python example_workflow.py input.mp4 'My Video Title'")