@echo off
echo ============================================
echo Pushing SDG Ethiopia Chatbot to GitHub
echo ============================================
echo.

REM Remove existing remote if it exists
git remote remove origin 2>nul

echo Step 1: Adding GitHub remote...
git remote add origin https://github.com/Jonas2127/sdg-ethiopia-chatbot.git

echo.
echo Step 2: Pushing to GitHub...
echo Please enter your Personal Access Token when prompted for password!
echo.

git push -u origin main

echo.
echo ============================================
if %ERRORLEVEL% EQU 0 (
    echo SUCCESS! Code pushed to GitHub!
    echo.
    echo View your repository at:
    echo https://github.com/Jonas2127/sdg-ethiopia-chatbot
) else (
    echo FAILED! There was an error.
    echo Make sure you entered the correct token.
)
echo ============================================
echo.
pause
