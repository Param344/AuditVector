/**
 * AuditVector Web Dashboard Frontend Client (Judge-Facing Presentation)
 */

document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const btnDemoAlpha = document.getElementById("btn-demo-alpha");
    const btnDemoControl = document.getElementById("btn-demo-control");
    const btnRunCustom = document.getElementById("btn-run-custom");
    const btnCopyReport = document.getElementById("btn-copy-report");
    const btnDownloadReport = document.getElementById("btn-download-report");

    const agentTracker = document.getElementById("agent-tracker");
    const resultsWorkspace = document.getElementById("results-workspace");
    const progressBar = document.getElementById("audit-progress-bar");
    const consoleOutput = document.getElementById("console-output");
    const trackerAuditId = document.getElementById("tracker-audit-id");

    const verdictBanner = document.getElementById("verdict-banner");
    const verdictIcon = document.getElementById("verdict-icon");
    const verdictText = document.getElementById("verdict-text");
    const verdictDesc = document.getElementById("verdict-desc");
    const capitalDiscrepancy = document.getElementById("capital-discrepancy");

    const countCritical = document.getElementById("count-critical");
    const countHigh = document.getElementById("count-high");
    const countMedium = document.getElementById("count-medium");
    const countLow = document.getElementById("count-low");
    const findingsTabCount = document.getElementById("findings-tab-count");

    const findingsContainer = document.getElementById("findings-container");
    const evidenceGraphContainer = document.getElementById("evidence-graph-container");
    const markdownViewer = document.getElementById("markdown-viewer");
    const duckdbStatsView = document.getElementById("duckdb-stats-view");

    // Tab buttons
    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    // Filter chips
    const filterChips = document.querySelectorAll(".filter-chip");

    let currentReportMarkdown = "";
    let currentFindings = [];
    let currentActiveFilter = "ALL";

    // Tab switching
    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            tabButtons.forEach(b => b.classList.remove("active"));
            tabContents.forEach(c => c.classList.remove("active"));

            btn.classList.add("active");
            const tabId = btn.getAttribute("data-tab");
            document.getElementById(tabId).classList.add("active");
        });
    });

    // Filter switching
    filterChips.forEach(chip => {
        chip.addEventListener("click", () => {
            filterChips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");
            currentActiveFilter = chip.getAttribute("data-filter");
            renderFindingsList(currentFindings);
        });
    });

    // Copy Report
    if (btnCopyReport) {
        btnCopyReport.addEventListener("click", () => {
            navigator.clipboard.writeText(currentReportMarkdown).then(() => {
                const original = btnCopyReport.textContent;
                btnCopyReport.textContent = "✅ Copied!";
                setTimeout(() => { btnCopyReport.textContent = original; }, 2000);
            });
        });
    }

    // Download Report
    if (btnDownloadReport) {
        btnDownloadReport.addEventListener("click", () => {
            const blob = new Blob([currentReportMarkdown], { type: "text/markdown" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `AuditVector-Executive-Report-${new Date().toISOString().slice(0, 10)}.md`;
            a.click();
            URL.revokeObjectURL(url);
        });
    }

    const btnDemoAIBIP = document.getElementById("btn-demo-aibip");

    // Trigger Demo Alpha
    btnDemoAlpha.addEventListener("click", () => {
        startAudit("/api/audits/demo/alpha", "POST");
    });

    // Trigger Demo Control
    btnDemoControl.addEventListener("click", () => {
        startAudit("/api/audits/demo/control", "POST");
    });

    // Trigger Demo AI-BIP
    if (btnDemoAIBIP) {
        btnDemoAIBIP.addEventListener("click", () => {
            startAudit("/api/audits/demo/aibip", "POST");
        });
    }

    // Trigger Custom Audit
    btnRunCustom.addEventListener("click", () => {
        const payload = {
            project_name: document.getElementById("input-project").value,
            repo_path: document.getElementById("input-repo").value,
            data_file: document.getElementById("input-data").value,
            report_file: document.getElementById("input-report").value
        };
        startAudit("/api/audits", "POST", payload);
    });

    async function startAudit(url, method, body = null) {
        // UI Reset
        agentTracker.classList.remove("hidden");
        resultsWorkspace.classList.add("hidden");
        consoleOutput.textContent = "[INIT] Connecting to AuditVector Autonomous Agent...\n";
        progressBar.style.width = "10%";
        resetStageCards();

        try {
            const options = {
                method: method,
                headers: { "Content-Type": "application/json" }
            };
            if (body) {
                options.body = JSON.stringify(body);
            }

            const response = await fetch(url, options);
            const data = await response.json();
            const auditId = data.audit_id;

            if (trackerAuditId) {
                trackerAuditId.textContent = `Job ID: ${auditId}`;
            }

            logConsole(`[DISPATCH] Audit job queued in asynchronous pipeline: ${auditId}`);
            pollAuditStatus(auditId);
        } catch (err) {
            logConsole(`[ERROR] Error dispatching audit: ${err.message}`);
        }
    }

    async function pollAuditStatus(auditId) {
        const maxAttempts = 60;
        let attempts = 0;

        const interval = setInterval(async () => {
            attempts++;
            try {
                const res = await fetch(`/api/audits/${auditId}`);
                if (!res.ok) {
                    throw new Error("Failed to fetch status");
                }
                const auditData = await res.json();
                updateProgressUI(auditData);

                if (auditData.stage === "COMPLETED" || auditData.stage === "FAILED" || attempts >= maxAttempts) {
                    clearInterval(interval);
                    if (auditData.stage === "COMPLETED" && auditData.result) {
                        displayAuditResults(auditData.result);
                    }
                }
            } catch (e) {
                logConsole(`[POLLING] Notice: ${e.message}`);
            }
        }, 150);
    }

    function updateProgressUI(auditData) {
        const stage = auditData.stage;
        progressBar.style.width = `${auditData.progress_pct || 50}%`;
        logConsole(`[STAGE] ${stage} (Progress: ${auditData.progress_pct || 50}%)`);

        const stages = ["stage-planner", "stage-repo", "stage-fin", "stage-contra", "stage-report"];
        const stageMap = {
            "QUEUED": 0,
            "RUNNING": 1,
            "INVESTIGATING": 2,
            "VERIFYING": 3,
            "REPORTING": 4,
            "COMPLETED": 5
        };

        const activeIdx = stageMap[stage] || 0;
        stages.forEach((id, idx) => {
            const el = document.getElementById(id);
            const statusEl = el.querySelector(".stage-status");
            if (idx < activeIdx) {
                el.className = "stage-card completed";
                statusEl.textContent = "Completed";
            } else if (idx === activeIdx) {
                el.className = "stage-card active";
                statusEl.textContent = "Executing...";
            } else {
                el.className = "stage-card";
                statusEl.textContent = "Waiting";
            }
        });
    }

    function resetStageCards() {
        ["stage-planner", "stage-repo", "stage-fin", "stage-contra", "stage-report"].forEach(id => {
            const el = document.getElementById(id);
            el.className = "stage-card";
            el.querySelector(".stage-status").textContent = "Idle";
        });
    }

    function logConsole(msg) {
        consoleOutput.textContent += `${new Date().toLocaleTimeString()} ${msg}\n`;
        consoleOutput.scrollTop = consoleOutput.scrollHeight;
    }

    function displayAuditResults(result) {
        agentTracker.classList.add("hidden");
        resultsWorkspace.classList.remove("hidden");

        const report = result.report;
        currentFindings = report.findings || [];

        // Verdict Banner
        const isClean = report.verdict.includes("VERIFIED");
        verdictBanner.className = `verdict-banner ${isClean ? "success" : "danger"}`;
        verdictIcon.textContent = isClean ? "✅" : "⚠️";
        verdictText.textContent = report.verdict;
        verdictDesc.textContent = isClean 
            ? "All financial metrics independently proved with underlying transactional evidence."
            : "AuditVector identified verified integrity failures where reported results contradict trade evidence.";
        
        capitalDiscrepancy.textContent = `$${(report.total_capital_discrepancy || 0).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;

        // Summary Counts
        const counts = report.summary_counts || { critical: 0, high: 0, medium: 0, low: 0 };
        countCritical.textContent = counts.critical || 0;
        countHigh.textContent = counts.high || 0;
        countMedium.textContent = counts.medium || 0;
        countLow.textContent = counts.low || 0;
        findingsTabCount.textContent = currentFindings.length;

        // Render Findings
        renderFindingsList(currentFindings);

        // Render Evidence Graphs
        renderEvidenceGraphs(result.evidence_graphs || []);

        // Render Markdown
        currentReportMarkdown = report.markdown_report || "";
        markdownViewer.textContent = currentReportMarkdown;

        // Render DuckDB Profile
        const duckdb = result.agent_pipeline?.duckdb_profile || { total_records: "N/A", unique_symbols: "N/A" };
        duckdbStatsView.innerHTML = `
            <h3 style="margin-bottom: 0.75rem; color: #60a5fa;">DuckDB In-Memory Analytical Summary</h3>
            <p><strong>Total Trade Records Scanned:</strong> ${duckdb.total_records || 'N/A'}</p>
            <p><strong>Unique Traded Assets:</strong> ${duckdb.unique_symbols || 'N/A'}</p>
            <p><strong>Analytics Engine:</strong> ${duckdb.engine || 'DuckDB SQL Engine'}</p>
            <p><strong>Verification Status:</strong> Deterministic Execution Complete (Zero LLM Arithmetic)</p>
        `;
    }

    function renderFindingsList(findings) {
        findingsContainer.innerHTML = "";
        
        const filtered = findings.filter(f => {
            if (currentActiveFilter === "ALL") return true;
            if (currentActiveFilter === "CRITICAL") return f.severity === "CRITICAL";
            if (currentActiveFilter === "HIGH") return f.severity === "HIGH";
            if (currentActiveFilter === "MEDIUM") return f.severity === "MEDIUM";
            if (currentActiveFilter === "LOW") return f.status === "VERIFIED" || f.severity === "LOW";
            return true;
        });

        if (filtered.length === 0) {
            findingsContainer.innerHTML = "<p style='color: var(--text-muted); font-size: 0.9rem;'>No findings match selected filter.</p>";
            return;
        }

        filtered.forEach(f => {
            const card = document.createElement("div");
            card.className = "finding-card";
            card.innerHTML = `
                <div class="finding-header">
                    <h4>[${f.finding_id}] ${f.title}</h4>
                    <div class="finding-tags">
                        <span class="status-badge status-${f.status}">${f.status}</span>
                        <span class="badge">Severity: ${f.severity}</span>
                        <span class="badge">Confidence: ${Math.round(f.confidence * 100)}%</span>
                    </div>
                </div>
                
                <div class="finding-comparison">
                    <div class="comparison-col claimed">
                        <small>SOFTWARE'S CLAIM</small>
                        <strong>${f.claim}</strong>
                    </div>
                    <div class="comparison-col reality">
                        <small>DETERMINISTIC REALITY & PROOF</small>
                        <strong>${f.explanation}</strong>
                    </div>
                </div>

                <div class="finding-details-grid">
                    <div><strong>Deterministic Verifier:</strong> <code>${f.verifier_name}</code></div>
                    <div><strong>Verification Method:</strong> <code>${f.verification_method}</code></div>
                    <div><strong>Capital at Risk:</strong> $${(f.capital_at_risk || 0).toLocaleString(undefined, {minimumFractionDigits: 2})}</div>
                    <div><strong>Cited Code Range:</strong> ${(f.sources || []).map(s => `${s.file}:${s.line_range}`).join(", ") || 'N/A'}</div>
                </div>
            `;
            findingsContainer.appendChild(card);
        });
    }

    function renderEvidenceGraphs(graphs) {
        evidenceGraphContainer.innerHTML = "";
        if (graphs.length === 0) {
            evidenceGraphContainer.innerHTML = "<p>No evidence graph chains generated.</p>";
            return;
        }

        graphs.forEach(g => {
            const card = document.createElement("div");
            card.className = "evidence-chain-card";
            card.innerHTML = `
                <h4 style="margin-bottom: 0.5rem; color: #93c5fd;">Evidence Contract Chain: [${g.finding_id}]</h4>
                <div class="chain-steps">
                    <div class="chain-node" title="Click to view Source Code metadata">
                        <strong>Source Citation</strong>
                        <small>${(g.nodes.find(n => n.type === 'SOURCE')?.label || 'Code Repo')}</small>
                    </div>
                    <span class="chain-arrow">→</span>
                    <div class="chain-node" title="Click to view Transaction Evidence hash">
                        <strong>Raw Data Event</strong>
                        <small>${(g.nodes.find(n => n.type === 'DATA')?.label || 'CSV Events')}</small>
                    </div>
                    <span class="chain-arrow">→</span>
                    <div class="chain-node" title="Click to view Canonical Schema">
                        <strong>Normalizer</strong>
                        <small>Canonical FinancialEvent</small>
                    </div>
                    <span class="chain-arrow">→</span>
                    <div class="chain-node" title="Click to view Verifier Algorithm">
                        <strong>Deterministic Verifier</strong>
                        <small>${(g.nodes.find(n => n.type === 'VERIFIER')?.label || 'FIFO PnL Engine')}</small>
                    </div>
                    <span class="chain-arrow">→</span>
                    <div class="chain-node" style="border-color: var(--color-critical); box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);" title="Click to view Finding">
                        <strong>Verified Contradiction</strong>
                        <small>${g.finding_id}</small>
                    </div>
                </div>
            `;
            evidenceGraphContainer.appendChild(card);
        });
    }
});
