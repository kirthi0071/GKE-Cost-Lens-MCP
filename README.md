
# GKE Cost Lens

**An MCP-powered agent that explains your Kubernetes costs — not just reports them.**

---

## What This Is

GKE Cost Lens is a Model Context Protocol (MCP) server that turns Claude into a conversational Kubernetes cost analyst for GCP. Instead of digging through the Billing Console or building Grafana dashboards, you ask a question in plain language — *"why did our cost go up this week?"* — and get back a ranked, plain-English explanation of what actually happened: which namespace, which node pool, whether it was traffic, over-provisioning, or autoscaling.

This isn't a dashboard. It's an **agent** — it decides which GCP APIs to query, joins the data itself, reasons about what changed, and answers the specific question you asked instead of dumping raw metrics on you.

---

## The Problem

GKE bills you for **nodes**, not for what runs on them. That creates a permanent blind spot:

- The invoice says spend went up. It never says *why*, or *who*.
- A single misconfigured HPA or an over-cautious `resources.requests` value can quietly inflate cost for months, invisible in a standard billing view.
- In a shared cluster running multiple client workloads, nobody can cleanly answer "what did team X's services cost this week" without manual filtering and guesswork.
- When finance or a manager asks "is this spike normal," the honest answer usually takes an engineer 30–60 minutes of console-digging to produce.

These aren't hypothetical — they're recurring, real situations in day-to-day cloud operations: monthly cost reviews, post-incident retros, and ad-hoc "why is this expensive" questions that currently have no fast answer.

---

## What We're Trying to Achieve

1. **Ask, don't dig.** Replace manual Billing Console spelunking with a direct question-and-answer interface.
2. **Explain, don't just report.** Every cost number comes with a root-cause: traffic increase, CPU/memory over-request, node scaling event, or network egress.
3. **Zero extra infrastructure.** No Prometheus stack, no BigQuery export setup, no separate dashboard to maintain — just GCP's existing APIs, queried on demand.
4. **Actionable output.** Where cost is reducible (over-provisioned pods, idle nodes), the agent says so and suggests the fix.

---

## Challenges We Faced (and How We Solved Them)

### 1. No native per-pod billing
GCP's billing data is scoped to nodes and SKUs, not individual pods. Getting pod-level cost normally requires enabling GKE Cost Allocation and exporting to BigQuery.

**Decision:** Skip BigQuery entirely. Instead of reconciling against the actual invoice, we **estimate** cost using the same approach open-source tools like Kubecost and OpenCost use when billing export isn't available:

```
pod_cost_share = (pod cpu/mem request ÷ node allocatable cpu/mem) × node hourly price
```

Node hourly price comes from the **Cloud Billing Catalog API** — a public price lookup, no setup required. This trades perfect invoice reconciliation for zero infrastructure overhead, which is the right tradeoff for a fast, on-demand tool.

### 2. "Traffic caused it" isn't a direct join
Kubernetes cost isn't traffic-metered like a CDN. Traffic influences cost indirectly — through autoscaling (more requests → HPA scales pods → cluster autoscaler adds nodes) or directly through network egress SKUs.

**Decision:** Build a correlation layer, not a false direct link. The agent pulls ingress/egress byte metrics, node-count-over-time, and cost-over-time from Cloud Monitoring, then presents the pattern rather than asserting causation it can't prove.

### 3. "Why did cost change" isn't magic — it's a diff
A single point-in-time cost number tells you nothing about cause.

**Decision:** Every explanation is period-over-period: today vs. yesterday, this week vs. last week. The agent computes deltas across cost, node count, CPU/memory requests vs. actual usage, and network egress — then ranks the top contributors instead of listing everything.

---

## How This Makes It Easy

| Before | With GKE Cost Lens |
|---|---|
| Open Billing Console, filter by label/SKU manually | Ask the question directly |
| No pod/namespace breakdown without BigQuery setup | Estimated breakdown from live API data, no setup |
| Cost spike noticed days later, cause unclear | On-demand root-cause explanation, any time |
| Over-provisioning invisible until someone audits manually | Flagged automatically as part of the answer |
| Static dashboards you have to interpret yourself | Conversational, reasoned answers via Claude |

---

## Architecture

```
Claude Desktop / Claude.ai
        │  (MCP protocol)
        ▼
┌─────────────────────────────────────┐
│      GKE Cost Lens MCP Server        │
│                                       │
│  Tools:                              │
│   • get_cost_summary                 │
│   • explain_cost_change              │
│   • get_top_cost_pods                │
│   • get_optimization_suggestions     │
│                                       │
│  Cost Estimation Engine              │
│   (usage × live price)               │
│                                       │
│  Root-Cause Diff Engine              │
│   (period comparison, ranked causes) │
└───────────────┬───────────────────────┘
                │
     ┌──────────┼──────────────┐
     ▼          ▼              ▼
 GKE API   Cloud Monitoring   Billing Catalog API
 (nodes,   (CPU/mem/network   (live price per
 machine    requests+usage)    machine type)
 types)
```

---

## Tools Exposed

- **`get_cost_summary(timeframe)`** — total estimated cost for today / 7 days / custom range, broken down by namespace and node pool
- **`explain_cost_change(timeframe)`** — compares to the prior equivalent period and returns ranked root causes in plain language
- **`get_top_cost_pods(timeframe)`** — pods/namespaces ranked by estimated cost contribution
- **`get_optimization_suggestions()`** — flags over-provisioned requests, idle nodes, and other reducible cost

---

## Why This Belongs in a Portfolio

Most cost tools are either read-only dashboards (GCP Billing Console) or heavyweight self-hosted platforms (Kubecost, OpenCost) that need their own Prometheus stack and ongoing maintenance. GKE Cost Lens sits in a gap neither fills: **a lightweight, conversational, on-demand agent** that requires no additional infrastructure beyond APIs GCP already exposes — built specifically to be asked a question and give a reasoned answer back, not to be stared at.

---

## Status

🚧 In active development — cost estimation engine and MCP tool scaffolding in progress.
