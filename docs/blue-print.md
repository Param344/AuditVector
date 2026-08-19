Autonomous Financial Integrity Agent
Tagline

AI reasons. Code proves. Evidence explains.

One-line product definition

AUDITVECTOR is an asynchronous AI agent that investigates financial and quantitative software, independently verifies its financial calculations against underlying evidence, detects contradictions and integrity failures, and produces an evidence-backed audit report.

This is a new standalone project for the All Things Agentic Hackathon. It is not CSE and it is not Agentic Studio.

1. THE PROBLEM

Financial and algorithmic trading systems can report:

PnL
returns
win rate
Sharpe ratio
drawdown
fees
exposure
performance

But the difficult question is:

Can we actually trust those numbers?

A system can be wrong without crashing.

For example:

Trading engine
     ↓
Trade executed correctly
     ↓
PnL calculation contains bug
     ↓
Performance report looks normal
     ↓
Dashboard shows +18%
     ↓
Actual performance = -3%

Traditional testing often doesn't catch this because:

the code runs
APIs respond
tests pass
numbers look plausible

AUDITVECTOR investigates the integrity of the entire financial evidence chain.

2. THE CORE IDEA

The user gives AUDITVECTOR:

┌──────────────────────────────┐
│ Financial / Quant System     │
├──────────────────────────────┤
│                              │
│ Source Code                  │
│ Trading Logs                 │
│ Trade History                │
│ Performance Reports          │
│ Configuration                │
│ Historical Data              │
│                              │
└──────────────────────────────┘

Then says:

"Audit this system and determine whether I can trust its financial results."

That's it.

The user does not tell the system:

"Find the PnL bug."

The agent decides what needs investigation.

3. WHAT MAKES AUDITVECTOR AGENTIC

AUDITVECTOR is not:

Upload → Chat → Answer.

It is:

USER
  │
  │ "Audit this system"
  ▼
START AUDIT
  │
  ▼
CREATE ASYNC JOB
  │
  ▼
USER CAN LEAVE
  │
  │
  │     ┌───────────────────────┐
  │     │ Agent works in        │
  │     │ background             │
  │     │                       │
  │     │ plans                 │
  │     │ investigates          │
  │     │ calculates            │
  │     │ compares              │
  │     │ verifies              │
  │     │ prioritizes           │
  │     │ reports               │
  │     └───────────────────────┘
  │
  ▼
USER RETURNS
  │
  ▼
AUDIT COMPLETE

This directly targets the hackathon's emphasis on background/asynchronous agents and complex workflows.

4. FINAL SYSTEM ARCHITECTURE
                         ┌─────────────────────┐
                         │        USER         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    AUDITVECTOR WEB     │
                         │      DASHBOARD      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      CLOUD RUN      │
                         │        API          │
                         └──────────┬──────────┘
                                    │
                            Create Audit Job
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       PUB/SUB       │
                         │    JOB DISPATCH     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    AUDIT WORKER     │
                         │      CLOUD RUN      │
                         │                     │
                         │      GOOGLE ADK     │
                         └──────────┬──────────┘
                                    │
                           ADK orchestration
                                    │
          ┌─────────────────────────┼────────────────────────┐
          │                         │                        │
          ▼                         ▼                        ▼
 ┌────────────────┐       ┌────────────────┐       ┌────────────────┐
 │ AUDIT PLANNER  │       │   REPOSITORY   │       │   FINANCIAL    │
 │     AGENT      │       │  INVESTIGATOR  │       │  INVESTIGATOR  │
 └───────┬────────┘       └───────┬────────┘       └───────┬────────┘
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  ▼
                       ┌──────────────────────┐
                       │   CONTRADICTION      │
                       │   INVESTIGATOR       │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │ DETERMINISTIC       │
                       │ VERIFICATION ENGINE │
                       │                      │
                       │ Python / DuckDB      │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │    RISK             │
                       │    PRIORITIZER       │
                       └──────────┬───────────┘
                                  │
                                  ▼
                       ┌──────────────────────┐
                       │    REPORT AGENT      │
                       │      GEMINI          │
                       └──────────┬───────────┘
                                  │
              ┌───────────────────┼──────────────────┐
              ▼                   ▼                  ▼
       ┌─────────────┐     ┌─────────────┐    ┌─────────────┐
       │  FIRESTORE  │     │CLOUD STORAGE│    │   EVIDENCE  │
       │             │     │             │    │    GRAPH    │
       └─────────────┘     └─────────────┘    └─────────────┘
              │
              ▼
       ┌────────────────────────────────┐
       │       LIVE DASHBOARD           │
       │                                │
       │ Progress / Findings / Evidence │
       └────────────────────────────────┘
