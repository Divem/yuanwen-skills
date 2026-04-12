#!/usr/bin/env node
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
function getArg(flag) {
  const i = args.indexOf(flag);
  return i >= 0 && i + 1 < args.length ? args[i + 1] : null;
}

const jsonFile = getArg('--input') || getArg('-i');
const title = getArg('--title') || `抖音视频评论-${new Date().toISOString().slice(0, 10).replace(/-/g, '')}`;
const folderToken = getArg('--folder-token') || '';

if (!jsonFile || !fs.existsSync(jsonFile)) {
  console.error('Usage: node upload_to_feishu.js --input <comments.json> [--title "Sheet Title"] [--folder-token TOKEN]');
  process.exit(1);
}

const comments = JSON.parse(fs.readFileSync(jsonFile, 'utf-8'));
if (!Array.isArray(comments) || comments.length === 0) {
  console.error('No comments found in input file.');
  process.exit(1);
}

console.log(`[INFO] ${comments.length} comments to upload`);

const headers = '["序号","昵称","评论内容","点赞数","时间·地区"]';
const createCmd = `npx lark-cli sheets +create --title "${title}" --headers '${headers}'${folderToken ? ` --folder-token "${folderToken}"` : ''}`;
console.log('[INFO] Creating spreadsheet...');
const createResult = JSON.parse(execSync(createCmd, { encoding: 'utf-8' }));
if (!createResult.ok) {
  console.error('[ERROR] Failed to create sheet:', JSON.stringify(createResult));
  process.exit(1);
}
const token = createResult.data.spreadsheet_token;
const sheetUrl = createResult.data.url;
console.log(`[INFO] Created: ${sheetUrl}`);

const infoResult = JSON.parse(execSync(`npx lark-cli sheets +info --url "${sheetUrl}"`, { encoding: 'utf-8' }));
const sheetId = infoResult.data.sheets.sheets[0].sheet_id;

const rows = comments.map((c, i) => [i + 1, c.nickname || '', c.content || '', c.likes || '0', c.time || '']);
const CHUNK = 20;

for (let i = 0; i < rows.length; i += CHUNK) {
  const chunk = rows.slice(i, i + CHUNK);
  const start = i + 2;
  const end = start + CHUNK - 1;
  const values = JSON.stringify(chunk);
  console.log(`[INFO] Appending rows ${start}-${end}...`);
  const r = JSON.parse(execSync(
    `npx lark-cli sheets +append --spreadsheet-token "${token}" --sheet-id "${sheetId}" --range "A${start}:E500" --values '${values.replace(/'/g, "'\\''")}'`,
    { encoding: 'utf-8' }
  ));
  if (!r.ok) console.error('[WARN] Append failed:', JSON.stringify(r));
}

console.log(`[DONE] Uploaded ${rows.length} comments to ${sheetUrl}`);
console.log(`URL: ${sheetUrl}`);
