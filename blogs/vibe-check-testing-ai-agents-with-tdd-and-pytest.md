# Vibe Check: Testing AI Agents with TDD and Pytest

> Master the art of deterministic orchestration in a non-deterministic world with TDD, Pydantic AI, and LangGraph.

In the landscape of 2026, the role of the developer has undergone a seismic shift. We are no longer just "writers of syntax"; we are **Vibe Coders**. We orchestrate high-level intent, directing swarms of AI agents to manifest complex systems through rapid iteration. But as we move faster, the risk of "vibe drift"—where an agent’s reasoning becomes untethered from the business logic—increases exponentially.

To thrive in this era, the modern architect doesn't abandon rigor; they evolve it. **Test-Driven Development (TDD)** is no longer a chore—it is the literal "vibe check" that ensures our agentic workflows remain grounded. By using **Pytest**, **Pydantic AI**, and **LangGraph**, we can create a deterministic safety net around non-deterministic intelligence.

---

## 1. The Red-Green-Vibe Loop: Redefining TDD for Agents

Traditional TDD follows a simple cadence: Write a failing test, write the code to pass, and refactor. In the world of Vibe Coding, we introduce the **Red-Green-Vibe** loop. 

Because LLMs like **Gemini 1.5 Pro** are probabilistic, your tests must do more than check for string equality. They must validate the *intent* and the *structure* of the agentic response.

### The Setup: Defining the Expectation
Before writing a single line of agent logic, we define the "Vibe" in a Pytest file. We use Pydantic to enforce a strict schema, ensuring the agent can't hallucinate outside its boundaries.

```python
import pytest
from pydantic import BaseModel
from my_agent_app.agents import SupportAgent

class SupportResponse(BaseModel):
    resolution_status: bool
    confidence_score: float
    summary: str

@pytest.mark.asyncio
async def test_agent_resolves_simple_query():
    # 1. Arrange: Define the vibe and the input
    agent = SupportAgent()
    user_input = "I can't access my dashboard, I forgot my password."
    
    # 2. Act: Run the agent
    result = await agent.run(user_input)
    
    # 3. Assert: The "Vibe Check"
    assert isinstance(result.data, SupportResponse)
    assert result.data.resolution_status is True
    assert "password" in result.data.summary.lower()
    assert result.data.confidence_score > 0.8
```

By starting here, you define the "shape" of the success before the AI ever attempts to solve the problem.

---

## 2. Structured Reasoning with Pydantic AI

The biggest friction point in Vibe Coding is the "Wall of Text" problem—where an agent returns a beautiful but un-parsable paragraph. **Pydantic AI** solves this by treating the LLM as a typed function.

When we write tests for these agents, we aren't just testing the output; we are testing the **Tool Call Logic**. If the agent needs to fetch data from a FastAPI backend, we test if the agent *correctly identifies* which tool to use.

### Code Snippet: Testing Tool Orchestration
```python
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.test import TestModel

def test_agent_calls_correct_tool():
    # Using TestModel to mock the Gemini API response
    model = TestModel()
    agent = Agent(model, result_type=SupportResponse)

    @agent.tool
    async def get_user_data(ctx: RunContext[None], user_id: str):
        return {"status": "active", "plan": "pro"}

    # We mock the LLM to trigger the tool call
    model.push_responses([
        "I'll check your account status first.",
        # The mock response that triggers a tool call
        {"tool_calls": [{"name": "get_user_data", "args": {"user_id": "123"}}]}
    ])
    
    # Verify the logic flow
    # ... test assertions here ...
```

This approach allows Vibe Coders to swap models (e.g., from Gemini Flash to Ultra) while ensuring the internal logic—the "vibe"—remains consistent.

---

## 3. LangGraph: Testing the State Machine

AI agents rarely act in isolation. They operate within graphs. **LangGraph** allows us to build stateful, multi-actor applications. Testing a graph requires a shift from testing functions to testing **State Transitions**.

In a Vibe Coding workflow, we use Pytest to ensure that our graph doesn't enter an infinite loop or "hallucination spiral."

### The State Consistency Check
| Feature | Traditional TDD | Vibe Coding TDD |
| :--- | :--- | :--- |
| **Input** | Static Data | Dynamic Context / State |
| **Output** | Exact Match | Semantic / Schema Match |
| **Logic** | Boolean Flow | State Machine Transitions |
| **Failure Mode** | Logic Error | Hallucination / Drift |

```python
from langgraph.graph import StateGraph

def test_graph_navigation():
    builder = StateGraph(MyStateSchema)
    # ... nodes definition ...
    graph = builder.compile()
    
    initial_state = {"messages": ["Help me buy a laptop"], "current_node": "start"}
    output = graph.invoke(initial_state)
    
    # Vibe Check: Did the graph move from 'start' to 'search_inventory'?
    assert output["current_node"] == "search_inventory"
    assert len(output["messages"]) > 1
```

---

## 4. Integration with FastAPI: The Last Mile

Once the agent's internal vibes are checked, we expose it via **FastAPI**. In this layer, the TDD focus shifts to performance and error handling. What happens if the Gemini API throttles? What if the Pydantic validation fails?

We use the `TestClient` in FastAPI to simulate these scenarios.

```python
from fastapi.testclient import TestClient
from my_api import app

client = TestClient(app)

def test_api_vibe_endpoint():
    response = client.post("/v1/agent/chat", json={"message": "Reset my key"})
    assert response.status_code == 200
    json_data = response.json()
    assert "resolution_status" in json_data
```

---

## The Practical "Vibe Check" Implementation Guide

To implement this workflow today, follow these four pillars of Agentic Quality Assurance:

1.  **Schema First:** Always define your agent's input and output using Pydantic classes. If you can't define it in a schema, the vibe is too vague.
2.  **Mock Early, Test Often:** Use `pydantic-ai`'s `TestModel` or `pytest-mock` to simulate LLM responses. This saves tokens and speeds up the "Red" phase of your TDD.
3.  **Semantic Assertions:** Use libraries like `instructor` or custom LLM-based evaluators to test the *quality* of the text, not just the presence of keywords.
4.  **Traceability:** Integrate **LangSmith** or similar tracing tools. While not a direct part of Pytest, these provide the "logs" for when a vibe check fails in production.

---

## Why This Fits the Broader Ecosystem

The industry is moving away from "Black Box" AI. We are entering the era of **Compound AI Systems**. In this world, the LLM is just a component—a "reasoning kernel"—inside a larger software machine. 

Vibe Coding without TDD is just gambling. By wrapping your LangGraph nodes and Pydantic AI agents in Pytest suites, you transform from a prompt-engineer into a **Systems Architect**. You gain the ability to deploy complex, self-correcting workflows with the confidence that the "vibe" is not just good—it's verified.

---

## Conclusion: Orchestrate with Confidence

Testing AI agents doesn't have to be a bottleneck for rapid orchestration. By applying TDD principles, you create a feedback loop that actually *accelerates* development, allowing you to iterate on prompts and logic without fear of breaking the system.

**Is your organization ready to transition from manual AI experimentation to automated, production-grade agentic workflows?**

At **Nexus Intelligence**, we specialize in **Document Workflow Automation** and high-orchestration AI systems. We help elite teams build the "vibe" and the guardrails to scale it.

[**Contact Nexus Intelligence Today**](https://example.com) to automate your most complex document-heavy workflows with the power of Pydantic AI and Gemini. Let’s build the future of agentic intelligence, one test at a time.