5. GOOGLE TECHNOLOGY STACK

Google technology isn't being added just to satisfy the rules.

It is fundamental to the architecture.

AI

Gemini 3.5 Flash

Used for:

investigation planning
code reasoning
semantic analysis
hypothesis generation
contradiction investigation
report generation
Agent framework

Google ADK

Responsible for:

agent orchestration
sessions
tool calls
multi-agent workflow
state management
Cloud Run

Runs:

API
audit workers
ADK runtime
Pub/Sub

Used only for asynchronous audit job dispatch.

Not for communication between every agent.

Firestore

Stores:

projects
audits
audit state
agent progress
findings
evidence references
verification results
Cloud Storage

Stores:

repositories
uploaded datasets
logs
reports
audit artifacts
6. WHY PUB/SUB IS ONLY AT THE JOB BOUNDARY

This is an important simplification.

Don't build this:
Agent 1
 ↓ Pub/Sub
Agent 2
 ↓ Pub/Sub
Agent 3
 ↓ Pub/Sub
Agent 4

That creates unnecessary distributed-system complexity.

Instead:

API
 ↓
Pub/Sub
 ↓
Audit Worker
 ↓
ADK
 ↓
Agents

ADK manages the internal workflow.

Pub/Sub gives us the asynchronous background execution that the hackathon wants.

7. THE AGENT SYSTEM: TARGET ARCHITECTURE VS. MVP PIPELINE

AUDITVECTOR defines a specialized Google ADK multi-agent architecture. To ensure rapid, unblocked execution while maintaining technical depth, we explicitly distinguish the **Target 5-Agent Architecture** from the **MVP Milestone Pipeline**.

### Full Target Architecture (Five Agents)
```text
Audit Planner
      ↓
Repository Investigator
      ↓
Financial Investigator
      ↓
Contradiction Investigator
      ↓
Report Agent
```

### MVP Milestone Pipeline (Three Agents)
```text
Audit Planner
      ↓
Contradiction Investigator
      ↓
Report Agent
```

In the MVP milestone, the three agents directly invoke deterministic ingestion, normalization, repository-analysis heuristics, and verification tools. This preserves full investigative depth while keeping initial implementation lean and robust. The 5-agent pipeline represents the specialized target architecture.

---

### The Five Primary ADK Agents

Agent 1 — Audit Planner
Responsibility

Determine what should be investigated.

Input:

Repository
Logs
Reports
Data
Configuration
User objective

Output:

Audit Plan

Example:

AUDIT PLAN


1. Map financial calculation pathways
2. Locate PnL calculations
3. Locate return calculations
4. Reconstruct selected trades
5. Reconcile reported PnL
6. Inspect fee calculations
7. Compare configuration assumptions
8. Search semantic contradictions
9. Independently verify critical findings
10. Produce final report

The plan is dynamic.

8. AGENT 2 — REPOSITORY INVESTIGATOR

This agent determines:

Where does the financial logic live?

It analyzes:

Python
JavaScript/TypeScript
configuration
SQL
notebooks
reports
relevant documentation

It builds a:

Financial Calculation Map

Example:

strategy_v3_ai.py
        │
        ▼
signal generation
        │
        ▼
execution_engine.py
        │
        ├── position
        ├── entry
        └── exit
        │
        ▼
pnl_engine.py
        │
        ▼
performance.py
        │
        ▼
performance_report.csv

The map becomes structured evidence for later agents.

9. AGENT 3 — FINANCIAL INVESTIGATOR

This agent determines:

Which financial claims need to be tested?

Examples:

PnL
return
fees
win rate
drawdown
exposure
position size
trade profitability
performance aggregation

It calls deterministic tools.

For example:

Agent:


"I found a reported PnL calculation."


        ↓


Verification Tool


"Reconstruct PnL from trade events."


        ↓


Result
10. AGENT 4 — CONTRADICTION INVESTIGATOR

This is the signature agent.

It searches for contradictions between:

CODE
 │
 ├── LOGS
 │
 ├── TRADE DATA
 │
 ├── REPORTS
 │
 ├── CONFIGURATION
 │
 └── CALCULATIONS

