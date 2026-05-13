@echo off
REM YouTube Post-Production Agent - Quick Run
REM Usage: run.bat input_video.mp4 "Video Title"

setlocal

if "%~1"=="" (
    echo Usage: run.bat input_video.mp4 "Video Title"
    echo Example: run.bat raw.mp4 "My Amazing Video"
    exit /b 1
)

set INPUT_VIDEO=%1
set VIDEO_TITLE=%2

if not exist "%INPUT_VIDEO%" (
    echo Error: Video file not found - %INPUT_VIDEO%
    exit /b 1
)

echo.
echo 🦀 YouTube Post-Production Agent
echo ================================
echo Input: %INPUT_VIDEO%
echo Title: %VIDEO_TITLE%
echo.

REM Run the agent
python youtube_post_agent_simple.py "%INPUT_VIDEO%" "%VIDEO_TITLE%"

if errorlevel 1 (
    echo.
    echo ❌ Processing failed
    exit /b 1
)

echo.
echo ✅ Done! Check the output folder for results.
echo.

endlocal