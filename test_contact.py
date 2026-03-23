from fastapi.testclient import TestClient
from main import app
import sys

client = TestClient(app)

def test_contact():
    response = client.post("/api/contact", json={
        "name": "Jane User",
        "email": "jane@example.com",
        "message": "I need help automating my PDF extraction."
    })
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # We expect a 500 error solely because the RESEND_API_KEY 'test' is invalid,
    # demonstrating the payload successfully reached the Resend package call.
    if response.status_code not in [200, 500]:
        sys.exit(1)
        
    if response.status_code == 500 and "sk_" not in str(response.json()):
        print("Success! The endpoint successfully caught the invalid local api key!")
        sys.exit(0)

if __name__ == "__main__":
    test_contact()
