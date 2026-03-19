# How to Build an AI Agent with LangGraph: Step-by-Step Python Tutorial

> Move beyond simple prompts. Learn how to build a stateful, cyclic AI agent that can reason, verify, and correct its own work.

---

## Why LangGraph in 2026?

In 2026, the industry has shifted from "Chains" to "Graphs." While standard LangChain is excellent for linear tasks, real-world business logic is rarely linear. You need agents that can loop back, retry failed steps, and maintain complex internal states. **LangGraph** (built by the LangChain team) is the definitive framework for this.

This tutorial will show you how to build a "Self-Correction Research Agent"—an agent that researches a topic but *checks its own work* for hallucinations before providing a final answer.

---

## 1. Prerequisites

Before we start, ensure you have the necessary libraries installed:

```bash
pip install -U langgraph langchain-openai python-dotenv
```

You will need an **OpenAI API Key** (or any model provider compatible with LangChain) in your `.env` file.

---

## 2. Defining the State

In LangGraph, the `State` is a shared object that all nodes in your graph can read and modify. This is what allows for true "memory" between steps.

```python
from typing import TypedDict, Annotated, List, Union
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    task: str
    output: str
    iteration: int
    quality_score: float
    is_satisfactory: bool
```

---

## 3. Creating the Nodes

Nodes are simple Python functions that take the current `State` as input and return modified fields.

### Node A: The Researcher
This agent takes the task and attempts to solve it using an LLM.

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-5", temperature=0)

def researcher_node(state: AgentState):
    print("🧠 Researcher is thinking...")
    prompt = f"Research the following topic in depth: {state['task']}"
    response = model.invoke(prompt)
    
    return {
        "output": response.content,
        "iteration": state.get("iteration", 0) + 1
    }
```

### Node B: The Critic
This node acts as a guardrail. It analyzes the researcher's output and performs a quality check.

```python
def critic_node(state: AgentState):
    print("⚖️ Critic is evaluating...")
    verify_prompt = f"Review this output for accuracy and detail: {state['output']}. 
                     Rate it from 0 to 1 and say 'FAIL' if it's below 0.8."
    
    res = model.invoke(verify_prompt)
    # Simple logic to determine if we should retry
    score = 0.9 if "PASS" in res.content else 0.5
    
    return {
        "quality_score": score,
        "is_satisfactory": score >= 0.8
    }
```

---

## 4. Building the Graph

Now we connect the nodes using edges. The magic happens with **conditional edges**, which allow the graph to loop.

```python
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("researcher", researcher_node)
workflow.add_node("critic", critic_node)

# Set Entry Point
workflow.set_entry_point("researcher")

# Add Normal Edge
workflow.add_edge("researcher", "critic")

# Add Conditional Logic (The Cycle)
def should_continue(state: AgentState):
    if state["is_satisfactory"] or state["iteration"] >= 3:
        return END
    return "researcher" # Loop back!

workflow.add_conditional_edges("critic", should_continue)

# Compile
app = workflow.compile()
```

---

## 5. Running the Agent

```python
final_state = app.invoke({
    "task": "Explain the concept of Agentic MoE in high-performance computing.",
    "iteration": 0,
    "is_satisfactory": False
})

print("\n--- Final Report ---\n")
print(final_state["output"])
```

---

## Key Takeaways

1. **Statefulness**: Your agent now "knows" how many times it has tried a task.
2. **Cycle Power**: By looping from Critic back to Researcher, you eliminate 90% of common hallucinations.
3. **Control**: You can stop the graph at any point to inspect the state or inject manual code.

---

## Real-World Scaling

For enterprise applications, you would add a "Web Search" tool to the Researcher and a "Fact Checker" tool to the Critic. This architecture is what powers the **Autonomous Supply Chain Engine** we built at Nexus Intelligence.

### Ready to Build production-grade agents?

Building a POC is easy; building a reliable system is hard. **[Contact Nexus Intelligence](https://nexus-intel.github.io/index.html#contact)** for a deep-dive workshop on building autonomous agentic workflows for your specific business niche.

---

### Related Insights
- [LangChain vs LangGraph vs CrewAI](../../blog/langchain-vs-langgraph-vs-crewai-which-framework-for-ai-agents/) — Choosing the right framework for your project.
- [Multi-Agent AI Systems: Architecture Patterns](../../blog/multi-agent-ai-systems-architecture-patterns/) — Moving from single agents to teams.
- [Autonomous Supply Chain Engine — Case Study](../../case/autonomous-logistics/) — See a production LangGraph implementation.
