@echo off
REM Setup script for YouTube Post-Production Agent

echo 📦 Installing dependencies...

python -m pip install moviepy Pillow google-auth google-auth-oauthlib google-api-python-client

if errorlevel 1 (
    echo ❌ Installation failed. Make sure Python and pip are installed.
    exit /b 1
)

mkdir output 2>nul

echo ✅ Setup complete!
echo.
echo 📝 Next steps:
echo 1. Get YouTube API credentials from Google Cloud Console
echo 2. Save as client_secret.json in this directory
echo 3. Run: python youtube_post_agent.py input.mp4 --title "My Video"