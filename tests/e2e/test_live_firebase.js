const puppeteer = require('puppeteer');

(async () => {
    let browser;
    try {
        console.log("Connecting to LIVE Firebase Hosting URL: https://auditvector-20610.web.app ...");
        browser = await puppeteer.launch({
            headless: "new",
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        });
        const page = await browser.newPage();
        await page.setViewport({ width: 1440, height: 900 });

        const consoleErrors = [];
        page.on('console', msg => {
            if (msg.type() === 'error') {
                consoleErrors.push(msg.text());
                console.error(`Live Browser Error: ${msg.text()}`);
            }
        });

        await page.goto("https://auditvector-20610.web.app", { waitUntil: 'networkidle0' });
        console.log("✅ Live Page loaded successfully.");

        // 1. Launch Alpha Benchmark
        console.log("Testing Live Alpha Benchmark...");
        await page.click('#btn-launch-alpha');
        await page.waitForSelector('#screen-verdict:not(.hidden-screen)', { timeout: 10000 });

        let vHead = await page.$eval('#verdict-headline', el => el.textContent.trim());
        let fis = await page.$eval('#final-fis-score', el => el.textContent.trim());
        let cap = await page.$eval('#final-capital-discrepancy', el => el.textContent.trim());
        let fBadge = await page.$eval('#tab-findings-badge', el => el.textContent.trim());
        let rBadge = await page.$eval('#tab-remediation-badge', el => el.textContent.trim());

        console.log(`Live Alpha: Verdict='${vHead}', FIS='${fis}', Discrepancy='${cap}', Findings='${fBadge}', Remediation='${rBadge}'`);

        // Test Tab Switching on Live
        await page.click('button[data-target="panel-remediation"]');
        let remActive = await page.$eval('#panel-remediation', el => window.getComputedStyle(el).display !== 'none');
        let findHidden = await page.$eval('#panel-findings', el => window.getComputedStyle(el).display === 'none');
        let remCards = await page.$$eval('#remediation-cards-list .remediation-card', els => els.length);
        console.log(`Live Alpha Remediation Tab: visible=${remActive}, findingsHidden=${findHidden}, patchCards=${remCards}`);

        // 2. Launch Control Benchmark
        console.log("Testing Live Control Benchmark & State Isolation...");
        await page.click('#btn-header-new-audit');
        await page.waitForSelector('#screen-launchpad:not(.hidden-screen)');
        await page.click('#btn-launch-control');
        await page.waitForSelector('#screen-verdict:not(.hidden-screen)', { timeout: 10000 });

        vHead = await page.$eval('#verdict-headline', el => el.textContent.trim());
        fis = await page.$eval('#final-fis-score', el => el.textContent.trim());
        cap = await page.$eval('#final-capital-discrepancy', el => el.textContent.trim());
        fBadge = await page.$eval('#tab-findings-badge', el => el.textContent.trim());
        rBadge = await page.$eval('#tab-remediation-badge', el => el.textContent.trim());

        console.log(`Live Control: Verdict='${vHead}', FIS='${fis}', Discrepancy='${cap}', Findings='${fBadge}', Remediation='${rBadge}'`);

        await page.click('button[data-target="panel-remediation"]');
        remActive = await page.$eval('#panel-remediation', el => window.getComputedStyle(el).display !== 'none');
        findHidden = await page.$eval('#panel-findings', el => window.getComputedStyle(el).display === 'none');
        remCards = await page.$$eval('#remediation-cards-list .remediation-card', els => els.length);
        let remEmptyText = await page.$eval('#remediation-cards-list', el => el.textContent);
        console.log(`Live Control Remediation Tab: visible=${remActive}, patchCards=${remCards} (Clean empty state=${remEmptyText.includes('Zero code remediation required')})`);

        if (remCards !== 0) throw new Error("Control leaked Alpha remediation cards!");

        // 3. Launch AI-BIP Benchmark
        console.log("Testing Live AI-BIP Benchmark...");
        await page.click('#btn-header-new-audit');
        await page.waitForSelector('#screen-launchpad:not(.hidden-screen)');
        await page.click('#btn-launch-aibip');
        await page.waitForSelector('#screen-verdict:not(.hidden-screen)', { timeout: 10000 });

        vHead = await page.$eval('#verdict-headline', el => el.textContent.trim());
        fis = await page.$eval('#final-fis-score', el => el.textContent.trim());
        cap = await page.$eval('#final-capital-discrepancy', el => el.textContent.trim());
        fBadge = await page.$eval('#tab-findings-badge', el => el.textContent.trim());
        rBadge = await page.$eval('#tab-remediation-badge', el => el.textContent.trim());

        console.log(`Live AI-BIP: Verdict='${vHead}', FIS='${fis}', Discrepancy='${cap}', Findings='${fBadge}', Remediation='${rBadge}'`);

        console.log("\n🚀 LIVE FIREBASE HOSTING URL CERTIFICATION SUCCESSFUL!");
    } catch (e) {
        console.error("❌ Live verification failed:", e);
        process.exitCode = 1;
    } finally {
        if (browser) await browser.close();
    }
})();
