# Structured Agency: Building Document Intelligence with Pydantic AI

> Revolutionizing OCR through schema-first orchestration, multimodal Gemini integration, and agentic state management.

The year is 2026, and the "Vibe Coding" movement has reached its zenith. We no longer write brittle Regex patterns or battle Tesseract configurations. Instead, we manifest systems through high-level intent, leveraging the latent space of Large Language Models (LLMs) to handle the "messy" reality of unstructured data. 

But "Vibe Coding" isn't about being imprecise; it’s about shifting the precision from the **low-level syntax** to the **high-level schema**. In the realm of Document Intelligence, this means moving beyond simple Optical Character Recognition (OCR) and into the territory of **Structured Agency**. We are building agents that don't just "read" text—they interpret, validate, and integrate document data into business logic with 100% type safety.

## The Vibe of 2026: From Parsing to Intelligence

Traditional OCR was a linear pipeline: Scan -> Binarize -> Segment -> Recognize -> Post-process. It was fragile, high-maintenance, and prone to "hallucinating" characters in noisy environments.

In the modern stack, we treat documents as **multimodal inputs**. Using **Pydantic AI** and the **Gemini 1.5 Pro** API (with its massive context window and native vision capabilities), we bypass the extraction nightmare. We define the *shape* of the data we want, and the agentic layer ensures the reality matches the expectation. This is "Structured Agency"—where the agent is constrained by a Pydantic schema but empowered by agentic reasoning to resolve ambiguities.

---

## Technical Deep Dive: The Structured OCR Stack

To build a production-grade Document Intelligence system, we utilize a stack that prioritizes speed, type safety, and orchestration.

### 1. Defining the Intent: Schema-First extraction with Pydantic AI

Pydantic AI allows us to define the "Vibe" of our data in pure Python. Before the agent even looks at a PDF, we define what success looks like.

```python
from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional

class InvoiceItem(BaseModel):
    description: str = Field(description="Description of the service or product")
    quantity: int
    unit_price: float
    total: float

class StructuredInvoice(BaseModel):
    invoice_number: str
    vendor_name: str
    tax_id: Optional[str]
    billing_date: date
    line_items: List[InvoiceItem]
    grand_total: float
    currency: str = Field(default="USD")
```

### 2. The Orchestrator: Pydantic AI + Gemini API

We use **Pydantic AI** to wrap the Gemini API. Gemini’s native ability to handle images and PDFs directly is a game-changer for Vibe Coders. We don't need to convert pages to images; we just stream the bytes.

```python
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel

# Initialize the Vibe: Gemini 1.5 Pro for complex reasoning
model = GeminiModel('gemini-1.5-pro')

# Define the Agency: The agent is bound to our StructuredInvoice model
document_agent = Agent(
    model=model,
    result_type=StructuredInvoice,
    system_prompt=(
        "You are a specialized Document Intelligence Agent. "
        "Extract data with surgical precision. If a field is missing, "
        "do not hallucinate—leave it null or use context to infer it."
    ),
)

async def extract_document(file_path: str):
    # Gemini handles the multimodal 'vibe' natively
    result = await document_agent.run(
        f"Extract the details from this document: {file_path}",
        deps=[], # Dependency injection for external lookups
    )
    return result.data
```

### 3. State Management with LangGraph

One-shot extraction is great, but "Structured Agency" requires a feedback loop. If the agent extracts a `grand_total` that doesn't match the sum of `line_items`, the vibe is off. We use **LangGraph** to manage the state and create a correction loop.

| Node | Responsibility | Failure Logic |
| :--- | :--- | :--- |
| **Extraction** | Raw data pull via Gemini | If schema fails, retry with prompt adjustment |
| **Validation** | Pydantic validation + Business Logic | If math fails, route back to Extraction |
| **Enrichment** | Querying internal CRM for Vendor IDs | If vendor unknown, flag for human-in-the-loop |

```python
from langgraph.graph import StateGraph, END

def validate_math(state: dict):
    invoice = state['invoice']
    calculated_total = sum(item.total for item in invoice.line_items)
    if abs(calculated_total - invoice.grand_total) > 0.01:
        return "re_extract"
    return "finalize"

# The Graph defines the flow of the Agency
workflow = StateGraph(DocumentState)
workflow.add_node("extract", call_pydantic_agent)
workflow.add_node("validate", validate_math)
workflow.set_entry_point("extract")
workflow.add_conditional_edges("validate", {"re_extract": "extract", "finalize": END})
```

### 4. Serving the Agency: FastAPI Integration

Finally, we wrap this in a **FastAPI** endpoint. This is where the Vibe meets the consumer. We use asynchronous streaming to keep the connection alive while the agent "thinks."

```python
from fastapi import FastAPI, UploadFile
from my_agency import workflow_app

app = FastAPI(title="Nexus OCR Agency")

@app.post("/v1/extract")
async def process_document(file: UploadFile):
    content = await file.read()
    # The Vibe Coder's dream: Intent in, Structured JSON out.
    structured_data = await workflow_app.ainvoke({"doc_bytes": content})
    return structured_data
```

---

## The Landscape: Why Pydantic AI Wins

In the evolving ecosystem of AI development, we are seeing a split between "Legacy Rag-tag" solutions and "Structured Agency."

| Feature | Legacy OCR (Tesseract/AWS) | LLM-Native (OpenAI/Claude) | Structured Agency (Pydantic AI + LangGraph) |
| :--- | :--- | :--- | :--- |
| **Parsing** | Regex/Positional | Natural Language | **Schema-Driven** |
| **Validation** | Manual Post-processing | None (Hallucination risk) | **Type-Safe / Auto-Correcting** |
| **Flexibility** | Extremely Low | High | **Infinite (Agentic Reasoning)** |
| **Development Speed** | Slow (Manual Rules) | Fast (Vibe only) | **Optimal (Intent + Structure)** |

Pydantic AI provides the necessary guardrails. It ensures that your "Vibe" doesn't drift into hallucination. By using Pydantic's internal validation, the agent knows *exactly* when it has failed, allowing it to self-correct before the data ever reaches your database.

---

## Practical Vibe Check: Implementing Today

If you are a Vibe Coder looking to deploy this today, follow these three rules:

1.  **Stop Pre-processing:** Don't waste time with image deskewing or grayscale conversions. Gemini and GPT-4o prefer the raw, high-resolution "vibe" of the original document.
2.  **Schema is Source of Truth:** Your Pydantic model is more important than your prompt. A well-defined model with `Field(description=...)` acts as the primary instruction set for the agent.
3.  **Embrace the Loop:** Never trust a single pass. Build a graph that checks for logical consistency (e.g., Subtotal + Tax == Total).

---

## Conclusion: Orchestrating the Future

The shift from "Coding Parsers" to "Orchestrating Agency" is the most significant leap in software engineering since the move to the cloud. By leveraging **Pydantic AI**, **Gemini**, and **LangGraph**, we are no longer just processing documents; we are building intelligent systems that understand the context and the consequences of the data they extract.

The complexity of modern business documents requires more than just a model; it requires a **Structured Agency**. 

### Ready to elevate your document workflows?
If your organization is drowning in unstructured data, it’s time for a Vibe Shift. **Nexus Intelligence** specializes in building bespoke Document Workflow Automation using this exact stack. We don't just build scripts; we build agents that think.

**[Contact Nexus Intelligence Today for a Custom Implementation Architecture]**