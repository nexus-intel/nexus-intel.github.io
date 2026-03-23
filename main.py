from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.hospital_bot import agent, PatientDeps
import uvicorn
import os

app = FastAPI(title="Nexus Healthcare Chatbot API", description="Production API serving the Pydantic AI hospital assistant.")

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
