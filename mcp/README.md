# GCP CloudOps Lens

### An MCP-powered AI agent for understanding, optimizing, securing, and operating your GCP project.

**GCP CloudOps Lens** is a Model Context Protocol (MCP) server that connects an AI assistant to a Google Cloud project and turns raw GCP infrastructure data into conversational answers and actionable recommendations.

Instead of manually jumping between the GCP Console, Billing, Monitoring, IAM, Security Command Center, and individual service dashboards, you ask questions in natural language.

> **"What is running in my GCP project?"**

> **"How much is everything costing me?"**

> **"What will my bill be at the end of this month?"**

> **"Which resources are wasting money?"**

> **"What can I safely stop today?"**

> **"Why did my GCP cost increase this week?"**

> **"Is this VM secure?"**

> **"What should I fix first?"**

> **"Delete vm-3."**

The agent discovers resources, analyzes cost and utilization, identifies risks and optimization opportunities, explains the reasoning, and — for supported operations — can perform actions only after appropriate validation and explicit user approval.

---

# Table of Contents

* [What Is GCP CloudOps Lens?](#what-is-gcp-cloudops-lens)
* [The Problem](#the-problem)
* [Vision](#vision)
* [Core Capabilities](#core-capabilities)
* [Example Conversations](#example-conversations)
* [Architecture](#architecture)
* [Resource Discovery](#resource-discovery)
* [FinOps Engine](#finops-engine)
* [Cost Projection](#cost-projection)
* [Optimization Engine](#optimization-engine)
* [Security Lens](#security-lens)
* [Change Detection](#change-detection)
* [Dependency Analysis](#dependency-analysis)
* [Safe Operations](#safe-operations)
* [Resource Aliases](#resource-aliases)
* [Policy and Criticality](#policy-and-criticality)
* [Audit Trail](#audit-trail)
* [GCP Services](#gcp-services)
* [MCP Tools](#mcp-tools)
* [Safety Model](#safety-model)
* [Project Scope](#project-scope)
* [Technology Stack](#technology-stack)
* [Project Roadmap](#project-roadmap)
* [Repository Structure](#repository-structure)
* [Authentication](#authentication)
* [IAM and Permissions](#iam-and-permissions)
* [Running Locally](#running-locally)
* [Example Workflow](#example-workflow)
* [Design Principles](#design-principles)
* [Existing GCP Capabilities](#existing-gcp-capabilities)
* [Project Status](#project-status)
* [Future Roadmap](#future-roadmap)
* [Contributing](#contributing)
* [License](#license)

---

# What Is GCP CloudOps Lens?

GCP CloudOps Lens is an **AI-powered GCP FinOps and Cloud Operations agent** built around the Model Context Protocol.

The goal is to create a conversational interface over a GCP project where the agent can understand:

```text
Resources
    +
Cost
    +
Usage
    +
Security
    +
Dependencies
    +
Changes
    +
Recommendations
    +
Actions
```

The project is intentionally designed around a **read → understand → recommend → approve → act → verify** workflow.

It is not intended to be another static dashboard.

It is also not intended to blindly execute arbitrary cloud commands.

The goal is to build an agent that can reason about cloud infrastructure before taking action.

---

# The Problem

Managing a GCP environment requires engineers to jump across many different systems.

For example:

```text
GCP Console
     │
     ├── Compute Engine
     ├── GKE
     ├── Cloud Run
     ├── Cloud SQL
     ├── Cloud Storage
     ├── Load Balancing
     ├── Pub/Sub
     ├── BigQuery
     ├── IAM
     ├── Monitoring
     ├── Billing
     └── Security Command Center
```

The infrastructure data exists, but it is fragmented.

A billing console can tell you that spending increased.

Monitoring can tell you that CPU increased.

GKE can tell you that a node scaled.

IAM can tell you that permissions changed.

Security Command Center can tell you that a vulnerability exists.

But the engineer still has to connect these pieces manually.

### The goal of CloudOps Lens is to connect them.

Instead of:

> "GCP Compute cost increased by 23%."

The agent should eventually be able to explain:

> "Compute cost increased by approximately 23% because your production Managed Instance Group increased from 4 to 9 instances after traffic increased. The additional instances accounted for approximately ₹4,200 of the increase."

---

# Vision

The long-term vision is:

```text
                USER
                  │
                  ▼
          AI / MCP CLIENT
                  │
                  ▼
        ┌─────────────────────┐
        │  GCP CloudOps Lens  │
        └──────────┬──────────┘
                   │
       ┌───────────┼────────────┐
       ▼           ▼            ▼
   DISCOVER      ANALYZE      RECOMMEND
       │           │            │
       ▼           ▼            ▼
   Resources     Cost         Optimization
   Services      Usage        Security
   Dependencies  Health       Reliability
   Changes       Trends       Operations
                   │
                   ▼
                 ACT
                   │
             ┌─────┴─────┐
             ▼           ▼
          APPROVE      REJECT
             │
             ▼
          EXECUTE
             │
             ▼
          VERIFY
             │
             ▼
           AUDIT
```

---

# Core Capabilities

CloudOps Lens is designed around seven major capabilities.

## 1. Resource Discovery

Understand what exists in the GCP project.

```text
Compute Engine
GKE
Cloud Run
Cloud SQL
Cloud Storage
Pub/Sub
BigQuery
Load Balancers
Artifact Registry
Cloud Functions
VPC
Firewall rules
Disks
IP addresses
...
```

---

## 2. FinOps

Understand where money is being spent.

```text
Current spend
Historical spend
Daily spend
Weekly spend
Monthly spend
Cost by service
Cost by resource
Cost trends
Cost projections
Cost anomalies
Potential savings
```

---

## 3. Optimization

Identify resources that may be wasting money.

Examples:

```text
Idle VM
Under-utilized VM
Oversized VM
Unattached disk
Unused static IP
Low-traffic Cloud Run service
Over-provisioned GKE node
Unused development environment
Excessive storage
```

---

## 4. Security

Analyze security posture and explain what should be improved.

Examples:

```text
Public IP
Open SSH
Open firewall
Excessive IAM permissions
Weak service-account permissions
Missing security controls
Missing monitoring
Missing backup
Risky configuration
```

---

## 5. Change Intelligence

Understand what changed.

Examples:

```text
VM created
VM deleted
Machine type changed
GKE node count increased
Cloud Run revision deployed
IAM role changed
Firewall rule modified
Cloud SQL configuration changed
Cost increased
```

---

## 6. Safe Operations

Eventually allow supported infrastructure operations.

Examples:

```text
Stop
Start
Restart
Scale
Resize
Delete
Cordon
Drain
Update
Schedule
```

Actions are not executed blindly.

---

## 7. Human-Approved Automation

The agent should explain the proposed operation before executing it.

```text
Understand
    ↓
Impact analysis
    ↓
Risk assessment
    ↓
Expected cost saving
    ↓
User approval
    ↓
Execute
    ↓
Verify
```

---

# Example Conversations

## Discover the project

### User

```text
What is running in my GCP project?
```

### CloudOps Lens

```text
I found 27 active resources.

Compute Engine
  vm-1   production-api
  vm-2   staging-api
  vm-3   test-server

GKE
  gke-1  production-cluster

Cloud Run
  run-1  payment-api
  run-2  frontend

Cloud SQL
  sql-1  production-db

Cloud Storage
  bucket-1 production-data

Pub/Sub
  topic-1 orders

...

Would you like a cost breakdown?
```

---

# Cost Analysis

### User

```text
How much am I spending?
```

### CloudOps Lens

```text
Current project spend

Today:
₹1,240

Last 7 days:
₹8,730

Current month:
₹28,430

Previous month:
₹24,810

Change:
+14.6%

Top contributors:

1. Compute Engine
   ₹8,420

2. Cloud SQL
   ₹5,840

3. GKE
   ₹4,210

4. Cloud Run
   ₹2,130

5. Cloud Storage
   ₹1,420
```

---

# Cost Projection

### User

```text
What will my bill be at the end of this month?
```

The agent estimates:

```text
Current spend:
₹28,430

Average daily spend:
₹1,580

Projected month-end:
~₹48,980

Previous month:
₹24,810

Projected increase:
~97.4%
```

The projection should clearly be identified as an **estimate**, not an invoice.

---

# Cost Explanation

### User

```text
Why did my cost increase this week?
```

The agent investigates multiple signals:

```text
Cost
   │
   ├── Compute
   ├── GKE
   ├── Cloud SQL
   ├── Network
   └── Storage

Monitoring
   │
   ├── CPU
   ├── Memory
   ├── Requests
   └── Network traffic

Infrastructure changes
   │
   ├── VM creation
   ├── Scaling
   ├── Deployment
   └── Configuration changes
```

Then produces a ranked explanation.

---

# "What Can I Stop Today?"

### User

```text
What can I stop today instead of wasting money?
```

Example:

```text
Potential candidates

1. dev-vm-1
   Cost: ₹120/day
   CPU: 3%
   Production dependency: No
   Risk: Low

2. test-vm-2
   Cost: ₹180/day
   CPU: 5%
   Production dependency: No
   Risk: Low

3. staging-sql
   Cost: ₹240/day
   Usage: Low
   Risk: Medium

Potential saving:
₹540/day

Potential monthly equivalent:
~₹16,200
```

The agent should distinguish between:

```text
SAFE TO STOP
REQUIRES REVIEW
DO NOT STOP
```

---

# Security Lens

### User

```text
vm-1 is a critical production server.
What security configuration should I have?
```

CloudOps Lens should inspect the available security signals and produce something like:

```text
VM Security Review

Resource:
production-api

Criticality:
CRITICAL

Findings:

✓ Shielded VM
✓ Secure Boot
✓ OS Login

⚠ Public IP
⚠ SSH exposed broadly
⚠ Service account permissions may be excessive
⚠ Missing alerting
⚠ Backup policy requires review

Priority:

CRITICAL
  Restrict public SSH access

HIGH
  Review service-account permissions

HIGH
  Remove unnecessary public exposure

MEDIUM
  Improve monitoring

MEDIUM
  Review backup strategy
```

For each recommendation, the agent should provide:

```text
What is wrong
Why it matters
Risk
Recommended change
Expected impact
Implementation steps
Official GCP documentation
```

---

# Resource Criticality

Resources can be classified using metadata/policy.

```text
criticality:
  CRITICAL
  HIGH
  MEDIUM
  LOW
  UNKNOWN
```

Environment:

```text
production
staging
development
test
unknown
```

Action policy:

```text
PROHIBITED
APPROVAL_REQUIRED
ALLOWED
```

Example:

```text
production-db

criticality:
CRITICAL

action_policy:
PROHIBITED
```

Whereas:

```text
test-vm

criticality:
LOW

action_policy:
APPROVAL_REQUIRED
```

---

# Dependency Analysis

Before destructive actions, CloudOps Lens should attempt to understand dependencies.

Example:

```text
vm-4

 ├── static IP
 ├── persistent disk
 ├── service account
 ├── firewall rules
 └── application dependency
```

The agent should identify potential impact before offering deletion.

Example:

```text
⚠ Potential impact

vm-4 is referenced by:
  production-load-balancer
  backend-service
  monitoring alert

Recommendation:
DO NOT DELETE
```

---

# Resource Aliases

The user should not need to remember long GCP resource names.

Instead:

```text
vm-1
vm-2
vm-3

gke-1

sql-1

run-1

bucket-1
```

Example:

```text
vm-3
  ↓
test-server
  ↓
Compute Engine VM
  ↓
asia-south1-a
```

Aliases are mapped internally to immutable resource identifiers.

Aliases should be associated with a resource snapshot/context so that an old alias cannot accidentally refer to a different resource later.

---

# Safe Operations

Supported actions will eventually include:

```text
stop_resource
start_resource
restart_resource
scale_resource
resize_resource
delete_resource
update_resource
schedule_resource
```

For Kubernetes:

```text
cordon_gke_node
drain_gke_node
remove_gke_node
scale_node_pool
```

Operations must be resource-aware.

For example, a GKE-managed node should not simply be deleted as an ordinary Compute Engine VM.

The action engine must determine the correct GCP/GKE operation.

---

# Action Lifecycle

Every potentially destructive operation follows:

```text
User Request
     │
     ▼
Resolve Resource
     │
     ▼
Validate Resource
     │
     ▼
Check Dependencies
     │
     ▼
Check Criticality
     │
     ▼
Calculate Impact
     │
     ▼
Estimate Cost/Savings
     │
     ▼
Show Proposed Action
     │
     ▼
Explicit User Approval
     │
     ▼
Execute
     │
     ▼
Verify
     │
     ▼
Audit
```

Example:

```text
User:
Delete vm-3
```

CloudOps Lens:

```text
Resource:
test-server

Type:
Compute Engine VM

Current cost:
~₹4,100/month

CPU:
4%

Production dependency:
None detected

Risk:
LOW

Estimated saving:
~₹4,100/month

Action:
DELETE

Do you want me to proceed?
```

Only after explicit approval should the action execute.

---

# "What Changed?"

CloudOps Lens should eventually provide infrastructure change intelligence.

Example:

```text
What changed yesterday?
```

Response:

```text
Infrastructure changes

Compute:
+3 VMs

GKE:
+2 nodes

Cloud Run:
1 new revision

IAM:
2 role changes

Firewall:
1 rule modified

Cloud SQL:
machine configuration changed

Billing:
+18%
```

Then:

```text
Which change caused the cost increase?
```

The agent correlates changes with monitoring and cost data.

---

# Optimization Engine

Optimization recommendations can include:

### Compute Engine

```text
Idle VM
Oversized VM
Low CPU utilization
Low memory utilization
Unattached disk
Unused IP
```

### GKE

```text
Over-provisioned requests
Idle nodes
Excessive node count
Node-pool sizing
Autoscaling opportunities
```

### Cloud Run

```text
Low traffic
Excessive minimum instances
CPU/memory sizing
Revision configuration
```

### Cloud SQL

```text
Under-utilized instance
Oversized machine
Storage growth
Backup configuration
```

### Cloud Storage

```text
Old objects
Missing lifecycle policies
Storage class opportunities
Unnecessary retained data
```

### BigQuery

```text
Expensive queries
Repeated scans
Partitioning opportunities
Storage optimization
```

---

# Cost Saving Schedules

A future capability is scheduled cost optimization.

Example:

```text
Development environment

Monday-Friday

08:00
Start eligible resources

18:00
Stop eligible resources

Excluded:
production
critical resources
user-defined exclusions
```

Before creating a schedule, CloudOps Lens should show:

```text
Estimated current daily cost:
₹540

Estimated potential saving:
₹320/day

Estimated monthly saving:
~₹9,600

Resources:
dev-vm-1
dev-vm-2
dev-cloud-sql
```

The user must approve the policy.

---

# Project Health Score

A future project-level overview can provide:

```text
GCP PROJECT HEALTH

Cost           72/100
Security       61/100
Reliability    88/100
Utilization    54/100
Operations     79/100

Overall        69/100
```

The score should always be explainable.

Example:

```text
Security score: 61

Main contributors:

1. Public SSH exposure
2. Excessive IAM permissions
3. Missing monitoring
4. Unreviewed service accounts
```

---

# GCP Services

The project is designed to support multiple GCP services.

Initial target services:

```text
Compute Engine
GKE
Cloud Run
Cloud SQL
Cloud Storage
```

Additional services:

```text
Pub/Sub
BigQuery
Load Balancing
Artifact Registry
Cloud Functions
VPC
Firewall
Persistent Disk
Static IP
```

The architecture is intentionally extensible so additional GCP services can be added without redesigning the core system.

---

# GCP APIs and Data Sources

The project will leverage existing GCP capabilities rather than rebuilding them.

Potential data sources include:

```text
Cloud Asset Inventory
Cloud Billing
Cloud Monitoring
Cloud Recommender
IAM / Policy Intelligence
Security Command Center
Compute Engine APIs
GKE APIs
Cloud Run APIs
Cloud SQL APIs
Cloud Storage APIs
BigQuery APIs
Pub/Sub APIs
```

The agent's primary job is to **correlate and explain** the information returned by these systems.

---

# MCP Tools

The tool surface will evolve as the project develops.

## Discovery

```text
discover_resources
list_resources
get_resource_details
get_resource_dependencies
```

## Cost

```text
get_cost_summary
get_resource_cost
get_top_cost_resources
get_cost_projection
explain_cost_change
```

## Monitoring

```text
get_resource_utilization
get_resource_health
get_resource_metrics
```

## FinOps

```text
get_optimization_suggestions
get_idle_resources
get_savings_opportunities
get_stop_candidates
```

## Security

```text
get_security_findings
get_iam_risks
get_resource_security_posture
get_security_recommendations
```

## Changes

```text
get_recent_changes
explain_resource_change
explain_cost_change
```

## Operations

```text
start_resource
stop_resource
restart_resource
scale_resource
resize_resource
delete_resource
```

## Kubernetes

```text
cordon_gke_node
drain_gke_node
remove_gke_node
scale_node_pool
```

---

# Safety Model

CloudOps Lens follows a strict principle:

> **Read freely. Recommend carefully. Act only with permission.**

Read-only operations should be separated from destructive operations.

Example:

```text
READ

discover_resources
get_cost_summary
get_resource_details
get_security_findings
get_recommendations
```

versus:

```text
ACTION

delete_resource
stop_resource
restart_resource
resize_resource
scale_resource
```

Destructive operations should require:

```text
Resource identity
+
Impact analysis
+
Criticality check
+
Dependency check
+
Explicit user approval
```

The MCP server itself must enforce these controls. The LLM should never be treated as a security boundary.

---

# Project Scope

## Current scope

The first version targets:

```text
ONE GCP PROJECT
```

An Organization is **not required** for the initial implementation.

Project-level architecture:

```text
GCP Project
     │
     ▼
CloudOps Lens MCP
     │
     ├── Resource discovery
     ├── Cost analysis
     ├── Monitoring
     ├── Security
     └── Recommendations
```

Organization/folder/multi-project support can be added later.

---

# Technology Stack

Proposed stack:

```text
Language:
Python

Protocol:
Model Context Protocol (MCP)

Cloud:
Google Cloud Platform

APIs:
Google Cloud APIs

Authentication:
Application Default Credentials
Service Account / Workload Identity for deployment

AI Client:
MCP-compatible AI client

Development:
Python virtual environment
pytest
ruff
mypy

Deployment:
Docker
Cloud Run / VM / other suitable runtime
```

The implementation may evolve as the project develops.

---

# Architecture

```text
                       ┌────────────────────┐
                       │   MCP Client / AI  │
                       │                    │
                       │ Claude / compatible│
                       └─────────┬──────────┘
                                 │
                                 │ MCP
                                 ▼
                  ┌────────────────────────────┐
                  │     GCP CloudOps Lens      │
                  │         MCP Server         │
                  │                            │
                  │ ┌────────────────────────┐ │
                  │ │ Resource Discovery      │ │
                  │ └────────────┬───────────┘ │
                  │              │             │
                  │ ┌────────────▼───────────┐ │
                  │ │ Resource Normalizer    │ │
                  │ └────────────┬───────────┘ │
                  │              │             │
                  │ ┌────────────▼───────────┐ │
                  │ │ Cost / FinOps Engine    │ │
                  │ └────────────┬───────────┘ │
                  │              │             │
                  │ ┌────────────▼───────────┐ │
                  │ │ Monitoring Engine       │ │
                  │ └────────────┬───────────┘ │
                  │              │             │
                  │ ┌────────────▼───────────┐ │
                  │ │ Security Engine         │ │
                  │ └────────────┬───────────┘ │
                  │              │             │
                  │ ┌────────────▼───────────┐ │
                  │ │ Dependency Engine       │ │
                  │ └────────────┬───────────┘ │
                  │              │             │
                  │ ┌────────────▼───────────┐ │
                  │ │ Recommendation Engine   │ │
                  │ └────────────┬───────────┘ │
                  │              │             │
                  │ ┌────────────▼───────────┐ │
                  │ │ Policy / Safety Engine  │ │
                  │ └────────────┬───────────┘ │
                  │              │             │
                  │ ┌────────────▼───────────┐ │
                  │ │ Action Engine           │ │
                  │ └────────────┬───────────┘ │
                  │              │             │
                  │ ┌────────────▼───────────┐ │
                  │ │ Verification / Audit    │ │
                  │ └────────────────────────┘ │
                  └──────────────┬─────────────┘
                                 │
       ┌─────────────────────────┼────────────────────────┐
       │                         │                        │
       ▼                         ▼                        ▼
Cloud Asset Inventory      Cloud Billing            Monitoring
       │                         │                        │
       └─────────────────────────┼────────────────────────┘
                                 │
                                 ▼
                         GCP Project Resources
```

---

# Repository Structure

Proposed structure:

```text
gcp-cloudops-lens/
│
├── src/
│   └── cloudops_lens/
│       │
│       ├── server.py
│       │
│       ├── config/
│       │   ├── settings.py
│       │   └── policies.py
│       │
│       ├── discovery/
│       │   ├── asset_inventory.py
│       │   ├── resource_registry.py
│       │   └── normalizer.py
│       │
│       ├── finops/
│       │   ├── billing.py
│       │   ├── pricing.py
│       │   ├── projection.py
│       │   ├── optimization.py
│       │   └── savings.py
│       │
│       ├── monitoring/
│       │   ├── metrics.py
│       │   └── utilization.py
│       │
│       ├── security/
│       │   ├── findings.py
│       │   ├── iam.py
│       │   └── posture.py
│       │
│       ├── dependencies/
│       │   └── analyzer.py
│       │
│       ├── changes/
│       │   └── detector.py
│       │
│       ├── actions/
│       │   ├── executor.py
│       │   ├── validator.py
│       │   └── verification.py
│       │
│       ├── resources/
│       │   ├── compute.py
│       │   ├── gke.py
│       │   ├── cloud_run.py
│       │   ├── cloud_sql.py
│       │   └── storage.py
│       │
│       └── tools/
│           ├── discovery_tools.py
│           ├── cost_tools.py
│           ├── security_tools.py
│           ├── optimization_tools.py
│           └── action_tools.py
│
├── tests/
│
├── docs/
│
├── scripts/
│
├── .env.example
├── .gitignore
├── Dockerfile
├── pyproject.toml
├── README.md
└── LICENSE
```

---

# Authentication

For local development, the preferred approach is Google Application Default Credentials.

Example:

```bash
gcloud auth application-default login
```

The MCP server should obtain credentials through Google's standard authentication mechanisms.

Do not commit:

```text
*.json
*.pem
*.key
credentials
tokens
secrets
```

to the repository.

For production deployment, use a dedicated service account with least-privilege IAM.

---

# IAM Philosophy

CloudOps Lens follows:

> **Least privilege by default.**

The initial development phase should be **read-only**.

Write permissions should be introduced only when the corresponding action engine is implemented and tested.

A conceptual permission model:

```text
Phase 1

READ ONLY
   │
   ├── Resource discovery
   ├── Cost
   ├── Monitoring
   ├── Security
   └── Recommendations

Phase 2

CONTROLLED WRITE
   │
   ├── Stop
   ├── Start
   ├── Restart
   └── Scale

Phase 3

DESTRUCTIVE
   │
   ├── Delete
   └── destructive remediation
```

---

# Running Locally

## Prerequisites

```text
Python 3.x
Google Cloud CLI
A GCP project
An MCP-compatible client
```

Authenticate:

```bash
gcloud auth application-default login
```

Set the project:

```bash
gcloud config set project YOUR_PROJECT_ID
```

Create the environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the MCP server:

```bash
python -m cloudops_lens.server
```

The exact startup command may change as implementation progresses.

---

# Example End-to-End Workflow

## Step 1 — Discover

```text
User:
What is running in my GCP project?
```

## Step 2 — Analyze

```text
User:
What are the top five resources by cost?
```

## Step 3 — Investigate

```text
User:
Why is vm-2 expensive?
```

## Step 4 — Optimize

```text
User:
What can I stop today?
```

## Step 5 — Evaluate impact

```text
User:
What happens if I stop vm-2?
```

## Step 6 — Approve

```text
User:
Stop vm-2.
```

## Step 7 — Confirmation

```text
CloudOps Lens:

vm-2
Production dependency: None detected
Estimated saving: ₹120/day
Risk: LOW

Proceed?
```

## Step 8 — Execute

```text
User:
Yes.
```

## Step 9 — Verify

```text
✓ vm-2 stopped successfully.

Estimated saving:
₹120/day
~₹3,600/month
```

## Step 10 — Audit

```text
Action:
STOP

Resource:
vm-2

Requested by:
user

Timestamp:
...

Result:
SUCCESS
```

---

# Design Principles

## 1. Explain, don't just report

Bad:

```text
Cost: ₹8,420
```

Better:

```text
Compute cost increased 24% because the production MIG
scaled from 4 to 9 instances.
```

---

## 2. Evidence before action

The agent should explain why it recommends something.

---

## 3. Never confuse estimation with billing truth

Projected costs and estimated resource allocation must be clearly labeled.

---

## 4. Read first, write later

The first version should be safe and read-only.

---

## 5. Human approval for destructive operations

The AI should propose.

The user approves.

The system executes.

---

## 6. Verify every action

Successful API submission is not enough.

The system should verify the resulting resource state.

---

## 7. Service-aware operations

A GKE node is not treated the same way as an ordinary Compute Engine VM.

A Cloud SQL instance is not treated like a VM.

A Cloud Run service is not treated like a Kubernetes deployment.

Actions must understand the underlying resource type.

---

## 8. Don't rebuild GCP

Use Google's APIs, recommendations and security systems wherever possible.

The value of CloudOps Lens is the **correlation, reasoning, prioritization, workflow and safe automation layer**.

---

# Existing GCP Capabilities

CloudOps Lens builds on existing Google Cloud capabilities rather than pretending to replace them.

Useful Google Cloud documentation includes:

* Cloud Asset Inventory
* Cloud Billing
* Cloud Monitoring
* Recommender
* FinOps Hub
* IAM Policy Intelligence
* Security Command Center
* Individual GCP service APIs

These services already expose valuable information.

CloudOps Lens aims to connect that information into a conversational workflow.

---

# Project Roadmap

## Phase 1 — Project Discovery

* [ ] GCP authentication
* [ ] Project configuration
* [ ] MCP server
* [ ] Cloud Asset Inventory integration
* [ ] Resource discovery
* [ ] Resource normalization
* [ ] Human-readable resource aliases
* [ ] Resource details

---

## Phase 2 — FinOps

* [ ] Billing integration
* [ ] Current spend
* [ ] Historical spend
* [ ] Cost by service
* [ ] Cost by resource where available
* [ ] Daily cost
* [ ] Weekly cost
* [ ] Monthly cost
* [ ] Month-end projection
* [ ] Cost trend analysis
* [ ] Cost-change explanations

---

## Phase 3 — Monitoring

* [ ] CPU utilization
* [ ] Memory utilization
* [ ] Network utilization
* [ ] Service metrics
* [ ] Resource health
* [ ] Utilization-based recommendations

---

## Phase 4 — Optimization

* [ ] Idle resource detection
* [ ] Over-provisioning detection
* [ ] Unattached resource detection
* [ ] Savings estimation
* [ ] Stop candidates
* [ ] Delete candidates
* [ ] Optimization ranking

---

## Phase 5 — Security

* [ ] Security findings
* [ ] IAM analysis
* [ ] Public exposure detection
* [ ] Firewall analysis
* [ ] Service-account analysis
* [ ] Critical resource security review
* [ ] Security recommendations
* [ ] Official documentation references

---

## Phase 6 — Change Intelligence

* [ ] Resource change detection
* [ ] Configuration changes
* [ ] Cost correlation
* [ ] Deployment correlation
* [ ] Scaling correlation
* [ ] "What changed?" workflow

---

## Phase 7 — Safe Operations

* [ ] Stop resource
* [ ] Start resource
* [ ] Restart resource
* [ ] Scale resource
* [ ] Resize resource
* [ ] Dependency checks
* [ ] Criticality checks
* [ ] Approval workflow
* [ ] Action verification
* [ ] Audit trail

---

## Phase 8 — FinOps Automation

* [ ] Start/stop schedules
* [ ] Development environment schedules
* [ ] Cost-saving policies
* [ ] Resource exclusions
* [ ] Maximum savings policies
* [ ] Automatic recommendation reports

---

## Phase 9 — Multi-Project

Future support:

```text
Organization
    │
    ├── Project A
    ├── Project B
    ├── Project C
    └── Project D
```

The initial version does **not** require organization access.

---

# Future Vision

The long-term goal is to make GCP CloudOps Lens capable of answering:

```text
"What is running?"
```

```text
"What is costing me?"
```

```text
"Why is it costing me?"
```

```text
"What changed?"
```

```text
"What is unhealthy?"
```

```text
"What is insecure?"
```

```text
"What is wasting money?"
```

```text
"What can I stop?"
```

```text
"What can I safely delete?"
```

```text
"What will happen if I change this?"
```

```text
"How much will I save?"
```

```text
"Fix the low-risk issues."
```

with the final operation always governed by explicit safety and authorization controls.

---

# Project Philosophy

GCP CloudOps Lens is built around one simple idea:

> **Cloud infrastructure should be understandable through conversation.**

Instead of requiring an engineer to manually correlate:

```text
Billing
+
Monitoring
+
Inventory
+
Security
+
IAM
+
GKE
+
Compute
+
Deployments
+
Dependencies
```

the agent should do the correlation and present the result in human terms.

The goal is not to replace cloud engineers.

The goal is to give them a **cloud-aware operational assistant** that can investigate faster, explain better, and automate safely.

---

# Project Status

🚧 **Early Development**

Current focus:

```text
GCP project connection
        ↓
Resource discovery
        ↓
Resource normalization
        ↓
MCP tool foundation
```

Cost analysis, monitoring, security, optimization and controlled actions will be introduced incrementally.

This README describes the **target architecture and roadmap**. Features marked in the roadmap should not be considered implemented until their corresponding implementation is available.

---

# License

License information will be added as the project matures.
