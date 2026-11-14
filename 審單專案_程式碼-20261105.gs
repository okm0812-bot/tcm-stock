// ==========================================
// 全域常數設定
// ==========================================
const SPREADSHEET_ID = '1A4LtTGVqQuJ8MTfrRGn41QmcYwGZgCNjOc4lOfRjgd0';
const SHEET_NAME = '工作表1';
const DUPLICATE_DAYS = 7;          // 幾天內算重複（備援上限；實務上由「每週五 17:00 換週」決定）
const LOOKBACK_ROWS = 300;         // 往回檢查幾筆（效能與準確度平衡）
const DUP_RESET_DOW = 5;           // 5 = 週五：重複下單審查每週重新起算
const DUP_RESET_HOUR = 17;         // 17:00 之後算新的一輪（17:00 之前送出的訂單不再列入重複比對）
const ORDER_CLEAR_DOW = 5;         // 5 = 週五：每週自動清空「工作表1」訂單資料
const ORDER_CLEAR_HOUR = 17;       // 17:00 之後清空（只留標題列，不留備份）
const ORDER_CLEAR_PROP = 'LAST_ORDER_CLEAR';   // 記錄上次清除的換週日，避免同一輪重複清
const SNAPSHOT_SHEET = '庫存快照';
const CHANGES_SHEET = '異動紀錄';
const TZ = 'Asia/Taipei';
// 異動紀錄只保留一週：以「每週五 18:00（台北時間）」為換週分界。
// 週五 18:00 之後的第一次更新就是新的一週的第一批（換週時先清掉更早的紀錄再寫入）。
const WEEK_RESET_DOW = 5;    // 5 = 週五
const WEEK_RESET_HOUR = 18;  // 18:00 之後算新的一週（與前端作業時段 18:00~23:00 對齊）

// 前端庫存表
const KEZHONG_CSV = 'https://docs.google.com/spreadsheets/d/1ekYUBtuQNjLB0RpWGCPJN7409sL74tqT36NfzUIM6o4/gviz/tq?tqx=out:csv';
const TABLET_CSV  = 'https://docs.google.com/spreadsheets/d/1e4EjRPC43YBAoPl4UyjZeEnS3XH7oKltgAG7k8wtfcc/gviz/tq?tqx=out:csv';

// ==========================================
// 核心路由
// ==========================================
function doPost(e) {
  try {
    let payload = null;

    if (e.postData && e.postData.contents) {
      try {
        payload = JSON.parse(e.postData.contents);
      } catch (err) {}
    }

    if (payload && payload.events) {
      return handleLineBotEvent(payload, e);
    }

    let action = e.parameter ? e.parameter.action : null;

    if (!payload && e.parameter && e.parameter.payload) {
      try {
        payload = JSON.parse(e.parameter.payload);
      } catch (err) {
        return ContentService.createTextOutput(JSON.stringify({ error: 'Invalid payload' }))
          .setMimeType(ContentService.MimeType.JSON);
      }
    }

    if ((payload && payload.action === 'record') || (action === 'record' && payload)) {
      return writeChangesAndSnapshot(payload.date, payload.changes, payload.snapshot);
    }

    return ContentService.createTextOutput('OK');

  } catch (err) {
    Logger.log('doPost 錯誤：' + err.toString());
    return ContentService.createTextOutput('OK');
  }
}

function doGet(e) {
  var action = e.parameter ? e.parameter.action : '';

  if (action === 'getsnapshot') {
    return getSnapshot(e);
  }

  // 前端開頁時讀取「最近一筆異動」，讓異動固定顯示在頁面下方
  if (action === 'getchanges') {
    return getLatestChanges();
  }

  return ContentService.createTextOutput(JSON.stringify({ error: 'Unknown action' }))
    .setMimeType(ContentService.MimeType.JSON);
}

