// ════════════════════════════════════════════════════════════════
//  공정 플로우시트 (Three.js 3D 입체) - 탱크·반응기·증류탑 3D 장치
//  + 파이프를 따라 흐르는 입자 + 떠있는 라벨(이름·판독값)
//  game.js 와의 인터페이스는 동일: mountFlowsheet → { update, pulseByIndicators }
// ════════════════════════════════════════════════════════════════
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { mountWorkers } from "./workers.js?v=1";

// 장치 정의 (pos = [x, 0, z]).  순서 = 공정 흐름 순서(스네이크 경로)
const EQUIP = [
  { key:"feed",      name:"원료 탱크", pos:[-7.0,0,-3], color:0x4db6ff, type:"tank",    role:"원료 등급 · 몰비",        read:s=>`원료비 ${s.원료비}` },
  { key:"pump",      name:"펌프",      pos:[-3.3,0,-3], color:0x4db6ff, type:"pump",    role:"유량 · 압력",            read:s=>`유량 ${s.유량}` },
  { key:"preheat",   name:"예열기",    pos:[ 0.3,0,-3], color:0xffb049, type:"hx",      role:"투입 온도 · 에너지",      read:s=>`에너지 ${s.에너지비}` },
  { key:"reactor",   name:"반응기",    pos:[ 4.0,0,-3], color:0xff7a85, type:"reactor", role:"온도 · 압력 · 체류 · 촉매", read:s=>`${s.반응기온도}℃ · 전환 ${s.전환율}%` },
  { key:"cooler",    name:"냉각기",    pos:[ 4.0,0, 3], color:0x2fe0c8, type:"hx",      role:"냉각수 유량 · 효율",       read:s=>`안전 ${s.안전지수}` },
  { key:"separator", name:"분리기",    pos:[ 0.3,0, 3], color:0x2fe0c8, type:"vessel",  role:"분리효율",               read:s=>`회수 ${s.분리회수율}%` },
  { key:"column",    name:"증류탑",    pos:[-3.3,0, 3], color:0xb08cff, type:"column",  role:"환류비 · 단수 · 에너지",   read:s=>`환류 ${s.환류비}` },
  { key:"product",   name:"제품 탱크", pos:[-7.0,0, 3], color:0x8ae65c, type:"tank",    role:"품질 검사 · 출하",        read:s=>`순도 ${s.순도}% · ${s.생산량}t` },
];
const IND_NODE = {
  반응기온도:"reactor", 전환율:"reactor", 선택도:"reactor", 촉매활성:"reactor", 압력:"reactor", 체류시간:"reactor",
  유량:"pump", 에너지비:"preheat", 원료비:"feed", 안전지수:"cooler",
  분리회수율:"separator", 환류비:"column", 순도:"column", 생산량:"product",
};
const PIPE_Y = 0.55;

function makeGeometry(type){
  switch(type){
    case "tank":    return { geo:new THREE.CylinderGeometry(0.9,0.9,1.7,24), h:1.7 };
    case "pump":    return { geo:new THREE.BoxGeometry(1.0,0.9,1.0), h:0.9 };
    case "hx":      return { geo:new THREE.CylinderGeometry(0.55,0.55,1.7,20).rotateZ(Math.PI/2), h:1.1 };
    case "reactor": return { geo:new THREE.CylinderGeometry(1.0,1.0,1.8,28), h:1.8 };
    case "vessel":  return { geo:new THREE.CylinderGeometry(0.8,0.8,1.5,24), h:1.5 };
    case "column":  return { geo:new THREE.CylinderGeometry(0.62,0.62,3.0,24), h:3.0 };
    default:        return { geo:new THREE.BoxGeometry(1,1,1), h:1 };
  }
}