Example:

SYSTEM REPORT


Return = +18.4%
       │
       │
       ▼
Independent reconstruction
       │
       ▼
Return = -3.7%


       ↓


🚨 CONTRADICTION

The agent then investigates:

Why?

It might discover:

Module A:
positive return = return > 0


Module B:
positive return = return < 0

That's a semantic integrity failure.

11. CANONICAL INGESTION & DETERMINISTIC VERIFICATION ENGINE

This is the most critical non-AI foundation of the system.

### Ingestion Adapters & Canonical Financial Event Model

Financial software codebases and data exports represent transactions in widely heterogeneous formats:
* Quantity fields: `qty`, `size`, `amount`, `volume`, `contracts`
* Fee fields: `fee`, `commission`, `trading_fee`, `cost`
* Timestamps: ISO strings, UNIX milliseconds, custom trade logs

To ensure robust mathematical verification, AUDITVECTOR implements a dedicated Ingestion and Normalization Layer:

```text
Raw CSV / JSON / Logs / Trade History
                ↓
       Ingestion Adapters
                ↓
      Canonical Financial Event
                ↓
      Deterministic Verification Engine
```

The canonical model (`FinancialEvent`) standardizes all transactional data:

```text
FinancialEvent
├── event_id: string
├── timestamp: string (ISO 8601 UTC)
├── symbol: string
├── side: "BUY" | "SELL"
├── quantity: float / Decimal
├── price: float / Decimal
├── fee: float / Decimal
├── fee_currency: string
├── position_id: optional[string]
├── trade_id: optional[string]
└── source: string (filename / log_ref)
```

### Deterministic Verification Engine

Gemini does not become the source of truth for mathematics. Once data is normalized, deterministic tools independently execute the calculations:

* PnL calculation and trade reconstruction
* Fee and commission recalculation (single vs. double deduction)
* Return calculation and polarity checking
* Position state reconstruction
* Trade reconciliation across logs, code, and reports
* Statistical distributions and analytical aggregations

```text
backend/
├── ingestion/
│   ├── repository.py
│   ├── csv.py
│   ├── logs.py
│   ├── reports.py
│   └── normalizer.py
│
├── models/
│   └── financial_event.py
│
└── verification/
    ├── pnl_recalculator.py
    ├── fee_recalculator.py
    ├── return_calculator.py
    ├── position_reconstructor.py
    ├── trade_reconciler.py
    ├── statistics.py
    └── comparison.py
```

For large tabular datasets, **DuckDB** executes deterministic analytical queries directly against normalized Parquet/Arrow/CSV buffers with microsecond performance.

12. THE CORE PRINCIPLE

**AI reasons. Code proves. Evidence explains.**

This is our strongest architectural foundation.

```text
                GEMINI / ADK
                      │
                      │  "Hypothesize possible discrepancy"
                      │
                      ▼
           DETERMINISTIC VERIFIER
                      │
                      │  Independently recalculates from canonical events
                      │
                      ▼
                    RESULT
                      │
                      ▼
                  COMPARISON
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
       MATCH                    MISMATCH
         │                         │
         ▼                         ▼
     VERIFIED                 CONTRADICTION
```

### Technical Accuracy of the Verification Principle

Financial claims are never accepted solely from LLM reasoning. Critical numerical claims are independently recomputed using deterministic verification tools and compared against the application's reported results.

Deterministic verification dramatically reduces LLM hallucination risk, but is not magically infallible. Verification correctness fundamentally depends on:
1. Canonical input data completeness
2. Ingestion adapter normalization fidelity
3. Explicit accounting and execution assumptions
4. Verifier implementation precision

We never label an issue "verified" merely because a second LLM agrees. Verification requires executable code and auditable data.

13. OFFICIAL FINDING CATEGORIES & VERIFICATION FLOW

AuditVector must never be forced to fabricate a definitive finding when underlying evidence is incomplete or inaccessible. Findings are strictly classified into four official categories:

1. **`VERIFIED`**
   Evidence and independent deterministic verification support the claim or calculation.
2. **`CONTRADICTION`**
   Independent evidence or deterministic reconstruction demonstrates that system claims conflict with underlying evidence or code logic.
3. **`WARNING`**
   Evidence indicates a suspicious or potentially material issue, but deterministic verification is incomplete or inconclusive.
