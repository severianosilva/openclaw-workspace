#!/bin/bash
# Setup script for YouTube Post-Production Agent

echo "📦 Installing dependencies..."

# Check if pip is available
if command -v pip &> /dev/null; then
    pip install moviepy Pillow google-auth google-auth-oauthlib google-api-python-client
elif command -v pip3 &> /dev/null; then
    pip3 install moviepy Pillow google-auth google-auth-oauthlib google-api-python-client
else
    echo "❌ pip not found. Please install Python 3 and pip."
    exit 1
fi

# Create output directory
mkdir -p output

echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Get YouTube API credentials from Google Cloud Console"
echo "2. Save as client_secret.json in this directory"
echo "3. Run: python youtube_post_agent.py input.mp4 --title 'My Video'"