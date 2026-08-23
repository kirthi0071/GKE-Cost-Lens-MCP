# GCP CloudOps Lens

**An MCP-powered AI agent that connects Claude directly to a GCP project — discover resources, understand cost/security state, and (eventually) safely operate on infrastructure, all through natural-language conversation.**

> Originally scoped as *GKE Cost Lens* (GKE-only cost analysis). Expanded into a full GCP CloudOps + FinOps agent — see [Project Vision](#project-vision) below.

---

## Status: Phase 1 Complete ✅

The first working milestone is live: Claude Desktop can query this project's real GCP environment and return actual resource data — not a mock, not a demo dataset.

```
Claude Desktop  --(MCP protocol)-->  gcp-cloudops-lens server  --(Cloud Asset Inventory API)-->  GCP Project
```

**Try it yourself:** ask Claude *"What resources are in my GCP project?"* once connected — see [Setup](#setup) below.

---

## Project Vision

Connect an AI assistant to a GCP project through MCP so it can **discover, explain, optimize, secure, and eventually operate** cloud resources — through conversation, not dashboards.

The core idea:
> Ask a question in plain language. Get an evidence-based answer and recommendation back — not a wall of raw metrics you have to interpret yourself.

Example questions this project is being built to answer:
- *"What resources are running in my GCP project?"* ✅ **Working (Phase 1)**
- *"Why did my GCP cost increase this week?"*
- *"What can I stop today to save money?"*
- *"Is vm-1 secure?"*
- *"Can I safely delete vm-3?"*

---

## Why This Exists

GCP bills you for infrastructure, not for *insight*. In day-to-day cloud ops, that gap shows up constantly:

- Monthly cost reviews where nobody can quickly explain a spend spike
- Over-provisioned or idle resources quietly wasting money for months, invisible until someone manually audits
- Security misconfigurations (like open SSH/RDP — which this tool already caught on its very first real query) sitting unnoticed
- No fast way to ask "what changed" or "is this normal" without digging through multiple console tabs

This project treats the GCP environment as something you can *have a conversation with*, using an AI agent as the interface — powered by the Model Context Protocol (MCP), which lets Claude call real tools against real infrastructure, safely.

---

## Architecture

```
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │   Claude Desktop │
                  └────────┬────────┘
                           │ MCP (stdio)
                           ▼
                ┌──────────────────────┐
                │  gcp-cloudops-lens    │
                │      MCP Server       │
                │   (Python, MCPServer) │
                └──────────┬───────────┘
                           │
                           ▼
                  Cloud Asset Inventory API
                           │
                           ▼
                  ┌────────────────┐
                  │  GCP Project   │
                  │ Compute Engine │
                  │ VPC / Firewall │
                  │ IAM / Security │
                  │ (more to come) │
                  └────────────────┘
```

---

## What's Implemented (Phase 1)

| Tool | Description |
|---|---|
| `discover_resources()` | Queries Cloud Asset Inventory and returns every resource in the project, grouped by type (Compute Engine, networking, IAM, etc.) |

## What's Planned (Phases 2–10)

Per the phased build order — read-only first, destructive actions only with explicit approval:

- **Resource details** — per-resource deep dives (VM specs, GKE, Cloud Run, Cloud SQL, Storage)
- **Cost analysis** — spend summary, projection, and *why* cost changed (correlation, not unproven causation)
- **FinOps optimization** — idle resources, over-provisioning, "what can I stop today"
- **Security posture** — firewall exposure, IAM risk, actionable recommendations
- **Dependency & criticality analysis** — before any destructive action
- **Safe operations** — stop/start/scale/delete, gated behind: resolve → validate → check dependencies → check criticality → show impact → **explicit user approval** → execute → verify → audit

**Core safety principle:** *Read freely. Recommend carefully. Act only with permission.* The MCP server enforces this — not the LLM.

---

## Setup

### Prerequisites
- Python 3.12 (a dedicated venv is strongly recommended — see notes below)
- `gcloud` CLI authenticated (`gcloud auth login` + `gcloud auth application-default login`)
- A GCP project with Cloud Asset Inventory API enabled and billing linked

### Install

```bash
python3.12 -m venv gcp-cloudops-lens-env
source gcp-cloudops-lens-env/bin/activate
pip install mcp google-cloud-asset
```

### Configure

Edit `server.py` and set your project ID:
```python
PROJECT_ID = "your-project-id-here"
```

### Connect to Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gcp-cloudops-lens": {
      "command": "/absolute/path/to/gcp-cloudops-lens-env/bin/python",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

Restart Claude Desktop completely (Cmd+Q, then reopen), then ask it about your GCP project.

---

## Notes from Building Phase 1

A few real issues hit and resolved during setup, worth knowing if you're replicating this:

- **Python version compatibility:** Very new Python releases (3.14+) can lag behind GCP client library support. A dedicated 3.12 venv avoided this entirely.
- **MCP SDK v2.0.0 rename:** The MCP Python SDK renamed `FastMCP` to `MCPServer` (now at `mcp.server.mcpserver`) in a recent major version. If you're on `mcp<2.0`, use `from mcp.server.fastmcp import FastMCP` instead.
- **No BigQuery required:** This project deliberately avoids BigQuery billing export for cost estimation (planned for later phases) — pricing is estimated live via the Cloud Billing Catalog API instead, keeping infrastructure overhead at zero.

---

## Tech Stack

- Python 3.12
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- Google Cloud client libraries (`google-cloud-asset`, more to follow per phase)
- GCP Application Default Credentials (no service account keys committed — ever)

---

## License

TBD
