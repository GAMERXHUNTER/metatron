
@echo off
echo ===============================
echo   🔧 Git Project Initializer
echo ===============================
echo.

:: Step 1: Initialize Git repo
git init

:: Step 2: Add all files (except those ignored by .gitignore)
git add .

:: Step 3: Commit with version message
git commit -m "Initial commit - Metatron v6"

:: Step 4: Prompt for remote repo URL
set /p REMOTE_URL="Enter your GitHub repo URL (e.g. https://github.com/youruser/metatron.git): "

:: Step 5: Add remote and push
git remote add origin %REMOTE_URL%
git branch -M main
git push -u origin main

echo.
echo ✅ GitHub push complete (if no errors above).
pause
