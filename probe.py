import urllib.request
import json

def probe(url, payload):
    req = urllib.request.Request(url, method="POST", headers={"Content-Type": "application/json"})
    try:
        response = urllib.request.urlopen(req, data=json.dumps(payload).encode('utf-8'))
        print(f"{url} -> {response.status}")
    except urllib.error.HTTPError as e:
        print(f"{url} -> HTTP Error {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"{url} -> Error: {e}")

payload_chat = {"message": "hello"}
payload_chatbot_api = {"patient_id": "test", "patient_name": "test", "message": "hello"}
payload_contact = {"name": "test", "email": "test@example.com", "message": "hello"}

probe("https://nexus-intelgithubio-production.up.railway.app/chat", payload_chat)
probe("https://nexus-intelgithubio-production.up.railway.app/api/chat", payload_chatbot_api)
probe("https://nexus-intelgithubio-production.up.railway.app/contact", payload_contact)
probe("https://nexus-intelgithubio-production.up.railway.app/api/contact", payload_contact)
probe("https://nexus-intelgithubio-production.up.railway.app/docs", {})
