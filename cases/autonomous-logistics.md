# Autonomous Supply Chain Engine

> How we deployed a LangGraph-powered agentic system that reduced transportation costs by 28%.

---

## The Challenge

A global logistics firm with operations across 14 countries was struggling with a critical bottleneck: **manual dispatch decisions**. Their legacy system relied on spreadsheet-based routing where dispatchers would manually assess routes each morning. The process couldn't account for real-time traffic, fuel price fluctuations, driver fatigue regulations, and vehicle maintenance schedules simultaneously.

The result was predictable:
- **Overloaded routes** that burned excess fuel
- **Idle drivers** waiting for reassignment during peak hours
- **SLA breaches** from delayed deliveries, costing €200K+/month in penalties
- **Zero visibility** into why specific routes were chosen

The operations team was spending 6+ hours daily just re-optimizing routes that should have been automated.

---

## The Solution

Azura AI designed and deployed an **Autonomous Multi-Agent System (AMAS)** built on Python and LangGraph. Rather than replacing the dispatch team, the system acts as an intelligent co-pilot that pre-calculates optimal routes and flags anomalies before they become costly errors.

### System Architecture

The system leverages a **Supervisor-Worker** pattern with three specialized agents:

#### 1. The Router Agent
Calculates optimal multi-stop paths using real-time API data from Google Maps, HERE Technologies, and OpenStreetMap. Unlike static route planners, it factors in:
- Live traffic congestion data (updated every 60 seconds)
- Time-of-day delivery preferences from customers
- Vehicle load capacity and weight distribution
- Cross-border customs clearance windows

#### 2. The Market Agent
A continuously running monitor that tracks:
- **Fuel prices** across 2,400+ gas stations in the operating region
- **Toll rates** and dynamic pricing changes
- **Currency fluctuations** for cross-border operations
- **Weather alerts** that may affect road conditions or delivery SLAs

The Market Agent feeds pricing data to the Router Agent, allowing for cost-optimized routing that isn't just about distance — it's about total cost per delivery.

#### 3. The Coordinator Agent
Handles the human side of logistics:
- Assigns tasks based on driver work-logs and hours-of-service regulations
- Monitors vehicle health through OBD-II telemetry integration
- Manages break schedules and shift handoffs
- Escalates exceptions to human dispatchers with full context

### Technical Implementation

```python
from langgraph.graph import StateGraph, END

class DispatchState(TypedDict):
    pending_orders: List[Order]
    route_plan: Optional[RoutePlan]
    cost_analysis: Optional[CostBreakdown]
    driver_assignments: Optional[dict]

workflow = StateGraph(DispatchState)
workflow.add_node("router", router_agent)
workflow.add_node("market", market_agent)
workflow.add_node("coordinator", coordinator_agent)

workflow.set_entry_point("router")
workflow.add_edge("router", "market")
workflow.add_edge("market", "coordinator")
workflow.add_conditional_edges(
    "coordinator",
    lambda s: "router" if s.get("needs_reroute") else END
)
```

The cyclic graph architecture means the Coordinator can send routes **back** to the Router for re-optimization — for example, when a driver calls in sick or a vehicle breaks down mid-route.

---

## Impact Results

After 90 days of production deployment:

| Metric | Before | After | Change |
|:---|:---|:---|:---|
| Average transport cost per delivery | €47.20 | €33.98 | **-28%** |
| On-time delivery rate | 78% | 93% | **+15%** |
| Manual scheduling overhead | 6.2 hrs/day | 0.9 hrs/day | **-85%** |
| Fuel cost per km | €0.38 | €0.29 | **-24%** |
| SLA penalty costs | €200K/month | €28K/month | **-86%** |

> "The system paid for itself in 6 weeks. What used to take our dispatch team half a day now happens in under a minute." — VP of Operations, [Client]

---

## Key Takeaways

1. **Agentic > Monolithic**: Breaking the problem into specialized agents (routing, pricing, coordination) produced better results than a single "do everything" AI.
2. **Cyclic graphs are essential**: Real-world logistics require re-planning. Linear AI pipelines can't handle the constant flux.
3. **Human-in-the-loop matters**: The system doesn't replace dispatchers — it turns them from data-entry operators into exception-handling strategists.

---

### Related Insights
- [The Future of AI Agents: From Chatbots to Autonomous Coworkers](../post.html?blog=the-future-of-ai-agents) — The architectural patterns powering next-gen autonomous systems.
- [Real-Time Fraud Detection — Case Study](../study.html?id=fintech-fraud-detection) — Another production deployment of multi-agent ML systems.
