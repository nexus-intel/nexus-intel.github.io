import os
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

# Define the dependencies the agent needs access to
@dataclass
class PatientDeps:
    patient_id: str
    patient_name: str

# Define models for structured responses if needed
class AppointmentResult(BaseModel):
    success: bool
    appointment_id: str | None = None
    message: str

class LabResult(BaseModel):
    test_name: str
    status: str
    result_value: str | None = None
    reference_range: str | None = None
    doctor_notes: str | None = None

# Initialize the agent
agent = Agent(
    'gemini-flash-latest',
    deps_type=PatientDeps,
    system_prompt=(
        "You are a helpful, empathetic, and professional virtual assistant for Nexus Health Network. "
        "You assist patients with checking their lab results, booking appointments, and answering general hospital FAQs. "
        "IMPORTANT: You are an AI, not a doctor. If the user asks for a medical diagnosis, treatment advice, or interpretation of symptoms, "
        "you MUST politely refuse and advise them to consult a qualified healthcare professional. "
        "Always be HIPAA-compliant in your tone—respect the user's privacy and maintain confidentiality."
    )
)

# Mock databases
MOCK_LAB_RESULTS = {
    "P12345": [
        LabResult(
            test_name="Complete Blood Count (CBC)",
            status="Completed",
            result_value="Normal",
            reference_range="Standard",
            doctor_notes="All values within normal range."
        ),
        LabResult(
            test_name="Lipid Panel",
            status="Pending",
        )
    ]
}

MOCK_APPOINTMENTS = {}

@agent.tool
def get_lab_results(ctx: RunContext[PatientDeps]) -> str:
    """Retrieve the latest lab results for the authenticated patient."""
    results = MOCK_LAB_RESULTS.get(ctx.deps.patient_id)
    if not results:
        return "No lab results found for your account."
    
    formatted_results = []
    for r in results:
        if r.status == "Pending":
            formatted_results.append(f"- {r.test_name}: Pending")
        else:
            formatted_results.append(
                f"- {r.test_name}: {r.result_value} (Notes: {r.doctor_notes})"
            )
    return "\n".join(formatted_results)

@agent.tool
def book_appointment(ctx: RunContext[PatientDeps], department: str, preferred_date: str) -> AppointmentResult:
    """Book a new medical appointment for the patient.
    
    Args:
        department: The hospital department (e.g., 'Cardiology', 'General Practice').
        preferred_date: The requested date and time (e.g., 'Tomorrow at 10 AM').
    """
    # Mock booking logic
    appointment_id = f"APT-{hash(ctx.deps.patient_id + department + preferred_date) % 10000}"
    MOCK_APPOINTMENTS[appointment_id] = {
        "patient_id": ctx.deps.patient_id,
        "department": department,
        "date": preferred_date
    }
    
    return AppointmentResult(
        success=True,
        appointment_id=appointment_id,
        message=f"Successfully booked an appointment with {department} for {preferred_date}."
    )

@agent.tool
def get_hospital_info(ctx: RunContext[PatientDeps], query_topic: str) -> str:
    """Retrieve general hospital information (hours, location, contact).
    
    Args:
        query_topic: The topic of inquiry, e.g., 'visiting hours', 'location', 'phone number'.
    """
    topic = query_topic.lower()
    if 'hour' in topic:
        return "Visiting hours are from 8:00 AM to 8:00 PM daily."
    elif 'location' in topic or 'address' in topic:
        return "We are located at 123 Healthway Blvd, Metropolis."
    elif 'phone' in topic or 'contact' in topic:
        return "Our main contact number is 555-0198."
    else:
        return "I don't have that specific information. Please call our main desk at 555-0198."
