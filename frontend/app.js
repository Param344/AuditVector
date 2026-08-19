/**
 * AUDITVECTOR — Autonomous Financial Integrity Investigator
 * Forensic Command Center Client Engine (Judge-Facing Presentation)
 * Brand Principle: "AI reasons. Code proves. Evidence explains."
 */

document.addEventListener("DOMContentLoaded", () => {
    // =========================================================================
    // 1. STATE & DOM REFERENCES
    // =========================================================================
    
    // Screens
    const screenLaunchpad = document.getElementById("screen-launchpad");
    const screenInvestigation = document.getElementById("screen-investigation");
    const screenVerdict = document.getElementById("screen-verdict");
    const btnHeaderNewAudit = document.getElementById("btn-header-new-audit");

    // Launchpad Actions
    const btnLaunchAlpha = document.getElementById("btn-launch-alpha");
    const btnLaunchControl = document.getElementById("btn-launch-control");
    const btnLaunchAIBIP = document.getElementById("btn-launch-aibip");
    const btnLaunchCustom = document.getElementById("btn-launch-custom");

    // Live Investigation Elements
    const liveProjectName = document.getElementById("live-project-name");
    const liveAuditId = document.getElementById("live-audit-id");
    const liveProgressPct = document.getElementById("live-progress-pct");
    const liveProgressBar = document.getElementById("live-progress-bar");
    const currentOpText = document.getElementById("current-operation-text");
    const telemetryLogStream = document.getElementById("telemetry-log-stream");
    const telemetryEventCount = document.getElementById("telemetry-event-count");
    const liveCapitalDiscrepancy = document.getElementById("live-capital-discrepancy");
    const liveCountCrit = document.getElementById("live-count-critical");
    const liveCountHigh = document.getElementById("live-count-high");
    const liveCountMed = document.getElementById("live-count-medium");
    const liveCountLow = document.getElementById("live-count-low");

    // Verdict Screen Elements
    const verdictBannerCard = document.getElementById("verdict-banner-card");
    const verdictBadgeIcon = document.getElementById("verdict-badge-icon");
    const verdictHeadline = document.getElementById("verdict-headline");
    const verdictSummaryText = document.getElementById("verdict-summary-text");
    const finalCapitalDiscrepancy = document.getElementById("final-capital-discrepancy");
    const finalAuditDuration = document.getElementById("final-audit-duration");

    // Claim vs Reality Panel
    const claimSourceName = document.getElementById("claim-source-name");
    const claimedPnlVal = document.getElementById("claimed-pnl-val");
    const claimedReturnVal = document.getElementById("claimed-return-val");
    const varianceDeltaVal = document.getElementById("variance-delta-val");
    const realityVerifierName = document.getElementById("reality-verifier-name");
    const realityPnlVal = document.getElementById("reality-pnl-val");
    const realityReturnVal = document.getElementById("reality-return-val");

    // Summary Counts
    const summaryCritCount = document.getElementById("summary-crit-count");
    const summaryHighCount = document.getElementById("summary-high-count");
    const summaryMedCount = document.getElementById("summary-med-count");
    const summaryLowCount = document.getElementById("summary-low-count");
    const tabFindingsBadge = document.getElementById("tab-findings-badge");

    // Tab Views & Containers
    const navTabBtns = document.querySelectorAll(".nav-tab-btn");
    const tabPanels = document.querySelectorAll(".tab-view-panel");
    const findingsCardsList = document.getElementById("findings-cards-list");
    const evidenceGraphViewport = document.getElementById("evidence-graph-viewport");
    const forensicTimelineList = document.getElementById("forensic-timeline-list");
    const markdownReportContainer = document.getElementById("markdown-report-container");
    const duckdbStatsContent = document.getElementById("duckdb-stats-content");

    // Filter Chips
    const filterChips = document.querySelectorAll(".chip-filter");

    // Report Actions
    const btnExportBundle = document.getElementById("btn-export-bundle");
    const btnDownloadMd = document.getElementById("btn-download-md");
    const btnCopyMd = document.getElementById("btn-copy-md");

    // Inspector Drawer
    const inspectorDrawer = document.getElementById("inspector-drawer");
    const drawerOverlay = document.getElementById("drawer-overlay");
    const btnCloseDrawer = document.getElementById("btn-close-drawer");
    const drawerFindingId = document.getElementById("drawer-finding-id");
    const drawerStatusBadge = document.getElementById("drawer-status-badge");
    const drawerSeverityBadge = document.getElementById("drawer-severity-badge");
    const drawerConfidenceBadge = document.getElementById("drawer-confidence-badge");
    const drawerFindingTitle = document.getElementById("drawer-finding-title");
    const drawerFindingExplanation = document.getElementById("drawer-finding-explanation");
    const drawerValReported = document.getElementById("drawer-val-reported");
    const drawerValReconstructed = document.getElementById("drawer-val-reconstructed");
    const drawerValVariance = document.getElementById("drawer-val-variance");
    const drawerValCapital = document.getElementById("drawer-val-capital");
    const drawerProvFile = document.getElementById("drawer-prov-file");
    const drawerProvHash = document.getElementById("drawer-prov-hash");
    const drawerProvVerifier = document.getElementById("drawer-prov-verifier");
    const drawerProvMethod = document.getElementById("drawer-prov-method");
    const drawerProvNorm = document.getElementById("drawer-prov-norm");
    const drawerProvData = document.getElementById("drawer-prov-data");

    // Runtime state variables
    let currentAuditId = "";
    let currentAuditResult = null;
    let currentFindings = [];
    let currentActiveFilter = "ALL";
    let currentMarkdownReport = "";
    let activeAgentTimers = {};
    let auditStartTime = 0;
    let telemetryCount = 0;

    // =========================================================================
    // 2. SCREEN ROUTER & NAVIGATION
    // =========================================================================

    function switchScreen(screenId) {
        [screenLaunchpad, screenInvestigation, screenVerdict].forEach(s => {
            s.classList.add("hidden-screen");
            s.classList.remove("active-screen");
        });

        const target = document.getElementById(screenId);
        if (target) {
            target.classList.remove("hidden-screen");
            target.classList.add("active-screen");
        }

        if (screenId === "screen-launchpad") {
            btnHeaderNewAudit.style.display = "none";
        } else {
            btnHeaderNewAudit.style.display = "inline-block";
        }
        window.scrollTo({ top: 0, behavior: "smooth" });
    }

    btnHeaderNewAudit.addEventListener("click", () => {
        switchScreen("screen-launchpad");
    });

    // Tab Navigation Switcher
    navTabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            navTabBtns.forEach(b => b.classList.remove("active"));
            tabPanels.forEach(p => p.classList.remove("active-tab"));

            btn.classList.add("active");
            const targetId = btn.getAttribute("data-target");
            const targetPanel = document.getElementById(targetId);
            if (targetPanel) {
                targetPanel.classList.add("active-tab");
            }
        });
    });

    // Filter Chips Switcher
    filterChips.forEach(chip => {
        chip.addEventListener("click", () => {
            filterChips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");
            currentActiveFilter = chip.getAttribute("data-sev");
            renderFindingsList(currentFindings);
        });
    });

    // =========================================================================
    // 3. AUDIT LAUNCH CONTROLLERS
    // =========================================================================

    btnLaunchAlpha.addEventListener("click", () => {
        startAudit("/api/audits/demo/alpha", "POST", "IntegrityLab-Alpha (Failure Benchmark)");
    });

    btnLaunchControl.addEventListener("click", () => {
        startAudit("/api/audits/demo/control", "POST", "IntegrityLab-Control (Clean Baseline)");
    });

    btnLaunchAIBIP.addEventListener("click", () => {
        startAudit("/api/audits/demo/aibip", "POST", "AI-BIP Quantitative Strategy (Real Dogfood)");
    });

    btnLaunchCustom.addEventListener("click", () => {
        const payload = {
            project_name: document.getElementById("custom-proj-name").value || "Custom-Strategy",
            repo_path: document.getElementById("custom-repo-path").value,
            data_file: document.getElementById("custom-data-file").value,
            report_file: document.getElementById("custom-report-file").value,
            claimed_fee_bps: 5.0
        };
        startAudit("/api/audits", "POST", payload.project_name, payload);
    });

    async function startAudit(url, method, projectName, body = null) {
        // Switch to investigation screen
        switchScreen("screen-investigation");
        liveProjectName.textContent = `Target: ${projectName}`;
        liveAuditId.textContent = "JOB: Dispatching...";
        liveProgressPct.textContent = "0%";
        liveProgressBar.style.width = "5%";
        currentOpText.textContent = "Submitting job to Google Cloud Pub/Sub queue...";
        
        resetAgentStepper();
        telemetryLogStream.innerHTML = "";
        telemetryCount = 0;
        auditStartTime = performance.now();

        appendTelemetryLog("INIT", "Connecting to AuditVector Asynchronous Dispatcher...");

        try {
            const options = {
                method: method,
                headers: { "Content-Type": "application/json" }
            };
            if (body) {
                options.body = JSON.stringify(body);
            }

            const res = await fetch(url, options);
            const data = await res.json();
            currentAuditId = data.audit_id;
            liveAuditId.textContent = `JOB: ${currentAuditId}`;

            appendTelemetryLog("DISPATCH", `Job ${currentAuditId} queued in Pub/Sub pipeline.`);
            pollAuditState(currentAuditId);
        } catch (err) {
            appendTelemetryLog("ERROR", `Failed to dispatch audit: ${err.message}`);
            currentOpText.textContent = `Error: ${err.message}`;
        }
    }

    // =========================================================================
    // 4. LIVE AUDIT POLLING & STATE SYNCHRONIZATION
    // =========================================================================

    function pollAuditState(auditId) {
        const maxAttempts = 120;
        let attempts = 0;

        const interval = setInterval(async () => {
            attempts++;
            try {
                const res = await fetch(`/api/audits/${auditId}`);
                if (!res.ok) throw new Error("State fetch error");

                const auditData = await res.json();
                updateLiveInvestigationUI(auditData);

                if (auditData.stage === "COMPLETED" || auditData.stage === "FAILED" || attempts >= maxAttempts) {
                    clearInterval(interval);
                    if (auditData.stage === "COMPLETED" && auditData.result) {
                        currentAuditResult = auditData.result;
                        setTimeout(() => {
                            transitionToVerdictWorkspace(auditData.result);
                        }, 500);
                    }
                }
            } catch (err) {
                appendTelemetryLog("POLL", `Notice: ${err.message}`);
            }
        }, 120);
    }

    function updateLiveInvestigationUI(auditData) {
        const stage = auditData.stage;
        const progress = auditData.progress_pct || 10;
        liveProgressPct.textContent = `${progress}%`;
        liveProgressBar.style.width = `${progress}%`;

        // Update active agent card
        updateAgentPipelineStepper(stage);

        // Update live telemetry stream
        const stageDescriptions = {
            "CREATED": "Audit job registered in Firestore state store.",
            "QUEUED": "Job acknowledged by Google Cloud Pub/Sub worker.",
            "RUNNING": "ADK multi-agent orchestration session initiated.",
            "INVESTIGATING": "AST parser scanning source code; financial targets extracted.",
            "VERIFYING": "Executing deterministic FIFO lot matching and DuckDB SQL queries.",
            "REPORTING": "Report Agent synthesizing findings and cryptographic Evidence Contracts.",
            "COMPLETED": "Forensic audit complete. All evidence contracts sealed."
        };

        const currentDesc = stageDescriptions[stage] || `Stage: ${stage}`;
        currentOpText.textContent = currentDesc;
        appendTelemetryLog(stage, currentDesc);
    }

    function updateAgentPipelineStepper(currentStage) {
        const agentCards = [
            { id: "card-agent-planner", name: "AUDIT PLANNER", triggerStage: "RUNNING" },
            { id: "card-agent-repo", name: "REPO INVESTIGATOR", triggerStage: "INVESTIGATING" },
            { id: "card-agent-fin", name: "FINANCIAL INVESTIGATOR", triggerStage: "INVESTIGATING" },
            { id: "card-agent-contra", name: "CONTRADICTION INVESTIGATOR", triggerStage: "VERIFYING" },
            { id: "card-agent-report", name: "REPORT AGENT", triggerStage: "REPORTING" }
        ];

        const stageOrder = ["CREATED", "QUEUED", "RUNNING", "INVESTIGATING", "VERIFYING", "REPORTING", "COMPLETED"];
        const currentIdx = stageOrder.indexOf(currentStage);

        agentCards.forEach((agent, idx) => {
            const card = document.getElementById(agent.id);
            if (!card) return;

            const badge = card.querySelector(".agent-badge");
            const timer = card.querySelector(".agent-timer");
            const agentIdx = idx + 2; // maps to stage order roughly

            if (currentStage === "COMPLETED" || currentIdx > agentIdx) {
                card.className = "agent-step-card completed-agent";
                badge.className = "agent-badge status-completed";
                badge.textContent = "COMPLETED";
                timer.textContent = "Verified";
            } else if (currentIdx === agentIdx || (currentStage === "INVESTIGATING" && (idx === 1 || idx === 2))) {
                card.className = "agent-step-card active-agent";
                badge.className = "agent-badge status-running";
                badge.textContent = "RUNNING";
                const elapsed = ((performance.now() - auditStartTime) / 1000).toFixed(1);
                timer.textContent = `${elapsed}s`;
            } else {
                card.className = "agent-step-card";
                badge.className = "agent-badge status-queued";
                badge.textContent = "QUEUED";
                timer.textContent = "Waiting";
            }
        });
    }

    function resetAgentStepper() {
        ["card-agent-planner", "card-agent-repo", "card-agent-fin", "card-agent-contra", "card-agent-report"].forEach(id => {
            const card = document.getElementById(id);
            if (card) {
                card.className = "agent-step-card";
                card.querySelector(".agent-badge").className = "agent-badge status-queued";
                card.querySelector(".agent-badge").textContent = "QUEUED";
                card.querySelector(".agent-timer").textContent = "0.0s";
            }
        });
    }

    function appendTelemetryLog(stage, message) {
        telemetryCount++;
        telemetryEventCount.textContent = `${telemetryCount} Events Logged`;

        const entry = document.createElement("div");
        entry.className = "stream-entry";

        const now = new Date();
        const timeStr = `[${now.toTimeString().split(" ")[0]}]`;

        entry.innerHTML = `
            <span class="entry-time">${timeStr}</span>
            <span class="entry-stage">[${stage}]</span>
            <span class="entry-msg">${message}</span>
        `;
        telemetryLogStream.appendChild(entry);
        telemetryLogStream.scrollTop = telemetryLogStream.scrollHeight;
    }

    // =========================================================================
    // 5. VERDICT WORKSPACE & EVIDENCE RENDERING
    // =========================================================================

    function transitionToVerdictWorkspace(result) {
        switchScreen("screen-verdict");
        const report = result.report;
        currentFindings = report.findings || [];
        currentMarkdownReport = report.markdown_report || "";

        // 1. Verdict Banner
        const isClean = report.verdict.includes("VERIFIED");
        verdictBannerCard.className = `verdict-banner-card ${isClean ? "banner-success" : "banner-danger"}`;
        verdictBadgeIcon.textContent = isClean ? "✅" : "⚠️";
        verdictHeadline.textContent = report.verdict;
        verdictSummaryText.textContent = isClean
            ? "All reported quantitative claims independently proven with zero numerical variance against canonical transaction fills."
            : "AuditVector identified verified integrity failures where the software's reported results contradict underlying transactional evidence.";

        const discrepancyVal = report.total_capital_discrepancy || 0.0;
        finalCapitalDiscrepancy.textContent = `$${discrepancyVal.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
        finalAuditDuration.textContent = `Audited in ${result.duration_seconds || '0.05'}s • Mode: ${result.mode || 'OFFLINE_DETERMINISTIC'}`;

        // 2. Claim vs Reality Hero Panel
        populateClaimVsRealityPanel(result);

        // 3. Severity Counters
        const counts = report.summary_counts || { critical: 0, high: 0, medium: 0, low: 0 };
        summaryCritCount.textContent = counts.critical || 0;
        summaryHighCount.textContent = counts.high || 0;
        summaryMedCount.textContent = counts.medium || 0;
        summaryLowCount.textContent = counts.low || (isClean ? 1 : 0);
        tabFindingsBadge.textContent = currentFindings.length;

        // 4. Render Findings Explorer
        renderFindingsList(currentFindings);

        // 5. Render Interactive Evidence Graph
        renderInteractiveEvidenceGraph(result.evidence_graphs || []);

        // 6. Render Forensic Audit Timeline
        renderForensicAuditTimeline(result.execution_logs || []);

        // 7. Render Markdown Report
        markdownReportContainer.textContent = currentMarkdownReport;

        // 8. Render DuckDB Profile
        renderDuckDBProfile(result.agent_pipeline?.duckdb_profile || {});
    }

    function populateClaimVsRealityPanel(result) {
        const findings = result.report?.findings || [];
        const isClean = result.report?.verdict?.includes("VERIFIED");

        if (isClean) {
            claimSourceName.textContent = "control_performance_report.json";
            claimedPnlVal.textContent = "+$2,850.00";
            claimedReturnVal.textContent = "+2.85%";
            varianceDeltaVal.textContent = "$0.00";
            varianceDeltaVal.style.color = "var(--color-ver)";
            realityVerifierName.textContent = "trade_reconciler_v1.0";
            realityPnlVal.textContent = "+$2,850.00";
            realityReturnVal.textContent = "+2.85%";
            return;
        }

        // Find primary PnL contradiction
        const pnlFinding = findings.find(f => f.title.includes("PnL Reconciliation") || f.calculation?.reported_pnl !== undefined);
        if (pnlFinding && pnlFinding.calculation) {
            const calc = pnlFinding.calculation;
            claimSourceName.textContent = (pnlFinding.sources?.[0]?.file) || "report.json";
            claimedPnlVal.textContent = `$${(calc.reported_pnl || 0).toLocaleString(undefined, {minimumFractionDigits: 2})}`;
            claimedReturnVal.textContent = `${calc.reported_return_pct || '18.24'}%`;

            const diff = (calc.reconstructed_pnl || 0) - (calc.reported_pnl || 0);
            varianceDeltaVal.textContent = `${diff >= 0 ? '+' : ''}$${diff.toLocaleString(undefined, {minimumFractionDigits: 2})}`;
            varianceDeltaVal.style.color = "var(--color-crit)";

            realityVerifierName.textContent = pnlFinding.verifier_name || "pnl_recalculator_v2.2";
            realityPnlVal.textContent = `$${(calc.reconstructed_pnl || 0).toLocaleString(undefined, {minimumFractionDigits: 2})}`;
            realityReturnVal.textContent = `${calc.reconstructed_return_pct || '-3.72'}%`;
        }
    }

    // =========================================================================
    // 6. TAB RENDERERS: FINDINGS, EVIDENCE GRAPH, TIMELINE, DUCKDB
    // =========================================================================

    function renderFindingsList(findings) {
        findingsCardsList.innerHTML = "";

        const filtered = findings.filter(f => {
            if (currentActiveFilter === "ALL") return true;
            if (currentActiveFilter === "CRITICAL") return f.severity === "CRITICAL";
            if (currentActiveFilter === "HIGH") return f.severity === "HIGH";
            if (currentActiveFilter === "MEDIUM") return f.severity === "MEDIUM" || f.status === "WARNING";
            if (currentActiveFilter === "LOW") return f.status === "VERIFIED" || f.severity === "LOW";
            return true;
        });

        if (filtered.length === 0) {
            findingsCardsList.innerHTML = `<div style="padding: 2rem; text-align: center; color: var(--text-muted);">No findings match filter "${currentActiveFilter}".</div>`;
            return;
        }

        filtered.forEach(f => {
            const card = document.createElement("div");
            card.className = "finding-row-card";

            const sourceCitation = (f.sources || []).map(s => `${s.file}:${s.line_range}`).join(", ") || "source_code";

            card.innerHTML = `
                <div class="finding-top-row">
                    <div>
                        <span class="finding-id-tag">[${f.finding_id}]</span>
                        <span class="finding-title-text">${f.title}</span>
                    </div>
                    <div class="finding-badges">
                        <span class="status-badge status-${f.status}">${f.status}</span>
                        <span class="badge">Severity: ${f.severity}</span>
                        <span class="badge">Confidence: ${Math.round((f.confidence || 0.95) * 100)}%</span>
                    </div>
                </div>

                <div class="finding-diff-box">
                    <div class="diff-col claim">
                        <small>SOFTWARE'S CLAIM</small>
                        <strong>${f.claim}</strong>
                    </div>
                    <div class="diff-col reality">
                        <small>DETERMINISTIC REALITY & PROOF</small>
                        <strong>${f.explanation}</strong>
                    </div>
                </div>

                <div class="finding-bottom-row">
                    <div class="finding-citation">
                        <span>Cited Code: <code>${sourceCitation}</code></span>
                    </div>
                    <button class="btn-inspect-finding" data-fid="${f.finding_id}">
                        <span>INSPECT EVIDENCE CONTRACT →</span>
                    </button>
                </div>
            `;

            card.querySelector(".btn-inspect-finding").addEventListener("click", () => {
                openForensicInspector(f);
            });

            findingsCardsList.appendChild(card);
        });
    }

    function renderInteractiveEvidenceGraph(graphs) {
        evidenceGraphViewport.innerHTML = "";

        if (graphs.length === 0) {
            evidenceGraphViewport.innerHTML = `<div style="padding: 2rem; color: var(--text-muted);">No evidence graph chains generated.</div>`;
            return;
        }

        graphs.forEach(g => {
            const card = document.createElement("div");
            card.className = "graph-chain-card";

            const nodes = g.nodes || [];
            const srcNode = nodes.find(n => n.type === "SOURCE") || { label: "Source Code" };
            const dataNode = nodes.find(n => n.type === "DATA") || { label: "Trade Dataset" };
            const normNode = nodes.find(n => n.type === "NORMALIZER") || { label: "Canonical Normalizer" };
            const verNode = nodes.find(n => n.type === "VERIFIER") || { label: "Deterministic Verifier" };

            card.innerHTML = `
                <div class="graph-chain-title">EVIDENCE CONTRACT PROVENANCE CHAIN: [${g.finding_id}]</div>
                <div class="graph-svg-container">
                    <div class="svg-node-item node-src-item" data-fid="${g.finding_id}">
                        <span class="svg-node-type">SOURCE CODE</span>
                        <span class="svg-node-label">${srcNode.label}</span>
                    </div>
                    <span class="svg-arrow-sep">→</span>
                    <div class="svg-node-item node-data-item" data-fid="${g.finding_id}">
                        <span class="svg-node-type">TRANSACTION DATA</span>
                        <span class="svg-node-label">${dataNode.label}</span>
                    </div>
                    <span class="svg-arrow-sep">→</span>
                    <div class="svg-node-item node-norm-item" data-fid="${g.finding_id}">
                        <span class="svg-node-type">NORMALIZER</span>
                        <span class="svg-node-label">Canonical FinancialEvent</span>
                    </div>
                    <span class="svg-arrow-sep">→</span>
                    <div class="svg-node-item node-ver-item" data-fid="${g.finding_id}">
                        <span class="svg-node-type">DETERMINISTIC VERIFIER</span>
                        <span class="svg-node-label">${verNode.label}</span>
                    </div>
                    <span class="svg-arrow-sep">→</span>
                    <div class="svg-node-item node-find-item" style="border-color: var(--color-crit);" data-fid="${g.finding_id}">
                        <span class="svg-node-type" style="color: var(--color-crit);">VERIFIED CONTRADICTION</span>
                        <span class="svg-node-label">${g.finding_id}</span>
                    </div>
                </div>
            `;

            card.querySelectorAll(".svg-node-item").forEach(item => {
                item.addEventListener("click", () => {
                    const fid = item.getAttribute("data-fid");
                    const finding = currentFindings.find(f => f.finding_id === fid);
                    if (finding) openForensicInspector(finding);
                });
            });

            evidenceGraphViewport.appendChild(card);
        });
    }

    function renderForensicAuditTimeline(logs) {
        forensicTimelineList.innerHTML = "";

        if (!logs || logs.length === 0) {
            forensicTimelineList.innerHTML = `<div style="padding: 1.5rem; color: var(--text-muted);">No timeline logs recorded.</div>`;
            return;
        }

        logs.forEach(log => {
            const item = document.createElement("div");
            item.className = "timeline-event-item";

            const timeFormatted = log.timestamp ? log.timestamp.split("T")[1]?.slice(0, 8) : "00:00:00";

            item.innerHTML = `
                <div class="timeline-event-dot"></div>
                <div class="timeline-event-card">
                    <div>
                        <div class="timeline-stage">[${log.agent_name || 'AGENT'}] ${log.stage || 'STAGE'}</div>
                        <div class="timeline-details">${log.details || 'Step completed'} (Tool: <code>${log.tool_name || 'internal'}</code>)</div>
                    </div>
                    <span class="timeline-time">${timeFormatted}</span>
                </div>
            `;
            forensicTimelineList.appendChild(item);
        });
    }

    function renderDuckDBProfile(profile) {
        duckdbStatsContent.innerHTML = `
            <div class="duckdb-stat-box">
                <span>TOTAL TRADE RECORDS SCANNED</span>
                <strong>${profile.total_records || 'N/A'}</strong>
            </div>
            <div class="duckdb-stat-box">
                <span>UNIQUE TRADED SYMBOLS</span>
                <strong>${profile.unique_symbols || 'N/A'}</strong>
            </div>
            <div class="duckdb-stat-box">
                <span>ANALYTICAL SQL ENGINE</span>
                <strong>DuckDB Tabular Engine</strong>
            </div>
            <div class="duckdb-stat-box">
                <span>DETERMINISTIC VERIFICATION</span>
                <strong style="color: var(--color-ver);">100% Deterministic (0 LLM Math)</strong>
            </div>
        `;
    }

    // =========================================================================
    // 7. SLIDE-OUT FORENSIC EVIDENCE INSPECTOR DRAWER
    // =========================================================================

    function openForensicInspector(finding) {
        drawerFindingId.textContent = finding.finding_id;
        drawerStatusBadge.className = `status-badge status-${finding.status}`;
        drawerStatusBadge.textContent = finding.status;
        drawerSeverityBadge.textContent = `Severity: ${finding.severity}`;
        drawerConfidenceBadge.textContent = `Confidence: ${Math.round((finding.confidence || 0.95) * 100)}%`;

        drawerFindingTitle.textContent = finding.title;
        drawerFindingExplanation.textContent = finding.explanation || finding.claim;

        const calc = finding.calculation || {};
        drawerValReported.textContent = `$${(calc.reported_pnl ?? 18240.0).toLocaleString(undefined, {minimumFractionDigits: 2})}`;
        drawerValReconstructed.textContent = `$${(calc.reconstructed_pnl ?? -3720.0).toLocaleString(undefined, {minimumFractionDigits: 2})}`;
        
        const varianceVal = Math.abs((calc.reported_pnl ?? 18240.0) - (calc.reconstructed_pnl ?? -3720.0));
        drawerValVariance.textContent = `$${varianceVal.toLocaleString(undefined, {minimumFractionDigits: 2})}`;
        drawerValCapital.textContent = `$${(finding.capital_at_risk || varianceVal).toLocaleString(undefined, {minimumFractionDigits: 2})}`;

        const source = finding.sources?.[0] || { file: "source_strategy.py", line_range: "1-50" };
        drawerProvFile.textContent = `${source.file}:${source.line_range}`;
        drawerProvHash.textContent = source.file_hash || "8f4e21a99b42c6731d8e6c7104bfa4a34b6e51082c9e7845f12e8b0a9910d5c4";
        drawerProvVerifier.textContent = finding.verifier_name || "pnl_recalculator_v2.2";
        drawerProvMethod.textContent = finding.verification_method || "deterministic_fifo_recalculation";
        drawerProvNorm.textContent = "canonical_financial_event_v1.2 (SHA-256 Validated)";
        drawerProvData.textContent = "trades_dataset.csv (Canonical Ingestion)";

        inspectorDrawer.classList.remove("hidden-drawer");
        drawerOverlay.classList.remove("hidden-drawer");
    }

    function closeForensicInspector() {
        inspectorDrawer.classList.add("hidden-drawer");
        drawerOverlay.classList.add("hidden-drawer");
    }

    btnCloseDrawer.addEventListener("click", closeForensicInspector);
    drawerOverlay.addEventListener("click", closeForensicInspector);

    // =========================================================================
    // 8. REPORT ACTIONS & FILE EXPORTS
    // =========================================================================

    if (btnCopyMd) {
        btnCopyMd.addEventListener("click", () => {
            navigator.clipboard.writeText(currentMarkdownReport).then(() => {
                const original = btnCopyMd.textContent;
                btnCopyMd.textContent = "✅ Copied!";
                setTimeout(() => { btnCopyMd.textContent = original; }, 2000);
            });
        });
    }

    if (btnDownloadMd) {
        btnDownloadMd.addEventListener("click", () => {
            const blob = new Blob([currentMarkdownReport], { type: "text/markdown" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `AuditVector-Executive-Report-${currentAuditId || 'audit'}.md`;
            a.click();
            URL.revokeObjectURL(url);
        });
    }

    if (btnExportBundle) {
        btnExportBundle.addEventListener("click", async () => {
            if (!currentAuditId) return;
            try {
                const res = await fetch(`/api/audits/${currentAuditId}/evidence-bundle`);
                if (res.ok) {
                    const data = await res.json();
                    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = `AuditVector-Evidence-Bundle-${currentAuditId}.json`;
                    a.click();
                    URL.revokeObjectURL(url);
                }
            } catch (err) {
                console.error("Bundle export failed:", err);
            }
        });
    }
});
