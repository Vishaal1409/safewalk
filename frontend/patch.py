"""Patch index.html with 3 upgrades: heatmap, time filter, area summary card."""
import re

PATH = r"C:\Users\shrut\safewalk\frontend\index.html"
with open(PATH, 'r', encoding='utf-8') as f:
    src = f.read()

# 1) Add leaflet.heat script
src = src.replace(
    '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>',
    '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>\n<script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>'
)

# 2) Add CSS before .drawer-handle{display:none}
NEW_CSS = r"""
/* Heatmap toggle */
#heatmap-btn{position:fixed;top:20px;right:220px;z-index:500;padding:10px 18px;border-radius:var(--radius);
background:var(--glass);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
border:1px solid var(--glass-border);box-shadow:var(--shadow);color:#fff;font-family:'Syne',sans-serif;
font-size:.85rem;font-weight:700;cursor:pointer;transition:var(--transition);display:flex;align-items:center;gap:6px}
#heatmap-btn:hover{transform:translateY(-2px);box-shadow:0 12px 40px rgba(109,16,54,0.25)}
#heatmap-btn.active{background:linear-gradient(135deg,var(--rose-deep),var(--rose));border-color:var(--rose)}
/* Time filter */
#time-filter{position:fixed;top:76px;right:20px;z-index:500;display:flex;gap:4px;padding:4px;
border-radius:var(--radius);background:var(--glass);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
border:1px solid var(--glass-border);box-shadow:var(--shadow)}
.tf-pill{padding:7px 16px;border:none;border-radius:var(--radius-sm);background:transparent;
color:rgba(255,255,255,0.5);font-family:'Syne',sans-serif;font-size:.78rem;font-weight:700;cursor:pointer;transition:var(--transition)}
.tf-pill:hover{color:#fff}.tf-pill.active{background:linear-gradient(135deg,var(--rose-deep),var(--rose));color:#fff}
/* Area summary card */
#area-summary{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(120%);z-index:500;
padding:18px 26px;border-radius:var(--radius);background:var(--glass);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
border:1px solid var(--glass-border);box-shadow:var(--shadow);color:#fff;min-width:300px;max-width:460px;
transition:transform .4s cubic-bezier(.4,0,.2,1),opacity .4s ease;opacity:0;pointer-events:none}
#area-summary.show{transform:translateX(-50%) translateY(0);opacity:1;pointer-events:auto}
#area-summary .area-name{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;margin-bottom:6px;
white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:360px}
.area-badge{display:inline-block;padding:4px 14px;border-radius:20px;font-family:'Syne',sans-serif;
font-size:.85rem;font-weight:700;margin-bottom:8px}
.area-badge.safe{background:rgba(52,211,153,0.15);color:#34d399}
.area-badge.caution{background:rgba(245,158,11,0.15);color:#f59e0b}
.area-badge.danger{background:rgba(239,68,68,0.15);color:#ef4444}
#area-summary .area-stats{font-size:.84rem;color:rgba(255,255,255,0.6);line-height:1.6}
#area-summary .close-btn{position:absolute;top:10px;right:12px;background:none;border:none;
color:rgba(255,255,255,0.4);font-size:1.1rem;cursor:pointer;transition:var(--transition);padding:2px 6px}
#area-summary .close-btn:hover{color:#fff}
@media(max-width:768px){
#area-summary{bottom:calc(52px + 16px);left:12px;right:12px;transform:translateX(0) translateY(120%);min-width:auto}
#area-summary.show{transform:translateX(0) translateY(0)}
#heatmap-btn{top:auto;bottom:130px;right:12px}
#time-filter{top:auto;bottom:175px;right:12px}}
"""
src = src.replace('.drawer-handle{display:none}', NEW_CSS + '.drawer-handle{display:none}')

# 3) Add HTML elements before toast container
NEW_HTML = """
<!-- HEATMAP TOGGLE -->
<button id="heatmap-btn" onclick="toggleHeatmap()" style="display:none">🔥 Heatmap</button>
<!-- TIME FILTER -->
<div id="time-filter" style="display:none">
<button class="tf-pill" data-filter="24h">24h</button>
<button class="tf-pill" data-filter="7d">7d</button>
<button class="tf-pill active" data-filter="all">All</button>
</div>
<!-- AREA SUMMARY -->
<div id="area-summary">
<button class="close-btn" onclick="this.parentElement.classList.remove('show')">✕</button>
<div class="area-name" id="area-name">—</div>
<div class="area-badge safe" id="area-badge">🟢 SAFE</div>
<div class="area-stats">
<div id="area-hazard-count">0 hazards in this area</div>
<div id="area-last-report" style="display:none">—</div>
</div>
</div>

"""
src = src.replace('<!-- TOAST CONTAINER -->', NEW_HTML + '<!-- TOAST CONTAINER -->')

# 4) Add JS variables
src = src.replace(
    'let map,markers=[],clickMarker=null,clickCoords=null,allHazards=[];',
    'let map,markers=[],clickMarker=null,clickCoords=null,allHazards=[],heatLayer=null,heatmapOn=false,activeTimeFilter=\'all\';'
)

# 5) In initApp, after float-score display, show buttons + create heat layer
src = src.replace(
    "document.getElementById('float-score').style.display='flex';",
    """document.getElementById('float-score').style.display='flex';
document.getElementById('heatmap-btn').style.display='flex';
document.getElementById('time-filter').style.display='flex';
heatLayer=L.heatLayer([],{radius:25,blur:20,maxZoom:17,gradient:{0.4:'blue',0.65:'orange',0.85:'red',1:'darkred'}});"""
)

