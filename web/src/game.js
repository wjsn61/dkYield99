// ════════════════════════════════════════════════════════════════
//  게임 화면 - HUD7 · 공정 플로우시트 · 공정 카드 · 차트 · 로그
// ════════════════════════════════════════════════════════════════
import { api } from "./api.js";
import { mountFlowsheet } from "./flowsheet.js?v=3";
import { drawChart, legendHTML } from "./charts.js";
import { initPanels } from "./panels.js";

const STATS = [
  { key:"예산",   color:"#ffb049", unit:"억", max:300, bar:true },
  { key:"월이익", color:"#8ae65c", unit:"억", max:40,  bar:false },
  { key:"생산량", color:"#4db6ff", unit:"t",  max:2000, bar:false },
  { key:"수율",   color:"#2fe0c8", unit:"%", max:100, bar:true },
  { key:"순도",   color:"#b08cff", unit:"%", max:100, bar:true },
  { key:"안전지수", color:"#ff7a85", unit:"", max:100, bar:true },
  { key:"환경지수", color:"#46d6a0", unit:"", max:100, bar:true },
];
const CAT = {
  운전:   { cls:"var(--cyan)",   label:"운전" },
  설비:   { cls:"var(--amber)",  label:"설비" },
  연구:   { cls:"var(--violet)", label:"R&D" },
  안전환경:{ cls:"var(--green)",  label:"안전·환경" },
  시장:   { cls:"var(--blue)",   label:"시장" },
};
const GRADE_COLOR = { S:"#2fe0c8", A:"#8ae65c", B:"#4db6ff", C:"#ffb049", D:"#ff7a85", F:"#ff5765" };

let gameId=null, state=null, prev=null, cards=[], cardById={}, flow=null, filter="전체";
const statEls={};
const $ = s=>document.querySelector(s);

export async function startGame(options){
  // 시드를 주면 공정이 조금씩 흔들립니다 (통계 실습용).
  // 시드가 있어야 나중에 같은 조건으로 다시 돌려 비교할 수 있습니다.
  const seed = options?.seed ?? Math.floor(Date.now() / 1000) % 100000000;
  const r = await api.newGame({ seed });
  gameId=r.gameId; state=r.state; prev=null;
  if(!cards.length){ cards=await api.cards(); cardById=Object.fromEntries(cards.map(c=>[c["아이디"],c])); }
  buildHUD();
  $("#chart-legend").innerHTML=legendHTML();
  buildFilter();
  if(!flow){
    try { flow = mountFlowsheet($("#flowsheet"), { onHover:showTip }); }
    catch(err){
      console.error("3D 플로우시트 초기화 실패 (게임은 계속 진행됩니다):", err);
      flow = { update(){}, pulseByIndicators(){}, resetView(){} };   // 안전 스텁
    }
  }
  wire();
  renderAll();
}

// ── HUD ──
function buildHUD(){
  const host=$("#hud-stats"); host.innerHTML="";
  for(const s of STATS){
    const el=document.createElement("div"); el.className="stat"; el.style.setProperty("--sc",s.color);
    el.innerHTML=`<div class="label"><span class="dot"></span>${s.key}</div>
      <div class="value"><span class="num">0</span><span class="unit">${s.unit}</span></div>
      ${s.bar?'<div class="bar"><i></i></div>':""}`;
    host.appendChild(el);
    statEls[s.key]={node:el,num:el.querySelector(".num"),bar:el.querySelector(".bar i")};
  }
}
function fmt(v){ return Number.isInteger(v)?v:(+v).toFixed(1); }
function updateHUD(){
  for(const s of STATS){
    const v=state[s.key], ref=statEls[s.key];
    ref.num.textContent=fmt(v);
    if(ref.bar) ref.bar.style.width=Math.max(2,Math.min(100,(v/s.max)*100))+"%";
    if(prev){ const d=v-prev[s.key];
      if(Math.abs(d)>0.05){ ref.node.classList.remove("flash-up","flash-down"); void ref.node.offsetWidth;
        ref.node.classList.add(d>0?"flash-up":"flash-down"); } }
  }
  $("#hud-month").textContent=`${state["턴"]}개월차`;
  $("#hud-tech").textContent=`기술력 ${Math.round(state["기술력"])}`;
  $("#turn-now").textContent=state["턴"];
}

// ── 플로우시트 툴팁 ──
function showTip(info,x,y){
  const tip=$("#flow-tip");
  if(!info){ tip.style.opacity=0; return; }
  const r=$(".flow-stage").getBoundingClientRect();
  tip.innerHTML=`<div class="tt-name">${info.name}</div><div class="tt-role">${info.role}</div>`;
  tip.style.left=(x-r.left)+"px"; tip.style.top=(y-r.top)+"px"; tip.style.opacity=1;
}

