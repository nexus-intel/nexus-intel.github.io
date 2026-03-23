import sys
from pydantic_ai.models.test import TestModel
from backend.hospital_bot import agent, PatientDeps
import asyncio

async def main():
    test_model = TestModel()
    deps = PatientDeps(patient_id="P12345", patient_name="John Doe")
    result = agent.run_sync("Hi", deps=deps, model=test_model)
    print("Result attributes:", dir(result))
    if hasattr(result, 'data'):
        print("Data:", type(result.data))
    
asyncio.run(main())
