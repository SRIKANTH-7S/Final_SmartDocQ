from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

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

# Placeholder endpoints for frontend
@app.post("/api/login")
def login():
    return {"message": "Login endpoint - not implemented yet"}

@app.post("/api/signup")
def signup():
    return {"message": "Signup endpoint - not implemented yet"}

@app.post("/api/upload")
def upload():
    return {"message": "Upload endpoint - not implemented yet"}

@app.post("/api/chat")
def chat():
    return {"message": "Chat endpoint - not implemented yet"}

@app.post("/api/logout")
def logout():
    return {"message": "Logout endpoint - not implemented yet"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
