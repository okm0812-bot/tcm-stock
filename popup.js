// NHI TCM Fee Lookup - Chrome Extension
// 自動操作健保署頁面，查詢中醫一般科院所掛號費

const NHI_QUERY_PAGE = 'https://info.nhi.gov.tw/INAE1000/INAE1000S01';
const NHI_DETAIL_PAGE = 'https://info.nhi.gov.tw/INAE1000/INAE1000S02';

// UI 狀態管理
function showStatus(msg, type = 'info') {
  const el = document.getElementById('status');
  if (!el) return;
  el.textContent = msg;
  el.className = 'status ' + type;
  el.style.display = 'block';
}

function setLoading(loading) {
  const btn = document.getElementById('searchBtn');
  if (!btn) return;
  btn.disabled = loading;
  btn.textContent = loading ? '⏳ 處理中...' : '🔍 查詢';
}

// 點擊「查詢」按鈕
document.getElementById('searchBtn').addEventListener('click', async () => {
  const city = document.getElementById('citySelect').value;
  const name = document.getElementById('hospitalName').value.trim();

  if (!city) {
    showStatus('⚠️ 請先選擇縣市', 'error');
    return;
  }

  setLoading(true);
  showStatus('正在開啟健保署頁面...', 'loading');

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    // 開新分頁前往查詢頁面
    const newTab = await chrome.tabs.create({ url: NHI_QUERY_PAGE, active: true });

    // 等待頁面載入
    await waitForPageLoad(newTab.id, 5000);

    // 注入腳本：填寫表單並查詢
    await chrome.scripting.executeScript({
      target: { tabId: newTab.id },
      func: autoFillAndSearch,
      args: [city, name]
    });

    setLoading(false);
    showStatus('✅ 已開啟健保署頁面並自動查詢', 'success');
  } catch (err) {
    setLoading(false);
    showStatus('❌ 錯誤：' + err.message, 'error');
  }
});

// 點擊「直接打開」按鈕
document.getElementById('openPageBtn').addEventListener('click', async () => {
  const city = document.getElementById('citySelect').value;
  const name = document.getElementById('hospitalName').value.trim();

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    await chrome.tabs.create({ url: NHI_QUERY_PAGE, active: true });
    showStatus('已打開健保署頁面', 'info');
  } catch (err) {
    showStatus('❌ 錯誤：' + err.message, 'error');
  }
});

// 等待頁面載入
function waitForPageLoad(tabId, timeout = 5000) {
  return new Promise((resolve, reject) => {
    let elapsed = 0;
    const interval = setInterval(async () => {
      elapsed += 200;
      if (elapsed >= timeout) {
        clearInterval(interval);
        resolve(); // 視為成功
      }
      try {
        const result = await chrome.tabs.sendMessage(tabId, { type: 'ping' });
        if (result && result.ok) {
          clearInterval(interval);
          resolve();
        }
      } catch (e) {
        // 頁面尚未就緒
      }
    }, 200);
  });
}

// 自動填寫並查詢（在健保署頁面內執行）
function autoFillAndSearch(cityName, hospitalName) {
  // 等待頁面 DOM 就緒
  function waitFor(selector, maxWait = 3000) {
    return new Promise((resolve, reject) => {
      const start = Date.now();
      function check() {
        const el = document.querySelector(selector);
        if (el) return resolve(el);
        if (Date.now() - start > maxWait) return resolve(null);
        setTimeout(check, 100);
      }
      check();
    });
  }

  async function doFill() {
    // 點擊「進階查詢」展開完整表單
    const advBtn = document.querySelector('button[data-i18n="advQuery"], button:has-text("進階查詢"), button.btn-outline-secondary');
    if (advBtn) advBtn.click();

    await new Promise(r => setTimeout(r, 500));

    // 縣市 combobox
    const citySelect = document.querySelector('select[name="C_AreaCod"], #C_AreaCod, .form-group select');
    if (citySelect) {
      for (let i = 0; i < citySelect.options.length; i++) {
        if (citySelect.options[i].text === cityName || citySelect.options[i].value === cityName) {
          citySelect.selectedIndex = i;
          citySelect.dispatchEvent(new Event('change', { bubbles: true }));
          break;
        }
      }
    }

    await new Promise(r => setTimeout(r, 300));

    // 型態別 → 中醫
    const allSelects = document.querySelectorAll('select');
    for (const sel of allSelects) {
      const label = sel.closest('.form-group')?.querySelector('label, .form-label, .form-title, .col-form-label');
      if (label && label.textContent.includes('型態')) {
        for (let i = 0; i < sel.options.length; i++) {
          if (sel.options[i].text === '中醫') {
            sel.selectedIndex = i;
            sel.dispatchEvent(new Event('change', { bubbles: true }));
            break;
          }
        }
      }
    }

    await new Promise(r => setTimeout(r, 300));

    // 診療科別 → 中醫一般科
    for (const sel of allSelects) {
      const parent = sel.closest('.form-group');
      const labelEl = parent?.querySelector('label, .form-label, .col-form-label');
      if (labelEl && labelEl.textContent.includes('診療科別')) {
        for (let i = 0; i < sel.options.length; i++) {
          if (sel.options[i].text === '中醫一般科') {
            sel.selectedIndex = i;
            sel.dispatchEvent(new Event('change', { bubbles: true }));
            break;
          }
        }
      }
    }

    await new Promise(r => setTimeout(r, 200));

    // 院所名稱
    const nameInput = document.querySelector('input[name="ws_hosp_name"], input[placeholder*="名稱"], input.form-control');
    if (nameInput && hospitalName) {
      nameInput.value = hospitalName;
      nameInput.dispatchEvent(new Event('input', { bubbles: true }));
    }

    await new Promise(r => setTimeout(r, 300));

    // 點擊查詢按鈕
    const btns = document.querySelectorAll('button');
    for (const btn of btns) {
      const t = btn.textContent.trim();
      if (t === '查詢' || t.includes('查詢')) {
        btn.click();
        return true;
      }
    }
    return false;
  }

  doFill();
}