// ==========================================
// LINE Bot 處理
// ==========================================
function handleLineBotEvent(data, e) {
  var events = data.events;
  if (!events || events.length === 0) return ContentService.createTextOutput('OK');

  var event = events[0];
  if (!event.message || event.message.type !== 'text') {
    return ContentService.createTextOutput('OK');
  }

  var replyToken = event.replyToken;
  var text = event.message.text;
  var userId = event.source.userId;
  var timestamp = event.timestamp;

  var parsedData = parseOrder(text, userId, timestamp);
  var orders = parsedData.orders;
  var customerName = parsedData.finalCustomer;
  var reply = '';

  if (orders.length === 0) {
    replyToUser(replyToken, '⚠️ 未偵測到有效品項，請確認格式。');
    return ContentService.createTextOutput('OK');
  }

  var removedItems = [];
  var newOrders = [];

  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000);

    var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    var sheet = ss.getSheetByName(SHEET_NAME);

    // 優化後的重複檢查
    var dupResult = checkDuplicate(orders, sheet);
    var dupKeys = dupResult.keys;

    for (var i = 0; i < orders.length; i++) {
      var o = orders[i];
      var k = makeDupKey(o.customer, o.spec, o.item);
      if (dupKeys[k]) {
        removedItems.push(o);
      } else {
        newOrders.push(o);
      }
    }

    if (newOrders.length > 0) {
      var writeData = [];
      for (var i = 0; i < newOrders.length; i++) {
        var o = newOrders[i];
        writeData.push([
          sanitizeCell(o.time),
          sanitizeCell(o.customer),
          sanitizeCell(o.spec),
          sanitizeCell(o.item),
          sanitizeCell(o.quantity),
          sanitizeCell(o.userId)
        ]);
      }
      sheet.getRange(sheet.getLastRow() + 1, 1, writeData.length, 6).setValues(writeData);
      SpreadsheetApp.flush();
    }

  } catch (err) {
    Logger.log('寫入失敗：' + err);
    replyToUser(replyToken, '⚠️ 系統忙碌中，請稍後再試。');
    return ContentService.createTextOutput('OK');
  } finally {
    lock.releaseLock();
  }

  // 回覆訊息
  if (removedItems.length > 0 && newOrders.length > 0) {
    reply += '⚠️ 以下品項重複已移除：\n';
    for (var i = 0; i < removedItems.length; i++) {
      reply += removedItems[i].item + ' x' + removedItems[i].quantity + '（' + removedItems[i].spec + '）\n';
    }
    reply += '------------------\n';
  }

  if (newOrders.length > 0) {
    reply += '📋 本次錄入成功：\n' + customerName + '\n';

    var grouped = {};
    for (var i = 0; i < newOrders.length; i++) {
      var s = newOrders[i].spec || '200g';
      if (!grouped[s]) grouped[s] = [];
      grouped[s].push(newOrders[i].item + ' x' + newOrders[i].quantity);
    }
    for (var spec in grouped) {
      reply += '【' + spec + '】\n';
      for (var j = 0; j < grouped[spec].length; j++) {
        reply += ' ' + grouped[spec][j] + '\n';
      }
    }
  } else if (removedItems.length > 0) {
    reply = '❌ 所有品項皆已下單過，未寫入資料。\n\n已存在品項：\n';
    for (var i = 0; i < removedItems.length; i++) {
      reply += removedItems[i].item + ' x' + removedItems[i].quantity + '（' + removedItems[i].spec + '）\n';
    }
  }

  if (orders.length > 0 && orders[0].remark) {
    reply += '\n💬 備註：' + orders[0].remark;
  }

  replyToUser(replyToken, reply);
  return ContentService.createTextOutput('OK');
}

function sanitizeCell(val) {
  var s = String(val == null ? '' : val);
  return /^[=+\-@]/.test(s) ? "'" + s : s;
}

// ==========================================
// 重複檢查（優化版）
// ==========================================
function makeDupKey(customer, spec, item) {
  return String(customer).trim() + '|' + String(spec).toLowerCase().trim() + '|' + String(item).trim();
}

// 重複下單審查的起算時間點：最近一次「週五 17:00」（台北時間）。
// 週五 17:00 之後再下單，就不會再被上一輪的訂單判定為重複。
// 搭配每週五 17:00 的定時清除（clearOrdersWeekly），表上只會有當週資料。
function getDupWindowStart_(now) {
  now = now || new Date();
  var y = Number(Utilities.formatDate(now, TZ, 'yyyy'));
  var mo = Number(Utilities.formatDate(now, TZ, 'MM'));
  var d = Number(Utilities.formatDate(now, TZ, 'dd'));
  var h = Number(Utilities.formatDate(now, TZ, 'HH'));
  var dow = new Date(Date.UTC(y, mo - 1, d)).getUTCDay();   // 0=週日、5=週五

  var back = (dow - DUP_RESET_DOW + 7) % 7;                 // 距離上一個週五幾天
  if (back === 0 && h < DUP_RESET_HOUR) back = 7;            // 本週五還沒過 17:00 → 仍屬上一輪

  // 回傳台北時間「換週日 17:00」對應的 UTC 時間
  return new Date(Date.UTC(y, mo - 1, d - back, DUP_RESET_HOUR - 8, 0));
}

// 換週日字串（yyyy-MM-dd）：最近一次「週五 17:00」所屬的日期，用來判斷這一輪清了沒
function getOrderClearBoundary_(now) {
  now = now || new Date();
  var y = Number(Utilities.formatDate(now, TZ, 'yyyy'));
  var mo = Number(Utilities.formatDate(now, TZ, 'MM'));
  var d = Number(Utilities.formatDate(now, TZ, 'dd'));
  var h = Number(Utilities.formatDate(now, TZ, 'HH'));
  var dow = new Date(Date.UTC(y, mo - 1, d)).getUTCDay();

  var back = (dow - ORDER_CLEAR_DOW + 7) % 7;
  if (back === 0 && h < ORDER_CLEAR_HOUR) back = 7;

  return Utilities.formatDate(new Date(Date.UTC(y, mo - 1, d - back)), TZ, 'yyyy-MM-dd');
}