4. **`UNVERIFIABLE`**
   There is insufficient source data, missing fields, inaccessible logic, or another limitation preventing independent verification.

### Core Trust & Safety Example: Missing Evidence

```text
PnL Integrity Check

Status: UNVERIFIABLE

Reason:
Exit-fee information and execution fills are missing from the supplied dataset.

AuditVector Rule:
AuditVector will not infer, guess, or hallucinate the missing values.
```

### Example Verification Flow for a Contradiction

Suppose the agent identifies: *"PnL calculation may be incorrect."*

1. Normalized trades are sent to `pnl_recalculator.py`.
2. System reported: `+$18,240`
3. Independent calculation: `-$3,720`
4. Variance: `$21,960`
5. Status: `CONTRADICTION` (Severity: CRITICAL, Confidence: 96%)

14. RISK PRIORITIZER

Findings are prioritized quantitatively based on:
`Severity + Financial Impact + Scope + Confidence + Status`

| Finding | Status | Severity | Confidence | Impact |
| :--- | :--- | :--- | :--- | :--- |
| Return polarity contradiction | 🔴 CONTRADICTION | Critical | 96% | Very High |
| PnL reconciliation failure | 🔴 CONTRADICTION | Critical | 94% | Very High |
| Fee double counting | 🟠 CONTRADICTION | High | 91% | High |
| Configuration mismatch | 🟡 WARNING | Medium | 88% | Medium |
| Exit fee verification | ⚪ UNVERIFIABLE | Info | N/A | Unknown |
| Logging consistency | 🟢 VERIFIED | Low | 97% | Low |

15. REPORT AGENT

Gemini turns verified evidence and deterministic outputs into a structured, human-readable audit report.

It does not invent findings. It ingests:
* Verified calculations and formulas
* Evidence contracts and provenance chains
* Source code locations
* Severity, status, and financial impact

And generates:
* Executive Summary
* Critical & High Findings
* Financial Impact Breakdown
* Root Causes & Code Citations
* Recommended Remediations
* Audit Limitations & Unverifiable Disclaimers

16. EVIDENCE GRAPH & EVIDENCE CONTRACT

The Evidence Graph provides full provenance from source to verdict.

```text
                     FINDING
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
    SOURCE CODE    RAW DATA / LOGS   REPORT
         │              │              │
      Function       Trades          Metric
         │              │              │
         │              ▼              │
         │        NORMALIZATION        │
         │       (Canonical Model)     │
         │              │              │
         └──────────────┼──────────────┘
                        ▼
                   CALCULATION
                        │
                        ▼
                  VERIFICATION
                        │
                        ▼
                      PROOF
```

### Architectural Rule: No Evidence Contract → No Verified Finding

Every finding labeled `VERIFIED` or `CONTRADICTION` must satisfy a strict **Evidence Contract**. Gemini may propose a hypothesis, but it cannot promote that hypothesis to a verified audit finding without fulfilling this contract.

```text
Finding (Evidence Contract)
├── Claim
├── Source Citations
├── Data Evidence
├── Normalization Provenance
├── Calculation Variance
├── Verification Status
├── Impact Assessment
├── Confidence Score
└── Provenance Metadata
```

17. EVIDENCE OBJECT & PROVENANCE SPECIFICATION

Every verified finding is structured as an immutable JSON evidence object:

```json
{
  "finding_id": "F-004",
  "title": "Return Polarity Contradiction",
  "status": "CONTRADICTION",
  "severity": "CRITICAL",
  "confidence": 0.96,
  "claim": "System reports +18.4% return on trade batch 17 while independent reconstruction shows negative return.",
  "sources": [
    {
      "file": "auto_trader_v2.py",
      "line_range": "180-195",
      "source_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    },
    {
      "file": "performance.py",
      "line_range": "88-104",
      "source_hash": "8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4"
    }
  ],
  "data_evidence": {
    "dataset_id": "trade_batch_17",
    "record_count": 14821,
    "source_path": "data/trades_2026_q1.csv",
    "source_hash": "c5d8868936e2f2e5bb5d2b1f81cf99f2b8a07c13280145c2637a3b378eb8816f"
  },
  "provenance": {
    "timestamp": "2026-08-19T08:24:00Z",
    "normalizer_version": "v1.2.0",
    "verifier_version": "pnl_recalculator_v2.1",
    "transformation": "canonical_financial_event_normalization"
  },
  "calculation": {
    "reported_pnl": 18240.00,
    "reconstructed_pnl": -3720.00,
    "reported_return_pct": 18.40,
    "reconstructed_return_pct": -3.72,
    "variance_amount": 21960.00
  },
  "verification": {
    "status": "CONTRADICTION",
    "method": "deterministic_recalculation",
    "verifier": "pnl_recalculator.py"
  },
  "impact": {
    "level": "VERY_HIGH",
    "capital_at_risk": 21960.00
  }
}
```
18. SECURITY / SECRET REDACTION

