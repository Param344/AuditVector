# AUDITVECTOR 🛡️
> **Autonomous Financial Integrity Investigator & Remediation Engine**  
> *Tagline:* **AI reasons. Code proves. Evidence explains.**  
> *Track:* **The Taskmaster** — [All Things Agentic Hackathon](https://allthingsagentichackathon.devpost.com/)  
> *Live Showcase:* **[https://auditvector-20610.web.app](https://auditvector-20610.web.app)**  
> *Core Tech:* **Gemini 3.5 Flash** • **Google ADK** • **Python** • **DuckDB** • **FastAPI** • **Google Cloud Run / PubSub / Firestore**

[![Test Suite](https://img.shields.io/badge/pytest-63%2F63%20passing-brightgreen.svg)](tests/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-Multi--Agent-4285F4.svg)](https://github.com/google/agent-development-kit)
[![Gemini](https://img.shields.io/badge/LLM-Gemini%203.5%20Flash-8E24AA.svg)](https://deepmind.google/technologies/gemini/)
[![Firebase Hosting](https://img.shields.io/badge/Live%20Demo-Firebase%20Hosting-FFA000.svg)](https://auditvector-20610.web.app)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

---

## 📖 1. Executive Summary & Problem

Financial trading systems, quantitative backtesters, and portfolio accounting engines silently lose billions to subtle integrity failures:
* **Polarity & Sign Inversions:** Flawed subtraction in PnL routines inverting capital losses into artificial profits.
* **Double-Deducted Execution Fees:** Trade commissions deducted once at fill time and deducted again during portfolio aggregation.
* **Config-to-Runtime Drift:** Strategy configuration assuming a 5.0 bps transaction cost while execution slippage averages 13.2 bps.

Standard LLM chatbots hallucinate arithmetic when asked to audit financial datasets with millions of rows. **AuditVector** solves this through a hybrid architecture:

1. **Google ADK + Gemini 3.5 Flash** performs autonomous investigation, hypotheses formulation, AST code mapping, and adaptive mission routing.
2. **Deterministic Verification Engine** (Python FIFO + DuckDB SQL) reconstructs ground-truth numbers directly from raw trade fills with zero LLM arithmetic.
3. **Autonomous Remediation Sandbox** formulates surgical unified-diff patches and verifies that the discrepancy is reduced to **$0.00** before requesting human authorization.
4. **Evidence Contract Architecture** enforces a strict cryptographic mandate: *No Evidence Contract $\to$ No Verified Finding*.

---

## 🏗️ 2. System Architecture & Multi-Agent Flow

```
                                    ┌────────────────────────────────────────────────────────┐
                                    │                     USER / JUDGE                       │
                                    │     Interactive Forensic Console & Live Web Showcase   │
                                    │          https://auditvector-20610.web.app             │
                                    └──────────────────────────┬─────────────────────────────┘
                                                               │ HTTP / REST
                                                               ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ GOOGLE CLOUD RUN ASYNC RUNTIME (Optional Cloud Execution)                                                              │
│                                                                                                                        │
│   ┌───────────────────────────┐      Publish Audit Job      ┌──────────────────────────┐      Async Worker Pull        │
│   │   FastAPI Cloud Run API   │ ──────────────────────────> │  Google Cloud Pub/Sub    │ ──────────────────────────┐   │
│   │   POST /api/audits        │                             │  Topic: audit-jobs       │                           │   │
│   └─────────────┬─────────────┘                             └──────────────────────────┘                           │   │
│                 │ State Updates                                                                                    │   │
│                 ▼                                                                                                  ▼   │
│   ┌───────────────────────────┐                                                             ┌──────────────────────────┴───┐
│   │  Google Cloud Firestore   │ <────────────────────────────────────────────────────────── │  PubSubAuditWorker (Cloud)   │
│   │  Collection: audits       │                   Stage & Result Synchronization            │  Idempotent Consumer         │
│   └───────────────────────────┘                                                             └──────────────┬───────────────┘
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┼───────────────────┘
                                                                                                             │
                                                                                                             ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ GOOGLE ADK + GEMINI 3.5 MULTI-AGENT ADAPTIVE INVESTIGATION & REMEDIATION PIPELINE                                              │
│                                                                                                                                │
│   [01 AUDIT PLANNER]       ──> Formulates audit plan, scopes repository structure & data schemas                               │
│   [02 REPO INVESTIGATOR]   ──> Bounded AST parser maps financial routines (calculate_pnl, calculate_return)                    │
│   [03 FINANCIAL INVEST.]   ──> Ingests performance reports, normalizes claims into typed FinancialClaim targets                │
│   [04 CONTRADICTION INV.]  ──> Dispatches deterministic tools (FIFO lot matcher, fee recalculators, DuckDB analytics)         │
│   [05 REMEDIATION AGENT]   ──> Formulates surgical unified diffs & proves $21,960 ➔ $0.00 in Isolated Verification Sandbox     │
│   [06 REPORT AGENT]        ──> Synthesizes executive verdict, Financial Integrity Score (FIS), and sealed evidence contracts   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                               │
                                                               ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ DETERMINISTIC VERIFICATION & EVIDENCE GRAPH FOUNDATION                                                                         │
│                                                                                                                                │
│   Source Code Citation  ──>  Raw Transaction Dataset  ──>  Canonical Normalizer  ──>  Deterministic FIFO  ──>  Sealed Evidence  │
│   (file:line_range)          (trades.csv SHA-256)          (FinancialEvent schema)    (DuckDB + Verifier)      Contract Finding│
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🤖 3. 6-Agent ADK Specification

| Agent Name | ADK Primitive | Primary Tool / Responsibility |
| :--- | :--- | :--- |
| **01 Audit Planner** | `google.adk.agents.Agent` | Scopes audit parameters, validates file existence, formulates staged plan. |
| **02 Repository Investigator** | `google.adk.agents.Agent` | `scan_repository_ast`: maps financial methods and keywords without sending bulk code to LLM. |
| **03 Financial Investigator** | `google.adk.agents.Agent` | `load_normalized_trades`: extracts reported metrics and config assumptions into canonical targets. |
| **04 Contradiction Investigator** | `google.adk.agents.Agent` | `execute_trade_reconciliation` & `analyze_duckdb_dataset`: reconstructs FIFO PnL, audits fee rates, constructs Evidence Contracts. |
| **05 Remediation Agent** | `google.adk.agents.Agent` | Generates minimal unified diffs and executes isolated sandbox regression tests to prove discrepancy resolves to **$0.00**. |
| **06 Report Agent** | `google.adk.agents.Agent` | Compiles verified findings, computes Financial Integrity Score (0–100), generates markdown reports & SVG evidence graphs. |

---

## 🛡️ 4. Core Innovation & Agentic Features

### 1. Isolated Remediation Sandbox ($21,960 ➔ $0.00)
When a financial contradiction is confirmed, the **Remediation Agent** generates a surgical unified diff and applies it inside an isolated in-memory sandbox. The deterministic verifier is rerun against the patched code:
* **Pre-patch variance:** `$21,960.00`
* **Post-patch variance:** **`$0.00` (RESOLVED)**
* **Safety Invariant:** Zero modifications to the user's real repository without explicit human authorization.

### 2. Interactive "WHY?" Evidence Provenance Traversal
Auditors can traverse the complete mathematical lineage from high-level software claim down to atomic execution fills:
1. **Mathematical Variance:** Exact claimed vs reconstructed dollar delta.
2. **Transaction Fill Evidence:** Canonical fills aggregated with deterministic FIFO matching.
3. **AST Source Code Citation:** Exact file and line range producing the flawed calculation.
4. **Deterministic Verifier Contract:** Verifier algorithm ID and SHA-256 dataset hash.

### 3. Financial Integrity Score (FIS) Engine
Institutional scoring framework (0–100) evaluating:
* Finding Severity Deductions (Critical, High, Medium, Low)
* Capital at Risk as a percentage of Portfolio Equity
* System Stability & Verification Confidence
* Clean systems achieve **100/100 (Grade A+)**; flawed systems receive an **F**.

### 4. 7-Stage Audit Mission Replay & Adaptive Log
An interactive replay controller allowing auditors to step backward and forward through each milestone of the autonomous investigation: `PLANNING` $\to$ `AST_SCAN` $\to$ `CLAIM_EXTRACTION` $\to$ `VERIFICATION` $\to$ `REMEDIATION` $\to$ `REPORTING` $\to$ `SEALED`.

---

## 🧪 5. Certified Benchmarks

AuditVector is certified across three rigorous verification benchmarks:

1. **IntegrityLab Alpha (Failure Benchmark):**
   * Synthetic quantitative engine containing 4 planted calculation flaws:
     * `F-001` (CRITICAL): PnL sign inversion ($+$18,240.00 reported vs $-$3,720.00 reconstructed).
     * `F-002` (CRITICAL): Return polarity contradiction ($+$18.24% reported on net losing portfolio).
     * `F-003` (HIGH): Fee double-counting in portfolio equity ($440.00 deducted vs $220.00 actual).
     * `F-004` (MEDIUM): Configuration fee policy mismatch (5.0 bps claimed vs 13.2 bps effective).
   * **Total Capital at Risk:** **$44,276.75** (FIS: 0 / 100, Grade F).
   * **Sandbox Remediation:** 4/4 patches verified $\to$ **$0.00 variance**.

2. **IntegrityLab Control (Clean Baseline):**
   * Mathematically sound quantitative strategy verifying **zero false positives**.
   * **Result:** **100/100 FIS (Grade A+)**, **$0.00** discrepancy, remediation autonomously bypassed.

3. **AI-BIP Quantitative Engine (Real-World Dogfood):**
   * Multi-asset momentum strategy across BTC, ETH, SOL, AVAX.
   * **Result:** **$16,286.24 discrepancy** independently proven (representing a **30.0484% profit erosion** against reported $54,200.00 profit).

---

## 📂 6. Repository Organization

```
AuditVector/
├── backend/                      # Python backend & Google ADK Multi-Agent core
│   ├── adk/                      # 6 ADK Agent definitions, tools, and Adaptive Orchestrator
│   ├── agents/                   # Planner, Repo, Financial, Contradiction, Remediation, Report
│   ├── cloud/                    # Google Cloud Run FastAPI app, Pub/Sub worker, Firestore store
│   ├── config/                   # Settings & Gemini 3.5 Flash configuration
│   ├── evidence/                 # EvidenceStore, EvidenceGraph, and cryptographic contracts
│   ├── ingestion/                # CSV Ingestion, DuckDB SQL tabular engine, normalizers
│   ├── models/                   # Pydantic schemas (FinancialEvent, Finding, Remediation, Mission)
│   ├── remediation/              # PatchGenerator & Isolated Remediation Sandbox
│   └── verification/             # FIFO PnL recalculator, Return & Fee verifiers, FIS engine
├── frontend/                     # Interactive Forensic Command Console (SPA)
│   ├── index.html                # Unified forensic dashboard UI
│   ├── styles.css                # Enterprise dark glassmorphism styling
│   ├── app.js                    # Dynamic UI state engine, Stepper, Replay, WHY-traversal
│   └── data/                     # Certified Alpha, Control, and AI-BIP offline benchmark exports
├── integritylab/                 # Synthetic failure & control benchmarks (code, trades, reports)
├── dogfood/                      # Real-world AI-BIP quantitative momentum strategy codebase
├── tests/                        # 63 automated unit, integration, and cloud tests (100% PASS)
│   └── e2e/                      # Headless Puppeteer UI integrity, walkthrough & Firebase tests
├── scripts/                      # Video synthesis & screenshot capture utilities
├── docs/                         # Architecture diagrams, Devpost story, blueprints, screenshots
├── run_audit.sh                  # One-command CLI audit launcher
├── verify_all.sh                 # Full verification test suite runner
├── Dockerfile                    # Containerized Cloud Run image specification
├── docker-compose.yml            # Local multi-service orchestration
├── firebase.json                 # Google Firebase Hosting configuration
├── requirements.txt              # Python runtime dependencies
└── LICENSE                       # Apache 2.0 Open Source License
```

---

## 🚀 7. Quickstart Guide

### Option A: Open the Live Showcase (Zero Setup)
Visit **[https://auditvector-20610.web.app](https://auditvector-20610.web.app)** in any modern web browser to interact with all benchmarks, "WHY?" traversals, sandbox remediation diffs, and replay controls.

### Option B: Local CLI Execution

```bash
# 1. Clone repository
git clone https://github.com/Param344/AuditVector.git
cd AuditVector

# 2. Set up virtual environment & install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Configure Gemini API key (optional for live LLM mode; offline deterministic runs out of the box)
export GEMINI_API_KEY="your-gemini-api-key"

# 4. Run the one-command verification test suite
./verify_all.sh

# 5. Run an autonomous audit on IntegrityLab Alpha
./run_audit.sh alpha
```

### Option C: Run the Local Web Server

```bash
# Launch the FastAPI backend and forensic console
PYTHONPATH=. uvicorn backend.cloud.api:app --host 0.0.0.0 --port 8000 --reload
```
Open `http://localhost:8000` in your browser.

---

## 🧪 8. Test Suite Verification

Run the full automated test suite (63 tests covering AST scanning, deterministic FIFO reconciliation, polarity contradiction detection, isolated sandbox remediation, and cloud runtime idempotency):

```bash
PYTHONPATH=. pytest -v
```

```
============================== 63 passed in 8.88s ==============================
```

---

## 📜 9. License

AuditVector is released under the **[Apache 2.0 License](LICENSE)**.
