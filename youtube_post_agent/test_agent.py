#!/usr/bin/env python3
"""
Test script for YouTube Post-Production Agent
Creates a sample video and processes it
"""

import subprocess
from pathlib import Path

def create_test_video():
    """Create a simple test video using FFmpeg."""
    output = Path("test_raw.mp4")
    
    print("Creating test video...")
    
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "testsrc2=duration=30:size=1280x720:rate=30",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        str(output)
    ], capture_output=True)
    
    return output if output.exists() else None


if __name__ == "__main__":
    test_video = create_test_video()
    
    if test_video:
        print(f"[OK] Test video created: {test_video}")
        
        import sys
        sys.path.insert(0, ".")
        from youtube_post_agent_simple import YouTubePostAgentFFmpeg
        
        agent = YouTubePostAgentFFmpeg()
        result = agent.process(
            input_video=str(test_video),
            output_title="Test Video - Automated Edit"
        )
        
        print("\n[DONE] Test complete!")
        print(f"Edited: {result['edited_video']}")
        print(f"Thumbnail: {result['thumbnail']}")
    else:
        print("[FAIL] Failed to create test video")