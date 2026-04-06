# -*- coding: utf-8 -*-
html = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>科學中藥庫存查詢</title>
<style>
* { box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 15px; margin: 0; }
.container { max-width: 500px; margin: 0 auto; }
.header { text-align: center; color: white; margin-bottom: 20px; }
.header h1 { font-size: 24px; margin: 0; }
.header .status { font-size: 12px; opacity: 0.8; margin-top: 5px; }
.search-box { background: white; border-radius: 20px; padding: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
.btn-group { display: flex; gap: 8px; margin-bottom: 10px; flex-wrap: wrap; }
.btn-small { background: #667eea; color: white; border: none; padding: 8px 12px; font-size: 13px; border-radius: 20px; cursor: pointer; flex: 1; min-width: 80px; }
.btn-small:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-clear { background: #dc3545; }
textarea { width: 100%; padding: 12px; font-size: 16px; border: 2px solid #ddd; border-radius: 12px; outline: none; height: 100px; resize: none; margin-bottom: 10px; }
textarea:focus { border-color: #667eea; }
.btn { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 12px; font-size: 16px; border-radius: 25px; cursor: pointer; width: 100%; font-weight: bold; }
.btn:disabled { background: #ccc; }
.result-item { background: white; border-radius: 10px; padding: 12px; margin-top: 8px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; }
.name { font-weight: bold; font-size: 15px; flex: 1; min-width: 120px; }
.original { font-size: 12px; color: #666; width: 100%; }
.badge { font-size: 12px; padding: 4px 10px; border-radius: 15px; white-space: nowrap; }
.in-stock { background: #d4edda; color: #155724; }
.out-stock { background: #f8d7da; color: #721c24; }
.not-found { background: #e2e3e5; color: #383d41; }
.corrected { background: #fff3cd; color: #856404; }
.price { font-size: 15px; font-weight: bold; }
.summary { background: white; border-radius: 15px; padding: 15px; margin-top: 12px; text-align: center; }
.summary .total { font-size: 26px; font-weight: bold; color: #28a745; }
.summary .count { color: #666; font-size: 13px; margin-top: 4px; }
.copy-box { background: white; border-radius: 15px; padding: 15px; margin-top: 12px; }
.copy-box h4 { margin: 0 0 10px 0; font-size: 14px; color: #333; }
.copy-content { background: #f5f5f5; border-radius: 10px; padding: 12px; font-size: 14px; white-space: pre-wrap; max-height: 200px; overflow-y: auto; }
.copy-btn { background: #28a745; color: white; border: none; padding: 8px 15px; font-size: 13px; border-radius: 20px; cursor: pointer; margin-top: 10px; }
.tip { background: rgba(255,255,255,0.2); border-radius: 15px; padding: 12px; margin-top: 15px; color: white; font-size: 12px; }
.tip li { margin: 3px 0; }
.error { background: #f8d7da; color: #721c24; padding: 10px; border-radius: 10px; text-align: center; font-size: 13px; }
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>科學中藥庫存查詢</h1><div class="status" id="status">載入中...</div></div>
<div class="search-box">
<div class="btn-group">
<button class="btn-small" id="refreshBtn" onclick="loadData()">更新資料</button>
<button class="btn-small btn-clear" onclick="clearInput()">清除</button>
<button class="btn-small" id="priceBtn" onclick="togglePrice()">顯示價格</button>
</div>
<div class="btn-group">
<button class="btn-small" id="voiceBtn" onclick="startVoiceInput()">語音輸入</button>
<button class="btn-small" id="imageBtn">圖片辨識</button>
<input type="file" id="imageInput" accept="image/*" style="display:none">
</div>
<textarea id="input" placeholder="每行輸入一個產品 支援錯別字自動更正 支援數量"></textarea>
<button class="btn" id="searchBtn" onclick="search()" disabled>查詢庫存</button>
</div>
<div id="result"></div>
<div class="tip"><li>有貨 = 可出貨</li><li>缺貨 = 無庫存</li><li>點顯示價格查看價格</li></div>
</div>
<script>
const SHEET_URL="https://docs.google.com/spreadsheets/d/1ekYUBtuQNjLB0RpWGCPJN7409sL74tqT36NfzUIM6o4/gviz/tq?tqx=out:csv";
let DB={},showPrice=false;
const isSingleHerb=n=>!["湯","散","丸","飲","煎","丹","膏"].some(c=>n.includes(c));
const parseCSVLine=l=>{let r=[],c="",q=false;for(let ch of l){if(ch==='"')q=!q;else if(ch===','&&!q){r.push(c.trim());c="";}else c+=ch;}r.push(c.trim());return r;};
const parseCSV=csv=>{let d={};const sk=["劃","品名","單方","目前","每日","實際","以上"];csv.split("\\n").slice(1).forEach(l=>{let row=parseCSVLine(l);for(let j=0;j<row.length;j+=4){let[n,s,p]=[row[j],row[j+1],row[j+2]];if(n&&!sk.some(w=>n.includes(w)))d[n]=[s==="無"?"缺货":"有货",p?.replace(/,/g,"")||"時價"];}});return d;};

const TYPO_MAP={
"一貫煎":["一罐煎","一貫間"],"乙字湯":["以致湯","一直湯"],
"八珍湯":["八珍"],"十全大補湯":["十全"],"四物湯":["四物"],
"加味逍遙散":["加味逍遙"],"逍遙散":["逍遙"],
"參苓白朮散":["參苓白朮","參靈白朮散","參零白朮散"],
"清暑益氣湯":["清暑益氣","青屬意氣湯","清數益氣湯"]
};

const SIMILAR_CHARS={
"白":["伯","柏"],"參":["参","身","深"],"朮":["术","竹"],
"黃":["黄","王"],"耆":["芪","奇"],"丸":["玩","完"],
"當":["当","黨"],"歸":["归","龜"],"湯":["汤","糖"],
"散":["傘","三"],"柴":["才","材"],"清":["青","輕"],
"乙":["一","已","致"],"字":["自","致"],"貫":["贯","罐"],
"煎":["間","簡"],"暑":["屬","數"],"益":["意","義"],"氣":["气","器"]
};
const getSimilarChars=c=>SIMILAR_CHARS[c]||[];

function findBestMatch(q){
q=q.trim();if(!q||!Object.keys(DB).length)return null;
if(DB[q])return{name:q,status:DB[q][0],price:DB[q][1],corrected:false};
for(let[c,t]of Object.entries(TYPO_MAP)){if(q===c||t?.includes(q))if(DB[c])return{name:c,status:DB[c][0],price:DB[c][1],corrected:true,original:q};}
for(let n of Object.keys(DB)){if(isSingleHerb(n)&&(n===q||n.includes(q)||q.includes(n)))return{name:n,status:DB[n][0],price:DB[n][1],corrected:n!==q,original:q};}
for(let n of Object.keys(DB)){if(n.includes(q)||q.includes(n))return{name:n,status:DB[n][0],price:DB[n][1],corrected:n!==q,original:q};}
if(q.length>=3){let b=null,s=0.7;for(let[n,d]of Object.entries(DB)){let cs=[...q].filter(c=>n.includes(c)).length/q.length;if(cs>s){s=cs;b={name:n,status:d[0],price:d[1],corrected:true,original:q};}}if(b)return b;}
return null;
}

function smartMatchProduct(text){
if(!text||text.length<2||!Object.keys(DB).length)return null;
let cleaned=text.replace(/[^\\u4e00-\\u9fa50-9]/g,"");
let dm=findBestMatch(cleaned);if(dm){let nm=cleaned.match(/(\\d+)$/);return dm.name+(nm?nm[1]:"");}
let nm=cleaned.match(/^(.+?)(\\d+)$/),pn=nm?nm[1]:cleaned,qty=nm?nm[2]:"";
let best=null,bestScore=0.5,bestCount=0;
for(let name of Object.keys(DB)){
let chars=[...pn],nc=[...name];
let exact=0;for(let c of chars)if(nc.includes(c))exact++;
let sim=0;for(let c of chars)if(!nc.includes(c))for(let sc of getSimilarChars(c))if(nc.includes(sc)){sim+=0.7;break;}
let score=(exact+sim)/Math.max(chars.length,nc.length);
let bonus=0;if(chars.length>=5&&exact>=3)bonus=0.15+(exact-3)*0.05;
let final=score+bonus;
if(final>bestScore){bestScore=final;best=name;bestCount=exact;}
}
if(best){console.log("匹配: "+text+"->"+best+" ("+(bestScore*100).toFixed(0)+"%)");return best+qty;}
return null;
}

async function loadData(){
let btn=document.getElementById("refreshBtn"),st=document.getElementById("status"),sb=document.getElementById("searchBtn");
btn.disabled=true;btn.textContent="載入中...";sb.disabled=true;
try{let r=await fetch(SHEET_URL);if(!r.ok)throw new Error();DB=parseCSV(await r.text());st.textContent="✅ 資料已更新 ("+Object.keys(DB).length+"項)";sb.disabled=false;}
catch{st.textContent="❌ 載入失敗";document.getElementById("result").innerHTML='<div class="error">無法連線</div>';}
btn.textContent="更新資料";btn.disabled=false;
}

function search(){
if(!Object.keys(DB).length){document.getElementById("result").innerHTML='<div class="error">請先更新資料</div>';return;}
let lines=document.getElementById("input").value.trim().split("\\n").map(l=>l.trim()).filter(Boolean);if(!lines.length)return;
let skip=["200g","100g"],html="",copy="",stats={in:0,out:0,cor:0,total:0},first=true;
for(let line of lines){
if(skip.some(k=>line.includes(k))){copy+=line+"\\n";continue;}
if(first){first=false;if!/\\d/.test(line)&&line.length<=4&&!["湯","散","丸"].some(c=>line.includes(c))){copy+=line+"\\n";continue;}}
let cl=line.replace(/錠$/,""),nm=cl.match(/^(.+?)(\\d+)$/),q=nm?nm[1].trim():cl.trim(),qty=nm?parseInt(nm[2]):1;
let res=findBestMatch(q);
if(res){
let{name,status,price}=res,up=price==="時價"?0:parseInt(price)||0,tp=up*qty,inStock=status==="有货";
if(inStock){stats.in+=qty;stats.total+=tp;}else{stats.out+=qty;}if(res.corrected)stats.cor++;
copy+=name+(qty>1?qty:"")+"\\t"+(inStock?"有貨":"缺貨")+"\\n";
let ps=showPrice?(price==="時價"?"請電洽":(qty>1?up+"x"+qty+"="+tp+"元":price+"元")):"";
html+='<div class="result-item"><div class="name">'+name+(qty>1?" x"+qty:"")+'</div>'+(res.corrected?'<div class="badge corrected">已更正</div>':'')+'<div class="badge '+(inStock?"in-stock'>有貨":"out-stock'>缺貨")+'</div><div class="price">'+ps+'</div></div>';
}else{copy+=line+"\\t找不到\\n";html+='<div class="result-item"><div class="name">'+line+'</div><div class="badge not-found">找不到</div></div>';}
}
html+='<div class="summary"><div class="total">'+(showPrice&&stats.total>0?stats.total+" 元":"-")+'</div><div class="count">有貨 '+stats.in+' 罐 | 缺貨 '+stats.out+' 罐</div></div>';
html+='<div class="copy-box"><h4>查詢結果</h4><div class="copy-content">'+copy+'</div><button class="copy-btn" id="copyBtn">複製結果</button></div>';
document.getElementById("result").innerHTML=html;
document.getElementById("copyBtn").onclick=function(){navigator.clipboard.writeText(copy).then(()=>{this.textContent="已複製!";});};
}

function clearInput(){document.getElementById("input").value="";document.getElementById("result").innerHTML="";}
function togglePrice(){showPrice=!showPrice;document.getElementById("priceBtn").textContent=showPrice?"隱藏價格":"顯示價格";}

let rec=null,listen=false;
function startVoiceInput(){
let btn=document.getElementById("voiceBtn"),SR=window.SpeechRecognition||window.webkitSpeechRecognition;
if(!SR){alert("不支援語音輸入");return;}
if(listen&&rec){rec.stop();rec=null;listen=false;btn.textContent="語音輸入";btn.style.background="#667eea";return;}
rec=new SR();rec.lang="zh-TW";rec.continuous=true;rec.interimResults=false;
rec.onresult=e=>{let ta=document.getElementById("input");for(let i=e.resultIndex;i<e.results.length;i++){let t=e.results[i][0].transcript.trim();if(t.length<2)continue;let m=smartMatchProduct(t.replace(/[，。、！？\\s]/g,""));if(m){let ct=ta.value.trim();ta.value=ct+(ct?"\\n":"")+m;}}};
rec.onerror=e=>console.error("語音錯誤:",e.error);
rec.onend=()=>{if(listen)try{rec.start();}catch{}};rec.start();listen=true;btn.textContent="停止聆聽";btn.style.background="#dc3545";
}

async function handleImage(e){
let file=e.target.files[0];if(!file)return;
let btn=document.getElementById("imageBtn"),ot=btn.textContent;
btn.textContent="辨識中...";btn.disabled=true;
try{
if(!window.Tesseract){let s=document.createElement("script");s.src="https://cdn.jsdelivr.net/npm/tesseract.js@4/dist/tesseract.min.js";document.head.appendChild(s);await new Promise(r=>s.onload=r);}
let res=await Tesseract.recognize(file,"chi_tra"),lines=res.data.text.split("\\n").map(l=>l.trim()).filter(l=>l.length>=2);
let m100=[],m200=[];
for(let line of lines){
let c=line.replace(/[^\\u4e00-\\u9fa50-9]/g,"").replace(/^\\d+/,"").replace(/\\d{3,}/g,"");if(c.length<2)continue;
let nm=c.match(/^(.+?)(\\d{1,2})$/),pn=nm?nm[1]:c,qty=nm?nm[2]:"";
if(qty&&parseInt(qty)>20){pn=c;qty="";}
let m=smartMatchProduct(pn);if(m){let fm=m+qty;if(isSingleHerb(m.replace(/\\d+$/,""))){if(!m100.includes(fm))m100.push(fm);}else{if(!m200.includes(fm))m200.push(fm);}}
}
let out="";if(m100.length)out+="100g\\n"+m100.join("\\n");if(m200.length){if(out)out+="\\n";out+="200g\\n"+m200.join("\\n");}
if(out)document.getElementById("input").value=out;else alert("無法辨識");
}catch(err){console.error(err);alert("辨識失敗");}
btn.textContent=ot;btn.disabled=false;e.target.value="";
}

document.addEventListener("DOMContentLoaded",function(){
let ii=document.getElementById("imageInput"),ib=document.getElementById("imageBtn");
if(ib&&ii){ib.onclick=()=>ii.click();ii.onchange=e=>handleImage(e);}
loadData();
});
</script>
</body>
</html>'''

with open(r'C:\Users\user\.qclaw\workspace\tcm_stock_lookup_online.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('File saved successfully!')