// 每週五 17:00 自動清空「工作表1」的訂單資料（保留第 1 列標題）。
// 不清快照、不動其他分頁；同一輪只清一次（用指令碼屬性記住換週日），
// 所以定時觸發重複執行、或當天剛好手動執行，都不會把新寫入的資料再清一次。
function clearOrdersWeekly() {
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000);

    var boundary = getOrderClearBoundary_(new Date());
    var props = PropertiesService.getScriptProperties();
    if (props.getProperty(ORDER_CLEAR_PROP) === boundary) {
      Logger.log('每週清除訂單：' + boundary + ' 這一輪已清過，跳過');
      return 0;
    }

    var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    var sheet = ss.getSheetByName(SHEET_NAME);
    if (!sheet) return 0;

    var lastRow = sheet.getLastRow();
    if (lastRow <= 1) {
      props.setProperty(ORDER_CLEAR_PROP, boundary);
      return 0;
    }

    var cols = Math.max(sheet.getLastColumn(), 6);
    var rows = lastRow - 1;
    sheet.getRange(2, 1, rows, cols).clearContent();   // 只清資料，標題列保留
    SpreadsheetApp.flush();

    props.setProperty(ORDER_CLEAR_PROP, boundary);
    Logger.log('每週清除訂單：' + boundary + ' 清除 ' + rows + ' 列');
    return rows;
  } finally {
    lock.releaseLock();
  }
}

// 一次性安裝：建立「每週五 17:00 清除訂單」的時間觸發器（重複執行會先刪舊的再加新的）。
// 同時把目前這一輪標記成已清，避免一安裝就立刻把現有資料清掉。
function installOrderClearTrigger() {
  var handlers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < handlers.length; i++) {
    if (handlers[i].getHandlerFunction() === 'clearOrdersWeekly') {
      ScriptApp.deleteTrigger(handlers[i]);
    }
  }

  ScriptApp.newTrigger('clearOrdersWeekly')
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.FRIDAY)
    .atHour(ORDER_CLEAR_HOUR)
    .create();

  PropertiesService.getScriptProperties()
    .setProperty(ORDER_CLEAR_PROP, getOrderClearBoundary_(new Date()));

  Logger.log('已建立每週五 ' + ORDER_CLEAR_HOUR + ':00 清除訂單的觸發器；本輪起算 ' +
    getOrderClearBoundary_(new Date()) + ' 視為已清，下次換週才清空。');
}

/**
 * 優化後的重複檢查
 * - 只檢查最近 LOOKBACK_ROWS 筆
 * - 只比對「最近一次週五 17:00 之後」的訂單（每週五 17:00 換週，等於每週清除一次）
 * - 客戶 + 規格 + 品名 三欄比對
 * - 規格不區分大小寫
 */
function checkDuplicate(orders, sheet) {
  var result = { keys: {}, list: [] };
  if (!orders || orders.length === 0) return result;

  var lastRow = sheet.getLastRow();
  if (lastRow <= 1) return result;

  var startRow = Math.max(2, lastRow - LOOKBACK_ROWS + 1);
  var numRows = lastRow - startRow + 1;
  var data = sheet.getRange(startRow, 1, numRows, 4).getValues(); // A~D：時間、客戶、規格、品名

  var now = new Date();
  var windowStart = getDupWindowStart_(now);
  var orderKeys = {};

  // 先把本次訂單的 key 建起來（同一則訊息內也避免自己重複）
  for (var i = 0; i < orders.length; i++) {
    var k = makeDupKey(orders[i].customer, orders[i].spec, orders[i].item);
    orderKeys[k] = true;
  }

  for (var i = 0; i < data.length; i++) {
    var row = data[i];
    if (!row[0]) continue;

    var rowTime = new Date(row[0]);
    if (isNaN(rowTime.getTime())) continue;

    // 換週判斷：上一個週五 17:00 之前送出的訂單不算重複
    if (rowTime < windowStart) continue;

    var diffDays = (now - rowTime) / (1000 * 60 * 60 * 24);
    if (diffDays > DUPLICATE_DAYS) continue;   // 備援上限，正常不會觸發

    var dbCustomer = row[1];
    var dbSpec = row[2];
    var dbItem = row[3];

    for (var j = 0; j < orders.length; j++) {
      var o = orders[j];
      if (isSameCustomer(dbCustomer, o.customer) &&
          String(dbSpec).toLowerCase() === String(o.spec).toLowerCase() &&
          String(dbItem).trim() === String(o.item).trim()) {

        var key = makeDupKey(o.customer, o.spec, o.item);
        if (!result.keys[key]) {
          result.keys[key] = true;
          result.list.push({
            customer: o.customer,
            spec: o.spec,
            item: o.item
          });
        }
      }
    }
  }

  return result;
}

