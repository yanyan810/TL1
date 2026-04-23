@echo off
setlocal

for /f "usebackq delims=" %%I in (`powershell -NoProfile -Command "[Environment]::GetFolderPath('Desktop')"`) do set "DESKTOP=%%I"

set "SRC=%DESKTOP%\TL1\level_editor.py"
set "DST=%APPDATA%\Blender Foundation\Blender\4.4\scripts\addons\level_editor.py"

echo === source ===
echo %SRC%
echo === destination ===
echo %DST%
echo.

if not exist "%SRC%" (
    echo [ERROR] source file not found
    pause
    exit /b 1
)

if not exist "%APPDATA%\Blender Foundation\Blender\4.4\scripts\addons\" (
    echo [ERROR] destination folder not found
    pause
    exit /b 1
)

copy /Y "%SRC%" "%DST%"
if errorlevel 1 (
    echo [ERROR] copy failed
    pause
    exit /b 1
)

echo [OK] copied
pause