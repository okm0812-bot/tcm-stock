// popup.js - NHI 中醫掛號費查詢 Chrome 擴充功能
const NHI_QUERY = 'https://info.nhi.gov.tw/INAE1000/INAE1000S01';

// UI helpers
function showStatus(msg, type = 'info') {
  const el = document.getElementById('status');
  if (!el) return;
  el.textContent = msg;
  el.className = 'status ' + type;
  el.style.display = 'block';
}
function setLoading(on) {
  const btn = document.getElementById('searchBtn');
  if (!btn) return;
  btn.disabled = on;
  btn.textContent = on ? '⏳ 處理中...' : '🔍 查詢';
}

// 鄉鎮市二層連動（與 HTML 同步）
const TOWN_MAP = {
  '01': ['中正區','大同區','中山區','松山區','大安區','萬華區','信義區','士林區','北投區','內湖區','南港區','文山區'],
  '02': ['鹽埕區','鼓山區','左營區','楠梓區','三民區','新興區','前金區','苓雅區','前鎮區','旗津區','小港區','鳳山區','林園區','大寮區','大樹區','大社區','仁武區','鳥松區','橋頭區','燕巢區','田寮區','阿蓮區','路竹區','湖內區','茄萣區','永安區','彌陀區','梓官區','六龜區','甲仙區','杉林區','內門區','茂林區','桃源區','那瑪夏區','岡山區','旗山區','美濃區'],
  '03': ['中區','東區','南區','西區','北區','西屯區','南屯區','北屯區','豐原區','大里區','太平區','清水區','沙鹿區','大甲區','東勢區','梧棲區','烏日區','大肚區','龍井區','霧峰區','潭子區','大雅區','新小區','石岡區','和平區','神岡區','后里區','外埔區','大安區'],
  '04': ['中西區','東區','南區','北區','安南區','安平區','永康區','歸仁區','新化區','左鎮區','玉井區','楠西區','南化區','仁德區','關廟區','龍崎區','官田區','麻豆區','佳里區','西港區','七股區','將軍區','學甲區','北門區','新營區','後壁區','白河區','東山區','六甲區','下營區','柳營區','鹽水區','善化區','大內區','山上區','新市區','安定區'],
  '05': ['板橋區','中和區','永和區','土城區','樹林區','三峽區','蘆洲區','三重區','新莊區','泰山區','林口區','八德區','大溪區','龍潭區','龜山區','鶯歌區','新店區','深坑區','石碇區','坪林區','烏來區','淡水區','三芝區','石門區','金山區','萬里區','汐止區','瑞芳區','貢寮區','平溪區','雙溪區'],
  '06': ['桃園區','中壢區','平鎮區','楊梅區','龍潭區','龜山區','八德區','大溪區','蘆竹區','大園區','觀音區','新屋區','復興區'],
  '07': ['東區','北區'],
  '08': ['竹北市','竹東鎮','新埔鎮','關西鎮','湖口鄉','新豐鄉','峨眉鄉','寶山鄉','北埔鄉','芎林鄉','橫山鄉','尖石鄉','五峰鄉'],
  '09': ['苗栗市','頭份市','竹南鎮','後龍鎮','通霄鎮','苑裡鎮','卓蘭鎮','西湖鄉','苗栗市','頭屋鄉','公館鄉','大湖鄉','泰安鄉','銅鑼鄉','南庄鄉','三義鄉','造橋鄉','三灣鄉','獅潭鄉'],
  '10': ['彰化市','員林市','和美鎮','鹿港鎮','溪湖鎮','二林鎮','田中鎮','北斗鎮','花壇鄉','芬園鄉','大村鄉','埔心鄉','永靖鄉','社頭鄉','二水鄉','田尾鄉','埤頭鄉','溪州鄉','竹塘鄉','大城鄉','芳苑鄉','福興鄉','秀水鄉','埔鹽鄉','線西鄉','伸港鄉'],
  '11': ['南投市','埔里鎮','草屯鎮','竹山鎮','集集鎮','名間鄉','鹿谷鄉','中寮鄉','魚池鄉','國姓鄉','水里鄉','信義鄉','仁愛鄉'],
  '12': ['斗六市','斗南鎮','虎尾鎮','西螺鎮','土庫鎮','北港鎮','古坑鄉','大埤鄉','莿桐鄉','林內鄉','二崙鄉','崙背鄉','麥寮鄉','東勢鄉','褒忠鄉','台西鄉','元長鄉','四湖鄉','口湖鄉','水林鄉'],
  '13': ['太保市','朴子市','布袋鎮','義竹鄉','鹿草鄉','水上鄉','番路鄉','梅山鄉','竹崎鄉','中埔鄉','大埔鄉','吳鳳鄉'],
  '14': ['東區','西區'],
  '15': ['屏東市','潮州鎮','東港鎮','恆春鎮','萬丹鄉','長治鄉','麟洛鄉','九如鄉','里港鄉','鹽埔鄉','高樹鄉','萬巒鄉','內埔鄉','竹田鄉','新埤鄉','枋寮鄉','新園鄉','崁頂鄉','林邊鄉','南州鄉','佳冬鄉','琉球鄉','車城鄉','滿州鄉','枋山鄉','春日鄉','獅子鄉','牡丹鄉','三地門鄉','霧台鄉','瑪家鄉','泰武鄉','來義鄉','春日鄉','獅子鄉'],
  '16': ['宜蘭市','羅東鎮','蘇澳鎮','頭城鎮','礁溪鄉','壯圍鄉','員山鄉','冬山鄉','五結鄉','三星鄉','大同鄉','南澳鄉'],
  '17': ['花蓮市','鳳林鎮','玉里鎮','新城鄉','吉安鄉','壽豐鄉','秀林鄉','豐濱鄉','瑞穗鄉','萬榮鄉','光復鄉','卓溪鄉'],
  '18': ['臺東市','成功鎮','關山鎮','卑南鄉','鹿野鄉','池上鄉','東河鄉','長濱鄉','太麻里鄉','金峰鄉','大武鄉','達仁鄉','綠島鄉','蘭嶼鄉','海端鄉','延平鄉'],
  '19': ['馬公市','湖西鄉','白沙鄉','西嶼鄉','望安鄉','七美鄉'],
  '20': ['中正區','信義區','仁愛區','中山區','安樂區','暖暖區','七堵區'],
  '21': ['金城鎮','金沙鎮','金湖鎮','金寧鄉','烈嶼鄉','烏坵鄉'],
  '22': ['南竿鄉','北竿鄉','莒光鄉','東引鄉'],
};

