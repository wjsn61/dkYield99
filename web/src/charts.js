// ════════════════════════════════════════════════════════════════
//  공정 지표 추이 차트 (canvas 직접 그리기)
// ════════════════════════════════════════════════════════════════
const SERIES = [
  { key:"수율",   color:"#2fe0c8", max:100 },
  { key:"순도",   color:"#b08cff", max:100 },
  { key:"이익",   color:"#8ae65c", max:40  },
  { key:"에너지비", color:"#ffb049", max:30  },
  { key:"안전",   color:"#ff7a85", max:100 },
];
export function legendHTML(){
  return SERIES.map(s=>`<span class="cl"><i style="background:${s.color}"></i>${s.key}</span>`).join("");
}
export function drawChart(canvas, history){
  const dpr=Math.min(devicePixelRatio,2), W=canvas.clientWidth, H=canvas.clientHeight;
  if(!W||!H) return;
  canvas.width=W*dpr; canvas.height=H*dpr;
  const ctx=canvas.getContext("2d"); ctx.setTransform(dpr,0,0,dpr,0,0); ctx.clearRect(0,0,W,H);
  const padL=8,padR=8,padT=8,padB=16, x0=padL,x1=W-padR,y0=padT,y1=H-padB;
  ctx.strokeStyle="rgba(86,150,140,0.10)"; ctx.lineWidth=1;
  for(let g=0;g<=4;g++){const y=y0+((y1-y0)*g)/4; ctx.beginPath(); ctx.moveTo(x0,y); ctx.lineTo(x1,y); ctx.stroke();}
  const n=history.length; if(n<1) return;
  const xAt=i=> x0+(x1-x0)*(n===1?0.5:i/(n-1));
  for(const s of SERIES){
    const yAt=v=> y1-(y1-y0)*Math.max(0,Math.min(1,v/s.max));
    const grad=ctx.createLinearGradient(0,y0,0,y1); grad.addColorStop(0,s.color+"33"); grad.addColorStop(1,s.color+"00");
    ctx.beginPath(); history.forEach((p,i)=>{const x=xAt(i),y=yAt(p[s.key]); i?ctx.lineTo(x,y):ctx.moveTo(x,y);});
    ctx.lineTo(xAt(n-1),y1); ctx.lineTo(xAt(0),y1); ctx.closePath(); ctx.fillStyle=grad; ctx.fill();
    ctx.beginPath(); history.forEach((p,i)=>{const x=xAt(i),y=yAt(p[s.key]); i?ctx.lineTo(x,y):ctx.moveTo(x,y);});
    ctx.strokeStyle=s.color; ctx.lineWidth=2; ctx.lineJoin="round"; ctx.shadowColor=s.color; ctx.shadowBlur=8; ctx.stroke(); ctx.shadowBlur=0;
    const lx=xAt(n-1), ly=yAt(history[n-1][s.key]);
    ctx.beginPath(); ctx.arc(lx,ly,3,0,Math.PI*2); ctx.fillStyle=s.color; ctx.fill(); ctx.strokeStyle="#081312"; ctx.lineWidth=1.5; ctx.stroke();
  }
}
