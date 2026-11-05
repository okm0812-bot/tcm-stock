/**
 * TCM 庫存異動紀錄 GAS Endpoint（獨立部署版）
 *
 * 現況說明（2026-11-05）：
 * - 前端實際使用的是「審單專案」內的合併版（程式碼.gs，已部署第 58 版），行為與本檔一致。
 * - 本檔只包含異動相關程式（不含 LINE Bot 訂單邏輯），適合另外部署一個乾淨的異動端點。
 * - 部署後把 /exec 網址填入 tcm_lookup HTML 的 CHANGE_GAS_URL 常數即可。
 *
 * 部署方式：
 * 1. 在 GAS 專案新增一個 .gs 檔案，貼入此程式碼（可與 LINE Bot 併存，互不影響）
 * 2. 部署為網頁應用程式（新部署），權限設「任何人」
 * 3. 取得 URL 後填入 tcm_lookup HTML 的 CHANGE_GAS_URL 常數
 *
 * Sheet ID：1A4LtTGVqQuJ8MTfrRGn41QmcYwGZgCNjOc4lOfRjgd0
 * 使用兩個分頁：
 * - 「庫存快照」：欄位 [日期, 資料庫類型, 品名, 狀態]，只保留最新一份（每次整表覆蓋）
 * - 「異動紀錄」：欄位 [日期, 資料庫類型, 品名, 舊狀態, 新狀態, 異動類型]，累積保留
 *
 * 端點：
 * - GET  ?action=getsnapshot  → { snapshot, date }                取得目前快照與其日期
 * - GET  ?action=getchanges   → { date, baseDate, changes }       取得最近一筆異動（給前端常駐顯示）
 * - POST action=record（payload JSON）→ 寫入異動紀錄並覆蓋快照
 */

const CHANGE_SS_ID = '1A4LtTGVqQuJ8MTfrRGn41QmcYwGZgCNjOc4lOfRjgd0';
const SNAPSHOT_SHEET = '庫存快照';
const CHANGES_SHEET = '異動紀錄';

function getOrCreateSheet(ss, name, headers) {
  let sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
    sheet.appendRow(headers);
    sheet.getRange(1, 1, 1, headers.length).setFontWeight('bold');
  }
  return sheet;
}

// 日期統一成 YYYY-MM-DD。
// Sheet 常把 "2026-11-05" 存成 Date 物件，直接 toString().slice(0,10) 會變成
// "Thu Nov 05"，導致日期永遠對不上（會重複寫入異動紀錄），所以先正規化再比較。
function normalizeDate_(value) {
  if (!value) return '';
  if (Object.prototype.toString.call(value) === '[object Date]') {
    return Utilities.formatDate(value, 'Asia/Taipei', 'yyyy-MM-dd');
  }
  const s = value.toString().trim();
  const m = s.match(/(\d{4})[-/](\d{1,2})[-/](\d{1,2})/);
  if (m) return m[1] + '-' + ('0' + m[2]).slice(-2) + '-' + ('0' + m[3]).slice(-2);
  return s.slice(0, 10);
}

function doGet(e) {
  const action = e.parameter.action;

  if (action === 'getsnapshot') {
    return getSnapshot(e);
  }

  if (action === 'getchanges') {
    return getLatestChanges();
  }

  return ContentService.createTextOutput(JSON.stringify({ error: 'Unknown action' }))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  const action = e.parameter.action;

  // 支援兩種格式：form-encoded (payload 參數) 或 JSON body
  let payload;
  if (e.postData && e.postData.contents) {
    try {
      payload = JSON.parse(e.postData.contents);
    } catch (err) {
      // 可能是 form-encoded
    }
  }
  if (!payload && e.parameter.payload) {
    try {
      payload = JSON.parse(e.parameter.payload);
    } catch (err) {
      return ContentService.createTextOutput(JSON.stringify({ error: 'Invalid payload' }))
        .setMimeType(ContentService.MimeType.JSON);
    }
  }

  if (payload && payload.action === 'record') {
    return recordChangesFromPayload(payload);
  }

  if (action === 'record') {
    return recordChanges(e);
  }

  return ContentService.createTextOutput(JSON.stringify({ error: 'Unknown action' }))
    .setMimeType(ContentService.MimeType.JSON);
}