// DOM 連動：選縣市 → 填充鄉鎮市
document.getElementById('citySelect').addEventListener('change', function () {
  const townSel = document.getElementById('townSelect');
  const cityCode = this.value;
  if (!cityCode) {
    townSel.disabled = true;
    townSel.innerHTML = '<option value="">-- 請先選擇縣市 --</option>';
    return;
  }
  const towns = TOWN_MAP[cityCode] || [];
  townSel.disabled = false;
  townSel.innerHTML = '<option value="">全部（不限）</option>';
  towns.forEach(t => {
    const opt = document.createElement('option');
    opt.value = t;
    opt.textContent = t;
    townSel.appendChild(opt);
  });
});

// 查詢按鈕
document.getElementById('searchBtn').addEventListener('click', async () => {
  const city     = document.getElementById('citySelect').value;
  const town     = document.getElementById('townSelect').value;
  const funcType = document.getElementById('funcTypeSelect').value;
  const name     = document.getElementById('hospitalName').value.trim();

  if (!city) { showStatus('⚠️ 請先選擇縣市', 'error'); return; }

  setLoading(true);
  showStatus('正在開啟健保署頁面...', 'loading');

  try {
    // 建 URL
    let url = NHI_QUERY + '?C_AreaCod=' + city + '&C_FuncType=' + funcType;
    if (town) url += '&C_Town=' + encodeURIComponent(town);
    if (name)  url += '&ws_hosp_name=' + encodeURIComponent(name);
    url += '&PageSize=50';

    const newTab = await chrome.tabs.create({ url, active: true });

    // 等頁面 DOM 載入
    await waitForDOM(newTab.id, 5000);

    // 注入腳本：設定每頁 50 筆 + 點查詢
    await chrome.scripting.executeScript({
      target: { tabId: newTab.id },
      func: autoSetAndSearch,
      args: [{ funcType, name }]
    });

    setLoading(false);
    showStatus('✅ 已開啟並自動查詢', 'success');
  } catch (err) {
    setLoading(false);
    showStatus('❌ ' + err.message, 'error');
  }
});

