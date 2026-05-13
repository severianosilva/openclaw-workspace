@echo off
REM YouTube Autonomous Scheduler
REM Executa automaticamente todos os dias

:loop
echo [%date% %time%] Iniciando geração...
python "C:\Users\User\.openclaw\workspace\run_autonomous.py"
timeout /t 86400 /nobreak >nul
goto loop