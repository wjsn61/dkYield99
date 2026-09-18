// ════════════════════════════════════════════════════════════════
//  앱 진입점 - 타이틀 화면 → 게임 화면 전환
// ════════════════════════════════════════════════════════════════
import { api } from "./api.js";
import { mountTitleScene } from "./three-mol.js";
import { startGame } from "./game.js?v=2";

const $ = s=>document.querySelector(s);
let titleScene=null;

async function initTitle(){
  titleScene=mountTitleScene($("#title-canvas"));
  try{
    const sc=await api.scenario();
    $("#scenario-name").textContent=sc["이름"];
    $("#scenario-reaction").textContent=sc["반응"];
    $("#scenario-desc").textContent=sc["설명"];
    const s=sc["초기상태"];
    $("#scenario-stats").innerHTML=[
      ["수율",`${s["수율"]}%`],["순도",`${s["순도"]}%`],
      ["예산",`${s["예산"]}억`],["안전",s["안전지수"]],
    ].map(([k,v])=>`<div class="s"><div class="k">${k}</div><div class="v">${v}</div></div>`).join("");
    $("#scenario-goals").innerHTML=sc["목표"].map(g=>`<li>${g}</li>`).join("");
  }catch(e){ console.warn("시나리오 로드 실패:",e); }
}

$("#start-btn").addEventListener("pointermove",e=>{
  const r=e.currentTarget.getBoundingClientRect();
  e.currentTarget.style.setProperty("--mx",(e.clientX-r.left)+"px");
});
$("#start-btn").addEventListener("click",async()=>{
  const btn=$("#start-btn"); btn.disabled=true; btn.querySelector(".btn-label").textContent="공정 가동 준비...";
  try{
    await startGame();
    $("#title-screen").classList.remove("is-active");
    $("#game-screen").classList.add("is-active");
    setTimeout(()=>{ titleScene&&titleScene.dispose(); titleScene=null; },700);
  }catch(e){
    console.error("게임 시작 실패:", e);
    btn.disabled=false; btn.querySelector(".btn-label").textContent="공정 가동하기";
    alert(
      "게임을 시작할 수 없습니다.\n\n" +
      "1) 서버가 켜져 있나요?  C:\\dkYield99\\start.bat 더블클릭\n" +
      "   (또는 server 폴더에서  python run.py)\n" +
      "2) 이 페이지 주소가  http://127.0.0.1:5000  인가요?\n\n" +
      "자세한 원인: " + (e && e.message ? e.message : e)
    );
  }
});

initTitle();
