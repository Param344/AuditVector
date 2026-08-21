# AUDITVECTOR 🛡️
> **Autonomous Financial Integrity Investigator & Evidence-Grounded Audit Engine**  
> *Tagline:* **AI reasons. Code proves. Evidence explains.**  
> *Track:* **The Taskmaster** — [All Things Agentic Hackathon](https://allthingsagentichackathon.devpost.com/)  
> *Core Tech:* **Gemini 3.5 Flash** • **Google ADK 2.7** • **Google Cloud Run** • **Google Cloud Pub/Sub** • **Google Cloud Firestore** • **DuckDB**

---

## 📖 1. Executive Summary & Problem

Financial trading systems, quantitative backtesters, and portfolio accounting engines silently lose billions to subtle integrity failures:
* **Polarity & Sign Inversions:** Negative returns inverted by flawed subtraction, disguising capital drawdowns as profitable alpha.
* **Double-Deducted Execution Fees:** Trade-level commissions subtracted at execution and subtracted a second time during portfolio aggregation.
* **Config-to-Runtime Drift:** Strategy configuration policies assuming 5 bps transaction costs while actual fill slippage averages 13.2 bps.

Standard LLM chatbots hallucinate mathematical calculations when fed millions of transaction rows. **AuditVector** solves this through a hybrid architecture:
1. **Google ADK + Gemini 3.5 Flash** performs autonomous reasoning: scopes repository paths, scans code ASTs, and extracts reported claims.
2. **Deterministic Verification Engine** (Python FIFO + DuckDB) reconstructs ground-truth numbers directly from raw canonical trade fills with zero LLM math hallucinations.
3. **Evidence Contract Architecture** enforces a strict cryptographic mandate: *No Evidence Contract $\to$ No Verified Finding*.

---

## 🏗️ 2. System Architecture & End-to-End Flow

```
                                    ┌────────────────────────────────────────────────────────┐
                                    │                     USER / JUDGE                       │
                                    │       Interactive Forensic Console (Port 8000)         │
                                    └──────────────────────────┬─────────────────────────────┘
                                                               │ HTTP / REST
                                                               ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ GOOGLE CLOUD RUN ASYNC RUNTIME                                                                                         │
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
│ GOOGLE ADK 2.7 + GEMINI 3.5 MULTI-AGENT INVESTIGATION PIPELINE                                                                 │
│                                                                                                                                │
│   [01 AUDIT PLANNER]       ──> Formulates audit plan, scopes repository structure & data schemas                               │
│   [02 REPO INVESTIGATOR]   ──> Bounded AST parser maps financial routines (calculate_pnl, calculate_return)                    │
│   [03 FINANCIAL INVEST.]   ──> Ingests performance reports, normalizes claims into typed FinancialClaim targets                │
│   [04 CONTRADICTION INV.]  ──> Dispatches deterministic tools (FIFO lot matcher, fee recalculators, DuckDB analytics)         │
│   [05 REPORT AGENT]        ──> Synthesizes executive verdict, capital-at-risk deltas, and cryptographically sealed graphs      │
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

## 🤖 3. 5-Agent ADK Specification

| Agent Name | ADK Primitive | Primary Tool / Responsibility |
| :--- | :--- | :--- |
| **01 Audit Planner** | `google.adk.agents.Agent` | Scopes audit parameters, validates file existence, formulates staged plan. |
| **02 Repository Investigator** | `google.adk.agents.Agent` | `scan_repository_ast` tool: maps financial methods and keywords without sending bulk code to LLM. |
| **03 Financial Investigator** | `google.adk.agents.Agent` | `load_normalized_trades` tool: extracts reported metrics and config assumptions into canonical targets. |
| **04 Contradiction Investigator** | `google.adk.agents.Agent` | `execute_trade_reconciliation` & `analyze_duckdb_dataset`: reconstructs FIFO PnL, audits fee rates, constructs Evidence Contracts. |
| **05 Report Agent** | `google.adk.agents.Agent` | Compiles verified findings, computes capital discrepancy, generates markdown report & SVG evidence graphs. |

---

## 🧪 4. Benchmarks & Validation Suite

AuditVector comes equipped with three comprehensive verification benchmarks:

1. **IntegrityLab Alpha (Failure Benchmark):**
   * Synthetic multi-strategy backtester containing 4 planted calculation flaws:
     1. `F-001` (CRITICAL): PnL sign inversion ($+$18,240.00 reported vs $-$3,720.00 reconstructed).
     2. `F-002` (CRITICAL): Return polarity contradiction ($+$18.24% reported on net losing portfolio).
     3. `F-003` (HIGH): Fee double-counting in portfolio equity ($440.00 deducted vs $220.00 actual).
     4. `F-004` (MEDIUM): Configuration fee policy mismatch (5.0 bps claimed vs 13.2 bps effective).
   * **Total Capital at Risk:** **$44,140.00**

2. **IntegrityLab Control (Clean Baseline):**
   * Mathematically sound quantitative strategy verifying **zero false positives** and zero hallucinations.
   * **Result:** **100% Verified Sound**, **$0.00** discrepancy.

3. **AI-BIP Quantitative Engine (Real-World Dogfood):**
   * Multi-asset momentum strategy across BTC, ETH, SOL, AVAX.
   * **Surfaces Real Flaw:** $16,286.24 unaccounted execution slippage drag between backtest report ($54,200.00) and fill reality ($37,913.76).

---

## 🚀 5. Spin-up Instructions (Reproducibility Guide)

### Prerequisites
* Python 3.10+ (tested on Python 3.10, 3.11, 3.12, 3.14)
* Google Cloud SDK (`gcloud`) optional for Cloud Run deployment

### Option A: Local Quickstart (Zero Configuration)

```bash
# 1. Clone repository
git clone https://github.com/Param344/AuditVector.git
cd AuditVector

# 2. Set up virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. (Optional) Configure Gemini API key for live Gemini 3.5 Flash mode
export GEMINI_API_KEY="your-gemini-api-key"
export GEMINI_MODEL="gemini-3.5-flash"

# 4. Launch FastAPI Web Console & Backend
uvicorn backend.api.server:app --host 0.0.0.0 --port 8000 --reload
```
*Open **[http://localhost:8000](http://localhost:8000)** in your browser.*

### Option B: CLI Audit Execution

```bash
# Run Alpha failure benchmark
./run_audit.sh --demo alpha

# Run Control clean baseline
./run_audit.sh --demo control

# Run Custom repository audit
./run_audit.sh --repo integritylab/source --data integritylab/data/trades_alpha_failure.csv --report integritylab/reports/alpha_performance_report.json
```

### Option C: Docker & Docker Compose

```bash
# Build and launch with Docker Compose
docker-compose up --build
```
*Console is accessible at [http://localhost:8000](http://localhost:8000).*

### Option D: Google Cloud Run Deployment

```bash
# Deploy directly to Google Cloud Run
GCP_PROJECT_ID="your-project-id" ./deploy_cloudrun.sh
```

---

## 🔬 6. Reproducible Testing & Verification Guide

AuditVector is engineered for **100% hermetic reproducibility**. Judges and auditors can verify the entire test suite, benchmark suite, and forensic calculations in under 2 seconds without requiring external API keys or cloud credentials (defaults to `OFFLINE_DETERMINISTIC` mode).

---

### ⚡ Method 1: Single-Command Master Verification (Recommended)

Run the master verification script, which executes all 55 automated tests followed by autonomous audits across all three benchmarks:

```bash
# Execute master test & benchmark verification suite
./verify_all.sh
```

**Expected Console Output:**
```text
============================================================
 🛡️ AUDITVECTOR — MASTER VERIFICATION & FORENSIC AUDIT SUITE
 Track: Taskmaster | Google ADK 2.7 + Gemini 3.5+ + DuckDB
 Tagline: AI reasons. Code proves. Evidence explains.
============================================================

[1/4] Running Complete 55-Test Verification Suite...
Ran 55 tests in 1.680s — OK

[2/4] Executing Autonomous Audit on IntegrityLab Alpha...
Verdict: ⚠️ RESULTS NOT FULLY TRUSTWORTHY
Total Capital Discrepancy: $44,140.00 (4 Contradictions Confirmed)

[3/4] Executing Autonomous Audit on IntegrityLab Control...
Verdict: ✅ FINANCIAL INTEGRITY VERIFIED
Total Capital Discrepancy: $0.00 (100% Sound, 0 False Positives)

[4/4] Executing Autonomous Audit on Real-World AI-BIP Dogfood...
Verdict: ⚠️ RESULTS NOT FULLY TRUSTWORTHY
Total Capital Discrepancy: $16,286.24 (Slippage Drag Identified)

============================================================
 ✅ ALL AUDITVECTOR SUBSYSTEMS 100% OPERATIONAL & VERIFIED
============================================================
```

---

### 🧪 Method 2: Comprehensive 55-Test Automated Suite

Run the full automated test suite covering ADK agents, deterministic math verifiers, FastAPI endpoints, Cloud Run pubsub push workers, and secret redactors:

```bash
# Run all 55 unit and integration tests
.venv/bin/python -m unittest discover -s tests -p "test_*.py" -v
```

| Subsystem Tested | Test File | Test Count | Expected Status |
| :--- | :--- | :---: | :---: |
| **Official Google ADK 2.7 Agents** | `test_adk_runner.py` | 3 | `3/3 PASS` |
| **Deterministic Tool Wrappers** | `test_adk_tools.py` | 6 | `6/6 PASS` |
| **FIFO PnL Recalculator (Long/Short)** | `test_pnl_recalculator.py` | 6 | `6/6 PASS` |
| **Return Polarity Inversion Detector** | `test_return_calculator.py` | 2 | `2/2 PASS` |
| **Fee Double-Count Recalculator** | `test_fee_recalculator.py` | 1 | `1/1 PASS` |
| **Comparison & Tolerance Engine** | `test_comparison.py` | 5 | `5/5 PASS` |
| **DuckDB In-Memory SQL Engine** | `test_duckdb_engine.py` | 1 | `1/1 PASS` |
| **Evidence Contract Gatekeeper** | `test_evidence_contract.py` | 2 | `2/2 PASS` |
| **Secret Redaction (Private Keys/API)** | `test_secret_redactor.py` | 3 | `3/3 PASS` |
| **IntegrityLab Benchmarks (Alpha & Control)** | `test_integritylab_audit.py` | 2 | `2/2 PASS` |
| **AI-BIP Real Quantitative Dogfood** | `test_aibip_dogfood.py` | 2 | `2/2 PASS` |
| **FastAPI REST Endpoints & 404/422** | `test_audit_api.py` | 7 | `7/7 PASS` |
| **Cloud Run & Pub/Sub Push Webhook** | `test_cloud_runtime.py` | 5 | `5/5 PASS` |
| **Static UI Serving (`/`, CSS, JS)** | `test_frontend_serving.py` | 3 | `3/3 PASS` |
| **Ingestion Normalizer & Aliasing** | `test_normalizer.py` | 3 | `3/3 PASS` |
| **AST Repository Keyword Mapper** | `test_repository_investigator.py` | 1 | `1/1 PASS` |
| **Financial Claim Target Extractor** | `test_financial_investigator.py` | 1 | `1/1 PASS` |
| **Settings & Gemini 3.5 Config** | `test_settings_config.py` | 2 | `2/2 PASS` |
| **TOTAL** | **17 Test Modules** | **55** | **`55/55 PASS` (100%)** |

---

### 💻 Method 3: Direct CLI Benchmark Execution

Execute each benchmark scenario individually from the command line:

```bash
# 1. Audit IntegrityLab Alpha (Confirms 4 planted flaws: PnL inversion, polarity, fees)
./run_audit.sh --demo alpha

# 2. Audit IntegrityLab Control (Proves clean baseline: $0.00 discrepancy, 0 hallucinations)
./run_audit.sh --demo control

# 3. Audit Real-World AI-BIP Quantitative Strategy (Uncovers $16,286.24 slippage drag)
./run_audit.sh --demo aibip

# 4. Audit Any Custom Repository & Dataset
./run_audit.sh --repo integritylab/source \
               --data integritylab/data/trades_alpha_failure.csv \
               --report integritylab/reports/alpha_performance_report.json \
               --fee-bps 5.0
```

---

### 🌐 Method 4: Interactive Web UI Verification

1. Start the local server:
   ```bash
   uvicorn backend.api.server:app --host 0.0.0.0 --port 8000
   ```
2. Open **[http://localhost:8000](http://localhost:8000)** in your browser.
3. Click **"START AUDIT"** on **IntegrityLab Alpha**.
   * *Verify:* Active 5-agent ADK stepper transitions from `AuditPlanner` $\to$ `ReportAgent`.
   * *Verify:* Real-time streaming telemetry event log updates.
   * *Verify:* Final Verdict shows **$44,140.00** discrepancy with side-by-side **Claim vs. Reality** comparison (`+$18,240.00` claimed vs `-$3,720.00` reconstructed).
   * *Verify:* Click **"Inspect Evidence Contract"** on finding `F-001` to view source code line citations and SHA-256 hashes.
   * *Verify:* Switch to **"Interactive Evidence Graph"** tab to view node-and-edge provenance chains.
4. Click **"+ New Audit"** and run **IntegrityLab Control**.
   * *Verify:* Screen switches to emerald green **FINANCIAL INTEGRITY VERIFIED** with **$0.00 discrepancy**.

---

## 🔒 7. Hackathon Compliance Matrix

| Requirement | Implementation in AuditVector | Verification |
| :--- | :--- | :--- |
| **Model Eligibility** | Gemini 3.5 Flash (`gemini-3.5-flash`) | Configurable via `backend/config/settings.py` |
| **Google Agent Framework** | Google ADK 2.7 (`google.adk.agents.Agent`, `google.adk.models.Gemini`) | 5 official ADK Agents in `backend/adk/` |
| **Google Cloud Infrastructure** | Google Cloud Run, Cloud Pub/Sub, Cloud Firestore | `backend/cloud/` & `deploy_cloudrun.sh` |
| **Track Alignment** | **The Taskmaster** (Asynchronous, heavy-lifting forensic workflow) | Full automated AST, DuckDB & Evidence Graph |
| **Deterministic Safety** | Python FIFO lot matching + DuckDB Tabular SQL | 0 LLM arithmetic hallucinations |
| **Cryptographic Provenance** | Evidence Contracts with SHA-256 hashes & source citations | Sealed Evidence Graphs & Exportable Bundles |

---

## 📄 8. License

Distributed under the Apache 2.0 License.