Before source code or configuration reaches Gemini:

Source
 ↓
Secret Scanner
 ↓
Redaction
 ↓
Sanitized Content
 ↓
Gemini

Detect:

API_KEY
SECRET
PASSWORD
TOKEN
PRIVATE_KEY
AWS_SECRET
BINANCE_SECRET
GOOGLE_API_KEY

Convert:

BINANCE_SECRET="abc123..."

into:

BINANCE_SECRET="[REDACTED]"

The original stays in controlled storage.

Gemini sees only the sanitized representation.

This is both technically responsible and a strong architecture point.

19. LARGE DATASET ARCHITECTURE

We should design for large datasets without forcing the demo to process 50 GB.

               RAW DATA
                   │
                   ▼
            CLOUD STORAGE
                   │
                   ▼
             DATA PROFILER
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
      Schema    Partition   Statistics
        │          │          │
        └──────────┼──────────┘
                   ▼
          RELEVANT DATA EXTRACTION
                   │
                   ▼
            DUCKDB / PYTHON
                   │
                   ▼
            VERIFIED RESULTS
                   │
                   ▼
                GEMINI

Gemini receives evidence, not millions of raw records.

20. DEMO DATASET: INTEGRITYLAB TEST FIXTURE

We create a dedicated synthetic project: **IntegrityLab** — a small but realistic quantitative trading codebase with matched execution logs, configuration, and performance reports.

To rigorously demonstrate discrimination power, IntegrityLab contains:
* **4 known integrity failures**
* **1 known correct control case**

### Failure 1 — Return Polarity Contradiction
One performance module interprets negative returns as positive gains due to an inverted sign convention.

### Failure 2 — Fee Double-Counting
Fees are subtracted during order execution and deducted a second time in aggregate portfolio equity calculations.

### Failure 3 — Configuration Mismatch
System runtime logic applies a 15 bps fee model while reporting metadata claims a 5 bps fee assumption.

### Failure 4 — PnL Reconciliation Discrepancy
Reported summary PnL differs materially from the independent bottom-up reconstruction of canonical fill events.

### Control Case 5 — Correct Financial Calculation
A deliberately correct sub-strategy calculation with strictly consistent code logic, fill logs, configuration parameters, and reported summary metrics.

**Purpose of the Control Case:**
Demonstrate that AUDITVECTOR correctly verifies sound calculations and does not manufacture or hallucinate findings merely because it is prompted as an auditor.

### Expected Demonstration Results on IntegrityLab Fixture
```text
IntegrityLab Test Results:
├── 4 verified/confirmed integrity contradictions
├── 1 verified control case (clean calculation)
└── 0 fabricated or hallucinated findings
```
*(Note: The control case proves verifier discrimination on the benchmark test fixture, avoiding unsubstantiated global claims of infallible LLM reasoning.)*

21. REAL-WORLD DATASET

Then we use:

AI-BIP

as our real-world dogfood example.

The story becomes:

"We created IntegrityLab so the demo is reproducible, then we ran the exact same auditor against a real quantitative system we were already developing."

This is much stronger than pretending a hypothetical company exists.

22. DATA SCALE

For the actual hackathon demo:

IntegrityLab:
10,000–50,000 trades


AI-BIP:
Real repository + selected real data

We don't need 10 million records live.

The architecture is capable of scaling because:

Cloud Storage
partitioning
filtering
aggregation
DuckDB
deterministic workers

handle the heavy lifting.

23. ASYNCHRONOUS WORKFLOW

This is one of the most important features.

User:
START AUDIT
System:
Audit created
       ↓
Pub/Sub job
       ↓
Worker starts
       ↓
ADK starts
       ↓
Agents investigate

The browser can be closed.

Later:

USER RETURNS


AUDIT COMPLETE


17 findings discovered
3 critical
5 high
6 medium
3 low
24. FIRESTORE STATE

Example:

