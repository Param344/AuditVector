# Devpost Submission — AUDITVECTOR 🛡️

**Tagline:** Autonomous Financial Integrity Investigator: AI reasons. Code proves. Evidence explains.  
**Track:** Taskmaster  
**Hackathon:** All Things Agentic Hackathon  

---

## 💡 Inspiration

In quantitative trading and algorithmic finance, software errors rarely trigger noisy crashes. Instead, they produce **silent financial integrity decay**:
* An inverted subtraction sign `(start_capital - end_capital)` disguises catastrophic drawdowns as profitable quarters.
* Commission rates are subtracted at execution and mistakenly subtracted a second time during portfolio rollups.
* Backtesting configurations claim a 5 bps fee tier while production engines execute at 13+ bps.

When financial engineers try using generative AI to audit quantitative code, they run into a fatal wall: **LLMs hallucinate arithmetic.** Asking a standard LLM whether a trading strategy's PnL is correct across 50,000 order fills yields fabricated numbers and false confidence.

We built **AuditVector** to solve this integrity gap. AuditVector is an autonomous multi-agent financial investigator that operates on one core principle:
$$\mathbf{AI\ reasons.\ Code\ proves.\ Evidence\ explains.}$$

---

## 🚀 What It Does

AuditVector takes a financial strategy repository, execution logs, and trade data, and autonomously:
1. **Maps Financial Pathways**: Uses bounded AST parsing to trace where PnL, inventory, fees, and returns are computed.
2. **Extracts Reported Claims**: Identifies self-reported backtest and live metrics (Net PnL, Return %, Fees, Win Rate).
3. **Executes Deterministic Re-computations**: Independently reconstructs PnL from raw trade events using a bottom-up Python FIFO lot matcher and DuckDB analytical query engine.
4. **Detects Contradictions & Quantifies Capital-at-Risk**: Identifies sign inversions, fee double-counting, and rate mismatches, assigning official statuses (`VERIFIED`, `CONTRADICTION`, `WARNING`, `UNVERIFIABLE`).
5. **Generates Cryptographic Evidence Graphs**: Enforces strict **Evidence Contracts** (`No Evidence Contract → No Verified Finding`), linking every claim back to exact code lines, transaction hashes, normalizer versions, and verifier algorithms.
6. **Produces Executive Audit Reports**: Delivers a human-verifiable report with dollar discrepancies, severity breakdowns, and actionable remediation steps.

---

## 🏗️ How We Built It

AuditVector's architecture is organized into three distinct layers:

### 1. Agentic Reasoning Layer
* Built with official **Google ADK 2.7** (`google.adk.agents.Agent`) and **Gemini 3.5 Flash**.
* Specialized 5-Agent Pipeline:
  * **Audit Planner**: Scopes directories and plans investigation targets.
  * **Repository Investigator**: Bounded AST parser identifying financial calculation functions without leaking entire codebases to the LLM.
  * **Financial Investigator**: Extracts reported claims into typed verification targets.
  * **Contradiction Investigator**: Invokes deterministic tools and formulates Evidence Contracts.
  * **Report Agent**: Synthesizes verified findings into executive reports.

### 2. Deterministic Verification Engine
* **Python FIFO Lot Matcher**: Dual-direction lot reconstruction for Longs, Shorts, Partial Fills, and Multi-Asset Portfolios.
* **DuckDB SQL Engine**: In-memory tabular analytical queries for fast trade profiling and symbol distribution.
* **Secret Redactor**: Automatically sanitizes API keys, Binance credentials, AWS keys, and private keys before LLM exposure.

### 3. Asynchronous Cloud Runtime & Persistent State
* **Google Cloud Run**: Containerized FastAPI REST API and static dashboard server.
* **Google Cloud Pub/Sub**: Asynchronous job dispatcher with strict idempotency guards against duplicate message delivery.
* **Google Cloud Firestore**: Persistent state management tracking the audit lifecycle (`QUEUED → RUNNING → INVESTIGATING → VERIFYING → REPORTING → COMPLETED`).

---

## 🔬 Testing & Validation

* **IntegrityLab Synthetic Benchmark**: A controlled financial testbed with 4 planted integrity bugs + 1 clean control case (confirming 0 false positive fabrications).
* **AI-BIP Real-World Dogfooding**: Audited our live multi-asset quant engine across BTC, ETH, SOL, and AVAX, discovering a $16,286 calculation discrepancy from unmodeled execution slippage.
* **Test Suite**: **55 comprehensive unit, integration, and API test suites** passing with 100% success.

---

## 🏆 Accomplishments that We're Proud Of

1. **Zero Arithmetic Hallucinations**: Financial numbers are never accepted from LLM reasoning; every numerical verdict is grounded by deterministic code execution.
2. **True Google ADK & Gemini 3.5 Implementation**: Built using official Google ADK agents and tools with full offline hermetic test mode support.
3. **Real Cloud Asynchronous Runtime**: Scalable Pub/Sub and Firestore state machine handling long-running audits without timing out HTTP connections.
4. **Interactive Provenance Evidence Graph**: Visual node-and-edge chains enabling risk managers to verify the math from source code to trade fill.

---

## 📦 Tech Stack

* **AI & Agent Framework**: Google ADK 2.7, Gemini 3.5 Flash, Google GenAI SDK
* **Verification & Math**: Python 3.12/3.14, DuckDB SQL Engine, Decimal FIFO Matcher
* **Cloud Infrastructure**: Google Cloud Run, Google Cloud Pub/Sub, Google Cloud Firestore
* **Backend API**: FastAPI, Pydantic, Uvicorn
* **Frontend**: HTML5, CSS3 Cyber-Terminal Theme, Vanilla ES6 JavaScript
