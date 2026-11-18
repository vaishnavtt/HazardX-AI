const puppeteer = require('../frontend/node_modules/puppeteer-core');
const CHROME_PATH = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: ['--no-sandbox']
  });
  const page = await browser.newPage();
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  page.on('pageerror', err => errors.push(err.toString()));

  await page.goto('http://localhost:5173/models', { waitUntil: 'networkidle2' });
  console.log('Opened /models');

  const hazards = ['Landslides', 'Earthquakes', 'Cyclones', 'Wildfires', 'Floods'];
  for (const h of hazards) {
    const clicked = await page.evaluate((hazardName) => {
      const btns = Array.from(document.querySelectorAll('button'));
      const target = btns.find(b => b.innerText && b.innerText.includes(hazardName));
      if (target) {
        target.click();
        return true;
      }
      return false;
    }, h);

    await new Promise(r => setTimeout(r, 600));
    console.log(`Tab: ${h} | Clicked: ${clicked} | Console errors: ${errors.length}`);
  }

  await browser.close();
  if (errors.length > 0) {
    console.error('Errors found:', errors);
    process.exit(1);
  } else {
    console.log('ALL HAZARD TABS PASSED WITH 0 CONSOLE ERRORS!');
  }
})();