function isSameCustomer(dbName, newName) {
  if (!dbName || !newName) return false;
  var s1 = String(dbName).trim();
  var s2 = String(newName).trim();
  if (s1 === s2) return true;

  var clean1 = s1.replace(/[^\u4e00-\u9fa5a-zA-Z0-9]/g, '');
  var clean2 = s2.replace(/[^\u4e00-\u9fa5a-zA-Z0-9]/g, '');

  var suffixReg = /(中醫|診所|藥局|醫院|股份有限公司|有限公司|企業社)/g;
  clean1 = clean1.replace(suffixReg, '');
  clean2 = clean2.replace(suffixReg, '');

  if (clean1.length < 2 || clean2.length < 2) {
    return s1.indexOf(s2) !== -1 || s2.indexOf(s1) !== -1;
  }

  // 連續兩字相同即視為同一客戶（彈性匹配）
  for (var i = 0; i <= clean2.length - 2; i++) {
    if (clean1.indexOf(clean2.substring(i, i + 2)) !== -1) return true;
  }
  return false;
}

// ==========================================
// 查表自動判斷規格
// ==========================================
function getSpecLookupMap() {
  var cache = CacheService.getScriptCache();
  var cached = cache.get('SPEC_LOOKUP_MAP');
  if (cached) {
    try { return JSON.parse(cached); } catch (e) {}
  }

  var map = {};

  try {
    // 科中庫
    var kzResp = UrlFetchApp.fetch(KEZHONG_CSV, { muteHttpExceptions: true });
    if (kzResp.getResponseCode() === 200) {
      var kzData = parseInventoryCSV(kzResp.getContentText(), 'kezhong');
      for (var name in kzData) {
        if (kzData[name].spec) {
          if (!map[name] || kzData[name].spec === '200g') {
            map[name] = kzData[name].spec;
          }
        } else {
          if (!map[name]) map[name] = '一般';
        }
      }
    }

    // 錠劑庫
    var tbResp = UrlFetchApp.fetch(TABLET_CSV, { muteHttpExceptions: true });
    if (tbResp.getResponseCode() === 200) {
      var tbData = parseInventoryCSV(tbResp.getContentText(), 'tablet');
      for (var name in tbData) {
        map[name] = '錠劑';
      }
    }

    cache.put('SPEC_LOOKUP_MAP', JSON.stringify(map), 900); // 15 分鐘
  } catch (err) {
    Logger.log('載入庫存表失敗：' + err);
  }

  return map;
}

function parseInventoryCSV(csvText, source) {
  var data = {};
  var groupSpec = {};
  var skipWords = ['劃', '品名', '單方', '目前', '每日', '實際', '以上', '其他', '預訂', '下單', '交期', '庫存量表', '庫存均', '有庫存', '會缺貨'];

  var lines = csvText.split('\n');
  for (var i = 1; i < lines.length; i++) {
    var row = parseCSVLine(lines[i]);
    for (var j = 0; j < row.length; j += 4) {
      var name = (row[j] || '').trim();
      if (!name) continue;

      var specMarker = name.match(/^單方\s*(100|200)\s*[Gg]/i);
      if (specMarker) {
        groupSpec[j] = specMarker[1] + 'g';
        continue;
      }

      if (skipWords.some(function(w) { return name.indexOf(w) !== -1; })) continue;

      var spec = (source === 'tablet') ? '錠劑' : (groupSpec[j] || null);
      data[name] = { spec: spec };
    }
  }
  return data;
}

function parseCSVLine(line) {
  var result = [], current = '', inQuotes = false;
  for (var i = 0; i < line.length; i++) {
    var c = line[i];
    if (c === '"') inQuotes = !inQuotes;
    else if (c === ',' && !inQuotes) {
      result.push(current.trim());
      current = '';
    } else {
      current += c;
    }
  }
  result.push(current.trim());
  return result;
}

/**
 * 查表取得規格
 * 規則：錠劑必須品名以「錠」結尾
 */
function lookupSpecByName(itemName, lookupMap) {
  if (!itemName || !lookupMap) return null;

  if (lookupMap[itemName]) {
    var spec = lookupMap[itemName];
    if (spec === '錠劑' && !itemName.endsWith('錠')) return null;
    return spec;
  }

  // 使用者沒打「錠」就不自動轉成錠劑
  if (!itemName.endsWith('錠') && lookupMap[itemName + '錠'] === '錠劑') {
    return null;
  }

  var suffixes = ['湯', '散', '丸', '飲', '膏', '丹', '煎', '劑', '露', '片'];
  for (var i = 0; i < suffixes.length; i++) {
    var tryName = itemName + suffixes[i];
    if (lookupMap[tryName] && lookupMap[tryName] !== '錠劑') {
      return lookupMap[tryName];
    }
  }

  if (itemName.endsWith('錠')) {
    var without = itemName.slice(0, -1);
    if (lookupMap[without] && lookupMap[without] !== '錠劑') {
      return lookupMap[without];
    }
  }

  return null;
}

