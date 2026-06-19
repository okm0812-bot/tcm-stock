/**
 * TCM 庫存異動紀錄 GAS Endpoint
 * 
 * 部署方式：
 * 1. 在現有 GAS 專案加入此程式碼（或在同一專案新增 .gs 檔案）
 * 2. 部署為網頁應用程式，權限設「任何人」
 * 3. 取得 URL 後填入 tcm_lookup HTML 的 CHANGE_GAS_URL 常數
 * 
 * 需要的 Google Sheet 分頁：
 * - 「庫存快照」：欄位 [日期, 資料庫類型, 品名, 狀態]
 * - 「異動紀錄」：欄位 [日期, 資料庫類型, 品名, 舊狀態, 新狀態, 異動類型]
 * 
 * 若分頁不存在會自動建立
 */

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

function doGet(e) {
  const action = e.parameter.action;
  
  if (action === 'getsnapshot') {
    return getSnapshot(e);
  }
  
  return ContentService.createTextOutput(JSON.stringify({ error: 'Unknown action' }))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  const action = e.parameter.action;
  
  if (action === 'record') {
    return recordChanges(e);
  }
  
  return ContentService.createTextOutput(JSON.stringify({ error: 'Unknown action' }))
    .setMimeType(ContentService.MimeType.JSON);
}

function getSnapshot(e) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const snapshotSheet = getOrCreateSheet(ss, SNAPSHOT_SHEET, ['日期', '資料庫類型', '品名', '狀態']);
  
  const data = snapshotSheet.getDataRange().getValues();
  if (data.length <= 1) {
    // 無快照
    return ContentService.createTextOutput(JSON.stringify({ snapshot: {}, date: '' }))
      .setMimeType(ContentService.MimeType.JSON);
  }
  
  // 取最新日期的快照（假設按日期排序，最後一筆最新）
  let latestDate = '';
  for (let i = 1; i < data.length; i++) {
    const rowDate = data[i][0];
    if (rowDate) latestDate = rowDate.toString().slice(0, 10);
  }
  
  // 建立快照 map
  const snapshot = {};
  for (let i = 1; i < data.length; i++) {
    const rowDate = data[i][0].toString().slice(0, 10);
    if (rowDate !== latestDate) continue; // 只取最新日期
    const dbType = data[i][1];
    const name = data[i][2];
    const status = data[i][3];
    const prefix = dbType === '錠劑' ? 'TB:' : 'KZ:';
    snapshot[prefix + name] = status;
  }
  
  return ContentService.createTextOutput(JSON.stringify({ snapshot, date: latestDate }))
    .setMimeType(ContentService.MimeType.JSON);
}

function recordChanges(e) {
  const payload = JSON.parse(e.postData.contents);
  const date = payload.date;
  const changes = payload.changes;
  const snapshot = payload.snapshot;
  
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const changesSheet = getOrCreateSheet(ss, CHANGES_SHEET, ['日期', '資料庫類型', '品名', '舊狀態', '新狀態', '異動類型']);
  const snapshotSheet = getOrCreateSheet(ss, SNAPSHOT_SHEET, ['日期', '資料庫類型', '品名', '狀態']);
  
  // 寫入異動紀錄
  const changeRows = [];
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
  
  // 更新快照（寫入今天所有品項）
  const snapshotRows = [];
  for (const [key, status] of Object.entries(snapshot)) {
    const prefix = key.substring(0, 3);
    const dbType = prefix === 'TB:' ? '錠劑' : '科中';
    const name = key.substring(3);
    snapshotRows.push([date, dbType, name, status]);
  }
  
  if (snapshotRows.length) {
    snapshotSheet.getRange(snapshotSheet.getLastRow() + 1, 1, snapshotRows.length, 4).setValues(snapshotRows);
  }
  
  return ContentService.createTextOutput(JSON.stringify({ success: true, changesCount: changeRows.length, snapshotCount: snapshotRows.length }))
    .setMimeType(ContentService.MimeType.JSON);
}
