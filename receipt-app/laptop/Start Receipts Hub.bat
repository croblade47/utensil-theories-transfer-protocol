@echo off
cd /d "%~dp0"
echo Starting Door Receipts hub... leave this window open.
py receipt_hub.py 2>nul || python receipt_hub.py
pause
