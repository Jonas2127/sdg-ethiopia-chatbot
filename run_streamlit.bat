@echo off
echo Starting SDG Ethiopia Chatbot...
echo.
echo The app will open automatically in your browser.
echo If it doesn't open, manually visit: http://localhost:8502
echo.
python -m streamlit run app.py --server.port=8502 --server.headless=false