projects/
audits/
audit_jobs/
agent_runs/
findings/
evidence/
calculations/
reports/

Audit state:

CREATED
   ↓
QUEUED
   ↓
RUNNING
   ↓
INVESTIGATING
   ↓
VERIFYING
   ↓
REPORTING
   ↓
COMPLETED

If something fails:

RUNNING
   ↓
FAILED
   ↓
RETRY

The user doesn't lose the audit.

25. FRONTEND

Keep the frontend small and polished.

Screen 1 — Dashboard
┌──────────────────────────────────────────┐
│ AUDITVECTOR                     ● ONLINE    │
├──────────────────────────────────────────┤
│                                          │
│ AI-BIP                                   │
│ Financial Integrity Audit                │
│                                          │
│ ███████████████████░░ 82%                │
│                                          │
│ Files analyzed             1,842         │
│ Trade events analyzed      4.2M          │
│ Findings                   17            │
│                                          │
│ 🔴 Critical                 3            │
│ 🟠 High                     5            │
│ 🟡 Medium                   6            │
│ 🟢 Low                      3            │
│                                          │
└──────────────────────────────────────────┘

26. SCREEN 2 — LIVE AUDIT
AUDIT IN PROGRESS

✓ Repository discovered
✓ Secrets redacted
✓ Canonical normalization complete
✓ Financial modules mapped
✓ Trade data indexed
✓ PnL reconstruction
⚠ Contradiction detected
● Verification running
○ Report generation

Also show:

Agent Activity

Audit Planner
     ✓

Repository Investigator
     ✓

Financial Investigator
     ✓

Contradiction Investigator
     ●

Verification Engine
     ○

Report Agent
     ○

27. SCREEN 3 — FINDINGS
CRITICAL FINDINGS

🔴 F-004
Return Polarity Contradiction
Status: CONTRADICTION
96% confidence

🔴 F-007
PnL Reconciliation Failure
Status: CONTRADICTION
94% confidence

🔴 F-011
Fee Calculation Integrity Failure
Status: CONTRADICTION
91% confidence

28. SCREEN 4 — EVIDENCE

This is the wow screen.

F-004

RETURN POLARITY CONTRADICTION

CRITICAL
STATUS: CONTRADICTION
96% CONFIDENCE

──────────────────────────────

SYSTEM CLAIM

Return: +18.4%

             ↓

SOURCE CODE

auto_trader_v2.py
performance.py

             ↓

CANONICAL TRADE DATA

14,821 normalized events

             ↓

INDEPENDENT CALCULATION

Return: -3.7%

             ↓

VERIFICATION

✓ Deterministically verified mismatch

             ↓

IMPACT

Reported:      +$18,240
Reconstructed: -$3,720

Difference:    $21,960

This screen is worth polishing heavily.

29. SCREEN 5 — FINAL REPORT
FINANCIAL INTEGRITY REPORT

Audit:
AI-BIP

Duration:
6m 42s

Sources:
1,842 files
4.2M trade events
37 reports

──────────────────────────────

FINDINGS

Critical       3
High           5
Medium         6
Low            3

──────────────────────────────

VERDICT

⚠️ RESULTS NOT FULLY TRUSTWORTHY

Primary risks:

1. Return polarity contradiction
2. PnL reconciliation failure
3. Fee calculation discrepancy

Recommended action:

Resolve critical findings before
relying on reported performance.

30. TECH STACK
Layer	Technology
Frontend	React + Vite + TypeScript
Backend	Python
Agent framework	Google ADK
LLM	Gemini 3.5 Flash
API	FastAPI
Async	Google Pub/Sub
Compute	Cloud Run
Database	Firestore
Files	Cloud Storage
Analytics	DuckDB
Numerical engine	Python
Authentication	Firebase/Google Identity
Containerization	Docker
Deployment	Google Cloud

