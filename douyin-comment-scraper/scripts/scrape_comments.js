#!/usr/bin/env node
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
function getArg(flag) {
  const i = args.indexOf(flag);
  return i >= 0 && i + 1 < args.length ? args[i + 1] : null;
}

const videoUrl = getArg('--url') || getArg('-u');
const cookieStr = getArg('--cookies') || getArg('-c');
const count = parseInt(getArg('--count') || '100', 10);
const output = getArg('--output') || getArg('-o') || 'douyin_comments.json';

if (!videoUrl) {
  console.error('Usage: node scrape_comments.js --url <douyin_url> [--cookies <json_string_or_@file>] [--count 100] [--output out.json]');
  console.error('');
  console.error('Required:');
  console.error('  --url, -u        Douyin video URL (e.g. https://www.douyin.com/video/123 or https://www.douyin.com/jingxuan?modal_id=123)');
  console.error('Optional:');
  console.error('  --cookies, -c    Cookies JSON array string, or @path to read from file');
  console.error('  --count          Number of comments to scrape (default: 100)');
  console.error('  --output, -o     Output file path (default: douyin_comments.json)');
  process.exit(1);
}

let cookies = [];
if (cookieStr) {
  try {
    const raw = cookieStr.startsWith('@') ? fs.readFileSync(cookieStr.substring(1), 'utf-8') : cookieStr;
    cookies = JSON.parse(raw);
  } catch (e) {
    console.error('Failed to parse cookies:', e.message);
    process.exit(1);
  }
}

const videoIdMatch = videoUrl.match(/(?:video\/|modal_id=)(\d+)/);
const videoId = videoIdMatch ? videoIdMatch[1] : null;
if (!videoId) {
  console.error('Cannot extract video ID from URL. Use /video/<id> or ?modal_id=<id> format.');
  process.exit(1);
}

function save(data) {
  fs.writeFileSync(output, JSON.stringify(data, null, 2), 'utf-8');
}

async function extractComments(page) {
  return page.evaluate(() => {
    const items = document.querySelectorAll('[data-e2e="comment-item"]');
    const results = [];
    items.forEach((item) => {
      const nickname = (item.querySelector('.BT7MlqJC a')?.textContent || '').trim();
      const content = (item.querySelector('.C7LroK_h')?.textContent || '').trim();
      const timeLoc = (item.querySelector('.fJhvAqos span')?.textContent || '').trim();
      const likes = (item.querySelector('.vXZJEXVc p')?.textContent || '0').trim();
      if (content) {
        results.push({ nickname, content: content.substring(0, 500), likes, time: timeLoc });
      }
    });
    return results;
  });
}

(async () => {
  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled'],
  });
  const ctx = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    viewport: { width: 1440, height: 900 },
  });
  if (cookies.length > 0) await ctx.addCookies(cookies);
  const page = await ctx.newPage();

  const url = `https://www.douyin.com/jingxuan?modal_id=${videoId}`;
  console.log(`[INFO] Video ID: ${videoId}`);
  console.log(`[INFO] Opening: ${url}`);
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(8000);

  await page.evaluate(() => {
    document.querySelector('[data-e2e="recommend-guide-mask"]')?.remove();
    document.querySelector('#trust-logout-dialog')?.remove();
    document.querySelector('#uc-second-verify')?.remove();
    document.querySelectorAll('[class*="second-verify"], [class*="trust-login"], [class*="guide-mask"]').forEach(el => el.remove());
  });
  await page.waitForTimeout(500);

  console.log('[INFO] Clicking comment icon...');
  try {
    await page.$eval('[data-e2e="feed-comment-icon"]', el => el.click());
  } catch (_) {
    console.error('[ERROR] Comment icon not found. Page may require login or has CAPTCHA.');
    await browser.close().catch(() => {});
    process.exit(1);
  }
  await page.waitForTimeout(3000);

  try {
    await page.waitForSelector('[data-e2e="comment-item"]', { timeout: 10000 });
    console.log('[INFO] Comment list loaded.');
  } catch (_) {
    console.error('[ERROR] Comment items did not appear. The page may need CAPTCHA verification or login.');
    await browser.close().catch(() => {});
    process.exit(1);
  }

  const comments = [];
  let lastCount = 0;
  let staleRounds = 0;

  while (comments.length < count && staleRounds < 5) {
    const newComments = await extractComments(page);
    for (const c of newComments) {
      if (!comments.find(x => x.content === c.content && x.nickname === c.nickname)) {
        comments.push(c);
      }
    }
    console.log(`[${comments.length}/${count}] comments collected`);

    if (comments.length === lastCount) {
      staleRounds++;
    } else {
      staleRounds = 0;
    }
    lastCount = comments.length;

    if (comments.length < count) {
      await page.evaluate(() => {
        const cl = document.querySelector('[data-e2e="comment-list"]');
        if (cl) cl.scrollTop += 800;
      });
      await page.waitForTimeout(1500);
    }

    if (comments.length % 20 === 0 && comments.length > 0) save(comments);
  }

  const final = comments.slice(0, count);
  save(final);
  console.log(`[DONE] ${final.length} comments saved to ${output}`);

  if (fs.existsSync(path.join(__dirname, 'upload_to_feishu.js'))) {
    console.log('[INFO] Uploading to Feishu...');
    try {
      const { execSync } = require('child_process');
      const videoUrlFull = videoUrl;
      const feishuTitle = `抖音评论 - ${videoId} (${videoUrlFull})`;
      const uploadCmd = `node "${path.join(__dirname, 'upload_to_feishu.js')}" --input "${path.resolve(output)}" --title "${feishuTitle}"`;
      execSync(uploadCmd, { encoding: 'utf-8', stdio: 'inherit' });
    } catch (e) {
      console.error('[WARN] Feishu upload failed:', e.message);
    }
  }

  await browser.close().catch(() => {});
})().catch(err => {
  console.error('[FATAL]', err.message);
  process.exit(1);
});
