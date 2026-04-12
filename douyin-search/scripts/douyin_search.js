const { createRequire } = require('module');
const { chromium } = createRequire(process.cwd() + '/node_modules/playwright')('playwright');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const keyword = args[0];
if (!keyword) {
  console.error('Usage: node douyin_search.js <keyword> [--target N] [--output PATH] [--feishu] [--cookies PATH] [--headless]');
  process.exit(1);
}

let target = 50;
let outputFile = null;
let feishu = false;
let cookiesPath = null;
let headless = false;

for (let i = 1; i < args.length; i++) {
  switch (args[i]) {
    case '--target': target = parseInt(args[++i], 10) || 50; break;
    case '--output': outputFile = args[++i]; break;
    case '--feishu': feishu = true; break;
    case '--cookies': cookiesPath = args[++i]; break;
    case '--headless': headless = true; break;
  }
}

if (!outputFile) {
  outputFile = path.join(process.cwd(), `douyin_search_${keyword}.json`);
}

function loadCookies() {
  const paths = [
    cookiesPath,
    path.join(process.cwd(), 'douyin_cookies.json'),
    path.join(__dirname, 'douyin_cookies.json'),
  ].filter(Boolean);

  for (const p of paths) {
    if (fs.existsSync(p)) {
      const data = JSON.parse(fs.readFileSync(p, 'utf-8'));
      console.log(`Cookies loaded from: ${p}`);
      return data;
    }
  }
  console.error('ERROR: No cookies file found. Create douyin_cookies.json or use --cookies flag.');
  console.error('Required cookies: sessionid, sessionid_ss');
  process.exit(1);
}

function save(data) {
  fs.writeFileSync(outputFile, JSON.stringify(data, null, 2), 'utf-8');
}

function extractCards() {
  const ul = document.querySelector('[data-e2e="scroll-list"]');
  if (!ul) return [];
  const lis = ul.querySelectorAll('li');
  const cards = [];
  lis.forEach(li => {
    const card = li.querySelector('.search-result-card');
    if (!card) return;
    const a = card.querySelector('a[href*="/video/"]');
    if (!a) return;

    const href = a.getAttribute('href') || '';
    const videoId = href.match(/video\/(\d+)/)?.[1] || '';

    const titleEl = card.querySelector('.VDYK8Xd7');
    const title = titleEl?.textContent?.trim() || '';

    const authorEl = card.querySelector('.dW_QmDH1');
    const authorRaw = authorEl?.textContent?.trim() || '';
    const authorMatch = authorRaw.match(/@(.+?)(\d+[天小时分钟周月年前]+)$/);
    const author = authorMatch ? authorMatch[1] : authorRaw.replace(/^@/, '').replace(/\d+[天小时分钟周月年前]+$/, '').trim();
    const time = authorMatch ? authorMatch[2] : authorRaw.replace(/^@.+?/, '').trim();

    const likesEl = card.querySelector('.z2lFLtJ0 .cIiU4Muu') || card.querySelector('.z2lFLtJ0');
    const likes = likesEl?.textContent?.trim() || '';

    const durationEl = card.querySelector('.ckopQfVu');
    const duration = durationEl?.textContent?.trim() || '';

    if (title && videoId) {
      cards.push({
        title: title.substring(0, 300),
        author,
        likes,
        duration,
        time,
        videoId,
        url: `https://www.douyin.com/video/${videoId}`,
      });
    }
  });
  return cards;
}

function writeToFeishu(videos) {
  const rows = videos.map(v => [v.title, v.author, v.likes, v.duration, v.time, v.url]);
  const data = JSON.stringify(rows);
  const title = `抖音搜索 - ${keyword} (${new Date().toLocaleDateString('zh-CN')})`;
  console.log('正在写入飞书表格...');
  try {
    const result = execSync(
      `lark-cli sheets +create --title "${title}" --headers '["视频标题","作者","点赞数","时长","发布时间","链接"]' --data '${data}'`,
      { encoding: 'utf-8', timeout: 30000 }
    );
    const res = JSON.parse(result);
    if (res.ok) {
      console.log(`\n飞书表格已创建: ${res.data.url}`);
    } else {
      console.error('写入飞书失败:', JSON.stringify(res));
    }
  } catch (err) {
    console.error('飞书写入异常:', err.message);
  }
}

(async () => {
  const cookies = loadCookies();

  const browser = await chromium.launch({
    headless,
    args: ['--disable-blink-features=AutomationControlled'],
  });
  const ctx = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    viewport: { width: 1440, height: 900 },
  });
  await ctx.addCookies(cookies);
  const page = await ctx.newPage();

  const searchUrl = `https://www.douyin.com/search/${encodeURIComponent(keyword)}?type=video`;
  console.log(`打开抖音搜索: ${keyword}`);
  await page.goto(searchUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(8000);

  const allVideos = [];
  const seenIds = new Set();
  let noNewCount = 0;

  for (let scroll = 0; scroll < 30 && allVideos.length < target; scroll++) {
    const cards = await page.evaluate(extractCards);
    let newCount = 0;
    for (const card of cards) {
      if (!seenIds.has(card.videoId)) {
        seenIds.add(card.videoId);
        allVideos.push(card);
        newCount++;
        console.log(`[${allVideos.length}/${target}] ${card.title.substring(0, 50)}... (赞:${card.likes} @${card.author})`);
      }
    }

    if (newCount === 0) {
      noNewCount++;
      if (noNewCount >= 5) {
        console.log('连续多次无新数据，停止滚动');
        break;
      }
    } else {
      noNewCount = 0;
    }

    await page.evaluate(() => window.scrollBy(0, 1000));
    await page.waitForTimeout(2000 + Math.floor(Math.random() * 1500));
  }

  save(allVideos);
  console.log(`\n共提取 ${allVideos.length} 个视频，已保存到 ${outputFile}`);

  if (feishu && allVideos.length > 0) {
    writeToFeishu(allVideos);
  }

  await browser.close().catch(() => {});
})().catch(err => {
  console.error('FATAL:', err.message);
  process.exit(1);
});