// ==========================================
// 訂單解析（最終優化版）
// ==========================================
function parseOrder(text, userId, timestamp) {
  var lines = text.split('\n').map(function(l) { return l.trim(); }).filter(Boolean);
  var orders = [];
  var currentCustomer = userId;
  var currentSpec = '';
  var remark = '';
  var timeStr = Utilities.formatDate(new Date(timestamp), 'Asia/Taipei', 'yyyy-MM-dd HH:mm:ss');
  var lookupMap = getSpecLookupMap();

  function extractSpec(str) {
    if (!str) return null;
    var s = str.toLowerCase().replace(/\s+/g, '');
    if (/200\s*g|200g|單方200g/.test(s)) return '200g';
    if (/100\s*g|100g|單方100g/.test(s)) return '100g';
    // 「錠」可能是品名的一部分（例如乙字湯錠），僅錠劑才視為行內規格。
    if (/錠劑/.test(s)) return '錠劑';
    if (/單方/.test(s)) return '單方';
    if (/複方|科中/.test(s)) return '';
    return null;
  }

  // 規格標題可使用全形或半形括號，例如（200g）、(100g)、（錠劑）。
  // 規格會沿用到下一個規格標題出現為止。
  function extractSpecHeader(str) {
    if (!str) return null;
    var s = String(str).toLowerCase()
      .replace(/\s+/g, '')
      .replace(/[（(［\[]/g, '')
      .replace(/[）)］\]]/g, '');

    if (/^(?:單方)?200g$/.test(s)) return '200g';
    if (/^(?:單方)?100g$/.test(s)) return '100g';
    if (/^(?:錠劑|錠)$/.test(s)) return '錠劑';
    if (/^單方$/.test(s)) return '單方';
    if (/^(?:複方|科中)$/.test(s)) return '';
    return null;
  }

  function cleanItemName(name) {
    return name
      .replace(/[（(]\s*(100|200)\s*[gG]\s*[）)]/g, '')
      .replace(/\s*(100|200)\s*[gG]/gi, '')
      .replace(/\s*錠劑/g, '')
      .replace(/\s*(單方|複方|科中)/g, '')
      .replace(/\s+/g, ' ')
      .trim();
  }

  // 處理「各N」
  var gePositions = [];
  for (var i = 0; i < lines.length; i++) {
    var m = lines[i].match(/^各\s*(\d{1,3})$/);
    if (m) gePositions.push({ index: i, qty: m[1] });
  }
  for (var g = gePositions.length - 1; g >= 0; g--) {
    var geIdx = gePositions[g].index;
    var geQty = gePositions[g].qty;
    var prev = g > 0 ? gePositions[g - 1].index : -1;
    var j = geIdx - 1;
    while (j > prev) {
      var lj = lines[j];
      if (lj.startsWith('@') || extractSpecHeader(lj) !== null) break;
      if (!/\d{1,3}(?:[瓶罐包盒顆粒]|\s*$)/.test(lj)) {
        lines[j] = lj + ' ' + geQty;
      }
      j--;
    }
    lines.splice(geIdx, 1);
  }

  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    if (!line) continue;

    // 客戶名
    if (line.startsWith('@')) {
      currentCustomer = line.substring(1).trim();
      continue;
    }
    var q = line.match(/^[\[［「](.+?)[\]］」]$/);
    if (q) {
      currentCustomer = q[1].trim();
      continue;
    }

    // 獨立規格標題；支援（200g）、(100g)、（錠劑）等格式。
    var headerSpec = extractSpecHeader(line);
    if (headerSpec !== null) {
      currentSpec = headerSpec;
      continue;
    }

    // ===== 品名 + 數量（重點修正）=====
    var itemName = '';
    var quantity = '1';
    var itemSpec = currentSpec;

    // 優先：品名 + 數字 + （100g/200g）  例如 延胡索5（100g）
    var specialMatch = line.match(/^(.+?)(\d+(?:\.\d+)?)\s*[（(]\s*(100|200)\s*[gG]\s*[）)]\s*$/i);
    if (specialMatch) {
      itemName = specialMatch[1].trim();
      quantity = specialMatch[2];
      itemSpec = specialMatch[3].toLowerCase() + 'g';
    } else {
      // 一般格式
      var match = line.match(/^(.+?)(?:[\s*xX×＊]+|\s+)(\d+(?:\.\d+)?)\s*(?:[瓶罐包盒顆粒gG]|)?$/);
      if (!match) {
        match = line.match(/^(.+?)(\d+(?:\.\d+)?)\s*(?:[瓶罐包盒顆粒]|)?$/);
      }

      if (match) {
        itemName = match[1].trim();
        quantity = match[2];
      } else {
        itemName = line;
      }

      // 從品名再抽規格
      var nameSpec = extractSpec(itemName);
      if (nameSpec !== null) {
        itemSpec = nameSpec;
        itemName = cleanItemName(itemName);
      }
    }

    // 特殊：麻黃
    if (itemName === '麻黃' || itemName === '麻黃200g') {
      itemName = '麻黃200g';
      itemSpec = '健保';
    }

    // 查表自動判斷
    if (!itemSpec || itemSpec === '一般') {
      var looked = lookupSpecByName(itemName, lookupMap);
      if (looked) itemSpec = looked;
    }

    // 所有複方 / 沒明確規格 → 預設 200g
    if (!itemSpec || itemSpec === '一般') {
      itemSpec = '200g';
    }

    if (itemName.length < 2) {
      remark += (remark ? ' ' : '') + line;
      continue;
    }

    orders.push({
      time: timeStr,
      customer: currentCustomer,
      spec: itemSpec,
      item: itemName,
      quantity: quantity,
      userId: userId
    });
  }

  if (orders.length > 0) orders[0].remark = remark;
  return { orders: orders, finalCustomer: currentCustomer };
}

