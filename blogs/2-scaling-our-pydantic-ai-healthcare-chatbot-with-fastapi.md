# Scaling our Pydantic AI Healthcare Chatbot with FastAPI
> Moving from local testing to a production-ready REST API for enterprise medical workflows seamlessly with FastAPI and Uvicorn.

Welcome back! In our previous tutorial, we walked through building our core agent logic using Pydantic AI and Gemini Flash. But local scripts only take you so far.

## Bridging the Gap: Why FastAPI?
To enable real-world deployments—whether integrating into a hospital's React frontend, a mobile app, or a secure internal networking dashboard—we need an API layer. **FastAPI** is the ideal choice for AI orchestration due to its native asynchronous support, auto-generated OpenAPI documentation, and strict Pydantic parsing.

## The Integration Architecture
Because `pydantic-ai` relies heavily on standard Python async paradigms, integrating our `agent` instance is exceptionally clean. We set up a single `POST /api/chat` route that accepts standard `ChatRequest` payloads (including our `patient_id` and `message`).

```python
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    deps = PatientDeps(patient_id=request.patient_id, patient_name=request.patient_name)
    result = await agent.run(request.message, deps=deps)
    return ChatResponse(response=result.data)
```

## Native Tooling with uv
To manage dependencies, we shifted to the industry standard `uv`. By moving away from `pip install`, we accelerated our Docker build times dramatically.

We updated our deployments to natively leverage:

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
```

By placing the FastAPI application server within this robust, dependency-locked environment, we achieve high throughput concurrency against the Gemini API simultaneously.