// ── 카드 ──
function buildFilter(){
  const host=$("#card-filter"); const cats=["전체","운전","설비","연구"];
  host.innerHTML=cats.map(c=>`<button data-c="${c}" class="${c===filter?"on":""}">${c==="연구"?"R&D":c}</button>`).join("");
  host.querySelectorAll("button").forEach(b=>b.addEventListener("click",()=>{filter=b.dataset.c;buildFilter();renderCards();}));
}
function fxChips(card){
  const chips=[];
  const add=(obj,suf="")=>{ for(const [k,v] of Object.entries(obj||{}))
    chips.push(`<span class="fx ${v>=0?"up":"down"}">${k} ${v>=0?"+":""}${v}${suf}</span>`); };
  if(card["분류"]==="연구"){ add(card["성공효과"]); }
  else { add(card["즉시효과"]); add(card["부작용"]); add(card["장기효과"],"/턴"); }
  return chips.slice(0,6).join("");
}
function renderCards(){
  const host=$("#card-list"); host.innerHTML="";
  const researching=new Set(state["연구중"].map(r=>r["아이디"]));
  for(const c of cards){
    if(filter!=="전체" && c["분류"]!==filter) continue;
    const cat=CAT[c["분류"]]||CAT["운전"];
    const busy=c["분류"]==="연구" && researching.has(c["아이디"]);
    const cant=!busy && state["예산"]<c["비용"];
    const el=document.createElement("div");
    el.className="ccard"+(busy?" busy":cant?" cant":"");
    el.style.setProperty("--cc",cat.cls);
    el.innerHTML=`
      <div class="ccard-top">
        <div><div class="ccard-cat">${cat.label}</div><div class="ccard-name">${c["이름"]}</div></div>
        <div class="ccard-cost">${c["비용"]}억${c["유지비"]?`<small>유지 ${c["유지비"]}/턴</small>`:""}</div>
      </div>
      <div class="ccard-fx">${fxChips(c)}</div>
      ${c["분류"]==="연구"?`<div class="ccard-rnd">⚗ 연구기간 ${c["연구기간"]}턴${busy?" · 진행 중":""}</div>`:""}`;
    el.addEventListener("click",()=>onCard(c,busy,cant));
    host.appendChild(el);
  }
}
async function onCard(c,busy,cant){
  if(busy) return toast(`'${c["이름"]}'은(는) 이미 연구 중입니다.`,"bad");
  if(cant) return toast(`예산이 부족합니다. (필요 ${c["비용"]}억)`,"bad");
  const before=state;
  const r=await api.enact(gameId,c["아이디"]);
  if(!r.ok) return toast(r.message,"bad");
  prev=before; state=r.state;
  toast(r.message,"good");
  spawnFloaters();
  flow.update(state);
  flow.pulseByIndicators(changedIndicators(c));
  updateHUD(); renderCards(); renderRnd(); renderLog(); updateWorkers();
}
function changedIndicators(c){
  const keys=new Set();
  for(const ef of ["즉시효과","부작용","장기효과","성공효과"])
    for(const k in (c[ef]||{})) keys.add(k);
  return [...keys];
}

// ── R&D 진행 스트립 ──
function renderRnd(){
  const host=$("#rnd-strip");
  host.innerHTML=state["연구중"].map(r=>{
    const dur=cardById[r["아이디"]]?.["연구기간"]||r["남은턴"];
    const pct=Math.round(((dur-r["남은턴"])/dur)*100);
    return `<div class="rnd-item"><span class="nm">⚗ ${r["이름"]}</span>
      <span class="pg"><i style="width:${pct}%"></i></span>
      <span class="rem">${r["남은턴"]}턴</span></div>`;
  }).join("");
}

// ── 턴 종료 ──
async function onEndTurn(){
  const before=state;
  const r=await api.endTurn(gameId);
  prev=before; state=r.state;
  spawnFloaters();
  flow.update(state);
  updateHUD(); renderCards(); renderRnd(); renderLog(); renderChart(); updateWorkers();
  // R&D 성공 알림
  for(const line of state["기록"].slice(-3)) if(line.includes("R&D 성공")) toast("🎉 "+line.replace(/^🎉?\s*/,""),"good");
  if(r.ended) showResult(r.ending);
}