// 等待 DOM 就緒
function waitForDOM(tabId, timeout = 5000) {
  return new Promise(resolve => {
    let elapsed = 0;
    const iv = setInterval(async () => {
      elapsed += 300;
      if (elapsed >= timeout) { clearInterval(iv); resolve(); return; }
      try {
        await chrome.tabs.sendMessage(tabId, { type: 'ping' });
        clearInterval(iv); resolve();
      } catch (_) { /* 頁面尚未就緒 */ }
    }, 300);
  });
}

// 在健保署頁面內執行的腳本
function autoSetAndSearch({ funcType, name }) {

  // === DOM ref ===
  // ref=e10  縣市 combobox
  // ref=e27  鄉鎮市 combobox
  // ref=e74  院所層級 combobox
  // ref=e89  已加入計畫 combobox
  // ref=e168 一般服務項目 combobox
  // ref=e197 預防保健 combobox
  // ref=e210 型態別 combobox
  // ref=e215 診療科別 combobox
  // ref=e362 院所名稱 textbox
  // ref=e382 每頁筆數 combobox
  // ref=e386 查詢 button

  function selectByText(selectEl, text) {
    if (!selectEl) return false;
    for (let i = 0; i < selectEl.options.length; i++) {
      if (selectEl.options[i].textContent === text) {
        selectEl.selectedIndex = i;
        selectEl.dispatchEvent(new Event('change', { bubbles: true }));
        return true;
      }
    }
    return false;
  }

  function selectByValue(selectEl, val) {
    if (!selectEl) return false;
    for (let i = 0; i < selectEl.options.length; i++) {
      if (selectEl.options[i].value === val) {
        selectEl.selectedIndex = i;
        selectEl.dispatchEvent(new Event('change', { bubbles: true }));
        return true;
      }
    }
    return false;
  }

  function wait(ms) { return new Promise(r => setTimeout(r, ms)); }

  async function run() {
    // 1. 型態別（URL 已預填，此處確保一致）
    if (funcType) {
      const funcTypeMap = { '60': '中醫', '01': '西醫', '02': '牙醫' };
      const ftText = funcTypeMap[funcType] || funcType;
      const allSelects = document.querySelectorAll('select');
      for (const sel of allSelects) {
        if (sel.closest('.form-group')?.querySelector('label, .col-form-label')?.textContent?.includes('型態別')) {
          selectByText(sel, ftText);
          break;
        }
      }
    }

    await wait(400);

    // 2. 診療科別 → 中醫一般科（URL 已預填，確保一致）
    if (funcType === '60') {
      const allSelects2 = document.querySelectorAll('select');
      for (const sel of allSelects2) {
        const lbl = sel.closest('.form-group')?.querySelector('label, .col-form-label');
        if (lbl && lbl.textContent.includes('診療科別')) {
          selectByText(sel, '中醫一般科');
          break;
        }
      }
      await wait(300);
    }

    // 3. 每頁筆數 → 50
    const allSelects3 = document.querySelectorAll('select');
    for (const sel of allSelects3) {
      if (sel.closest('.form-group')?.querySelector('label, .col-form-label')?.textContent?.includes('每頁')) {
        selectByValue(sel, '50');
        break;
      }
    }

    await wait(300);

    // 4. 院所名稱（URL 已預填，再次確保）
    if (name) {
      const allInputs = document.querySelectorAll('input[type="text"], input:not([type])');
      for (const inp of allInputs) {
        const lbl = inp.closest('.form-group')?.querySelector('label, .col-form-label');
        if (lbl && lbl.textContent.includes('院所名稱')) {
          inp.value = name;
          inp.dispatchEvent(new Event('input', { bubbles: true }));
          break;
        }
      }
    }

    await wait(300);

    // 5. 點查詢
    const btns = document.querySelectorAll('button');
    for (const btn of btns) {
      if (btn.textContent.trim() === '查詢') {
        btn.click();
        break;
      }
    }
  }

  run();
}
