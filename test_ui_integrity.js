const puppeteer = require('puppeteer');
const http = require('http');
const fs = require('fs');
const path = require('path');

// Simple static file server for local testing
const server = http.createServer((req, res) => {
    if (req.url === '/favicon.ico') {
        res.writeHead(204);
        res.end();
        return;
    }
    let filePath = path.join(__dirname, 'frontend', req.url === '/' ? 'index.html' : req.url);
    if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
        const ext = path.extname(filePath);
        const contentTypes = {
            '.html': 'text/html',
            '.js': 'text/javascript',
            '.css': 'text/css',
            '.json': 'application/json',
            '.png': 'image/png'
        };
        res.writeHead(200, { 'Content-Type': contentTypes[ext] || 'text/plain' });
        fs.createReadStream(filePath).pipe(res);
    } else {
        console.log(`[404 on Server]: ${req.url}`);
        res.writeHead(404);
        res.end('Not found');
    }
});

server.listen(0, async () => {
    const port = server.address().port;
    console.log(`Test server running at http://localhost:${port}`);
    let browser;
    try {
        browser = await puppeteer.launch({ 
            headless: "new",
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        });
        const page = await browser.newPage();
        await page.setViewport({ width: 1440, height: 900 });

        // Listen for console errors
        const consoleErrors = [];
        page.on('console', msg => {
            if (msg.type() === 'error') {
                consoleErrors.push(msg.text());
                console.error(`Browser Console Error: ${msg.text()}`);
            }
        });
        page.on('pageerror', err => {
            consoleErrors.push(err.toString());
            console.error(`Browser Page Error: ${err.toString()}`);
        });

        await page.goto(`http://localhost:${port}`, { waitUntil: 'networkidle0' });
        console.log("✅ Page loaded successfully");

        // TEST 1: ALPHA BENCHMARK
        console.log("\n=== TEST 1: LAUNCHING ALPHA BENCHMARK ===");
        await page.click('#btn-launch-alpha');
        await page.waitForSelector('#screen-verdict:not(.hidden-screen)', { timeout: 8000 });

        let verdictHeadline = await page.$eval('#verdict-headline', el => el.textContent.trim());
        let fisScore = await page.$eval('#final-fis-score', el => el.textContent.trim());
        let capitalDiscrepancy = await page.$eval('#final-capital-discrepancy', el => el.textContent.trim());
        let findingsBadge = await page.$eval('#tab-findings-badge', el => el.textContent.trim());
        let remediationBadge = await page.$eval('#tab-remediation-badge', el => el.textContent.trim());

        console.log(`Alpha Verdict: ${verdictHeadline} | FIS: ${fisScore} | Discrepancy: ${capitalDiscrepancy}`);
        console.log(`Alpha Findings Badge: ${findingsBadge} | Remediation Badge: ${remediationBadge}`);

        if (!verdictHeadline.includes('RESULTS NOT FULLY TRUSTWORTHY') && !verdictHeadline.includes('CONTRADICTION')) {
            throw new Error(`Alpha expected failure verdict, got ${verdictHeadline}`);
        }
        if (fisScore !== '0 / 100') throw new Error(`Alpha expected FIS 0 / 100, got ${fisScore}`);
        if (capitalDiscrepancy !== '$44,140.00') throw new Error(`Alpha expected $44,140.00, got ${capitalDiscrepancy}`);
        if (findingsBadge !== '4') throw new Error(`Alpha expected 4 findings, got ${findingsBadge}`);
        if (remediationBadge !== '4') throw new Error(`Alpha expected 4 remediation plans, got ${remediationBadge}`);

        // Test Alpha Tabs Synchronization
        console.log("Testing Alpha Tab Transitions...");
        
        // Tab 1: Findings visible by default
        let isFindingsActive = await page.$eval('#panel-findings', el => el.classList.contains('active') && el.classList.contains('active-tab'));
        let isRemediationActive = await page.$eval('#panel-remediation', el => el.classList.contains('active') || el.classList.contains('active-tab'));
        if (!isFindingsActive || isRemediationActive) throw new Error("Initial tab is not panel-findings!");

        // Switch to Remediation Tab
        console.log("Clicking Autonomous Remediation tab...");
        await page.click('button[data-target="panel-remediation"]');
        let remActive = await page.$eval('#panel-remediation', el => window.getComputedStyle(el).display !== 'none');
        let findActive = await page.$eval('#panel-findings', el => window.getComputedStyle(el).display === 'none');
        let remCards = await page.$$eval('#remediation-cards-list .remediation-card', els => els.length);
        console.log(`Remediation Panel Display: visible=${remActive}, Findings hidden=${findActive}, Cards rendered=${remCards}`);
        if (!remActive || !findActive || remCards !== 4) throw new Error(`Remediation tab sync failure! remActive=${remActive}, findActive=${findActive}, remCards=${remCards}`);

        // Switch to Replay Tab
        console.log("Clicking Audit Replay tab...");
        await page.click('button[data-target="panel-replay"]');
        let replayActive = await page.$eval('#panel-replay', el => window.getComputedStyle(el).display !== 'none');
        let decisionsCount = await page.$$eval('#adaptive-decisions-list .decision-card', els => els.length);
        console.log(`Replay Panel Display: visible=${replayActive}, Adaptive Decisions=${decisionsCount}`);
        if (!replayActive || decisionsCount !== 5) throw new Error(`Replay tab sync failure! replayActive=${replayActive}, decisionsCount=${decisionsCount}`);

        // TEST 2: SWITCH TO CONTROL BENCHMARK
        console.log("\n=== TEST 2: SWITCHING TO CONTROL BENCHMARK ===");
        await page.click('#btn-header-new-audit');
        await page.waitForSelector('#screen-launchpad:not(.hidden-screen)');
        await page.click('#btn-launch-control');
        await page.waitForSelector('#screen-verdict:not(.hidden-screen)', { timeout: 8000 });

        verdictHeadline = await page.$eval('#verdict-headline', el => el.textContent.trim());
        fisScore = await page.$eval('#final-fis-score', el => el.textContent.trim());
        capitalDiscrepancy = await page.$eval('#final-capital-discrepancy', el => el.textContent.trim());
        findingsBadge = await page.$eval('#tab-findings-badge', el => el.textContent.trim());
        remediationBadge = await page.$eval('#tab-remediation-badge', el => el.textContent.trim());

        console.log(`Control Verdict: ${verdictHeadline} | FIS: ${fisScore} | Discrepancy: ${capitalDiscrepancy}`);
        console.log(`Control Findings Badge: ${findingsBadge} | Remediation Badge: ${remediationBadge}`);

        if (!verdictHeadline.includes('FINANCIAL INTEGRITY VERIFIED')) throw new Error(`Control expected FINANCIAL INTEGRITY VERIFIED, got ${verdictHeadline}`);
        if (fisScore !== '100 / 100') throw new Error(`Control expected FIS 100 / 100, got ${fisScore}`);
        if (capitalDiscrepancy !== '$0.00') throw new Error(`Control expected $0.00, got ${capitalDiscrepancy}`);
        if (findingsBadge !== '1' && findingsBadge !== '0') throw new Error(`Control expected 0 or 1 findings, got ${findingsBadge}`);
        if (remediationBadge !== '0') throw new Error(`Control expected 0 remediation, got ${remediationBadge}`);

        // Test Control Tab Synchronization & Zero State Leakage
        console.log("Testing Control Tab Transitions & Zero State Leakage...");
        await page.click('button[data-target="panel-remediation"]');
        remActive = await page.$eval('#panel-remediation', el => window.getComputedStyle(el).display !== 'none');
        findActive = await page.$eval('#panel-findings', el => window.getComputedStyle(el).display === 'none');
        remCards = await page.$$eval('#remediation-cards-list .remediation-card', els => els.length);
        let remText = await page.$eval('#remediation-cards-list', el => el.textContent);
        console.log(`Control Remediation: visible=${remActive}, Cards count=${remCards} (Should be 0, Clean empty state)`);
        if (!remActive || !findActive || remCards !== 0 || !remText.includes('Zero code remediation required')) {
            throw new Error(`Control Remediation leaked Alpha cards or failed empty state! remCards=${remCards}`);
        }

        // Test Control Replay
        await page.click('button[data-target="panel-replay"]');
        decisionsCount = await page.$$eval('#adaptive-decisions-list .decision-card', els => els.length);
        console.log(`Control Adaptive Decisions count: ${decisionsCount} (Expected 4, skipping remediation)`);
        if (decisionsCount !== 4) throw new Error(`Control Replay expected 4 decisions, got ${decisionsCount}`);

        // TEST 3: SWITCH TO AI-BIP BENCHMARK
        console.log("\n=== TEST 3: SWITCHING TO AI-BIP BENCHMARK ===");
        await page.click('#btn-header-new-audit');
        await page.waitForSelector('#screen-launchpad:not(.hidden-screen)');
        await page.click('#btn-launch-aibip');
        await page.waitForSelector('#screen-verdict:not(.hidden-screen)', { timeout: 8000 });

        verdictHeadline = await page.$eval('#verdict-headline', el => el.textContent.trim());
        fisScore = await page.$eval('#final-fis-score', el => el.textContent.trim());
        capitalDiscrepancy = await page.$eval('#final-capital-discrepancy', el => el.textContent.trim());
        findingsBadge = await page.$eval('#tab-findings-badge', el => el.textContent.trim());
        remediationBadge = await page.$eval('#tab-remediation-badge', el => el.textContent.trim());

        console.log(`AI-BIP Verdict: ${verdictHeadline} | FIS: ${fisScore} | Discrepancy: ${capitalDiscrepancy}`);
        console.log(`AI-BIP Findings Badge: ${findingsBadge} | Remediation Badge: ${remediationBadge}`);

        if (!verdictHeadline.includes('RESULTS NOT FULLY TRUSTWORTHY') && !verdictHeadline.includes('CONTRADICTION')) {
            throw new Error(`AI-BIP expected failure verdict, got ${verdictHeadline}`);
        }
        if (fisScore !== '65.5 / 100') throw new Error(`AI-BIP expected FIS 65.5 / 100, got ${fisScore}`);
        if (capitalDiscrepancy !== '$16,286.24') throw new Error(`AI-BIP expected $16,286.24, got ${capitalDiscrepancy}`);
        if (findingsBadge !== '2') throw new Error(`AI-BIP expected 2 findings, got ${findingsBadge}`);
        if (remediationBadge !== '2') throw new Error(`AI-BIP expected 2 remediation plans, got ${remediationBadge}`);

        // TEST 4: RAPID TRANSITION SEQUENCE (Alpha -> Control -> AI-BIP -> Control -> Alpha)
        console.log("\n=== TEST 4: RAPID ROUND-TRIP TRANSITIONS ===");
        const sequence = ['control', 'alpha', 'aibip', 'control', 'alpha'];
        for (const target of sequence) {
            console.log(`Transitioning to ${target}...`);
            await page.click('#btn-header-new-audit');
            await page.waitForSelector('#screen-launchpad:not(.hidden-screen)');
            await page.click(`#btn-launch-${target}`);
            await page.waitForSelector('#screen-verdict:not(.hidden-screen)', { timeout: 8000 });
            
            const badge = await page.$eval('#tab-findings-badge', el => el.textContent.trim());
            const remBadge = await page.$eval('#tab-remediation-badge', el => el.textContent.trim());
            const expectedF = target === 'alpha' ? '4' : target === 'control' ? '1' : '2';
            const expectedR = target === 'alpha' ? '4' : target === 'control' ? '0' : '2';
            
            if (badge !== expectedF || remBadge !== expectedR) {
                throw new Error(`State leak on rapid transition to ${target}! Expected F=${expectedF}, R=${expectedR}, got F=${badge}, R=${remBadge}`);
            }
        }
        console.log("✅ All rapid round-trip transitions completed with ZERO state leakage!");

        if (consoleErrors.length > 0) {
            throw new Error(`Console errors observed during test: ${consoleErrors.join(', ')}`);
        }

        console.log("\n🎉 ALL UI INTEGRITY TESTS PASSED WITH 100% SUCCESS!");
    } catch (err) {
        console.error("❌ TEST FAILED:", err);
        process.exitCode = 1;
    } finally {
        if (browser) await browser.close();
        server.close();
    }
});