# 6) In map click handler, add showAreaSummary after setting tooltip text
src = src.replace(
    "setTimeout(()=>ttip.classList.remove('show'),3000);",
    "setTimeout(()=>ttip.classList.remove('show'),3000);\nshowAreaSummary(name,e.latlng.lat,e.latlng.lng);"
)

# 7) Add initTimeFilter to init calls
src = src.replace(
    'initTabs();initReport();initSearch();initSafetySearch();loadHazards();',
    'initTabs();initReport();initSearch();initSafetySearch();initTimeFilter();loadHazards();'
)

# 8) In main search handler, add showAreaSummary
src = src.replace(
    "map.flyTo([parseFloat(it.dataset.lat),parseFloat(it.dataset.lon)],16,{duration:1.2});\ninp.value=it.textContent;res.classList.remove('show')",
    "map.flyTo([parseFloat(it.dataset.lat),parseFloat(it.dataset.lon)],16,{duration:1.2});\nshowAreaSummary(it.textContent,parseFloat(it.dataset.lat),parseFloat(it.dataset.lon));\ninp.value=it.textContent;res.classList.remove('show')"
)

# 9) In safety search handler, add showAreaSummary
src = src.replace(
    "fetchSafetyScore(lat,lon);\n}));",
    "fetchSafetyScore(lat,lon);\nshowAreaSummary(it.textContent,lat,lon);\n}));"
)

# 10) Replace renderMarkers to support filtering + heatmap
OLD_RENDER = """function renderMarkers(){
markers.forEach(m=>map.removeLayer(m));markers=[];
allHazards.forEach(h=>{"""
NEW_RENDER = """function getFilteredHazards(){
if(activeTimeFilter==='all')return allHazards;
const ms=activeTimeFilter==='24h'?86400000:604800000;
return allHazards.filter(h=>h.created_at&&(Date.now()-new Date(h.created_at).getTime()<ms));
}
function renderMarkers(){
markers.forEach(m=>map.removeLayer(m));markers=[];
const filtered=getFilteredHazards();const heatData=[];
filtered.forEach(h=>{"""
src = src.replace(OLD_RENDER, NEW_RENDER)

# Add heatData push after isNew line, and wrap marker creation
src = src.replace(
    "const isNew=h.created_at&&(Date.now()-new Date(h.created_at).getTime()<3600000);\nconst html=",
    "const isNew=h.created_at&&(Date.now()-new Date(h.created_at).getTime()<3600000);\nheatData.push([h.latitude,h.longitude,0.8]);\nif(!heatmapOn){\nconst html="
)

# Close the if(!heatmapOn) block and add heatLayer update
src = src.replace(
    "m.bindPopup(popupHtml,{maxWidth:280});markers.push(m);\n});\n}",
    "m.bindPopup(popupHtml,{maxWidth:280});markers.push(m);\n}\n});\nif(heatLayer)heatLayer.setLatLngs(heatData);\n}"
)

# 11) Add new functions before closing </script>
NEW_FUNCS = """
/* ===== HEATMAP TOGGLE ===== */
function toggleHeatmap(){
heatmapOn=!heatmapOn;
document.getElementById('heatmap-btn').classList.toggle('active',heatmapOn);
if(heatmapOn){heatLayer.addTo(map)}else{map.removeLayer(heatLayer)}
renderMarkers();toast(heatmapOn?'Heatmap enabled 🔥':'Heatmap disabled',heatmapOn?'success':'info');
}
/* ===== TIME FILTER ===== */
function initTimeFilter(){
document.querySelectorAll('.tf-pill').forEach(p=>p.addEventListener('click',()=>{
document.querySelectorAll('.tf-pill').forEach(x=>x.classList.remove('active'));
p.classList.add('active');activeTimeFilter=p.dataset.filter;renderMarkers();updateStats();
toast('Showing '+p.dataset.filter+' hazards','info');
}));
}
/* ===== AREA SUMMARY ===== */
function showAreaSummary(areaName,lat,lng){
const card=document.getElementById('area-summary');
const R=0.005;
const nearby=allHazards.filter(h=>Math.abs(h.latitude-lat)<R&&Math.abs(h.longitude-lng)<R);
const n=nearby.length;
let badge,cls;
if(n===0){badge='🟢 SAFE';cls='safe'}
else if(n<=3){badge='🟡 CAUTION';cls='caution'}
else{badge='🔴 DANGER';cls='danger'}
document.getElementById('area-name').textContent=areaName;
const bel=document.getElementById('area-badge');bel.textContent=badge;bel.className='area-badge '+cls;
document.getElementById('area-hazard-count').textContent=n+' hazard'+(n!==1?'s':'')+' in this area';
const lr=document.getElementById('area-last-report');
if(n>0){
const latest=nearby.reduce((a,b)=>new Date(b.created_at||0)>new Date(a.created_at||0)?b:a);
if(latest.created_at){const mins=Math.round((Date.now()-new Date(latest.created_at).getTime())/60000);
lr.textContent='Last reported: '+(mins<60?mins+' mins ago':Math.round(mins/60)+' hrs ago');
lr.style.display='block'}else{lr.style.display='none'}
}else{lr.style.display='none'}
card.classList.add('show');
}
"""
src = src.replace('</script>', NEW_FUNCS + '</script>')

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(src)

print("✅ Patched index.html with all 3 upgrades")