export function mountFlowsheet(container, { onHover } = {}){
  container.style.position = "relative";
  const canvas = document.createElement("canvas");
  container.innerHTML = ""; container.appendChild(canvas);
  const labelHost = document.createElement("div");
  labelHost.className = "fs-labels"; container.appendChild(labelHost);

  const renderer = new THREE.WebGLRenderer({ canvas, antialias:true, alpha:true });
  renderer.setPixelRatio(Math.min(devicePixelRatio,2));
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const scene = new THREE.Scene();

  // 공장에서 일하는 사람들 - 잘 돌아갈수록 현장이 붐빕니다
  const workers = mountWorkers(scene);
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);
  const HOME_POS = new THREE.Vector3(1.5, 11, 16);
  const HOME_TARGET = new THREE.Vector3(-1.2, 0.5, 0);
  camera.position.copy(HOME_POS);

  // 대화형 카메라 (드래그 회전 · 휠 줌) - OrbitControls를 캔버스에 직접 부착
  const controls = new OrbitControls(camera, canvas);
  controls.enableDamping = true; controls.dampingFactor = 0.12;
  controls.target.copy(HOME_TARGET);
  controls.maxPolarAngle = Math.PI / 2 - 0.02;   // 지면 아래로 못 내려가게
  controls.minDistance = 6; controls.maxDistance = 42;
  controls.update();

  // 초기 뷰로 부드럽게 복귀
  let resetting = false, resetT = 0;
  const resetFromPos = new THREE.Vector3(), resetFromTarget = new THREE.Vector3();
  function resetView(){
    resetFromPos.copy(camera.position); resetFromTarget.copy(controls.target);
    resetT = 0; resetting = true;   // controls는 계속 활성 - 루프에서 매 프레임 카메라를 덮어써 복귀(멈춤 방지)
  }

  // 조명
  scene.add(new THREE.AmbientLight(0x33514c, 1.05));
  const key = new THREE.DirectionalLight(0xffffff, 1.35);
  key.position.set(6, 13, 8); key.castShadow = true;
  key.shadow.mapSize.set(1024,1024);
  key.shadow.camera.near=1; key.shadow.camera.far=46;
  key.shadow.camera.left=-14; key.shadow.camera.right=14; key.shadow.camera.top=12; key.shadow.camera.bottom=-12;
  scene.add(key);
  const pL1 = new THREE.PointLight(0x2fe0c8, 90, 60); pL1.position.set(-10, 5, 8); scene.add(pL1);
  const pL2 = new THREE.PointLight(0xffb049, 70, 60); pL2.position.set(10, 5, -6); scene.add(pL2);

  // 바닥
  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(40,28),
    new THREE.MeshStandardMaterial({ color:0x081311, roughness:1 })
  );
  ground.rotation.x = -Math.PI/2; ground.position.y = -0.01; ground.receiveShadow = true;
  scene.add(ground);
  const grid = new THREE.GridHelper(34, 24, 0x1c3a35, 0x12241f);
  grid.position.y = 0; scene.add(grid);

  // 장치
  const equipMeshes = {};
  for(const e of EQUIP){
    const { geo, h } = makeGeometry(e.type);
    const mat = new THREE.MeshStandardMaterial({
      color:e.color, emissive:new THREE.Color(e.color), emissiveIntensity:0.14,
      roughness:0.42, metalness:0.35,
    });
    const m = new THREE.Mesh(geo, mat);
    m.position.set(e.pos[0], h/2, e.pos[2]);
    m.castShadow = true; m.receiveShadow = true;
    m.userData = { key:e.key, base:0.14, flash:0, top:h };
    scene.add(m);
    equipMeshes[e.key] = m;

    // 라벨 (HTML 오버레이)
    const div = document.createElement("div");
    div.className = "fs-label";
    div.style.setProperty("--lc", "#"+e.color.toString(16).padStart(6,"0"));
    div.innerHTML = `<div class="box"><div class="nm">${e.name}</div><div class="rd"></div></div>`;
    labelHost.appendChild(div);
    e._label = div; e._read = div.querySelector(".rd");
    e._anchor = new THREE.Vector3(e.pos[0], h + 0.5, e.pos[2]);
  }

  // 파이프 (장치들을 잇는 곡선) + 흐름 입자
  const pts = EQUIP.map(e => new THREE.Vector3(e.pos[0], PIPE_Y, e.pos[2]));
  const curve = new THREE.CatmullRomCurve3(pts, false, "catmullrom", 0.15);
  const tube = new THREE.Mesh(
    new THREE.TubeGeometry(curve, 220, 0.09, 10, false),
    new THREE.MeshStandardMaterial({ color:0x0e2b27, emissive:0x123b35, emissiveIntensity:0.5, roughness:0.6, metalness:0.4 })
  );
  tube.castShadow = true; scene.add(tube);

  const PN = 30;
  const particles = [];
  const pGeo = new THREE.SphereGeometry(0.12, 10, 10);
  const pMat = new THREE.MeshStandardMaterial({ color:0x74f4e2, emissive:0x2fe0c8, emissiveIntensity:1.4 });
  for(let i=0;i<PN;i++){
    const p = new THREE.Mesh(pGeo, pMat); p.userData.t = i/PN; scene.add(p); particles.push(p);
  }
  let flowSpeed = 0.0016;

  // 호버 (raycast)
  const ray = new THREE.Raycaster(); const ptr = new THREE.Vector2();
  function onMove(ev){
    const r = canvas.getBoundingClientRect();
    ptr.x = ((ev.clientX-r.left)/r.width)*2-1;
    ptr.y = -((ev.clientY-r.top)/r.height)*2+1;
    ray.setFromCamera(ptr, camera);
    const hit = ray.intersectObjects(Object.values(equipMeshes), false);
    if(hit.length){
      const e = EQUIP.find(x=>x.key===hit[0].object.userData.key);
      onHover && onHover({ name:e.name, role:e.role }, ev.clientX, ev.clientY);
      canvas.style.cursor = "pointer";
    } else { onHover && onHover(null); canvas.style.cursor = "default"; }
  }
  canvas.addEventListener("pointermove", onMove);
  canvas.addEventListener("pointerleave", ()=>onHover&&onHover(null));

  // 라벨 위치 갱신
  function positionLabels(){
    const r = canvas.getBoundingClientRect();
    if(!r.width) return;
    for(const e of EQUIP){
      const v = e._anchor.clone().project(camera);
      const x = (v.x*0.5+0.5)*r.width, y = (-v.y*0.5+0.5)*r.height;
      e._label.style.left = x+"px"; e._label.style.top = y+"px";
      e._label.style.display = (v.z < 1) ? "block" : "none";
    }
  }

  const TEAL = new THREE.Color(0x2fe0c8), RED = new THREE.Color(0xff5765);
  function update(state){
    for(const e of EQUIP) e._read.textContent = e.read(state);
    // 반응기: 온도 높을수록 붉게
    const t = Math.max(0, Math.min(1, (state.반응기온도-80)/50));
    const rm = equipMeshes.reactor.material;
    rm.emissive.copy(TEAL).lerp(RED, t); rm.color.copy(new THREE.Color(0xff7a85)).lerp(RED, t*0.5);
    equipMeshes.reactor.userData.base = 0.14 + t*0.5;
    // 흐름 속도: 유량 연동
    flowSpeed = 0.0009 + (state.유량||100)*0.000022;
    positionLabels();
  }

  function pulseByIndicators(indicators){
    const keys = new Set(indicators.map(i=>IND_NODE[i]).filter(Boolean));
    keys.forEach(k=>{ if(equipMeshes[k]) equipMeshes[k].userData.flash = 1; });
  }

  let raf, alive = true;
  function resize(){
    const w = container.clientWidth, h = container.clientHeight;
    if(!w||!h) return;
    renderer.setSize(w, h, false); canvas.style.width=w+"px"; canvas.style.height=h+"px";
    camera.aspect = w/h; camera.updateProjectionMatrix(); positionLabels();
  }
  let lastFrame = performance.now();
  function loop(){
    if(!alive) return; raf = requestAnimationFrame(loop);
    // 사람들을 조금씩 걷게 합니다 (dt = 지난 프레임과의 시간 차, 초 단위)
    const nowFrame = performance.now();
    const dt = Math.min(0.05, (nowFrame - lastFrame) / 1000);
    lastFrame = nowFrame;
    workers.tick(dt);
    // 컨트롤은 항상 갱신하고, 복귀 중이면 그 위에 카메라를 덮어써 보간(컨트롤이 꺼진 채 멈추는 일 없음)
    controls.update();
    if(resetting){
      resetT = Math.min(1, resetT + 1/36);
      const e = resetT*resetT*(3-2*resetT);   // smoothstep
      camera.position.lerpVectors(resetFromPos, HOME_POS, e);
      controls.target.lerpVectors(resetFromTarget, HOME_TARGET, e);
      camera.lookAt(controls.target);
      if(resetT>=1) resetting = false;
    }
    // 입자 이동
    for(const p of particles){
      p.userData.t = (p.userData.t + flowSpeed) % 1;
      curve.getPointAt(p.userData.t, p.position);
    }
    // 장치 플래시 감쇠 + 반응기 발광
    for(const e of EQUIP){
      const m = equipMeshes[e.key], u = m.userData;
      u.flash *= 0.9;
      m.material.emissiveIntensity = u.base + u.flash * 0.9;
    }
    positionLabels();   // 카메라가 움직이므로 매 프레임 라벨 위치 갱신
    renderer.render(scene, camera);
  }
  const ro = new ResizeObserver(resize); ro.observe(container);
  resize(); loop();
  setTimeout(positionLabels, 60);

  return {
    update, pulseByIndicators, resetView,
    // 공정 상태가 바뀌면 현장의 사람 수와 종류를 다시 맞춥니다
    updateWorkers: (state) => workers.update(state),
    workers,
    dispose(){ alive=false; cancelAnimationFrame(raf); ro.disconnect(); workers.dispose();
      canvas.removeEventListener("pointermove",onMove); controls.dispose(); renderer.dispose(); labelHost.remove(); }
  };
}