function replyToUser(replyToken, message) {
  var token = PropertiesService.getScriptProperties().getProperty('LINE_TOKEN');
  if (!token) return;

  UrlFetchApp.fetch('https://api.line.me/v2/bot/message/reply', {
    method: 'post',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    },
    payload: JSON.stringify({
      replyToken: replyToken,
      messages: [{ type: 'text', text: message }]
    }),
    muteHttpExceptions: true
  });
}

// ==========================================
// 庫存異動與快照
// ==========================================
function getOrCreateSheet(ss, name, headers) {
  var sheet = ss.getSheetByName(name);
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
  var s = value.toString().trim();
  var m = s.match(/(\d{4})[-/](\d{1,2})[-/](\d{1,2})/);
  if (m) return m[1] + '-' + ('0' + m[2]).slice(-2) + '-' + ('0' + m[3]).slice(-2);
  return s.slice(0, 10);
}

// 目前這一週的起始日（yyyy-MM-dd）。
// 分界固定在每週五 18:00：週五 18:00 之前仍算上一週，之後才算新的一週；
// 週五 18:00 之後的第一次更新，就是新一週的第一批異動。
function getWeekStart_(now) {
  now = now || new Date();
  var y = Number(Utilities.formatDate(now, TZ, 'yyyy'));
  var mo = Number(Utilities.formatDate(now, TZ, 'MM'));
  var d = Number(Utilities.formatDate(now, TZ, 'dd'));
  var h = Number(Utilities.formatDate(now, TZ, 'HH'));
  var dow = new Date(Date.UTC(y, mo - 1, d)).getUTCDay();   // 0=週日、5=週五
  var back = (dow - WEEK_RESET_DOW + 7) % 7;                // 距離上一個週五幾天
  if (back === 0 && h < WEEK_RESET_HOUR) back = 7;           // 本週五還沒過 18:00 → 仍屬上一週
  return Utilities.formatDate(new Date(Date.UTC(y, mo - 1, d - back)), TZ, 'yyyy-MM-dd');
}

