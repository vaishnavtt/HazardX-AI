const puppeteer = require('../frontend/node_modules/puppeteer-core');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--no-sandbox']
  });
  const page = await browser.newPage();
  page.on('console', msg => console.log('LOG:', msg.text()));
  page.on('pageerror', err => console.log('PAGEERR:', err.message));
  await page.goto('http://localhost:5173/check-location', { waitUntil: 'networkidle2' });
  await new Promise(r => setTimeout(r, 1000));
  
  const buttons = await page.$$('button');
  for (const b of buttons) {
    const t = await page.evaluate(el => el.textContent, b);
    if (t && t.includes('Tokyo')) {
      console.log('Found button:', t.trim());
      await b.click();
      break;
    }
  }
  
  await new Promise(r => setTimeout(r, 4000));
  const afterClick = await page.evaluate(() => document.body.innerText);
  console.log('--- After Click Body Text ---');
  console.log(afterClick.slice(0, 1000));
  
  await browser.close();
})();
