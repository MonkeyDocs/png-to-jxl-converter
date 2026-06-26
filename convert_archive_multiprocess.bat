@echo off

set SCRIPT_DIR=%~dp0
set SCRIPT_NAME=convert_archive_multiprocess.py

:: Check if a folder was dragged and dropped onto the file
if "%~1" == "" (
    echo [!] No folder dropped. Running converter in the current directory...
    echo     Target: %CD%
    echo.
    python "%SCRIPT_DIR%%SCRIPT_NAME%" "%CD%"
) else (
    echo [✓] Folder detected: %1
    echo.
    python "%SCRIPT_DIR%%SCRIPT_NAME%" %1
)

echo.
echo Operation complete.
pause