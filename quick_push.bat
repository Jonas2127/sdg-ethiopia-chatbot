@echo off
echo ========================================
echo  Quick Push - SDG Ethiopia Chatbot
echo ========================================
echo.

echo Step 1: Adding changes...
git add app.py requirements.txt

echo.
echo Step 2: Creating commit...
git commit -m "Fix: Support Streamlit Cloud secrets for API key"

echo.
echo Step 3: Pushing to GitHub...
git push

echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo  SUCCESS! Changes pushed to GitHub
    echo ========================================
    echo.
    echo Streamlit Cloud will auto-deploy in ~1 minute
    echo.
    echo NEXT STEPS:
    echo 1. Go to: https://sdg-ethiopia-chatbot-bknmwudn4vic6svzugeebe.streamlit.app/
    echo 2. Click "Manage app" button ^(bottom right^)
    echo 3. Click on "Settings" then "Secrets" in the left menu
    echo 4. Add your GOOGLE_API_KEY in the secrets text box
    echo 5. Click "Save"
    echo 6. Wait for app to redeploy automatically
    echo ========================================
) else (
    echo ========================================
    echo  ERROR: Push failed
    echo ========================================
    echo Please check your internet connection
    echo and GitHub authentication.
)
echo.
pause
