// ════════════════════════════════════════════════════════════════
//  Three.js - 타이틀 분자 네트워크 배경 (천천히 회전)
// ════════════════════════════════════════════════════════════════
import * as THREE from "three";

export function mountTitleScene(canvas){
  const renderer = new THREE.WebGLRenderer({ canvas, antialias:true, alpha:true });
  renderer.setPixelRatio(Math.min(devicePixelRatio,2));
  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x050c0b, 0.055);
  const camera = new THREE.PerspectiveCamera(46, 1, 0.1, 200);
  camera.position.set(0, 0, 30);

  const group = new THREE.Group(); scene.add(group);

  // 원자(노드) 생성
  const COLORS = [0x2fe0c8, 0xffb049, 0x8ae65c, 0x4db6ff, 0xb08cff];
  const N = 46;
  const nodes = [];
  const sphereGeo = new THREE.SphereGeometry(0.42, 16, 16);
  for(let i=0;i<N;i++){
    const c = COLORS[(Math.random()*COLORS.length)|0];
    const mat = new THREE.MeshStandardMaterial({ color:c, emissive:c, emissiveIntensity:0.6, roughness:0.35, metalness:0.2 });
    const m = new THREE.Mesh(sphereGeo, mat);
    const p = new THREE.Vector3((Math.random()-0.5)*36,(Math.random()-0.5)*24,(Math.random()-0.5)*22);
    m.position.copy(p);
    const s = 0.5 + Math.random()*1.3; m.scale.setScalar(s);
    group.add(m); nodes.push(p);
  }
  // 결합(본드) 생성 - 가까운 원자끼리 선으로 연결
  const positions = [];
  for(let i=0;i<N;i++) for(let j=i+1;j<N;j++){
    if(nodes[i].distanceTo(nodes[j]) < 7.5){
      positions.push(nodes[i].x,nodes[i].y,nodes[i].z, nodes[j].x,nodes[j].y,nodes[j].z);
    }
  }
  const bondGeo = new THREE.BufferGeometry();
  bondGeo.setAttribute("position", new THREE.Float32BufferAttribute(positions,3));
  const bonds = new THREE.LineSegments(bondGeo, new THREE.LineBasicMaterial({ color:0x2fe0c8, transparent:true, opacity:0.18 }));
  group.add(bonds);

  scene.add(new THREE.AmbientLight(0x2a4a44, 1.2));
  const d = new THREE.DirectionalLight(0xffffff, 0.8); d.position.set(10,12,18); scene.add(d);
  const p1 = new THREE.PointLight(0x2fe0c8, 120, 80); p1.position.set(-14,8,12); scene.add(p1);
  const p2 = new THREE.PointLight(0xffb049, 90, 80); p2.position.set(16,-8,10); scene.add(p2);

  let raf, t=0, alive=true;
  function resize(){ const w=canvas.clientWidth,h=canvas.clientHeight; if(!w||!h) return;
    renderer.setSize(w,h,false); camera.aspect=w/h; camera.updateProjectionMatrix(); }
  function loop(){ if(!alive) return; raf=requestAnimationFrame(loop);
    t+=0.0014; group.rotation.y=t; group.rotation.x=Math.sin(t*0.6)*0.18; renderer.render(scene,camera); }
  const ro=new ResizeObserver(resize); ro.observe(canvas); resize(); loop();

  return { dispose(){ alive=false; cancelAnimationFrame(raf); ro.disconnect(); renderer.dispose(); } };
}