function getSnapshot(e) {
  const ss = SpreadsheetApp.openById(CHANGE_SS_ID);
  const snapshotSheet = getOrCreateSheet(ss, SNAPSHOT_SHEET, ['日期', '資料庫類型', '品名', '狀態']);

  const data = snapshotSheet.getDataRange().getValues();
  if (data.length <= 1) {
    return ContentService.createTextOutput(JSON.stringify({ snapshot: {}, date: '' }))
      .setMimeType(ContentService.MimeType.JSON);
  }

  let latestDate = '';
  const rowDates = [];
  for (let i = 1; i < data.length; i++) {
    const d = normalizeDate_(data[i][0]);
    rowDates.push(d);
    if (d && d > latestDate) latestDate = d;
  }

  const snapshot = {};
  for (let i = 1; i < data.length; i++) {
    if (rowDates[i - 1] !== latestDate) continue;
    const prefix = data[i][1] === '錠劑' ? 'TB:' : 'KZ:';
    snapshot[prefix + data[i][2]] = data[i][3];
  }

  return ContentService.createTextOutput(JSON.stringify({ snapshot, date: latestDate }))
    .setMimeType(ContentService.MimeType.JSON);
}

// 最近一筆異動（「異動紀錄」分頁中最新日期的所有列），給前端常駐顯示用
function getLatestChanges() {
  const ss = SpreadsheetApp.openById(CHANGE_SS_ID);
  const changesSheet = getOrCreateSheet(ss, CHANGES_SHEET, ['日期', '資料庫類型', '品名', '舊狀態', '新狀態', '異動類型']);
  const data = changesSheet.getDataRange().getValues();
  const empty = { date: '', baseDate: '', changes: { added: [], removed: [], statusChanged: [] } };

  if (data.length <= 1) {
    return ContentService.createTextOutput(JSON.stringify(empty))
      .setMimeType(ContentService.MimeType.JSON);
  }

  let latestDate = '';
  for (let i = 1; i < data.length; i++) {
    const d = normalizeDate_(data[i][0]);
    if (d && d > latestDate) latestDate = d;
  }
  if (!latestDate) {
    return ContentService.createTextOutput(JSON.stringify(empty))
      .setMimeType(ContentService.MimeType.JSON);
  }

  const added = [], removed = [], statusChanged = [];
  for (let i = 1; i < data.length; i++) {
    if (normalizeDate_(data[i][0]) !== latestDate) continue;

    const db = data[i][1] === '錠劑' ? '錠劑' : '科中';
    const name = data[i][2] ? data[i][2].toString() : '';
    const oldStatus = data[i][3];
    const newStatus = data[i][4];
    const type = data[i][5] ? data[i][5].toString() : '';

    if (type === '新增') {
      added.push({ name, status: newStatus, db });
    } else if (type === '消失') {
      removed.push({ name, status: oldStatus, db });
    } else {
      statusChanged.push({ name, oldStatus, newStatus, db });
    }
  }

  // 快照只保留最新一份，基準日改由指令碼屬性取得
  const props = PropertiesService.getScriptProperties();
  let baseDate = '';
  if (props.getProperty('LAST_CHANGE_DATE') === latestDate) {
    baseDate = normalizeDate_(props.getProperty('LAST_BASE_DATE'));
  }
  if (!baseDate) baseDate = getBaseDate_(ss, latestDate);

  return ContentService.createTextOutput(JSON.stringify({
    date: latestDate,
    baseDate,
    changes: { added, removed, statusChanged }
  })).setMimeType(ContentService.MimeType.JSON);
}

