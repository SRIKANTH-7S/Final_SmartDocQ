# SmartDocumentationAI

A smart documentation system that allows users to upload documents and ask questions about them using AI. The system stores chat history in MongoDB Atlas and provides persistent chat sessions.

## Features

- **Document Upload**: Support for PDF, DOCX, and TXT files
- **AI-Powered Q&A**: Ask questions about uploaded documents using Google Gemini AI
- **Chat History**: Persistent chat sessions stored in MongoDB Atlas
- **Interview Copilot**: Generate and evaluate interview questions based on documents
- **User Authentication**: JWT-based authentication system

## Setup Instructions

### 1. Environment Variables

Create a `.env` file in the `server/` directory with the following variables:

```env
# MongoDB Configuration
MONGO_URI=mongodb+srv://your-username:your-password@your-cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=smartdocq

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_EXPIRY_MINUTES=60

# Google Gemini API
GOOGLE_API_KEY=your-google-gemini-api-key
```

### 2. MongoDB Atlas Setup

1. Create a MongoDB Atlas account
2. Create a new cluster
3. Get your connection string and update `MONGO_URI` in `.env`
4. The system will automatically create the following collections:
   - `users` - User accounts
   - `chats` - Chat sessions and messages
   - `interviews` - Interview sessions and results

### 3. Google Gemini API Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Add it to your `.env` file as `GOOGLE_API_KEY`

### 4. Installation

```bash
# Install dependencies
npm install

# Start the development server
npm run dev
```

### 5. Backend Setup

```bash
# Navigate to server directory
cd server

# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
python main.py
```

## API Endpoints

### Chat Management
- `POST /api/chat` - Send a message and get AI response
- `POST /api/chat/sessions` - Create a new chat session
- `GET /api/chat/sessions` - Get all chat sessions
- `GET /api/chat/sessions/{session_id}` - Get specific chat session
- `DELETE /api/chat/sessions/{session_id}` - Delete a chat session

### Document Management
- `POST /api/upload` - Upload and process a document
- `POST /api/logout` - Clear document cache

### User Authentication
- `POST /api/signup` - Register a new user
- `POST /api/login` - Login user

### Interview System
- `POST /api/interview/start` - Start a new interview session
- `POST /api/interview/{session_id}/submit` - Submit interview answers
- `GET /api/interview/{session_id}/review` - Get interview results

## Chat Storage Implementation

The system now includes complete chat storage functionality:

1. **Chat Sessions**: Each conversation is stored as a session with metadata
2. **Message History**: All user questions and AI responses are persisted
3. **User Association**: Chat sessions can be associated with authenticated users
4. **Retrieval**: Users can view and continue previous conversations
5. **Persistence**: Chat history survives server restarts

## Technology Stack

- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: FastAPI + Python
- **Database**: MongoDB Atlas
- **AI**: Google Gemini API
- **Authentication**: JWT tokens
- **File Processing**: PyMuPDF, python-docx
- **Vector Search**: FAISS + Sentence Transformers