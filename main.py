from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.hospital_bot import agent, PatientDeps
import uvicorn
import os
import resend

app = FastAPI(title="Nexus Healthcare Chatbot API", description="Production API serving the Pydantic AI hospital assistant.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    patient_id: str
    patient_name: str
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        deps = PatientDeps(patient_id=request.patient_id, patient_name=request.patient_name)
        result = await agent.run(request.message, deps=deps)
        return ChatResponse(response=result.data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ContactRequest(BaseModel):
    name: str
    email: str
    message: str

@app.post("/api/contact")
async def contact_endpoint(request: ContactRequest):
    resend.api_key = os.environ.get("RESEND_API_KEY", "re_123456789")
    try:
        email = resend.Emails.send({
            "from": "Acme <onboarding@resend.dev>",
            "to": [os.environ.get("CONTACT_EMAIL", "admin@yourdomain.com")],
            "subject": f"New Lead: {request.name}",
            "text": f"Name: {request.name}\nEmail: {request.email}\n\nMessage:\n{request.message}"
        })
        return {"status": "success", "id": email.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
