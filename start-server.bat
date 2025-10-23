@echo off
echo Starting SmartDocQ Server...
echo.
echo IMPORTANT: Make sure you have set up your Google API key!
echo 1. Get your API key from: https://makersuite.google.com/app/apikey
echo 2. Create a .env file in the server folder with:
echo    GOOGLE_API_KEY=your_actual_api_key_here
echo.
echo Starting server on http://localhost:10000
echo.

cd server
python -m uvicorn clean_main:app --host 0.0.0.0 --port 10000 --reload

pause