// ── 로그 / 차트 / 플로터 ──
function logClass(l){
  if(l.includes("R&D")) return "rnd";
  if(l.includes("즉시효과")) return "imm";
  if(l.includes("부작용")) return "side";
  if(l.includes("장기효과")) return "long";
  return "";
}
function renderLog(){
  $("#log-list").innerHTML=state["기록"].slice().reverse().map(l=>`<div class="log-line ${logClass(l)}">${l}</div>`).join("");
}
function renderChart(){ drawChart($("#chart-canvas"), state["추이"]); }
function spawnFloaters(){
  if(!prev) return;
  const host=$("#floaters"); const keys=["예산","월이익","수율","순도","안전지수","환경지수"]; let n=0;
  for(const k of keys){
    const d=+(state[k]-prev[k]).toFixed(1);
    if(Math.abs(d)<0.1) continue;
    const el=document.createElement("div"); el.className="floater "+(d>0?"pos":"neg");
    el.textContent=`${d>0?"+":""}${d} ${k}`;
    el.style.left=(38+Math.random()*24)+"%"; el.style.top=(40+n*7)+"%";
    host.appendChild(el); setTimeout(()=>el.remove(),1500); n++;
  }
}

// ── 결과 모달 ──
function showResult(e){
  const col=GRADE_COLOR[e["등급"]]||"#2fe0c8";
  $("#result-grade").textContent=e["등급"];
  $("#result-grade").style.color=col;
  $("#result-glow").style.background=col;
  $("#result-title").textContent=e["이름"];
  const win=["S","A","B"].includes(e["등급"]);
  $("#result-desc").textContent= win
    ? "공정 최적화에 성공했습니다. 수율과 품질, 안전·환경의 균형을 잡았습니다."
    : "균형을 잃은 운영이었습니다. 수율·순도·안전·재정을 다시 맞춰 도전해 보세요.";
  $("#result-breakdown").innerHTML=[
    ["수율",`${e["수율"]}%`,"#2fe0c8"],["순도",`${e["순도"]}%`,"#b08cff"],
    ["누적이익",`${e["누적이익"]}억`,"#8ae65c"],["안전·환경",`${Math.round(e["안전지수"])}·${Math.round(e["환경지수"])}`,"#ff7a85"],
  ].map(([k,v,c])=>`<div class="b"><div class="k">${k}</div><div class="v" style="color:${c}">${v}</div></div>`).join("");
  $("#result-modal").classList.add("show");
}

// ── 공통 ──
let toastTimer;
function toast(msg,kind=""){ const t=$("#toast"); t.textContent=msg; t.className="toast show "+kind;
  clearTimeout(toastTimer); toastTimer=setTimeout(()=>t.className="toast",2300); }
function renderAll(){
  updateHUD(); flow.update(state); renderCards(); renderRnd(); renderLog(); renderChart();
  updateWorkers();
}

// ════════════════ 현장의 사람들 ════════════════
//  공장이 잘 돌아가면 사람이 늘고, 위험해지면 현장이 빕니다.
//  어떤 카드를 썼느냐에 따라 나오는 인력의 종류도 달라집니다.
function updateWorkers(){
  if(!flow || !flow.updateWorkers || !state) return;
  flow.updateWorkers(state);

  const badge = $("#vitality-badge");
  if(badge && flow.workers){
    const v = Math.round(flow.workers.활력 * 100);
    badge.textContent = `가동 ${v} · 현장에 ${flow.workers.인원}명`;
    badge.title =
      `공장 활성화 = 생산량·수율·순도·안전지수·환경지수를 합친 값입니다 (합성지표).\n` +
      `안전지수가 낮으면 사람이 빠지고 걸음도 조심스러워집니다.\n` +
      `지금 현장에 있는 인력: ${flow.workers.유형.join(", ")}`;
    badge.style.setProperty("--v", v + "%");
  }
}

let wired=false;
function wire(){
  if(wired) return; wired=true;

  // 통계 지표 보기 · 저장/불러오기 다이얼로그를 붙입니다.
  initPanels({
    getGameId: () => gameId,
    toast,
    onLoaded: (newId, newState) => {
      gameId = newId;
      prev = null;
      state = newState;
      renderAll();
    },
  });

  $("#end-turn-btn").addEventListener("click",onEndTurn);
  const rb=$("#reset-view-btn");
  if(rb){ rb.addEventListener("pointerdown",e=>e.stopPropagation());
          rb.addEventListener("click",e=>{ e.stopPropagation(); if(flow&&flow.resetView) flow.resetView(); }); }
  $("#replay-btn").addEventListener("click",async()=>{ $("#result-modal").classList.remove("show"); await startGame(); });
  window.addEventListener("resize",renderChart);
}