31. REPOSITORY STRUCTURE
AUDITVECTOR/
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Audit.tsx
│   │   │   ├── Findings.tsx
│   │   │   └── Evidence.tsx
│   │   │
│   │   ├── components/
│   │   ├── hooks/
│   │   └── services/
│   │
│   └── package.json
│
├── backend/
│   │
│   ├── api/
│   │   ├── routes/
│   │   └── server.py
│   │
│   ├── agents/
│   │   ├── audit_planner.py
│   │   ├── repository_investigator.py
│   │   ├── financial_investigator.py
│   │   ├── contradiction_investigator.py
│   │   └── report_agent.py
│   │
│   ├── verification/
│   │   ├── pnl_recalculator.py
│   │   ├── fee_recalculator.py
│   │   ├── return_calculator.py
│   │   ├── position_reconstructor.py
│   │   ├── trade_reconciler.py
│   │   ├── statistics.py
│   │   └── comparison.py
│   │
│   ├── ingestion/
│   │   ├── repository.py
│   │   ├── csv.py
│   │   ├── logs.py
│   │   ├── reports.py
│   │   └── normalizer.py
│   │
│   ├── security/
│   │   └── secret_redactor.py
│   │
│   ├── evidence/
│   │   ├── evidence_store.py
│   │   └── evidence_graph.py
│   │
│   ├── workers/
│   │   └── audit_worker.py
│   │
│   └── models/
│       └── financial_event.py
│
├── cloud/
│   ├── cloudrun/
│   ├── pubsub/
│   ├── firestore/
│   └── storage/
│
├── integritylab/
│   ├── source/
│   ├── data/
│   └── expected_findings/
│
├── tests/
│
├── docs/
│   ├── architecture.md
│   └── demo.md
│
├── Dockerfile
├── README.md
└── .env.example

32. WHAT WE ARE NOT BUILDING

This is just as important.

❌ No trading execution

AUDITVECTOR never trades.

❌ No exchange credentials

No Binance API keys required.

❌ No automatic code modification

The agent recommends fixes.

❌ No massive enterprise platform

Not needed for the hackathon.

❌ No 20-agent architecture

Five agents in target architecture; three in MVP milestone.

❌ No Pub/Sub agent mesh

Pub/Sub only dispatches the audit job.

❌ No generic AI code reviewer

Financial integrity is the specialization.

❌ No dependency on AI-BIP

AI-BIP is a real-world test case, not the product itself.

33. MVP DEFINITION & IMPLEMENTATION MILESTONES

To guarantee rapid delivery, we sequence development across two explicit milestones:

### Milestone 1: MVP Pipeline (Build First)

```text
INPUTS
(Repository + Trade CSV / JSON + Performance Report)
        ↓
Secret Redaction & Canonical Normalization
        ↓
Audit Planner Agent
        ↓
Contradiction Investigator Agent
(directly invoking AST/code tools + Deterministic Verification Engine)
        ↓
Evidence Contract Verification
        ↓
Report Agent (Gemini)
        ↓
OUTPUTS
(Verified Findings + Evidence Contract JSON + Executive Report)
```

### Milestone 2: Target 5-Agent Pipeline (Specialized Full Architecture)

```text
Audit Planner
      ↓
Repository Investigator (deep AST logic mapper)
      ↓
Financial Investigator (claim extractor)
      ↓
Contradiction Investigator
      ↓
Report Agent
```

### Supported Tech Infrastructure for MVP:
* Cloud Run (API & Worker)
* Pub/Sub (Job dispatch boundary)
* Firestore (Job status & findings)
* Cloud Storage (Artifacts & data)
* Google ADK & Gemini 3.5 Flash
* DuckDB & Python Deterministic Verifiers

34. THE DEMO

The demo should be built around one question:

"Can you trust your financial system's numbers?"
0:00–0:30 — Problem

Show IntegrityLab reporting:

+18.4% return

Then say:

"But what if the number is wrong?"

0:30–0:50 — Start

Upload the system.

Click:

START AUTONOMOUS AUDIT

0:50–1:20 — Agent starts

Show:

Audit Planner ✓
Repository Investigator ●
Financial Investigator ○

Then:

"The audit is now running asynchronously."

1:20–1:40 — Google Cloud

Briefly show:

Cloud Run
   ↓
Pub/Sub
   ↓
Audit Worker
   ↓
ADK
   ↓
Gemini

This establishes that the architecture is genuinely running on Google Cloud.

1:40–2:10 — Agent works

Show timeline:

1,842 files
10,000 trades
37 reports


Analyzing...
2:10–2:40 — Findings

Suddenly:

3 CRITICAL
5 HIGH
6 MEDIUM
3 LOW
2:40–3:20 — Killer finding

Open:

Return Polarity Contradiction

Show:

System:
+18.4%


Independent:
-3.7%


Difference:
$21,960


Verification Status:
CONTRADICTION

Then open the evidence graph.

3:20–3:45 — Real-world AI-BIP

