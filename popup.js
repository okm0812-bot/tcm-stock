// NHI TCM Fee Lookup - Chrome Extension
const NHI_PAGE = 'https://info.nhi.gov.tw/INAE1000/INAE1000S01';
const FUNC_TYPE_TCM = '60'; // 中醫一般科

function showStatus(msg, type = 'info') {
  const el = document.getElementById('status');
  el.textContent = msg;
  el.className = 'status ' + type;
  el.style.display = 'block';
}

function showResults(results) {
  const preview = document.getElementById('resultPreview');
  const list = document.getElementById('resultList');
  if (!results || results.length === 0) {
    preview.style.display = 'none';
    return;
  }
  const display = results.slice(0, 3);
  list.innerHTML = display.map(r => `
    <div class="result-row">
      <span class="name" title="${r.name}">${r.name}</span>
      <span class="fee">${r.fee}</span>
    </div>
  `).join('');
  preview.style.display = 'block';
}

function setLoading(loading) {
  const btn = document.getElementById('searchBtn');
  btn.disabled = loading;
  btn.textContent = loading ? '⏳ 處理中...' : '🔍 查詢';
}

// Open the NHI page with pre-filled parameters
document.getElementById('searchBtn').addEventListener('click', async () => {
  const city = document.getElementById('citySelect').value;
  const name = document.getElementById('hospitalName').value.trim();

  if (!city) {
    showStatus('請先選擇縣市', 'error');
    return;
  }

  setLoading(true);
  showStatus('正在打開健保署頁面並填入參數...', 'loading');

  // Build the NHI URL with query parameters
  // The NHI page accepts POST, but we can pre-build URL with parameters
  // Actually NHI uses POST forms, so we need to inject script into the page
  const url = `${NHI_PAGE}?C_AreaCod=${city}&C_FuncType=${FUNC_TYPE_TCM}`;

  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    // Check if already on the NHI page
    const isOnNhiPage = tab.url && tab.url.includes('info.nhi.gov.tw');

    if (!isOnNhiPage) {
      // Navigate to NHI page first
      await chrome.tabs.update(tab.id, { url: url });
      showStatus('正在跳轉到健保署頁面，請稍候...', 'loading');
      
      // Wait for navigation, then inject
      setTimeout(async () => {
        await chrome.scripting.executeScript({
          target: { tabId: tab.id },
          func: (cityCode, hospName) => {
            autoFillAndSearch(cityCode, hospName);
          },
          args: [city, name]
        });
        setLoading(false);
        showStatus('已自動填入參數，請查看新分頁', 'success');
      }, 2000);
    } else {
      // Already on the page, just inject
      await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: (cityCode, hospName) => {
          autoFillAndSearch(cityCode, hospName);
        },
        args: [city, name]
      });
      setLoading(false);
      showStatus('已自動填入並查詢，請查看頁面', 'success');
    }
  } catch (err) {
    setLoading(false);
    showStatus('錯誤：' + err.message, 'error');
  }
});

// Open NHI page without auto-fill
document.getElementById('openPageBtn').addEventListener('click', async () => {
  const city = document.getElementById('citySelect').value;
  const name = document.getElementById('hospitalName').value.trim();
  
  let url = NHI_PAGE;
  if (city) {
    url += `?C_AreaCod=${city}`;
    if (name) url += `&C_HospName=${encodeURIComponent(name)}`;
  }
  
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  await chrome.tabs.create({ url: url, active: true });
  showStatus('已在新分頁開啟健保署頁面', 'success');
});

// This function runs inside the NHI page context
function autoFillAndSearch(cityCode, hospName) {
  try {
    // NHI page selectors - these need to be verified against actual page
    // Try multiple possible selectors
    const selectors = {
      city: [
        'select[name="C_AreaCod"]',
        '#C_AreaCod',
        'select#C_AreaCod',
        'select[id="C_AreaCod"]'
      ],
      funcType: [
        'select[name="C_FuncType"]',
        '#C_FuncType',
        'input[name="C_FuncType"]'
      ],
      name: [
        'input[name="ws_hosp_name"]',
        '#ws_hosp_name',
        'input[id="ws_hosp_name"]',
        'input[name="C_HospName"]',
        '#C_HospName'
      ],
      search: [
        'button.btn-primary',
        'button.btn-query',
        '#btnQuery',
        'input[type="submit"]',
        'button[type="submit"]'
      ]
    };

    let cityEl = null, nameEl = null, searchBtn = null;
    
    // Find city selector
    for (const sel of selectors.city) {
      cityEl = document.querySelector(sel);
      if (cityEl) break;
    }
    
    // Find name input
    for (const sel of selectors.name) {
      nameEl = document.querySelector(sel);
      if (nameEl) break;
    }
    
    // Find search button
    for (const sel of selectors.search) {
      searchBtn = document.querySelector((sel.startsWith('button') || sel.startsWith('input')) ? sel : 'button' + sel);
      if (searchBtn) break;
    }
    
    // If no button found, try all buttons
    if (!searchBtn) {
      const buttons = document.querySelectorAll('button');
      for (const btn of buttons) {
        const text = btn.textContent.trim().toLowerCase();
        if (text.includes('查詢') || text.includes('search') || text.includes('query')) {
          searchBtn = btn;
          break;
        }
      }
    }

    if (!cityEl && !nameEl && !searchBtn) {
      // Page might not be loaded yet, try again
      setTimeout(() => autoFillAndSearch(cityCode, hospName), 1000);
      return;
    }

    // Fill in values
    if (cityEl) {
      if (cityEl.tagName === 'SELECT') {
        for (let i = 0; i < cityEl.options.length; i++) {
          if (cityEl.options[i].value === cityCode || cityEl.options[i].text.includes(cityCode)) {
            cityEl.selectedIndex = i;
            cityEl.dispatchEvent(new Event('change', { bubbles: true }));
            break;
          }
        }
      } else {
        cityEl.value = cityCode;
        cityEl.dispatchEvent(new Event('input', { bubbles: true }));
      }
    }

    if (nameEl && hospName) {
      nameEl.value = hospName;
      nameEl.dispatchEvent(new Event('input', { bubbles: true }));
    }

    if (searchBtn) {
      searchBtn.click();
    } else {
      // Try pressing Enter in the name field
      if (nameEl) {
        nameEl.dispatchEvent(new KeyboardEvent('keypress', { key: 'Enter', bubbles: true }));
      }
    }
  } catch (err) {
    console.error('Auto-fill error:', err);
  }
}