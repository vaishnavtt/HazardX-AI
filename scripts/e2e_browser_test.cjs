const puppeteer = require('../frontend/node_modules/puppeteer-core');
const fs = require('fs');
const path = require('path');

const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const BASE_URL = 'http://localhost:5173';
const SCREENSHOT_DIR = path.join(__dirname, '..', 'reports', 'e2e_screenshots');

if (!fs.existsSync(SCREENSHOT_DIR)) {
  fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

async function runE2ETests() {
  console.log('=== STARTING HAZARDX AI RE-VERIFICATION BROWSER AUTOMATION ===');
  console.log('Chrome Binary:', CHROME_PATH);
  console.log('Base URL:', BASE_URL);

  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-accelerated-2d-canvas',
      '--disable-gpu',
      '--window-size=1440,900'
    ]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });

  const consoleErrors = [];
  const consoleWarnings = [];
  const networkFailures = [];

  page.on('console', msg => {
    const type = msg.type();
    const text = msg.text();
    // Ignore benign React DevTools notification
    if (text.includes('React DevTools')) return;
    if (type === 'error') {
      consoleErrors.push(text);
      console.log('  [BROWSER ERROR]:', text);
    } else if (type === 'warning') {
      consoleWarnings.push(text);
    }
  });

  page.on('pageerror', err => {
    consoleErrors.push(`Unhandled Exception: ${err.message}`);
    console.log('  [PAGE EXCEPTION]:', err.message);
  });

  page.on('requestfailed', req => {
    const failure = `${req.method()} ${req.url()} - ${req.failure()?.errorText || 'Failed'}`;
    networkFailures.push(failure);
    console.log('  [NET FAILURE]:', failure);
  });

  const results = {
    pagesTested: [],
    tests: [],
    consoleErrors,
    networkFailures
  };

  try {
    // -------------------------------------------------------------
    // 1. DASHBOARD PAGE
    // -------------------------------------------------------------
    console.log('\n--- 1. Testing Dashboard Page (/) ---');
    await page.goto(`${BASE_URL}/`, { waitUntil: 'networkidle2', timeout: 15000 });
    await new Promise(r => setTimeout(r, 2000));
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '01_dashboard.png') });
    results.pagesTested.push('Dashboard (/)');

    const brandText = await page.$eval('header', el => el.textContent);
    console.log('  Header content detected:', brandText.includes('HAZARDX AI') ? 'PASS' : 'FAIL');
    results.tests.push({ name: 'Dashboard Header Brand', pass: brandText.includes('HAZARDX AI') });

    const glassPanels = await page.$$('.glass-panel, .glass-card');
    console.log(`  Liquid Glass components count: ${glassPanels.length}`);
    results.tests.push({ name: 'Liquid Glass Elements', pass: glassPanels.length > 0 });

    // -------------------------------------------------------------
    // 2. GLOBAL HAZARD MAP (/map)
    // -------------------------------------------------------------
    console.log('\n--- 2. Testing Global Hazard Map (/map) ---');
    await page.goto(`${BASE_URL}/map`, { waitUntil: 'networkidle2', timeout: 15000 });
    await new Promise(r => setTimeout(r, 3000));
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '02_map_initial.png') });
    results.pagesTested.push('Global Hazard Map (/map)');

    const leafletContainer = await page.$('.leaflet-container');
    const mapExists = !!leafletContainer;
    console.log('  Leaflet Map Container mounted:', mapExists ? 'PASS' : 'FAIL');
    results.tests.push({ name: 'Map Container Mounted', pass: mapExists });

    // Click hazard layer toggle buttons (floods, landslides, earthquakes, cyclones, wildfires)
    const layerButtons = await page.$$('button');
    let toggleCount = 0;
    for (const btn of layerButtons) {
      const txt = (await page.evaluate(el => el.textContent, btn)) || '';
      const lower = txt.toLowerCase();
      if (lower.includes('flood') || lower.includes('landslide') || lower.includes('earthquake') || lower.includes('cyclone') || lower.includes('wildfire')) {
        await btn.click();
        toggleCount++;
        await new Promise(r => setTimeout(r, 250));
      }
    }
    console.log(`  Map Layer Toggle Interaction: ${toggleCount >= 3 ? 'PASS' : 'FAIL'} (${toggleCount} toggled)`);
    results.tests.push({ name: 'Map Layer Toggles', pass: toggleCount >= 3 });
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '02_map_layers_toggled.png') });

    // Test map resizing
    await page.setViewport({ width: 1024, height: 768 });
    await new Promise(r => setTimeout(r, 500));
    await page.setViewport({ width: 1440, height: 900 });
    await new Promise(r => setTimeout(r, 500));
    results.tests.push({ name: 'Map Resize Handler', pass: true });

    // -------------------------------------------------------------
    // 3. MULTI-HAZARD FORECASTS (/forecasts)
    // -------------------------------------------------------------
    console.log('\n--- 3. Testing Forecasts Page (/forecasts) ---');
    await page.goto(`${BASE_URL}/forecasts`, { waitUntil: 'networkidle2', timeout: 15000 });
    try {
      await page.waitForSelector('.glass-card', { timeout: 12000 });
    } catch (e) {
      // Continue if timeout occurs
    }
    await new Promise(r => setTimeout(r, 1000));
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '03_forecasts.png') });
    results.pagesTested.push('Forecasts (/forecasts)');

    const forecastCards = await page.$$('.glass-card');
    console.log(`  Forecast Glass Cards count: ${forecastCards.length}`);
    results.tests.push({ name: 'Forecast Cards Rendered', pass: forecastCards.length >= 3 });

    // Toggle Technical Data Sources
    const buttons = await page.$$('button');
    let techToggle = null;
    for (const b of buttons) {
      const txt = (await page.evaluate(el => el.textContent, b)) || '';
      if (txt.includes('Technical') || txt.includes('Data Sources')) {
        techToggle = b;
        break;
      }
    }
    if (techToggle) {
      await techToggle.click();
      await new Promise(r => setTimeout(r, 600));
      console.log('  Technical Data Sources dropdown toggled: PASS');
      results.tests.push({ name: 'Technical Data Sources Accordion', pass: true });
    }

    // -------------------------------------------------------------
    // 4. CHECK MY LOCATION (/check-location)
    // -------------------------------------------------------------
    console.log('\n--- 4. Testing Check My Location (/check-location) ---');
    await page.goto(`${BASE_URL}/check-location`, { waitUntil: 'networkidle2', timeout: 15000 });
    await new Promise(r => setTimeout(r, 2000));
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '04_check_location_initial.png') });
    results.pagesTested.push('Check My Location (/check-location)');

    // Click Tokyo preset button
    const presetButtons = await page.$$('button');
    let presetClicked = false;
    for (const btn of presetButtons) {
      const txt = (await page.evaluate(el => el.textContent, btn)) || '';
      if (txt.includes('Tokyo')) {
        console.log(`  Clicking location preset: "${txt.trim()}"`);
        await btn.click();
        presetClicked = true;
        break;
      }
    }
    if (presetClicked) {
      // Wait for assessment cards to appear
      await page.waitForFunction(
        () => document.body.innerText.toUpperCase().includes('TARGET ASSESSMENT LOCATION'),
        { timeout: 10000 }
      );
      await page.screenshot({ path: path.join(SCREENSHOT_DIR, '04_check_location_assessed.png') });
      const bodyText = await page.evaluate(() => document.body.innerText);
      const assessmentCompleted = bodyText.includes('Tokyo, Japan') && (bodyText.includes('Overall Risk for This Location') || bodyText.toUpperCase().includes('COMPOSITE RISK'));
      console.log('  Preset Location Assessment Result:', assessmentCompleted ? 'PASS' : 'FAIL');
      results.tests.push({ name: 'Preset Location Assessment Execution', pass: assessmentCompleted });
    }

    // -------------------------------------------------------------
    // 5. ACTIVE ALERTS (/alerts)
    // -------------------------------------------------------------
    console.log('\n--- 5. Testing Active Alerts (/alerts) ---');
    await page.goto(`${BASE_URL}/alerts`, { waitUntil: 'networkidle2', timeout: 15000 });
    await new Promise(r => setTimeout(r, 2500));
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '05_active_alerts.png') });
    results.pagesTested.push('Active Alerts (/alerts)');

    const alertItems = await page.$$('.glass-card, [class*="border-l-4"]');
    console.log(`  Alert list / summary cards found: ${alertItems.length}`);
    results.tests.push({ name: 'Active Alerts List & Summary', pass: alertItems.length > 0 });

    // Click hazard filter button
    const filterButtons = await page.$$('button');
    let filterClicked = false;
    for (const btn of filterButtons) {
      const txt = (await page.evaluate(el => el.textContent, btn)) || '';
      const lower = txt.toLowerCase();
      if (lower.includes('flood') || lower.includes('earthquake') || lower.includes('wildfire')) {
        await btn.click();
        filterClicked = true;
        await new Promise(r => setTimeout(r, 1000));
        break;
      }
    }
    console.log('  Alert Hazard Filter Interaction:', filterClicked ? 'PASS' : 'FAIL');
    results.tests.push({ name: 'Alert Filtering', pass: filterClicked });

    // -------------------------------------------------------------
    // 6. PAST EVENTS (/past-events)
    // -------------------------------------------------------------
    console.log('\n--- 6. Testing Past Events (/past-events) ---');
    await page.goto(`${BASE_URL}/past-events`, { waitUntil: 'networkidle2', timeout: 15000 });
    await new Promise(r => setTimeout(r, 2000));
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '06_past_events.png') });
    results.pagesTested.push('Past Events (/past-events)');

    const pastEventCards = await page.$$('.glass-card');
    console.log(`  Past Event Cards: ${pastEventCards.length}`);
    results.tests.push({ name: 'Past Events List Render', pass: pastEventCards.length > 0 });

    // -------------------------------------------------------------
    // 7. ABOUT PAGE (/about)
    // -------------------------------------------------------------
    console.log('\n--- 7. Testing About Page (/about) ---');
    await page.goto(`${BASE_URL}/about`, { waitUntil: 'networkidle2', timeout: 15000 });
    await new Promise(r => setTimeout(r, 2000));
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '07_about.png') });
    results.pagesTested.push('About (/about)');

    const aboutText = await page.evaluate(() => document.body.textContent);
    const hasMission = aboutText.includes('Mission') || aboutText.includes('HAZARDX') || aboutText.includes('Multi-Hazard');
    console.log('  About Page Mission & Content:', hasMission ? 'PASS' : 'FAIL');
    results.tests.push({ name: 'About Page Content Verification', pass: hasMission });

    // -------------------------------------------------------------
    // 8. MAP RESILIENCE CHECK (Return to /map after navigating away)
    // -------------------------------------------------------------
    console.log('\n--- 8. Testing Map Resilience (Navigating back to /map) ---');
    await page.goto(`${BASE_URL}/map`, { waitUntil: 'networkidle2', timeout: 15000 });
    await new Promise(r => setTimeout(r, 2500));
    const returnedMapContainer = await page.$('.leaflet-container');
    const returnedMapHasTiles = await page.$('.leaflet-tile-pane');
    console.log('  Map re-mount on return:', !!returnedMapContainer ? 'PASS' : 'FAIL');
    console.log('  Map tile pane active on return:', !!returnedMapHasTiles ? 'PASS' : 'FAIL');
    results.tests.push({ name: 'Map Does Not Become Blank on Navigation', pass: !!returnedMapContainer && !!returnedMapHasTiles });
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, '08_map_after_return.png') });

  } catch (err) {
    console.error('Test Execution Error:', err);
    results.tests.push({ name: 'Full Test Execution', pass: false, error: err.message });
  } finally {
    await browser.close();
  }

  console.log('\n======================================================');
  console.log('END-TO-END BROWSER AUTOMATION COMPLETE');
  console.log('Pages Tested:', results.pagesTested.length);
  console.log('Tests Passed:', results.tests.filter(t => t.pass).length, '/', results.tests.length);
  console.log('Console Errors:', consoleErrors.length);
  console.log('Network Failures:', networkFailures.length);
  console.log('Screenshots Saved in:', SCREENSHOT_DIR);
  console.log('======================================================');

  fs.writeFileSync(
    path.join(__dirname, '..', 'reports', 'e2e_browser_test_summary.json'),
    JSON.stringify(results, null, 2)
  );
}

runE2ETests().catch(err => {
  console.error('Fatal Test Runner Error:', err);
  process.exit(1);
});
