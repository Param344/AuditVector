const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const outputDir = path.join(__dirname, 'docs', 'screenshots');
const artifactDir = '/Users/paramjeetsingh/.gemini/antigravity-cli/brain/161fde66-4dec-4965-b6aa-912a394f0c19';

if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

(async () => {
    let browser;
    try {
        console.log("Launching Puppeteer for High-Resolution Devpost Screenshot Capture...");
        browser = await puppeteer.launch({
            headless: "new",
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--window-size=1920,1080']
        });
        const page = await browser.newPage();
        await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 }); // 2x Retina quality

        const saveScreenshot = async (filename, description) => {
            const outPath = path.join(outputDir, filename);
            const artPath = path.join(artifactDir, filename);
            await page.screenshot({ path: outPath, fullPage: false });
            fs.copyFileSync(outPath, artPath);
            console.log(`📸 Captured [${filename}]: ${description}`);
        };

        // 1. Landing Page / Launchpad
        console.log("Navigating to https://auditvector-20610.web.app ...");
        await page.goto("https://auditvector-20610.web.app", { waitUntil: 'networkidle0' });
        await new Promise(r => setTimeout(r, 600));
        await saveScreenshot('01_landing_launchpad.png', 'Mission Launchpad & Benchmark Cards');

        // 2. Live Investigation Stepper (Alpha Launch)
        await page.click('#btn-launch-alpha');
        await page.waitForSelector('#screen-investigation:not(.hidden-screen)');
        await new Promise(r => setTimeout(r, 700)); // capture during active stepper
        await saveScreenshot('02_live_multiagent_stepper.png', '6-Agent ADK Live Investigation Stepper & Telemetry Stream');

        // Wait for Alpha Verdict Workspace
        await page.waitForSelector('#screen-verdict:not(.hidden-screen)', { timeout: 10000 });
        await new Promise(r => setTimeout(r, 600));

        // 3. Alpha Verdict & Claim vs Reality Hero Card
        await saveScreenshot('03_alpha_verdict_claim_vs_reality.png', 'Alpha Failure Verdict ($44,276.75 Discrepancy & Claim vs Deterministic Reality Hero)');

        // 4. Tab 1: Verified Findings with WHY Traversal
        await page.click('button[data-target="panel-findings"]');
        await new Promise(r => setTimeout(r, 400));
        // Scroll down slightly to show the findings and WHY traversal prominently
        await page.evaluate(() => window.scrollBy({ top: 380, behavior: 'instant' }));
        await new Promise(r => setTimeout(r, 400));
        await saveScreenshot('04_verified_findings_why_traversal.png', 'Verified Findings Explorer & Interactive WHY Evidence Traversal');

        // 5. Tab 2: Autonomous Remediation Sandbox ($21,960 -> $0)
        await page.evaluate(() => window.scrollTo({ top: 350, behavior: 'instant' }));
        await page.click('button[data-target="panel-remediation"]');
        await new Promise(r => setTimeout(r, 500));
        await saveScreenshot('05_autonomous_remediation_sandbox.png', 'Autonomous Remediation Sandbox ($21,960 to $0 Discrepancy Reduction & Unified Diffs)');

        // 6. Forensic Evidence Inspector Drawer
        await page.click('button[data-target="panel-findings"]');
        await new Promise(r => setTimeout(r, 300));
        await page.click('#findings-cards-list .btn-inspect-finding');
        await page.waitForSelector('#inspector-drawer:not(.hidden-drawer)');
        await new Promise(r => setTimeout(r, 500));
        await saveScreenshot('06_forensic_evidence_drawer.png', 'Slide-out Forensic Evidence Inspector & Cryptographic Anchors');
        await page.click('#btn-close-drawer');
        await new Promise(r => setTimeout(r, 300));

        // 7. Tab 3: Audit Replay & Adaptive Decisions Log
        await page.evaluate(() => window.scrollTo({ top: 350, behavior: 'instant' }));
        await page.click('button[data-target="panel-replay"]');
        await new Promise(r => setTimeout(r, 500));
        await saveScreenshot('07_audit_replay_adaptive_decisions.png', 'Audit Replay Controller & ADK Adaptive Routing Decision Log');

        // 8. Tab 4: Interactive Evidence Provenance Graph
        await page.click('button[data-target="panel-graph"]');
        await new Promise(r => setTimeout(r, 500));
        await saveScreenshot('08_cryptographic_provenance_graph.png', 'Interactive Cryptographic Provenance Graph (Source to Finding Contracts)');

        // 9. Control Clean Baseline (100/100 FIS Score, 0 False Positives)
        await page.click('#btn-header-new-audit');
        await page.waitForSelector('#screen-launchpad:not(.hidden-screen)');
        await page.click('#btn-launch-control');
        await page.waitForSelector('#screen-verdict:not(.hidden-screen)', { timeout: 10000 });
        await new Promise(r => setTimeout(r, 600));
        await saveScreenshot('09_control_clean_baseline_100_fis.png', 'Control Clean Baseline (100/100 FIS Score Grade A+ & 0 False Positives)');

        // 10. AI-BIP Quantitative Engine Dogfood ($16,286.24 Discrepancy)
        await page.click('#btn-header-new-audit');
        await page.waitForSelector('#screen-launchpad:not(.hidden-screen)');
        await page.click('#btn-launch-aibip');
        await page.waitForSelector('#screen-verdict:not(.hidden-screen)', { timeout: 10000 });
        await new Promise(r => setTimeout(r, 600));
        await saveScreenshot('10_aibip_quantitative_dogfood.png', 'AI-BIP Real Dogfood ($16,286.24 Discrepancy / 30.0484% Profit Erosion)');

        console.log("\n🎉 ALL 10 DEVPOST SCREENSHOTS CAPTURED SUCCESSFULLY IN HIGH RESOLUTION (2X RETINA)!");
    } catch (err) {
        console.error("Screenshot capture failed:", err);
        process.exitCode = 1;
    } finally {
        if (browser) await browser.close();
    }
})();
