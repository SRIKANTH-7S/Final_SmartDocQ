# SmartDocQ Setup Guide

## Quick Fix for "Failed to Fetch" Error

The "failed to fetch" error occurs because the server isn't running. Follow these steps:

### 1. Set up Environment Variables

Create a `.env` file in the `server` folder with the following content:

```env
# Database Configuration
MONGO_URI=mongodb://localhost:27017
DB_NAME=smartdocq

# JWT Configuration
JWT_SECRET=your_super_secret_jwt_key_here_change_in_production
JWT_EXPIRY_MINUTES=60

# Server Configuration
PORT=10000
NODE_ENV=development
HOST=0.0.0.0

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:4173

# Google AI Configuration (REQUIRED)
GOOGLE_API_KEY=your_google_ai_api_key_here

# Optional: Database URL for production
DATABASE_URL=your_database_url_here
```

### 2. Get Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Replace `your_google_ai_api_key_here` in the `.env` file with your actual API key

### 3. Install Dependencies

```bash
cd server
pip install -r requirements.txt
```

### 4. Start the Server

**Option A: Use the batch file (Windows)**
```bash
start-server.bat
```

**Option B: Manual start**
```bash
cd server
python -m uvicorn clean_main:app --host 0.0.0.0 --port 10000 --reload
```

### 5. Start the Frontend

In a new terminal:
```bash
cd client
npm install
npm run dev
```

### 6. Test the Application

1. Open http://localhost:5173 in your browser
2. Go to Interview Copilot
3. Upload a document
4. Select MCQ as question type
5. Click "Start Interview"

## Troubleshooting

### Server won't start?
- Make sure you have Python 3.8+ installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify your Google API key is correct in the `.env` file

### Still getting "failed to fetch"?
- Make sure the server is running on port 10000
- Check that no firewall is blocking the connection
- Verify the frontend is trying to connect to `http://localhost:10000/api`

### MCQ questions not showing as radio buttons?
- The fixes have been applied to the code
- Make sure you're using the updated code
- Check browser console for any JavaScript errors

## API Endpoints

The server provides these endpoints:
- `POST /api/interview/start` - Start an interview
- `POST /api/interview/{session_id}/submit` - Submit answers
- `GET /api/interview/{session_id}/review` - Get review results

All endpoints are available at `http://localhost:10000/api/`
