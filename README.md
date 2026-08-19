# AUDITVECTOR 🛡️
> **Autonomous Financial Integrity & Evidence-Backed Audit Agent**  
> *Tagline:* **AI reasons. Code proves. Evidence explains.**  
> *Track:* **Taskmaster** — All Things Agentic Hackathon

---

## 📖 Executive Overview

Financial trading strategies and quantitative backtesters frequently fail silently: sign inversions disguise losses as profits, double-counted commissions distort performance metrics, and configuration assumptions drift from runtime execution.

**AuditVector** is an autonomous multi-agent audit investigator that treats quantitative repositories, execution logs, and trade data not with blind LLM trust, but with **deterministic mathematical proof** and **traceable evidence graphs**.

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENTIC REASONING                        │
│            Google ADK 2.7 + Gemini 3.5 Flash                │
│       Plan → Map AST → Extract Claims → Explain             │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   DETERMINISTIC TRUTH                       │
│              Python FIFO Engine + DuckDB                    │
│       Reconstruct PnL → Audit Fees → Compare Rates          │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     EVIDENCE GRAPH                          │
│     Source Code → Data Record → Verifier → Finding          │
│                Human-verifiable proof                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🤖 5-Agent ADK Architecture

1. **Audit Planner (`google.adk.agents.Agent`)**: Scopes directory paths, dataset schemas, and prioritizes critical financial calculation pathways.
2. **Repository Investigator (`google.adk.agents.Agent`)**: Performs bounded AST parsing to map financial routines (`calculate_reported_pnl`, `calculate_portfolio_return`) and keywords without pushing whole codebases to the LLM.
3. **Financial Investigator (`google.adk.agents.Agent`)**: Extracts reported metrics (PnL, return %, fees, fee bps) into typed verification targets.
4. **Contradiction Investigator (`google.adk.agents.Agent`)**: Invokes deterministic verification tools (`execute_trade_reconciliation`, `evaluate_metric_variance`), computes variances, and constructs strict **Evidence Contracts** (`No Evidence Contract → No Verified Finding`).
5. **Report Agent (`google.adk.agents.Agent`)**: Synthesizes verified findings, capital-at-risk numbers, and provenance metadata into an Executive Financial Integrity Report.

---

## ⚡ Quickstart

### 1. Run Autonomous Audits Locally via CLI

```bash
# Execute Audit on IntegrityLab Alpha (4 Planted Contradictions)
./run_audit.sh --demo alpha

# Execute Audit on IntegrityLab Control Case (Clean Calculation)
./run_audit.sh --demo control

# Run Custom Audit
./run_audit.sh --repo path/to/source --data path/to/trades.csv --report path/to/report.json
```

### 2. Launch Web Dashboard & REST API

```bash
source .venv/bin/activate
uvicorn backend.api.server:app --host 0.0.0.0 --port 8000 --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser for the interactive web dashboard with live stage tracking and interactive evidence chains.

### 3. Run Forensic Test Suite

```bash
source .venv/bin/activate
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## 🚢 Google Cloud Run Deployment

```bash
# Deploy with automated script
GCP_PROJECT_ID=your-gcp-project-id ./deploy_cloudrun.sh
```

Or deploy using Docker Compose:
```bash
docker-compose up --build
```