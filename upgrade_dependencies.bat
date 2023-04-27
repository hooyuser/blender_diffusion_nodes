@echo off
setlocal

set BUNDLE_DIR=bundle_packages
set REQUIREMENTS_FILE=requirements.txt

echo Upgrading packages from %REQUIREMENTS_FILE% into %BUNDLE_DIR% ...

pip install -r "%REQUIREMENTS_FILE%" -t "%BUNDLE_DIR%" --upgrade

echo Done.

pause