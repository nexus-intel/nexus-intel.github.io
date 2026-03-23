from fastapi.testclient import TestClient
from main import app
import sys

client = TestClient(app)

def test_chat():
    response = client.post("/api/chat", json={
        "patient_id": "P12345",
        "patient_name": "John Doe",
        "message": "I need to book an appointment with Cardiology for next Monday."
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code != 200:
        sys.exit(1)

if __name__ == "__main__":
    test_chat()
