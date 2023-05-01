@echo off
setlocal

set BUNDLE_DIR=bundle_packages
set REQUIREMENTS_FILE=requirements.txt

echo Installing packages from %REQUIREMENTS_FILE% into %BUNDLE_DIR% ...

C:\Program Files\Blender Foundation\blender-3.6.0-alpha+main.e4eb9e04e016-windows.amd64-release\3.6\python\bin\python.exe -m pip install -r "%REQUIREMENTS_FILE%" -t "%BUNDLE_DIR%"

echo Done.

pause