// 換週清理：把分界日之前的異動紀錄刪掉，只保留「分界前最後一批（同一天）」當新週期的起點。
// 本週（分界日之後）已經寫入的紀錄一定要留著，否則剛換週就把本週資料清掉了。
// 回傳被刪掉的列數，方便寫 log。
function pruneOldChanges_(changesSheet, weekStart) {
  var data = changesSheet.getDataRange().getValues();
  if (data.length <= 1) return 0;

  var lastOldDate = '';
  for (var i = 1; i < data.length; i++) {
    var d = normalizeDate_(data[i][0]);
    if (d && d < weekStart && d > lastOldDate) lastOldDate = d;
  }
  if (!lastOldDate) return 0;   // 沒有上一週的資料，不必清

  var keep = [];
  for (var i = 1; i < data.length; i++) {
    var d = normalizeDate_(data[i][0]);
    if (d >= weekStart || d === lastOldDate) keep.push(data[i].slice(0, 6));
  }

  var removed = (data.length - 1) - keep.length;
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

// ==========================================================
// 異動比對用的品名正規化
// 同一品項若品名尾字不同（例如「川七錠1000T」與「川七錠1000T錠」），比對時視為同一項，
// 避免同一品項同時被記成「新增」與「消失」而在畫面上重複顯示。
// 只用於比對 key，顯示仍用原始品名。
// ==========================================================
function normChangeName_(name) {
  var n = String(name === null || name === undefined ? '' : name)
    .replace(/\s+/g, '')
    .replace(/锭/g, '錠')
    .replace(/碇/g, '錠')
    .replace(/碙/g, '錠');
  // 名稱中段已有「錠」（如 川七錠1000T）時，尾端多打的「錠」視為同一品項
  if (n.length > 1 && n.charAt(n.length - 1) === '錠' && n.substring(0, n.length - 1).indexOf('錠') !== -1) {
    n = n.substring(0, n.length - 1);
  }
  return n;
}

function changeKeyOf_(db, name) {
  return (db === '錠劑' ? 'TB' : 'KZ') + ':' + normChangeName_(name);
}

// 同一品項同時出現在「新增」與「消失」→ 兩邊都剔除；同一批裡重複的同名品項也只留一筆
function dedupeChanges_(changes) {
  changes = changes || {};
  var added = changes.added || [];
  var removed = changes.removed || [];
  var statusChanged = changes.statusChanged || [];

  var addKeys = {}, remKeys = {}, skip = {};
  added.forEach(function(it) { addKeys[changeKeyOf_(it.db, it.name)] = true; });
  removed.forEach(function(it) { remKeys[changeKeyOf_(it.db, it.name)] = true; });
  Object.keys(addKeys).forEach(function(k) { if (remKeys[k]) skip[k] = true; });

  var seenA = {}, seenR = {}, seenS = {};
  var outAdded = added.filter(function(it) {
    var k = changeKeyOf_(it.db, it.name);
    if (skip[k] || seenA[k]) return false;
    seenA[k] = true;
    return true;
  });
  var outRemoved = removed.filter(function(it) {
    var k = changeKeyOf_(it.db, it.name);
    if (skip[k] || seenR[k]) return false;
    seenR[k] = true;
    return true;
  });
  var outStatus = statusChanged.filter(function(it) {
    var k = changeKeyOf_(it.db, it.name);
    if (seenS[k]) return false;
    seenS[k] = true;
    return true;
  });

  return { added: outAdded, removed: outRemoved, statusChanged: outStatus };
}

function getSnapshot(e) {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var snapshotSheet = getOrCreateSheet(ss, SNAPSHOT_SHEET, ['日期', '資料庫類型', '品名', '狀態']);
  var data = snapshotSheet.getDataRange().getValues();
  if (data.length <= 1) {
    return ContentService.createTextOutput(JSON.stringify({ snapshot: {}, date: '' }))
      .setMimeType(ContentService.MimeType.JSON);
  }

  var latestDate = '';
  var rowDates = [];
  for (var i = 1; i < data.length; i++) {
    var d = normalizeDate_(data[i][0]);
    rowDates.push(d);
    if (d && d > latestDate) latestDate = d;
  }

  var snapshot = {};
  for (var i = 1; i < data.length; i++) {
    if (rowDates[i - 1] !== latestDate) continue;
    var prefix = data[i][1] === '錠劑' ? 'TB:' : 'KZ:';
    snapshot[prefix + data[i][2]] = data[i][3];
  }

  return ContentService.createTextOutput(JSON.stringify({ snapshot: snapshot, date: latestDate }))
    .setMimeType(ContentService.MimeType.JSON);
}

// 本週所有異動（「異動紀錄」分頁中，換週分界日之後的全部列），依日期分組給前端常駐顯示用。
// 記錄本身是往後追加、不覆蓋；每週五 18:00 之後換週，只保留分界前最後一批當起點。
function getLatestChanges() {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var changesSheet = getOrCreateSheet(ss, CHANGES_SHEET, ['日期', '資料庫類型', '品名', '舊狀態', '新狀態', '異動類型']);
  var weekStart = getWeekStart_();
  var data = changesSheet.getDataRange().getValues();
  var emptyChanges = { added: [], removed: [], statusChanged: [] };
  var empty = { date: '', baseDate: '', weekStart: weekStart, groups: [], anchor: null, changes: emptyChanges };

  if (data.length <= 1) {
    return ContentService.createTextOutput(JSON.stringify(empty))
      .setMimeType(ContentService.MimeType.JSON);
  }

  var byDate = {};      // 本週（分界日之後）
  var oldByDate = {};   // 分界日之前（換週時只保留最後一批，當作本期起點）
  var latestDate = '';
  for (var i = 1; i < data.length; i++) {
    var d = normalizeDate_(data[i][0]);
    if (!d) continue;

    // 分界日之前的舊紀錄不算「本週」，但最後一批要留下來顯示成起點
    var bucket = (d >= weekStart) ? byDate : oldByDate;
    if (!bucket[d]) bucket[d] = { added: [], removed: [], statusChanged: [] };

    var db = data[i][1] === '錠劑' ? '錠劑' : '科中';
    var name = data[i][2] ? data[i][2].toString() : '';
    var oldStatus = data[i][3];
    var newStatus = data[i][4];
    var type = data[i][5] ? data[i][5].toString() : '';

    if (type === '新增') {
      bucket[d].added.push({ name: name, status: newStatus, db: db });
    } else if (type === '消失') {
      bucket[d].removed.push({ name: name, status: oldStatus, db: db });
    } else {
      bucket[d].statusChanged.push({ name: name, oldStatus: oldStatus, newStatus: newStatus, db: db });
    }
    if (d >= weekStart && d > latestDate) latestDate = d;
  }

  // 同一天同一品項被同時記成「新增」與「消失」時只算一次（多半是品名尾字不同造成的假異動）
  Object.keys(byDate).forEach(function(day) { byDate[day] = dedupeChanges_(byDate[day]); });
  Object.keys(oldByDate).forEach(function(day) { oldByDate[day] = dedupeChanges_(oldByDate[day]); });

  // 分界日之前的最後一批：換週時保留在表裡當起點，順便回傳讓畫面顯示
  var anchor = null;
  var anchorDates = Object.keys(oldByDate).sort();
  if (anchorDates.length) {
    var anchorDate = anchorDates[anchorDates.length - 1];
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
  var groups = [];
  Object.keys(byDate).sort().reverse().forEach(function(dateKey) {
    groups.push({
      date: dateKey,
      added: byDate[dateKey].added,
      removed: byDate[dateKey].removed,
      statusChanged: byDate[dateKey].statusChanged
    });
  });

  // 快照只保留最新一份，基準日改由指令碼屬性取得
  var props = PropertiesService.getScriptProperties();
  var baseDate = '';
  if (props.getProperty('LAST_CHANGE_DATE') === latestDate) {
    baseDate = normalizeDate_(props.getProperty('LAST_BASE_DATE'));
  }
  if (!baseDate) baseDate = getBaseDate_(ss, latestDate);

  return ContentService.createTextOutput(JSON.stringify({
    date: latestDate,
    baseDate: baseDate,
    weekStart: weekStart,
    groups: groups,
    anchor: anchor,               // 換週後保留的最後一批（起點），前端另外顯示
    changes: byDate[latestDate] || emptyChanges   // 相容舊版前端：只給最新一天
  })).setMimeType(ContentService.MimeType.JSON);
}

// 備援用：快照分頁若還留有舊日期，取早於異動日的最近一個（快照只留最新一份後通常為空）
function getBaseDate_(ss, latestDate) {
  var snapshotSheet = getOrCreateSheet(ss, SNAPSHOT_SHEET, ['日期', '資料庫類型', '品名', '狀態']);
  var data = snapshotSheet.getDataRange().getValues();
  var baseDate = '';
  for (var i = 1; i < data.length; i++) {
    var d = normalizeDate_(data[i][0]);
    if (d && d < latestDate && d > baseDate) baseDate = d;
  }
  return baseDate;
}

function writeChangesAndSnapshot(date, changes, snapshot) {
  changes = dedupeChanges_(changes || {});
  snapshot = snapshot || {};
  date = date || Utilities.formatDate(new Date(), 'Asia/Taipei', 'yyyy-MM-dd');

  var changeRows = [], snapshotRows = [];
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(10000);
    var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    var changesSheet = getOrCreateSheet(ss, CHANGES_SHEET, ['日期', '資料庫類型', '品名', '舊狀態', '新狀態', '異動類型']);
    var snapshotSheet = getOrCreateSheet(ss, SNAPSHOT_SHEET, ['日期', '資料庫類型', '品名', '狀態']);

    if (changes.added) {
      changes.added.forEach(function(item) {
        changeRows.push([date, item.db, item.name, '(新增)', item.status, '新增']);
      });
    }
    if (changes.removed) {
      changes.removed.forEach(function(item) {
        changeRows.push([date, item.db, item.name, item.status, '(消失)', '消失']);
      });
    }
    if (changes.statusChanged) {
      changes.statusChanged.forEach(function(item) {
        changeRows.push([date, item.db, item.name, item.oldStatus, item.newStatus, '狀態變化']);
      });
    }

    // 異動紀錄保留一週：跨過分界日才清掉更早的紀錄，只留分界前最後一批當新週期起點。
    // 放在寫入前做，確保換週後第一批異動是接在保留的那批後面。
    var weekStart = getWeekStart_(new Date());
    var pruned = pruneOldChanges_(changesSheet, weekStart);
    if (pruned > 0) Logger.log('換週清理異動紀錄：刪除 ' + pruned + ' 列（本週起始 ' + weekStart + '）');

    if (changeRows.length) {
      changesSheet.getRange(changesSheet.getLastRow() + 1, 1, changeRows.length, 6).setValues(changeRows);
    }

    for (var key in snapshot) {
      var prefix = key.substring(0, 3);
      snapshotRows.push([date, prefix === 'TB:' ? '錠劑' : '科中', key.substring(3), snapshot[key]]);
    }

    // 快照只保留最新一份：先取出舊快照日期（當作這批異動的基準日），再整表覆蓋
    var prevDate = '';
    var existing = snapshotSheet.getDataRange().getValues();
    for (var i = 1; i < existing.length; i++) {
      var d = normalizeDate_(existing[i][0]);
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
    var props = PropertiesService.getScriptProperties();
    props.setProperty('SNAPSHOT_DATE', date);
    props.setProperty('LAST_BASE_DATE', prevDate);
    props.setProperty('LAST_CHANGE_DATE', date);

    SpreadsheetApp.flush();
  } catch (e) {
    Logger.log('寫入異動失敗：' + e);
    return ContentService.createTextOutput(JSON.stringify({ error: 'System busy' }))
      .setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }

  return ContentService.createTextOutput(JSON.stringify({
    success: true,
    changesCount: changeRows.length,
    snapshotCount: snapshotRows.length
  })).setMimeType(ContentService.MimeType.JSON);
}
