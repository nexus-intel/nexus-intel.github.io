# Real-Time Fraud Detection Solution

> Reducing Authorised Push Payment (APP) fraud by 92% using high-performance predictive ML.

---

## The Challenge

A London-based fintech processing £500M+ in monthly transactions was facing a surge in **Authorised Push Payment (APP) fraud** — the fastest-growing type of financial crime in the UK. Unlike traditional card fraud, APP fraud relies on sophisticated social engineering: criminals impersonate banks, HMRC, or delivery services to trick customers into voluntarily authorizing payments to fraudulent accounts.

The existing rule-based fraud system was failing badly:
- **False positive rate of 12%** — legitimate customers were being blocked, creating support overhead
- **Detection rate of only 34%** — most APP fraud slipped through because transfers were "authorized" by the account holder
- **Average response time of 8 seconds** — too slow for real-time payment decisioning
- **£2.8M annual losses** from fraud reimbursements under the new PSR regulations

The fundamental problem: rule-based systems can only detect patterns they've been explicitly programmed to recognize. APP fraud constantly evolves its tactics.

---

## The Solution

Nexus Intelligence implemented a **multi-layered predictive defense system** that analyzes transactions across three parallel dimensions simultaneously, delivering a fraud confidence score in under 50 milliseconds.

### Layer 1: Behavioral Biometrics

We built a real-time user behavior model that learns each customer's "digital fingerprint":
- **Typing patterns**: Keystroke dynamics, input speed, and correction frequency
- **Session behavior**: Time-of-day patterns, typical transaction amounts, usual recipients
- **Device signals**: Screen size, browser configuration, network origin

When a customer's interaction pattern deviates significantly from their baseline — for example, unusually fast typing (suggesting script-driven input) or an atypical time of day — the system raises the risk score.

### Layer 2: Graph-Based Network Analysis

We constructed a live **transaction graph** where:
- Nodes represent accounts (both sender and receiver)
- Edges represent money flows with timestamps and amounts

Using graph neural networks (GNNs), the system identifies **suspicious network patterns** such as:
- Newly created accounts receiving payments from multiple unrelated senders
- "Mule chains" where money flows through 3-4 accounts before reaching a final destination
- Account clusters that share device fingerprints or IP ranges

```python
# Simplified graph analysis pipeline
from torch_geometric.nn import GATConv

class FraudGraphModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = GATConv(in_channels=64, out_channels=32, heads=4)
        self.conv2 = GATConv(in_channels=128, out_channels=16, heads=2)
        self.classifier = torch.nn.Linear(32, 1)

    def forward(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))
        return torch.sigmoid(self.classifier(x))
```

### Layer 3: LLM Narrative Analysis

The most innovative component: we fine-tuned an LLM to analyze the **payment reference text** and **chat logs** (when available from in-app messaging) for known scam patterns:
- "Urgent" language suggesting pressure tactics
- References to fake invoices, tax refunds, or delivery fees
- Payment references that don't match the stated purpose of the transfer

This layer catches fraud that pure numerical analysis misses — because the social engineering happens in natural language.

### Ensemble Decision Engine

All three layers feed into a gradient-boosted ensemble model (XGBoost) that produces a final fraud probability score between 0 and 1. The system operates in three bands:

| Score | Action | Volume |
|:---|:---|:---|
| 0.0 – 0.3 | **Auto-approve** | ~88% of transactions |
| 0.3 – 0.7 | **Soft challenge** (additional verification step) | ~10% |
| 0.7 – 1.0 | **Block + human review** | ~2% |

---

## Financial Impact

After 120 days of production deployment:

| Metric | Before | After | Change |
|:---|:---|:---|:---|
| Successful fraud attempts (monthly) | 340 | 27 | **-92%** |
| False positive rate | 12% | 0.08% | **-99.3%** |
| Detection latency | 8,000ms | 47ms | **-99.4%** |
| Customer friction complaints | 2,100/month | 180/month | **-91%** |
| Annual fraud reimbursement costs | £2.8M | £0.4M | **-£2.4M saved** |

> "Nexus Intelligence's system didn't just catch more fraud — it made the experience better for our legitimate customers. Our support tickets dropped by 60% in the first month." — CTO, [Client]

---

## Key Takeaways

1. **Multi-modal analysis wins**: No single technique catches APP fraud. Combining behavioral, graph, and language analysis creates defense in depth.
2. **Speed is non-negotiable**: At 47ms response time, fraud scoring happens before the payment confirmation screen renders — invisible to the user.
3. **False positives matter more than false negatives**: Blocking legitimate customers has a compounding cost on trust and retention. Reducing FP rate from 12% to 0.08% was the highest-value outcome.

---

### Related Insights
- [DeepSeek-V3 vs. Llama 4: The 2026 Benchmark](../post.html?blog=deepseek-v3-vs-llama-4-the-2026-benchmark) — Choosing the right model backbone for ML inference pipelines.
- [Autonomous Supply Chain Engine — Case Study](../study.html?id=autonomous-logistics) — Another multi-agent production system delivering measurable ROI.
