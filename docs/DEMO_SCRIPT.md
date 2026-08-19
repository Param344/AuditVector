# AUDITVECTOR — 4-MINUTE HACKATHON VIDEO DEMO SCRIPT
**Track:** Taskmaster | **All Things Agentic Hackathon**  
**Tagline:** *AI reasons. Code proves. Evidence explains.*

---

## ⏱️ Video Breakdown (0:00 – 4:00)

### 1. The Financial Integrity Problem (0:00 – 0:40)
* **Visual:** Close-up of a trading dashboard showing **+18.4% Return** in green. Cut to code snippet with inverted subtraction `(starting_capital - ending_capital)`.
* **Audio / Voiceover:**
  > "In quantitative finance and algorithmic trading, software failures don't crash with error messages — they fail silently. Sign inversions disguise devastating losses as profits. Double-counted commissions distort risk models. And configuration assumptions drift from live trade execution.
  >
  > Today, teams try to audit code using generative LLMs. But when you ask an LLM if financial numbers look right, it hallucinates. LLMs cannot do mental arithmetic on 50,000 transaction fills.
  >
  > We built **AUDITVECTOR**: the autonomous financial integrity investigator."

---

### 2. The Three-Layer Architecture (0:40 – 1:20)
* **Visual:** Architecture diagram animation showing the 3 layers (*Agentic Reasoning $\to$ Deterministic Truth $\to$ Evidence Graph*).
* **Audio / Voiceover:**
  > "AuditVector operates on one uncompromising rule: **AI reasons. Code proves. Evidence explains.**
  >
  > We combine **Google ADK 2.7** and **Gemini 3.5 Flash** with a high-throughput deterministic verification engine in Python and **DuckDB**.
  >
  > Gemini reasons about where financial logic lives, extracts reported claims, and forms audit hypotheses. But it is strictly forbidden from doing mental arithmetic. Instead, it invokes deterministic verifiers that reconstruct PnL bottom-up from raw trade events and enforce strict **Evidence Contracts**."

---

### 3. Live Demo — IntegrityLab Alpha Failure (1:20 – 2:30)
* **Visual:** Web UI. Click `⚠️ IntegrityLab Alpha`. Live 5-Agent ADK Orchestration tracker animates across all 5 stages in real time.
* **Audio / Voiceover:**
  > "Let's watch AuditVector in action against our synthetic benchmark, **IntegrityLab**.
  >
  > The user dispatches the audit. Across our asynchronous Google Cloud Run and Pub/Sub pipeline, the 5 ADK agents take over:
  > 1. **Audit Planner** scopes the repository and dataset targets.
  > 2. **Repo Investigator** uses AST parsing to map financial routines.
  > 3. **Financial Investigator** extracts reported metrics.
  > 4. **Contradiction Investigator** runs deterministic trade reconciliation and variance checks.
  > 5. **Report Agent** synthesizes the Executive Report.
  >
  > In seconds, AuditVector catches all four planted integrity failures:
  > - **Critical PnL Reconciliation Failure:** The system reported +$18,240, but deterministic FIFO matching proved actual PnL was -$3,720.
  > - **Return Polarity Inversion:** Disguising a -3.7% loss as a +18.2% gain.
  > - **Fee Double-Counting:** Deducting commissions at order fill and again at portfolio summary.
  > - **Fee Model Rate Mismatch:** 13.2 bps effective vs 5.0 bps configured."

---

### 4. Traceable Evidence Graph & Control Case (2:30 – 3:20)
* **Visual:** Switch to the **🕸️ Evidence Graph** tab. Click on a node to view SHA-256 hashes and code citations. Then trigger `✅ IntegrityLab Control`.
* **Audio / Voiceover:**
  > "Every single finding in AuditVector is backed by an unalterable Evidence Contract.
  >
  > In the Evidence Graph, judges and risk managers can trace the unbroken chain: from the exact source file line range, to the raw transaction hash, through the canonical normalizer, into the deterministic verifier.
  >
  > And when we run AuditVector against **IntegrityLab Control** — a clean codebase — it proves 100% mathematical soundness with **zero fabricated findings**."

---

### 5. Real-World Dogfooding: AI-BIP Quantitative Engine (3:20 – 3:45)
* **Visual:** Click `⚡ Real AI-BIP Dogfood`. The audit runs and flags execution slippage drift.
* **Audio / Voiceover:**
  > "AuditVector isn't just a synthetic demo. We dogfooded it against our own multi-asset quantitative system, **AI-BIP**.
  >
  > It autonomously ingested live trade fills across Bitcoin, Ethereum, Solana, and Avalanche, instantly surfacing a $16,286 calculation discrepancy caused by unmodeled slippage drag."

---

### 6. Conclusion (3:45 – 4:00)
* **Visual:** Final Executive Report view with Google ADK, Gemini 3.5, and Cloud Run telemetry badges.
* **Audio / Voiceover:**
  > "AuditVector doesn't ask an AI if your numbers look correct. It investigates the evidence, independently proves the math, and explains the truth.
  >
  > **AI reasons. Code proves. Evidence explains.**
  > Thank you."
