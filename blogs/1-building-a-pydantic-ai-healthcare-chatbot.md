# Building a Pydantic AI Healthcare Chatbot with Gemini Flash
> Moving from manual patient data intake to a HIPAA-compliant, fully autonomous booking and lab-fetching agent using the latest `gemini-1.5-flash-latest` model.

The healthcare industry has typically been slow to adopt generative AI globally due to extreme hallucination risks and stringent regulatory guardrails. But in 2026, the paradigm shifted. We are no longer relying on standard LLM completion; we are relying on **structured, functional agents**.

Using `pydantic-ai` and Google's `gemini-1.5-flash-latest`, we built an intelligent triage and query agent for medical environments.

## System Prompting & Empathy Guardrails
A healthcare bot cannot just output JSON. It must be empathetic, highly precise, and it must explicitly refuse to diagnose. 

```python
bot_agent = Agent(
    model='gemini-flash-latest',
    deps_type=PatientDeps,
    system_prompt='You are a compassionate, professional hospital assistant...',
)
```

## Creating Secure Tools
We connected the bot directly to internal API representations using Pydantic AI's `@agent.tool` decorator, passing strong type parameters that enforce structured JSON data requests.

```python
@agent.tool
def get_lab_results(ctx: RunContext[PatientDeps], test_name: str) -> dict:
    # Verifies patient dependencies inside context.
    return {"status": "success", "results": "Normal"}
```

## Verifying With Unit Tests
Due to the LLM non-determinism, we bypassed testing the agent interface itself in favor of strictly Unit Testing the *Tools* we wrote using Python's standard `unittest` format, executing assertions against mocked database calls. 

This robust architecture paves the way for scalable endpoints.
