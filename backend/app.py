from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic_ai import Agent
from fastapi.middleware.cors import CORSMiddleware
import os
import sqlite3
from loguru import logger

# Initialize Database
def init_db():
    conn = sqlite3.connect('nexus.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS submissions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, name TEXT, email TEXT, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

app = FastAPI()

# Configure CORS for GitHub Pages and Local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your GitHub Pages domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Pydantic AI Agent
agent = Agent(
    'google-gla:gemini-1.5-flash',
    system_prompt=(
        "You are Nexus AI, the intelligent assistant for Nexus Intelligence. "
        "Provide professional, ROI-focused advice on AI/ML/OCR services."
    ),
)

class ChatRequest(BaseModel):
    message: str

class ContactRequest(BaseModel):
    name: str
    email: str
    message: str

class NewsletterRequest(BaseModel):
    email: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Run the agent (simulated if no API key is provided for now)
        # result = await agent.run(request.message)
        # return ChatResponse(response=result.data)
        
        # Fallback simulation if no API key is set
        if not os.getenv("GEMINI_API_KEY"):
            return ChatResponse(response=f"I'm currently in demo mode. You asked: '{request.message}'. Once the API key is set, I'll provide full intelligent insights!")
            
        result = await agent.run(request.message)
        return ChatResponse(response=str(result.data))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/newsletter")
async def subscribe_newsletter(request: NewsletterRequest):
    logger.info(f"New newsletter subscription: {request.email}")
    try:
        conn = sqlite3.connect('nexus.db')
        c = conn.cursor()
        c.execute("INSERT INTO submissions (type, email) VALUES (?, ?)", ('newsletter', request.email))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"DB Error: {e}")
    return {"status": "success", "message": "Subscribed successfully"}

@app.post("/contact")
async def contact_form(request: ContactRequest):
    logger.info(f"New contact form submission from {request.name} ({request.email}): {request.message}")
    try:
        conn = sqlite3.connect('nexus.db')
        c = conn.cursor()
        c.execute("INSERT INTO submissions (type, name, email, message) VALUES (?, ?, ?, ?)", 
                  ('contact', request.name, request.email, request.message))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"DB Error: {e}")
    return {"status": "success", "message": "Message received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
