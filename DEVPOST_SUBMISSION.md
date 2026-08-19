# 🛡️ AUDITVECTOR — DEVPOST SUBMISSION FORM CONTENT

Use the sections below to fill out the official submission form on [Devpost](https://allthingsagentichackathon.devpost.com/).

---

### 📌 1. Basic Information
* **Project Name:** AuditVector
* **Tagline:** Autonomous Financial Integrity Investigator & Evidence-Grounded Audit Engine
* **Track:** The Taskmaster
* **GitHub Repository:** `https://github.com/Param344/AuditVector`
* **Hosted URL:** `http://localhost:8000` (or your Cloud Run `.run.app` URL)

---

### 💡 2. Inspiration
In quantitative finance and algorithmic trading, millions of dollars are lost not because strategies were inherently unprofitable, but because the software calculating their performance contained silent integrity flaws:
* A sign inversion in a PnL routine disguises a 3.7% loss as an 18.2% profit.
* Commissions subtracted at trade execution are deducted a second time during portfolio aggregation.
* Slippage and execution fees configured in policies diverge materially from real-world exchange fills.

Traditional code reviews miss these issues because they hide across hundreds of thousands of transaction logs. Standard generative AI chatbots hallucinate arithmetic when given large tabular financial records. We built **AuditVector** on a simple principle:
$$\textbf{"AI reasons. Code proves. Evidence explains."}$$

---

### ⚙️ 3. What It Does
AuditVector is an autonomous, multi-agent financial integrity investigator powered by **Google ADK** and **Gemini 3.5 Flash**. Given a quantitative codebase, raw trade execution logs (CSV), and reported performance summaries (JSON):

1. **Autonomous Investigation:** 5 specialized Google ADK agents orchestrate the audit workflow—formulating plans, parsing AST call paths, and extracting reported metrics.
2. **Zero-Hallucination Deterministic Truth:** Instead of relying on LLM math, AuditVector invokes a bottom-up FIFO Lot Matching engine and DuckDB SQL analytics to reconstruct ground-truth PnL, fees, and returns directly from transaction fills.
3. **Cryptographic Evidence Contracts:** Enforces a strict mandate: *No Evidence Contract $\to$ No Verified Finding*. Every finding links directly to source code citations (`file:line_range`), source code SHA-256 hashes, normalizer versions, and verifier algorithms.
4. **Interactive Provenance Graphs:** Visualizes the complete cryptographic chain of custody from raw CSV $\to$ Canonical Normalizer $\to$ Verifier Engine $\to$ Sealed Finding.
5. **Executive Synthesis:** Generates human-readable Executive Markdown reports, exportable JSON Evidence Bundles, and side-by-side Claim vs. Reality calculations.

---

### 🏗️ 4. How We Built It

* **Agentic Orchestration:** Built with **Google ADK 2.7** and **Gemini 3.5 Flash** using official `google.adk.agents.Agent`, `google.adk.models.Gemini`, and `google.adk.tools.FunctionTool` primitives across 5 dedicated agents:
  1. `AuditPlanner` (Planning & Scoping)
  2. `RepositoryInvestigator` (Bounded AST mapping)
  3. `FinancialInvestigator` (Claim extraction & normalization)
  4. `ContradictionInvestigator` (Deterministic tool execution & Evidence Contract construction)
  5. `ReportAgent` (Executive synthesis & graph generation)
* **Deterministic Verification Engine:** Python FIFO Lot Matcher + DuckDB Tabular Analytics for ultra-fast, 100% deterministic reconstruction.
* **Google Cloud Asynchronous Runtime:**
  * **Google Cloud Run:** Hosts the async FastAPI REST backend and command center UI.
  * **Google Cloud Pub/Sub:** Asynchronous event broker decoupling audit job dispatch from execution workers.
  * **Google Cloud Firestore:** Persistent, distributed state store tracking audit stages and findings across sessions with idempotency guards.
* **Forensic Command Console:** Bloomberg/Palantir-inspired dark UI with live 5-agent telemetry streams, dynamic Claim vs. Reality calculation comparators, interactive SVG provenance chains, and slide-out Evidence Contract drawers.

---

### 🥊 5. Challenges We Ran Into & Solutions

1. **Eliminating LLM Arithmetic Hallucinations:**
   * *Problem:* Large Language Models inherently struggle with multi-thousand-row floating-point arithmetic.
   * *Solution:* We strictly separated reasoning from proof. Gemini 3.5 reasons about repository pathways, while deterministic tools (DuckDB & FIFO matcher) prove the numbers.
2. **Preventing Code Context Window Explosion:**
   * *Problem:* Pushing whole quant codebases into prompt context clutters reasoning and incurs high token latency.
   * *Solution:* Built a bounded Python AST scanner that maps financial routines and extracts only relevant method boundaries.
3. **Asynchronous Distributed Idempotency:**
   * *Problem:* In high-throughput cloud environments, Pub/Sub may deliver duplicate messages.
   * *Solution:* Implemented stage-based idempotency checks in `PubSubAuditWorker`, preventing re-execution of running or completed audits.

---

### 🏆 6. Accomplishments That We're Proud Of

* **100% Deterministic Precision:** Verified on our synthetic `IntegrityLab Alpha` benchmark (caught all 4 planted flaws) and `IntegrityLab Control` (0 false positives, 0 hallucinations).
* **Real-World Dogfood Validation:** Audited the real-world `AI-BIP` multi-asset quantitative system and successfully surfaced an unmodeled **$16,286.24** execution slippage drag between backtest claims and fill reality.
* **Rigorous Test Coverage:** 55 comprehensive automated tests passing in 1.2s covering all unit, integration, ADK, API, and cloud runtime pathways.

---

### 📚 7. What We Learned

* Combining LLM cognitive planning with deterministic formal verification creates enterprise-grade trust that neither approach can achieve in isolation.
* Google ADK's modular agent abstractions provide a clean, production-ready framework for multi-agent asynchronous pipelines on Google Cloud.

---

### 🔮 8. What's Next for AuditVector

* **Live Brokerage & Exchange Connectors:** Direct read-only API connectors to Binance, Coinbase, Interactive Brokers, and Alpaca for continuous real-time execution audits.
* **Regulatory Compliance Rulesets:** Pre-packaged rulepacks for SEC 15c3-5 risk controls, MiFID II algorithmic trade reporting, and SOX financial audit readiness.
* **Smart Contract EVM Support:** Extending AST scanners to Solidity bytecode to audit DeFi AMM liquidity invariant calculations.
