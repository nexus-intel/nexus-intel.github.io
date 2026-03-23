from backend.hospital_bot import agent, PatientDeps
import sys

deps = PatientDeps(patient_id="P12345", patient_name="John Doe")
result = agent.run_sync("Hi", deps=deps)
print(dir(result))
