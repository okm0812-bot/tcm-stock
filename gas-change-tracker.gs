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
const TZ = 'Asia/Taipei';
// 異動紀錄只保留一週：以「每週五 18:00（台北時間）」為換週分界。
// 週五 18:00 之後的第一次更新就是新的一週的第一批（換週時先清掉更早的紀錄再寫入）。
const WEEK_RESET_DOW = 5;    // 5 = 週五
const WEEK_RESET_HOUR = 18;  // 18:00 之後算新的一週（與前端作業時段 18:00~23:00 對齊）

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

// 目前這一週的起始日（yyyy-MM-dd）。
// 分界固定在每週五 18:00：週五 18:00 之前仍算上一週，之後才算新的一週；
// 週五 18:00 之後的第一次更新，就是新一週的第一批異動。
function getWeekStart_(now) {
  now = now || new Date();
  const y = Number(Utilities.formatDate(now, TZ, 'yyyy'));
  const mo = Number(Utilities.formatDate(now, TZ, 'MM'));
  const d = Number(Utilities.formatDate(now, TZ, 'dd'));
  const h = Number(Utilities.formatDate(now, TZ, 'HH'));
  const dow = new Date(Date.UTC(y, mo - 1, d)).getUTCDay();   // 0=週日、5=週五
  let back = (dow - WEEK_RESET_DOW + 7) % 7;                  // 距離上一個週五幾天
  if (back === 0 && h < WEEK_RESET_HOUR) back = 7;             // 本週五還沒過 18:00 → 仍屬上一週
  return Utilities.formatDate(new Date(Date.UTC(y, mo - 1, d - back)), TZ, 'yyyy-MM-dd');
}

// 換週清理：把分界日之前的異動紀錄刪掉，只保留「分界前最後一批（同一天）」當新週期的起點。
// 本週（分界日之後）已經寫入的紀錄一定要留著，否則剛換週就把本週資料清掉了。
// 回傳被刪掉的列數，方便寫 log。
function pruneOldChanges_(changesSheet, weekStart) {
  const data = changesSheet.getDataRange().getValues();
  if (data.length <= 1) return 0;

  let lastOldDate = '';
  for (let i = 1; i < data.length; i++) {
    const d = normalizeDate_(data[i][0]);
    if (d && d < weekStart && d > lastOldDate) lastOldDate = d;
  }
  if (!lastOldDate) return 0;   // 沒有上一週的資料，不必清

  const keep = [];
  for (let i = 1; i < data.length; i++) {
    const d = normalizeDate_(data[i][0]);
    if (d >= weekStart || d === lastOldDate) keep.push(data[i].slice(0, 6));
  }

  const removed = (data.length - 1) - keep.length;
  if (removed <= 0) return 0;   // 沒有可清的舊資料，不要白寫一次整表

  changesSheet.clearContents();
  changesSheet.getRange(1, 1, 1, 6)
    .setValues([['日期', '資料庫類型', '品名', '舊狀態', '新狀態', '異動類型']])
    .setFontWeight('bold');
  if (keep.length) {
    changesSheet.getRange(2, 1, keep.length, 6).setValues(keep);
  }
  return removed;
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

// 本週所有異動（「異動紀錄」分頁中，換週分界日之後的全部列），依日期分組給前端常駐顯示用。
// 記錄本身是往後追加、不覆蓋；每週五 18:00 之後換週，只保留分界前最後一批當起點。
function getLatestChanges() {
  const ss = SpreadsheetApp.openById(CHANGE_SS_ID);
  const changesSheet = getOrCreateSheet(ss, CHANGES_SHEET, ['日期', '資料庫類型', '品名', '舊狀態', '新狀態', '異動類型']);
  const weekStart = getWeekStart_();
  const data = changesSheet.getDataRange().getValues();
  const emptyChanges = { added: [], removed: [], statusChanged: [] };
  const empty = { date: '', baseDate: '', weekStart, groups: [], anchor: null, changes: emptyChanges };

  if (data.length <= 1) {
    return ContentService.createTextOutput(JSON.stringify(empty))
      .setMimeType(ContentService.MimeType.JSON);
  }

  const byDate = {};      // 本週（分界日之後）
  const oldByDate = {};   // 分界日之前（換週時只保留最後一批，當作本期起點）
  let latestDate = '';
  for (let i = 1; i < data.length; i++) {
    const d = normalizeDate_(data[i][0]);
    if (!d) continue;

    // 分界日之前的舊紀錄不算「本週」，但最後一批要留下來顯示成起點
    const bucket = (d >= weekStart) ? byDate : oldByDate;
    if (!bucket[d]) bucket[d] = { added: [], removed: [], statusChanged: [] };

    const db = data[i][1] === '錠劑' ? '錠劑' : '科中';
    const name = data[i][2] ? data[i][2].toString() : '';
    const oldStatus = data[i][3];
    const newStatus = data[i][4];
    const type = data[i][5] ? data[i][5].toString() : '';

    if (type === '新增') {
      bucket[d].added.push({ name, status: newStatus, db });
    } else if (type === '消失') {
      bucket[d].removed.push({ name, status: oldStatus, db });
    } else {
      bucket[d].statusChanged.push({ name, oldStatus, newStatus, db });
    }
    if (d >= weekStart && d > latestDate) latestDate = d;
  }

  // 分界日之前的最後一批：換週時保留在表裡當起點，順便回傳讓畫面顯示
  let anchor = null;
  const anchorDates = Object.keys(oldByDate).sort();
  if (anchorDates.length) {
    const anchorDate = anchorDates[anchorDates.length - 1];
    anchor = {
      date: anchorDate,
      added: oldByDate[anchorDate].added,
      removed: oldByDate[anchorDate].removed,
      statusChanged: oldByDate[anchorDate].statusChanged
    };
  }

  if (!latestDate) {
    // 本週還沒有新異動：仍把換週保留的最後一批回傳，畫面才有起點可對照
    empty.anchor = anchor;
    return ContentService.createTextOutput(JSON.stringify(empty))
      .setMimeType(ContentService.MimeType.JSON);
  }

  // 依日期新 → 舊排列，讓前端可以按天分段顯示
  const groups = Object.keys(byDate).sort().reverse().map(dateKey => ({
    date: dateKey,
    added: byDate[dateKey].added,
    removed: byDate[dateKey].removed,
    statusChanged: byDate[dateKey].statusChanged
  }));

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
    weekStart,
    groups,
    anchor,                       // 換週後保留的最後一批（起點），前端另外顯示
    changes: byDate[latestDate] || emptyChanges   // 相容舊版前端：只給最新一天
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

    // 異動紀錄保留一週：跨過分界日才清掉更早的紀錄，只留分界前最後一批當新週期起點。
    // 放在寫入前做，確保換週後第一批異動是接在保留的那批後面。
    const weekStart = getWeekStart_(new Date());
    const pruned = pruneOldChanges_(changesSheet, weekStart);
    if (pruned > 0) Logger.log('換週清理異動紀錄：刪除 ' + pruned + ' 列（本週起始 ' + weekStart + '）');

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
