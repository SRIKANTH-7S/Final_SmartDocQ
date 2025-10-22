from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any

app = FastAPI(title="SmartDocQ API", version="1.0")

# CORS configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")
origins = (
    [o.strip() for o in ALLOWED_ORIGINS.split(",") if o.strip()]
    if ALLOWED_ORIGINS != "*"
    else ["*"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock classes
class DocumentQA:
    def __init__(self):
        pass
    def load_document(self, file_path):
        return {"status": "Document loaded successfully"}
    def ask_question(self, question):
        return f"Mock answer for: {question}"
    def clear_cache(self):
        return "Cache cleared"

class InterviewCopilot:
    def __init__(self):
        pass
    def load_document(self, file_path):
        return {"status": "Document loaded successfully"}
    def generate_questions(self, num_questions=5, level="medium", qtype=None):
        return [f"Mock question {i+1}" for i in range(num_questions)]
    def evaluate_answers(self, answers):
        return 85.0, [{"question": f"Q{i+1}", "score": 8.5, "feedback": "Good answer"} for i in range(len(answers))]

# Global instances
qa_system = DocumentQA()
INTERVIEW_SESSIONS: Dict[str, Dict[str, Any]] = {}

# Pydantic models
class SignupModel(BaseModel):
    full_name: str
    email: str
    password: str
    confirm_password: str

class LoginModel(BaseModel):
    email: str
    password: str

class ChatRequest(BaseModel):
    question: str
    chat_session_id: Optional[str] = None

# Routes
@app.get("/")
def read_root():
    return {"message": "SmartDocQ API is running!"}

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "SmartDocQ API is healthy",
        "environment": os.getenv("NODE_ENV", "development")
    }

@app.get("/api/smart")
def smart_check():
    return {"status": "ok", "message": "Smart endpoint working"}

@app.post("/api/signup")
def signup(data: SignupModel):
    return {"message": "User created successfully", "user": {"id": str(uuid.uuid4()), "email": data.email}}

@app.post("/api/login")
def login(data: LoginModel):
    return {"message": "Login successful", "token": "mock_token", "user": {"email": data.email}}

@app.post("/api/logout")
def logout():
    return {"message": "Logged out successfully"}

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    return {"message": "Document processed successfully", "status": "uploaded"}

@app.post("/api/chat")
async def chat(data: ChatRequest):
    answer = qa_system.ask_question(data.question)
    return {"answer": answer, "chat_session_id": str(uuid.uuid4())}

@app.post("/api/interview/start")
async def start_interview(
    file: UploadFile = File(...),
    num_questions: int = Form(5),
    level: Optional[str] = Form("medium"),
    question_type: Optional[str] = Form(None)
):
    session_id = str(uuid.uuid4())
    questions = [f"Mock interview question {i+1}" for i in range(num_questions)]
    
    INTERVIEW_SESSIONS[session_id] = {
        "session_id": session_id,
        "created_at": datetime.utcnow(),
        "num_questions": num_questions,
        "level": level,
        "questions": questions,
        "completed": False
    }
    
    return {"session_id": session_id, "questions": questions}

@app.post("/api/interview/{session_id}/submit")
def submit_answers(session_id: str, answers: List[str]):
    if session_id not in INTERVIEW_SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = INTERVIEW_SESSIONS[session_id]
    session["completed"] = True
    session["answers"] = answers
    session["avg_score"] = 85.0
    session["feedback"] = [{"question": f"Q{i+1}", "score": 8.5, "feedback": "Good answer"} for i in range(len(answers))]
    
    return {"session_id": session_id, "avg_score": 85.0, "feedback": session["feedback"]}

@app.get("/api/interview/{session_id}/review")
def interview_review(session_id: str):
    if session_id not in INTERVIEW_SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = INTERVIEW_SESSIONS[session_id]
    return {
        "session_id": session_id,
        "questions": session["questions"],
        "answers": session.get("answers", []),
        "feedback": session.get("feedback", []),
        "avg_score": session.get("avg_score", 0)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
