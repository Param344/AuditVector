const puppeteer = require('puppeteer');

(async () => {
    let browser;
    try {
        console.log("=== FINAL JUDGE WALKTHROUGH SIMULATION ===");
        console.log("Target URL: https://auditvector-20610.web.app");
        
        browser = await puppeteer.launch({
            headless: "new",
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        });
        const page = await browser.newPage();
        await page.setViewport({ width: 1440, height: 900 });

        // Collect console messages
        const logs = [];
        page.on('console', msg => logs.push(`[Browser ${msg.type()}]: ${msg.text()}`));

        // 1. Landing Page / Launchpad
        console.log("\n[STEP 1] Opening Landing Page...");
        const t0 = Date.now();
        await page.goto("https://auditvector-20610.web.app", { waitUntil: 'networkidle0' });
        const loadTime = Date.now() - t0;
        console.log(`Page loaded in ${loadTime}ms`);

        // Check Landing Page Headings & Branding
        const brandTitle = await page.$eval('h1, .hero-headline, .brand-text-lg, title', el => el.textContent.trim());
        console.log(`Brand title / Title tag: "${brandTitle}"`);

        // 2. Launch Alpha Failure Benchmark
        console.log("\n[STEP 2] Clicking 'IntegrityLab-Alpha'...");
        await page.click('#btn-launch-alpha');
        
        // Investigation Stepper view
        await page.waitForSelector('#screen-investigation:not(.hidden-screen)', { timeout: 5000 });
        console.log("Investigation screen displayed. Stepper progress and live telemetry active.");
        
        // Wait for Verdict Workspace
        await page.waitForSelector('#screen-verdict:not(.hidden-screen)', { timeout: 10000 });
        console.log("Alpha Investigation complete. Verdict workspace loaded.");

        // Inspect Alpha Verdict & Claim vs Reality Hero
        const alphaVerdict = await page.$eval('#verdict-headline', el => el.textContent.trim());
        const alphaDiscrepancy = await page.$eval('#final-capital-discrepancy', el => el.textContent.trim());
        const alphaClaimPnl = await page.$eval('#claimed-pnl-val', el => el.textContent.trim());
        const alphaRealPnl = await page.$eval('#reality-pnl-val', el => el.textContent.trim());
        const alphaDeltaVal = await page.$eval('#variance-delta-val', el => el.textContent.trim());
        const alphaDeltaDesc = await page.$eval('.comparison-delta-card .delta-desc', el => el.textContent.trim());

        console.log(`Alpha Verdict: ${alphaVerdict}`);
        console.log(`Alpha Capital Discrepancy Stat: ${alphaDiscrepancy}`);
        console.log(`Claimed PnL: ${alphaClaimPnl} vs Reconstructed PnL: ${alphaRealPnl}`);
        console.log(`Variance Delta: ${alphaDeltaVal}`);
        console.log(`Delta Description & Sandbox tag: "${alphaDeltaDesc}"`);

        // 3. Inspect Findings & "WHY?" Provenance Chain
        console.log("\n[STEP 3] Inspecting Findings Explorer & WHY Evidence Chain...");
        const findingsCards = await page.$$eval('#findings-cards-list .finding-row-card', cards => {
            return cards.map(c => {
                const id = c.querySelector('.finding-id-tag')?.textContent.trim();
                const title = c.querySelector('.finding-title-text')?.textContent.trim();
                const claim = c.querySelector('.diff-col.claim strong')?.textContent.trim();
                const proof = c.querySelector('.diff-col.reality strong')?.textContent.trim();
                const whySteps = Array.from(c.querySelectorAll('.why-step-item')).map(s => s.textContent.replace(/\s+/g, ' ').trim());
                return { id, title, claim, proof, whyStepsCount: whySteps.length, sampleWhy: whySteps[0] };
            });
        });

        console.log(`Total Findings Rendered: ${findingsCards.length}`);
        findingsCards.forEach(f => {
            console.log(` - Finding [${f.id}]: "${f.title}" | WHY steps: ${f.whyStepsCount}`);
        });

        // 4. Click 'INSPECT EVIDENCE CONTRACT' button on finding 1
        console.log("\n[STEP 4] Opening Slide-Out Forensic Evidence Inspector...");
        await page.click('#findings-cards-list .btn-inspect-finding');
        await page.waitForSelector('#inspector-drawer:not(.hidden-drawer)', { timeout: 2000 });
        
        const drawerTitle = await page.$eval('#drawer-finding-title', el => el.textContent.trim());
        const drawerReported = await page.$eval('#drawer-val-reported', el => el.textContent.trim());
        const drawerReconstructed = await page.$eval('#drawer-val-reconstructed', el => el.textContent.trim());
        const drawerVariance = await page.$eval('#drawer-val-variance', el => el.textContent.trim());
        const drawerVerifier = await page.$eval('#drawer-prov-verifier', el => el.textContent.trim());
        const drawerMethod = await page.$eval('#drawer-prov-method', el => el.textContent.trim());
        const drawerHash = await page.$eval('#drawer-prov-hash', el => el.textContent.trim());

        console.log(`Drawer Finding: "${drawerTitle}"`);
        console.log(`Reported: ${drawerReported} | Reconstructed: ${drawerReconstructed} | Variance: ${drawerVariance}`);
        console.log(`Verifier Engine: ${drawerVerifier} | Method: ${drawerMethod}`);
        console.log(`Cryptographic Hash Anchor: ${drawerHash}`);

        // Close Drawer
        await page.click('#btn-close-drawer');

        // 5. Inspect Autonomous Remediation Sandbox Tab
        console.log("\n[STEP 5] Switching to Autonomous Remediation Sandbox Tab...");
        await page.click('button[data-target="panel-remediation"]');
        const remCards = await page.$$eval('#remediation-cards-list .remediation-card', cards => {
            return cards.map(c => {
                const target = c.querySelector('.remediation-target-file')?.textContent.trim();
                const pre = c.querySelector('.patch-metric-item:nth-child(1) strong')?.textContent.trim();
                const post = c.querySelector('.patch-metric-item:nth-child(2) strong')?.textContent.trim();
                const tests = c.querySelector('.patch-metric-item:nth-child(3) strong')?.textContent.trim();
                const targetFinding = c.querySelector('.patch-metric-item:nth-child(4) strong')?.textContent.trim();
                return { target, pre, post, tests, targetFinding };
            });
        });

        console.log(`Remediation Plans Rendered: ${remCards.length}`);
        remCards.forEach((r, idx) => {
            console.log(` - Patch #${idx+1} [${r.targetFinding}]: ${r.target}`);
            console.log(`   Pre-Patch Variance: ${r.pre} ➔ Post-Patch Variance: ${r.post}`);
            console.log(`   Sandbox Regression: ${r.tests}`);
        });

        // 6. Inspect Control Clean Baseline Benchmark
        console.log("\n[STEP 6] Switching to Control Clean Baseline...");
        await page.click('#btn-header-new-audit');
        await page.waitForSelector('#screen-launchpad:not(.hidden-screen)');
        await page.click('#btn-launch-control');
        await page.waitForSelector('#screen-verdict:not(.hidden-screen)', { timeout: 10000 });

        const ctrlVerdict = await page.$eval('#verdict-headline', el => el.textContent.trim());
        const ctrlFis = await page.$eval('#final-fis-score', el => el.textContent.trim());
        const ctrlDiscrepancy = await page.$eval('#final-capital-discrepancy', el => el.textContent.trim());
        const ctrlFindingsBadge = await page.$eval('#tab-findings-badge', el => el.textContent.trim());
        const ctrlRemBadge = await page.$eval('#tab-remediation-badge', el => el.textContent.trim());

        console.log(`Control Verdict: ${ctrlVerdict}`);
        console.log(`Control FIS Score: ${ctrlFis} | Discrepancy: ${ctrlDiscrepancy}`);
        console.log(`Control Badges: Findings=${ctrlFindingsBadge}, Remediation=${ctrlRemBadge}`);

        // Check Control Remediation Tab
        await page.click('button[data-target="panel-remediation"]');
        const ctrlRemText = await page.$eval('#remediation-cards-list', el => el.textContent.trim());
        console.log(`Control Remediation Message: "${ctrlRemText.replace(/\s+/g, ' ')}"`);

        // 7. Inspect AI-BIP Quantitative Strategy Dogfood
        console.log("\n[STEP 7] Switching to AI-BIP Quantitative Strategy Dogfood...");
        await page.click('#btn-header-new-audit');
        await page.waitForSelector('#screen-launchpad:not(.hidden-screen)');
        await page.click('#btn-launch-aibip');
        await page.waitForSelector('#screen-verdict:not(.hidden-screen)', { timeout: 10000 });

        const aibipVerdict = await page.$eval('#verdict-headline', el => el.textContent.trim());
        const aibipFis = await page.$eval('#final-fis-score', el => el.textContent.trim());
        const aibipDiscrepancy = await page.$eval('#final-capital-discrepancy', el => el.textContent.trim());
        const aibipClaimPnl = await page.$eval('#claimed-pnl-val', el => el.textContent.trim());
        const aibipRealPnl = await page.$eval('#reality-pnl-val', el => el.textContent.trim());
        const aibipDeltaVal = await page.$eval('#variance-delta-val', el => el.textContent.trim());

        console.log(`AI-BIP Verdict: ${aibipVerdict}`);
        console.log(`AI-BIP FIS Score: ${aibipFis} | Discrepancy: ${aibipDiscrepancy}`);
        console.log(`AI-BIP Claimed PnL: ${aibipClaimPnl} vs Reconstructed: ${aibipRealPnl} (Variance: ${aibipDeltaVal})`);

        // 8. Inspect Audit Replay & Adaptive Decisions Log
        console.log("\n[STEP 8] Inspecting Audit Replay & Adaptive Decisions Tab...");
        await page.click('button[data-target="panel-replay"]');
        const replayStep = await page.$eval('#replay-step-label', el => el.textContent.trim());
        const replayCard = await page.$eval('#replay-stage-viewer', el => el.textContent.trim().replace(/\s+/g, ' '));
        const adaptiveDecisions = await page.$$eval('#adaptive-decisions-list .decision-card', cards => {
            return cards.map(c => {
                const tag = c.querySelector('.decision-agent-tag')?.textContent.trim();
                const badge = c.querySelector('.decision-action-badge')?.textContent.trim();
                const reasoning = c.querySelector('.decision-reasoning')?.textContent.trim();
                return { tag, badge, reasoning };
            });
        });

        console.log(`Replay Initial Step: ${replayStep}`);
        console.log(`Replay Stage Snapshot: "${replayCard}"`);
        console.log(`Adaptive Routing Decisions Count: ${adaptiveDecisions.length}`);
        adaptiveDecisions.forEach(d => {
            console.log(` - ${d.tag} | Action: ${d.badge}`);
        });

        // 9. Inspect Executive Audit Report Tab
        console.log("\n[STEP 9] Inspecting Executive Report Tab...");
        await page.click('button[data-target="panel-report"]');
        const reportSnippet = await page.$eval('#markdown-report-container', el => el.textContent.slice(0, 300).replace(/\s+/g, ' '));
        console.log(`Report Markdown Snippet: "${reportSnippet}..."`);

        console.log("\n=== WALKTHROUGH COMPLETE ===");
    } catch (err) {
        console.error("Walkthrough error:", err);
    } finally {
        if (browser) await browser.close();
    }
})();
