# 🛡️ AuditVector — Devpost Submission Story

> **Tagline:** Autonomous financial integrity agent that investigates trading systems, proves hidden calculation errors deterministically, and delivers cryptographic evidence without letting AI fabricate the numbers.  
> **Track:** The Taskmaster — All Things Agentic Hackathon  
> **Live Interactive Demo:** [https://auditvector-20610.web.app](https://auditvector-20610.web.app)  
> **GitHub Repository:** [https://github.com/Param344/AuditVector.git](https://github.com/Param344/AuditVector.git)

---

## Inspiration

I built AuditVector from a simple concern:

**Financial software can be wrong while still looking completely correct.**

When working with quantitative systems, I saw how easily a small mathematical or logic error can become a large financial mistake — a reversed sign, fees being counted twice, a mismatch between configuration and execution, or a backtest reporting results that the underlying trades cannot actually support.

What bothered me most was that AI could explain financial data very well, but an explanation is not proof.

That led to the idea behind AuditVector:

> **What if an AI agent could investigate a financial system autonomously, but every important numerical conclusion had to be proven by deterministic code?**

That became our core principle:

**AI reasons. Code proves. Evidence explains.**

---

## What it does

AuditVector is an **autonomous financial integrity investigation and remediation agent** designed to find and safely remediate hidden mathematical and logic failures in quantitative trading and financial software.

It investigates a repository together with its financial reports, configuration, source code, and raw transaction data.

The agent can:

* **Map financial logic** inside source code using AST analysis
* **Extract reported PnL, returns, fees**, and configuration claims
* **Reconstruct financial results independently** from raw trade fills
* **Perform deterministic FIFO lot reconciliation** and DuckDB SQL tabular profiling
* **Detect PnL and return polarity reversals**, fee double-counting, and configuration drift
* **Compute a Financial Integrity Score (FIS)** from 0–100 with grades A+ to F
* **Formulate surgical unified-diff remediation patches**
* **Execute isolated sandbox re-verification** to prove candidate patches reduce discrepancy to $0.00 before touching the real repository
* **Enforce a strict human-in-the-loop safety boundary** before applying patches
* **Enable interactive "WHY?" evidence provenance traversal** from a finding to its underlying transaction and source evidence
* **Create sealed cryptographic evidence contracts** and provenance graphs
* **Support step-by-step Audit Replay** with an adaptive ADK decision log
* **Produce an executive forensic report** ready for risk and compliance review

The key architectural invariant is:

**The LLM never calculates the financial numbers.**

AI investigates, hypothesizes, and scopes pathways. Deterministic verifiers and isolated execution sandboxes perform the actual mathematics and regression verification.

This creates a closed-loop workflow:

$$\text{Investigate} \longrightarrow \text{Prove} \longrightarrow \text{Explain} \longrightarrow \text{Remediate} \longrightarrow \text{Sandbox-Verify} \longrightarrow \text{Human Approval}$$

---

## How we built it

AuditVector is built around **Google ADK (Agent Development Kit)** and **Gemini 3.5 Flash**, with an evidence-driven adaptive orchestration loop.

The investigation flows through six specialized agents:

**Audit Planner → Repository Investigator → Financial Investigator → Contradiction Investigator → Remediation Agent → Report Agent**

Underneath the agents is a deterministic verification layer built in Python and DuckDB:

* **Canonical Normalization:** Ingests raw trades into a strictly typed `FinancialEvent` model.
* **Deterministic FIFO Recalculator:** Independently reconstructs multi-symbol positions, realized PnL, fees, and cash flows from canonical trade fills.
* **Evidence-Driven Adaptive Loop:** After each investigation step, an ADK decision component evaluates the available evidence and dynamically routes to the appropriate investigation, tool, or verifier.
* **Isolated Remediation Sandbox:** Generates minimal unified diffs and executes semantic regression checks in a safe temporary environment before any real repository modification.
* **Cryptographic Provenance:** Seals each finding with SHA-256 dataset hashes, AST source citations, and verifier engine metadata.

We evaluated AuditVector across three complementary benchmarks:

1. **IntegrityLab Alpha:** A flawed quantitative repository containing four planted financial contradictions. AuditVector detected all four and quantified **$44,276.75 of capital at risk**.
2. **IntegrityLab Control:** A mathematically sound baseline used to prove 0 false positives. AuditVector produced 0 findings, $0 discrepancy, and a **100/100 FIS (Grade A+)**.
3. **AI-BIP Quantitative Engine:** Real-world production dogfooding independently proving a **$16,286.24 discrepancy**, representing **30.0484% erosion of reported $54,200.00 profit**, against canonical trade fills.

The final codebase contains **63/63 automated tests passing**.

AuditVector is deployed as a zero-cost public interactive demonstration on Google Firebase Hosting:  
[https://auditvector-20610.web.app](https://auditvector-20610.web.app)

---

## Challenges we ran into

The hardest challenge was not getting an LLM to explain financial problems — it was making the explanation provable and safe.

### 1. The Proof Boundary
If an LLM says *"the PnL looks suspicious,"* that cannot be sufficient for a financial audit. We created **Evidence Contracts** requiring deterministic verifier metadata, source-level citations, canonical transaction evidence, and SHA-256 data hashes for important claims.

### 2. Safe Autonomous Remediation
We wanted the agent to fix bugs without risking silent code corruption. We engineered an **Isolated Sandbox Verifier** that tests candidate patches against regression suites and deterministic financial reconcilers. The patch must pass verification and demonstrate that the financial discrepancy is reduced to $0.00 before it can be considered verified. The real repository remains protected by an explicit human authorization gate.

### 3. Zero False Positives
An auditing system that flags healthy code is useless. We designed the IntegrityLab Control benchmark and adaptive decision loop so the agent can recognize when the evidence is clean and autonomously bypass remediation:

$$\text{0 findings} \longrightarrow \text{\$0 discrepancy} \longrightarrow \text{0 remediation actions} \longrightarrow \text{100/100 FIS}$$

### 4. Exposing Agent Autonomy
Rather than hiding agent behavior behind a final report, our UI exposes the six-agent pipeline, adaptive decisions, telemetry, interactive "WHY?" traversal, remediation verification, and full Audit Replay.

---

## Accomplishments that we're proud of

* **4/4 financial contradictions detected and verified** in IntegrityLab Alpha
* **$44,276.75 capital at risk** independently quantified in Alpha
* **0 false positives** on the clean Control benchmark
* **100/100 FIS — Grade A+** on Control
* **4/4 remediation patches sandbox-verified**
* **Alpha remediation reduced the verified discrepancy to $0.00**
* **$16,286.24 discrepancy** independently proven on the real-world AI-BIP dogfood audit
* **AI-BIP discrepancy represents 30.0484% erosion of reported $54,200.00 profit**
* **63/63 automated tests passing**
* **Evidence-driven adaptive ADK orchestration** that dynamically re-routes based on emerging evidence
* **Interactive "WHY?" Evidence Traversal** connecting findings to verified transaction and source evidence
* **Deterministic mathematical verification** independent of LLM arithmetic
* **Human authorization gate** protecting real repository modifications
* **Live zero-cost deployment** on Google Firebase Hosting

---

## What we learned

### 1. Autonomy requires deterministic guardrails
A high-stakes AI agent should have autonomy over what to investigate and what evidence to pursue, while critical mathematical conclusions and code modifications remain constrained by deterministic verifiers and sandbox safety boundaries.

### 2. Evidence is part of the product
A financial finding is only as useful as the evidence supporting it. AuditVector therefore treats provenance as a first-class product feature:

$$\text{Source Code} \longrightarrow \text{Transaction Data} \longrightarrow \text{Deterministic Verifier} \longrightarrow \text{Evidence Contract} \longrightarrow \text{Remediation Sandbox} \longrightarrow \text{Verdict}$$

### 3. Remediation is harder than detection
Finding a bug is only half the problem. A trustworthy agent must demonstrate that its proposed fix actually resolves the underlying problem without introducing another one. The isolated remediation sandbox turns an AI-generated suggestion into a testable, independently verified change.

### 4. Trust requires provable benchmarks
Having both failure and clean control benchmarks was essential. The Alpha benchmark proves that AuditVector can aggressively discover real contradictions. The Control benchmark proves that it can also avoid inventing problems when the system is correct.

---

**AuditVector — AI reasons. Code proves. Evidence explains.**
