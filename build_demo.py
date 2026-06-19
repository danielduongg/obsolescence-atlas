import json
D=json.load(open("occupations.json"))
import numpy as np
occ=D["occupations"]
fo=np.array([d["fo"] for d in occ]);gpt=np.array([d["gpt"] for d in occ]);ai=np.array([d["aioe"] for d in occ])
corr={"fo_gpt":round(float(np.corrcoef(fo,gpt)[0,1]),2),"fo_aioe":round(float(np.corrcoef(fo,ai)[0,1]),2),"aioe_gpt":round(float(np.corrcoef(ai,gpt)[0,1]),2)}
BLOB=json.dumps({"occ":occ,"corr":corr})
HTML=r'''<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>obsolescence-atlas — will a robot take this job?</title>
<style>
 :root{--bg:#0a0710;--panel:#161020;--panel2:#100b18;--line:#2a2040;--ink:#f1eaff;--mut:#a99cc4;
   --p1:#ff7b9c;--p2:#b07bff;--p3:#5b8cff;--green:#27d08a;--red:#ff5d6c;--warn:#ffce54;}
 *{box-sizing:border-box}
 body{margin:0;background:radial-gradient(1100px 650px at 75% -10%,#2a1640 0%,var(--bg) 55%);color:var(--ink);
   font:16px/1.55 ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Inter,sans-serif;-webkit-font-smoothing:antialiased}
 .wrap{max-width:920px;margin:0 auto;padding:36px 20px 80px}
 .eyebrow{letter-spacing:.16em;text-transform:uppercase;font-size:12px;color:var(--p2);font-weight:700}
 h1{font-size:29px;margin:.25em 0 .15em;line-height:1.15}
 .sub{color:var(--mut);max-width:66ch}
 .grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:22px}
 @media(max-width:780px){.grid{grid-template-columns:1fr}}
 .card{background:linear-gradient(180deg,var(--panel),var(--panel2));border:1px solid var(--line);border-radius:16px;padding:18px 20px;box-shadow:0 20px 50px -30px #000}
 select{width:100%;background:#120c1c;color:var(--ink);border:1px solid var(--line);border-radius:9px;padding:10px 12px;font-size:15px}
 .gauge{margin:13px 0}
 .gauge .lab{display:flex;justify-content:space-between;font-size:13px;color:var(--mut);margin-bottom:4px}
 .gauge .lab b{color:var(--ink);font-variant-numeric:tabular-nums}
 .track{height:13px;background:#120c1c;border:1px solid var(--line);border-radius:999px;overflow:hidden}
 .fill{height:100%;border-radius:999px}
 .kpis{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:6px}
 .kpi{background:#120c1c;border:1px solid var(--line);border-radius:11px;padding:11px;text-align:center}
 .kpi .k{font-size:11px;color:var(--mut)}.kpi .v{font-size:24px;font-weight:800;font-variant-numeric:tabular-nums}
 .pz{font-size:12px;border:1px solid var(--line);background:#120c1c;color:var(--mut);padding:5px 10px;border-radius:999px;cursor:pointer}
 .pz.on{border-color:var(--p2);color:#fff;background:#241a3a}
 .verdict{margin-top:14px;padding:12px 15px;border-radius:12px;font-size:14.5px;font-weight:600;border:1px solid}
 svg{width:100%;height:auto;display:block}
 h2{font-size:14px;margin:4px 0 8px;color:var(--mut);font-weight:600;letter-spacing:.02em;text-transform:uppercase}
 .note{margin-top:14px;border-left:3px solid var(--warn);background:#1a160c;padding:12px 15px;border-radius:0 10px 10px 0;color:#ecd9b0;font-size:14px}
 .foot{margin-top:22px;color:var(--mut);font-size:13px;text-align:center}
 a{color:var(--p2);text-decoration:none}a:hover{text-decoration:underline}
</style></head><body><div class="wrap">
 <div class="eyebrow">obsolescence-atlas · live demo</div>
 <h1>Will a robot take this job?</h1>
 <p class="sub">Three published forecasts rate every occupation's exposure to automation/AI — Frey–Osborne (2013), Felten's AI Occupational Exposure, and Eloundou's GPT-exposure (2023). Pick a job and see how much <b>they disagree</b>, against what the BLS actually projects for jobs.</p>
 <div class="grid">
  <div class="card">
   <select id="occ"></select>
   <div class="gauge"><div class="lab"><span>Frey–Osborne automation (2013)</span><b id="vfo"></b></div><div class="track"><div class="fill" id="ffo" style="background:var(--p1)"></div></div></div>
   <div class="gauge"><div class="lab"><span>Felten AI exposure (AIOE)</span><b id="vai"></b></div><div class="track"><div class="fill" id="fai" style="background:var(--p2)"></div></div></div>
   <div class="gauge"><div class="lab"><span>Eloundou GPT-exposure (2023)</span><b id="vgpt"></b></div><div class="track"><div class="fill" id="fgpt" style="background:var(--p3)"></div></div></div>
   <div class="kpis">
     <div class="kpi"><div class="k">BLS 10-yr jobs outlook</div><div class="v" id="vbls"></div></div>
     <div class="kpi"><div class="k">Median wage</div><div class="v" id="vwage"></div></div>
   </div>
   <div class="verdict" id="verdict"></div>
  </div>
  <div class="card">
   <h2>The forecasters disagree</h2>
   <div style="display:flex;gap:6px;margin-bottom:8px"><span class="pz" id="mFO">x: Frey–Osborne</span><span class="pz" id="mWage">x: median wage</span></div>
   <svg id="scatter" viewBox="0 0 380 320"></svg>
   <div style="font-size:12.5px;color:var(--mut);text-align:center" id="scatcap">each dot = an occupation · the cloud has almost no slope</div>
   <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px">
     <div><div style="font-size:12px;color:var(--mut);margin-bottom:5px">Most GPT-exposed</div><div id="rankTop" style="font-size:12.5px"></div></div>
     <div><div style="font-size:12px;color:var(--mut);margin-bottom:5px">Exposed &amp; shrinking (BLS)</div><div id="rankFade" style="font-size:12.5px"></div></div>
   </div>
  </div>
 </div>
 <div class="note" id="note"></div>
 <div class="foot">Frey–Osborne 2013 · Felten et al. 2021 · Eloundou et al. 2023 · BLS Employment Projections · <a href="https://github.com/danielduongg/obsolescence-atlas" target="_blank">source &amp; data →</a></div>
</div>
<script>
const M=__BLOB__;const OCC=M.occ.slice().sort((a,b)=>a.name.localeCompare(b.name));
const sel=document.getElementById('occ');
OCC.forEach((o,i)=>{const e=document.createElement('option');e.value=i;e.textContent=o.name;sel.appendChild(e);});
let smode='fo';
function drawScatter(cur){
  const W=380,H=320,pad=40;
  const xVal=o=>smode==='fo'?o.fo:(o.wage/200000);
  const xlab=smode==='fo'?'Frey–Osborne automation →':'median wage →';
  const xs=v=>pad+v*(W-pad-12);const ys=v=>H-pad-v*(H-pad-12);
  let s=`<line x1="${pad}" y1="${H-pad}" x2="${W-12}" y2="${H-pad}" style="stroke:#2a2040"/><line x1="${pad}" y1="12" x2="${pad}" y2="${H-pad}" style="stroke:#2a2040"/>`;
  s+=`<text x="${(W+pad)/2}" y="${H-10}" fill="#a99cc4" font-size="11" text-anchor="middle">${xlab}</text>`;
  s+=`<text x="14" y="${(H-pad)/2}" fill="#a99cc4" font-size="11" text-anchor="middle" transform="rotate(-90 14 ${(H-pad)/2})">GPT-exposure →</text>`;
  OCC.forEach(o=>{const isC=o.name===cur.name;s+=`<circle cx="${xs(xVal(o)).toFixed(1)}" cy="${ys(o.gpt).toFixed(1)}" r="${isC?6:3.2}" fill="${isC?'#ffce54':'#b07bff'}" opacity="${isC?1:0.55}"${isC?' stroke="#fff" stroke-width="1.5"':''}/>`;});
  if(smode==='fo') s+=`<text x="${W-12}" y="20" fill="#ffce54" font-size="11" text-anchor="end">r = ${M.corr.fo_gpt.toFixed(2)} (≈ none)</text>`;
  document.getElementById('scatter').innerHTML=s;
}
function render(){
  const o=OCC[+sel.value];
  const set=(idf,idv,val)=>{document.getElementById(idf).style.width=(val*100)+'%';document.getElementById(idv).textContent=Math.round(val*100)+'%';};
  set('ffo','vfo',o.fo);set('fai','vai',o.aioe);set('fgpt','vgpt',o.gpt);
  document.getElementById('vbls').textContent=(o.bls>=0?'+':'')+o.bls+'%';
  document.getElementById('vbls').style.color=o.bls>=5?'var(--green)':o.bls<=-5?'var(--red)':'var(--warn)';
  document.getElementById('vwage').textContent='$'+(o.wage/1000).toFixed(0)+'k';
  const me=Math.max(o.fo,o.gpt);const v=document.getElementById('verdict');
  let txt,cls,col;
  if(o.bls<=-5&&me>0.6){txt='🔴 Fading — high exposure <i>and</i> the BLS projects the workforce shrinking.';col='#2a121a';}
  else if(me>0.6&&o.bls>=5){txt='🟡 Exposed but growing — high AI exposure, yet projected demand is rising. Exposure ≠ replacement.';col='#1a160c';}
  else if(me<0.35){txt='🟢 Robot-proof (for now) — low exposure on every measure.';col='#0f2a20';}
  else{txt='🟠 Contested — the measures disagree or exposure is moderate.';col='#1a1228';}
  const disagree=Math.abs(o.fo-o.gpt)>0.4;
  v.style.background=col;v.style.borderColor='#3a2f55';v.innerHTML=txt+(disagree?` <br><span style="font-weight:400;color:var(--mut)">Note: the 2013 automation forecast and the 2023 LLM forecast <b>strongly disagree</b> about this job (${Math.round(o.fo*100)}% vs ${Math.round(o.gpt*100)}%).</span>`:'');
  drawScatter(o);
}
sel.addEventListener('change',render);
const startIdx=OCC.findIndex(o=>o.name==='Welders');sel.value=startIdx<0?0:startIdx;
document.getElementById('note').innerHTML=`<b>The honest finding.</b> Frey–Osborne (2013) and GPT-exposure (2023) correlate just <b>r=${M.corr.fo_gpt.toFixed(2)}</b> — practically unrelated. The old automation lens points at <b>manual/routine</b> jobs (welders, cashiers, drivers); the LLM lens points at <b>cognitive/writing</b> jobs (writers, analysts, paralegals). The two AI-era measures agree with each other (r=${M.corr.aioe_gpt.toFixed(2)}) but not with 2013. And "exposure" was never "replacement": many high-exposure jobs are still <i>growing</i>. Forecasting which trades vanish is far less certain than headlines imply.`;

function rankings(){
  const top=[...OCC].sort((a,b)=>b.gpt-a.gpt).slice(0,6);
  const fade=[...OCC].filter(o=>o.bls<0).sort((a,b)=>Math.max(b.fo,b.gpt)-Math.max(a.fo,a.gpt)).slice(0,6);
  const row=o=>`<div style="display:flex;justify-content:space-between;color:var(--mut);padding:2px 0"><span style="color:#e9e2ff">${o.name.split(' (')[0].slice(0,22)}</span><span>${Math.round(o.gpt*100)}%</span></div>`;
  document.getElementById('rankTop').innerHTML=top.map(row).join('');
  document.getElementById('rankFade').innerHTML=fade.map(o=>`<div style="display:flex;justify-content:space-between;color:var(--mut);padding:2px 0"><span style="color:#e9e2ff">${o.name.split(' (')[0].slice(0,20)}</span><span style="color:var(--red)">${o.bls}%</span></div>`).join('');
}
document.getElementById('mFO').onclick=()=>{smode='fo';document.getElementById('mFO').className='pz on';document.getElementById('mWage').className='pz';render();};
document.getElementById('mWage').onclick=()=>{smode='wage';document.getElementById('mWage').className='pz on';document.getElementById('mFO').className='pz';render();};
document.getElementById('mFO').className='pz on';
rankings();
render();
</script></body></html>'''
open("index.html","w").write(HTML.replace("__BLOB__",BLOB))
print("wrote index.html",round(len(HTML)/1024,1),"KB")