// 備援用：快照分頁若還留有舊日期，取早於異動日的最近一個（快照只留最新一份後通常為空）
function getBaseDate_(ss, latestDate) {
  const snapshotSheet = getOrCreateSheet(ss, SNAPSHOT_SHEET, ['日期', '資料庫類型', '品名', '狀態']);
  const data = snapshotSheet.getDataRange().getValues();
  let baseDate = '';
  for (let i = 1; i < data.length; i++) {
    const d = normalizeDate_(data[i][0]);
    if (d && d < latestDate && d > baseDate) baseDate = d;
  }
  return baseDate;
}

function recordChangesFromPayload(payload) {
  return writeChangesAndSnapshot(payload.date, payload.changes, payload.snapshot);
}

function recordChanges(e) {
  const payload = JSON.parse(e.postData.contents);
  return writeChangesAndSnapshot(payload.date, payload.changes, payload.snapshot);
}

function writeChangesAndSnapshot(date, changes, snapshot) {
  changes = changes || {};
  snapshot = snapshot || {};
  date = date || Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd');

  const changeRows = [];
  const snapshotRows = [];

  const lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000);

    const ss = SpreadsheetApp.openById(CHANGE_SS_ID);
    const changesSheet = getOrCreateSheet(ss, CHANGES_SHEET, ['日期', '資料庫類型', '品名', '舊狀態', '新狀態', '異動類型']);
    const snapshotSheet = getOrCreateSheet(ss, SNAPSHOT_SHEET, ['日期', '資料庫類型', '品名', '狀態']);

    // 寫入異動紀錄（累積保留）
    if (changes.added) {
      for (const item of changes.added) {
        changeRows.push([date, item.db, item.name, '(新增)', item.status, '新增']);
      }
    }
    if (changes.removed) {
      for (const item of changes.removed) {
        changeRows.push([date, item.db, item.name, item.status, '(消失)', '消失']);
      }
    }
    if (changes.statusChanged) {
      for (const item of changes.statusChanged) {
        changeRows.push([date, item.db, item.name, item.oldStatus, item.newStatus, '狀態變化']);
      }
    }

    if (changeRows.length) {
      changesSheet.getRange(changesSheet.getLastRow() + 1, 1, changeRows.length, 6).setValues(changeRows);
    }

    // 整理這次的快照
    for (const key of Object.keys(snapshot)) {
      const prefix = key.substring(0, 3);
      const dbType = prefix === 'TB:' ? '錠劑' : '科中';
      snapshotRows.push([date, dbType, key.substring(3), snapshot[key]]);
    }

    // 快照只保留最新一份：先取出舊快照日期（當作這批異動的基準日），再整表覆蓋
    let prevDate = '';
    const existing = snapshotSheet.getDataRange().getValues();
    for (let i = 1; i < existing.length; i++) {
      const d = normalizeDate_(existing[i][0]);
      if (d && d > prevDate) prevDate = d;
    }

    snapshotSheet.clearContents();
    snapshotSheet.getRange(1, 1, 1, 4)
      .setValues([['日期', '資料庫類型', '品名', '狀態']])
      .setFontWeight('bold');
    if (snapshotRows.length) {
      snapshotSheet.getRange(2, 1, snapshotRows.length, 4).setValues(snapshotRows);
    }

    // 舊快照已被覆蓋，把基準日記在指令碼屬性，之後才能顯示「基準日 → 異動日」
    const props = PropertiesService.getScriptProperties();
    props.setProperty('SNAPSHOT_DATE', date);
    props.setProperty('LAST_BASE_DATE', prevDate);
    props.setProperty('LAST_CHANGE_DATE', date);

    SpreadsheetApp.flush();
  } finally {
    lock.releaseLock();
  }

  return ContentService.createTextOutput(JSON.stringify({
    success: true,
    changesCount: changeRows.length,
    snapshotCount: snapshotRows.length
  })).setMimeType(ContentService.MimeType.JSON);
}
