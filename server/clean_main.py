from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uuid
import tempfile
from datetime import datetime
from typing import List, Optional, Dict, Any
from final_smartmodel import DocumentQA, InterviewCopilot

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
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # Process document
        result = qa_system.load_document(tmp_file_path)
        
        # Clean up temp file
        os.unlink(tmp_file_path)
        
        return {"message": "Document processed successfully", "status": result}
    except Exception as e:
        return {"message": f"Error processing document: {str(e)}", "status": "error"}

@app.post("/api/chat")
async def chat(data: ChatRequest):
    try:
        answer = qa_system.ask_question(data.question)
        return {"answer": answer, "chat_session_id": str(uuid.uuid4())}
    except Exception as e:
        return {"answer": f"Error: {str(e)}", "chat_session_id": str(uuid.uuid4())}

@app.post("/api/interview/start")
async def start_interview(
    file: UploadFile = File(...),
    num_questions: int = Form(5),
    level: Optional[str] = Form("medium"),
    question_type: Optional[str] = Form(None)
):
    try:
        # Create interview copilot instance
        interview_copilot = InterviewCopilot()
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # Load document
        load_result = interview_copilot.load_document(tmp_file_path)
        
        # Clean up temp file
        os.unlink(tmp_file_path)
        
        if load_result.get("status") != "Document loaded successfully":
            raise Exception(f"Failed to load document: {load_result}")
        
        # Generate questions
        questions = interview_copilot.generate_questions(
            num_questions=num_questions,
            level=level,
            qtype=question_type
        )
        
        session_id = str(uuid.uuid4())
        
        INTERVIEW_SESSIONS[session_id] = {
            "session_id": session_id,
            "created_at": datetime.utcnow(),
            "num_questions": num_questions,
            "level": level,
            "questions": questions,
            "interview_copilot": interview_copilot,
            "completed": False
        }
        
        return {"session_id": session_id, "questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting interview: {str(e)}")

@app.post("/api/interview/{session_id}/submit")
def submit_answers(session_id: str, answers: List[str]):
    if session_id not in INTERVIEW_SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = INTERVIEW_SESSIONS[session_id]
    
    try:
        # Get interview copilot instance
        interview_copilot = session.get("interview_copilot")
        if not interview_copilot:
            raise Exception("Interview copilot not found in session")
        
        # Evaluate answers
        avg_score, feedback = interview_copilot.evaluate_answers(answers)
        
        # Update session
        session["completed"] = True
        session["answers"] = answers
        session["avg_score"] = avg_score
        session["feedback"] = feedback
        
        return {"session_id": session_id, "avg_score": avg_score, "feedback": feedback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating answers: {str(e)}")

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