Say:

"This isn't only a synthetic demonstration. We also ran the same auditor against a real quantitative system we were developing."

Show one or two real findings.

3:45–4:00 — Closing

"AUDITVECTOR doesn't ask an AI whether your financial numbers look correct."

"It investigates the evidence, independently recalculates the numbers, and proves where the system disagrees with itself."

Then:

AI reasons. Code proves. Evidence explains.
35. HACKATHON POSITIONING
Track
Taskmaster

Because the user gives AUDITVECTOR a complex objective:

"Audit this financial system."

and the agent autonomously completes the workflow.

36. JUDGING STRATEGY
40% — Innovation & Operational Utility

Our argument:

Financial systems can silently produce incorrect numbers even when they appear operationally healthy. AUDITVECTOR autonomously investigates this integrity gap.

Strong.

30% — Architecture & Technology

We demonstrate:

Gemini
ADK
Cloud Run
Pub/Sub
Firestore
Cloud Storage
deterministic verification
secret redaction
asynchronous execution
persistent state
evidence graph

Strong.

30% — Demo & Production Readiness

We demonstrate:

working software
real asynchronous execution
repeatable synthetic dataset
real AI-BIP dogfood
evidence-backed findings
polished UI
reproducible deployment

Strong.

37. THE THREE-LAYER ARCHITECTURE

This should be the centerpiece of our architecture diagram:

┌───────────────────────────────────────────────┐
│              AGENTIC REASONING                │
│                                               │
│             Gemini + Google ADK               │
│                                               │
│   Plan → Investigate → Hypothesize → Explain │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│             DETERMINISTIC TRUTH               │
│                                               │
│       Python + DuckDB + Verification          │
│                                               │
│   Calculate → Reconstruct → Compare → Prove  │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│                  EVIDENCE                     │
│                                               │
│     Source → Data → Calculation → Finding    │
│                                               │
│            Human-verifiable proof             │
└───────────────────────────────────────────────┘

This is the architecture I'd want judges to remember.

38. THE PRODUCT'S DIFFERENTIATOR

There are many:

AI coding agents.

There are many:

AI trading assistants.

There are many:

AI financial analysts.

AUDITVECTOR is different:

An autonomous investigator that challenges the financial system's own claims.

It doesn't assume:

"The dashboard says +18%, therefore +18%."

It asks:

"Show me the evidence."

That's the heart of the product.

39. FINAL BLUEPRINT IN ONE VIEW
                         AUDITVECTOR
                          │
                          ▼
                   ┌─────────────┐
                   │  Dashboard  │
                   └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
                   │  Cloud Run  │
                   │     API     │
                   └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
                   │   Pub/Sub   │
                   │ Async Job   │
                   └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ Audit Worker│
                   │   + ADK     │
                   └──────┬──────┘
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
          Planner      Repository    Financial
           Agent         Agent        Agent
             │            │            │
             └────────────┼────────────┘
                          ▼
                   Contradiction
                    Investigator
                          │
                          ▼
               ┌────────────────────┐
               │ DETERMINISTIC      │
               │ VERIFICATION ENGINE│
               │                    │
               │ PnL                │
               │ Fees               │
               │ Returns            │
               │ Positions          │
               │ Reconciliation     │
               └─────────┬──────────┘
                         │
                         ▼
                   Risk Prioritizer
                         │
                         ▼
                    Report Agent
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
         Firestore   Cloud Storage  Evidence
                                     Graph
             │
             ▼
       ┌──────────────────┐
       │ AUDIT COMPLETE   │
       │                  │
       │ 3 Critical       │
       │ 5 High           │
       │ 6 Medium         │
       │ 3 Low            │
       └──────────────────┘




              CORE PRINCIPLE


             AI REASONS
                 +
              CODE PROVES
                 +
            EVIDENCE EXPLAINS
Final product statement

AUDITVECTOR is an asynchronous financial integrity investigator. Give it a quantitative or financial system, its code, data and reports. It autonomously determines what needs investigation, traces financial logic, reconstructs calculations using deterministic tools, detects contradictions, independently verifies critical findings, and produces an evidence-backed integrity report — without requiring the user to supervise the investigation.

AI reasons. Code proves. Evidence explains.

That is the blueprint I would freeze now. From here, we should stop redesigning the product and move into implementation, with the deterministic verification engine and IntegrityLab synthetic system as the first build milestone.