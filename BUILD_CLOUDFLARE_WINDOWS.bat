@echo off
python tools\build_cloudflare.py || exit /b 1
python tools\qa_cloudflare.py || exit /b 1
echo.
echo Cloudflare bundle verified in dist\
pause
