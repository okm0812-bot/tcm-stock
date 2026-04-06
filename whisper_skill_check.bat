@echo off
set PATH=C:\Users\user\AppData\Roaming\Python\Python314\Scripts;%PATH%
echo Whisper path check:
where whisper 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo whisper not found in PATH
)
echo.
echo Testing whisper:
whisper.exe --help 2>&1 | findstr /i "usage"
