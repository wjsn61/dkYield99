// ════════════════════════════════════════════════════════════════
//  공장의 사람들 (workers.js)
//
//  공장이 잘 돌아가면 사람이 늘고, 위험해지면 현장이 빕니다.
//  이 파일은 그것을 눈에 보이게 만듭니다.
//
//  ▶ 어떻게 그리나요?
//     픽셀아트를 캔버스에 직접 그린 뒤(px 함수) 텍스처로 만들어
//     THREE.Sprite 로 세웁니다. 스프라이트는 늘 카메라를 바라보기 때문에
//     3D 플랜트 안에서도 2D 도트 캐릭터로 보입니다.
//
//  ▶ 몇 명이 나오나요?   ← 공장 활성화
//     생산량 · 수율 · 순도 가 높을수록 사람이 늘고,
//     안전지수 · 환경지수 가 낮으면 현장이 빕니다.
//     위험한 공장에서는 걸음도 조심스러워집니다(느려집니다).
//
//  ▶ 누가 나오나요?      ← 시행한 카드
//     연구를 시작하면 연구자가, 예방정비를 넣으면 정비원이,
//     온라인 분석기를 달면 품질검사원이 나타납니다.
//     "카드가 공장의 풍경을 바꾼다"를 그림으로 보여 줍니다.
// ════════════════════════════════════════════════════════════════
import * as THREE from "three";

// ── 1. 색 팔레트 ─────────────────────────────────────────────────
const PALETTES = {
  skin: ["#ffd7b0", "#f2c49a", "#d9a06b", "#b87d4f"],
  hair: ["#2c2c3a", "#7a4a2b", "#e5b84b", "#4a6fb0", "#6b4a8c"],
  pants: ["#2f3542", "#3d4454", "#4a5568"],
};
const pick = (list, rng) => list[Math.floor(rng() * list.length)];

function makeRng(seed) {
  let s = seed >>> 0;
  return () => {
    s = (s * 1664525 + 1013904223) >>> 0;
    return s / 4294967296;
  };
}

// ── 2. 인력 유형과 등장 조건 ─────────────────────────────────────
export const WORKER_TYPES = {
  관리자: {
    카드: null, 기본: true, 작업복: "#f5a623",
    설명: "공정 관리자 - 늘 현장에 있습니다. 생산량이 늘면 인원도 늘어납니다",
  },
  연구자: {
    카드: ["high_selectivity_catalyst", "condition_opt", "membrane_research",
           "runaway_analysis", "high_purity_product"],
    연구중포함: true, 작업복: "#e8edf2",
    설명: "R&D 를 시작하면 흰 가운을 입은 연구자가 나타납니다",
  },
  정비원: {
    카드: ["preventive_maint", "hx_clean"], 작업복: "#4db6ff",
    설명: "예방정비·세정을 하면 정비원이 설비를 돌아봅니다",
  },
  품질검사원: {
    카드: ["online_analyzer", "qc_sampling"], 작업복: "#b08cff",
    설명: "분석기를 달거나 QC 를 강화하면 검사원이 시료를 받으러 다닙니다",
  },
  환경담당: {
    카드: ["wastewater", "heat_recovery"], 작업복: "#8ae65c",
    설명: "폐수처리·폐열회수 설비가 생기면 환경담당이 순찰합니다",
  },
};

// ── 3. 픽셀아트 그리기 ───────────────────────────────────────────
const CELL = 4;
const GRID_W = 10, GRID_H = 14;

function drawWorker(type, colors, frame) {
  const canvas = document.createElement("canvas");
  canvas.width = GRID_W * CELL;
  canvas.height = GRID_H * CELL;
  const g = canvas.getContext("2d");
  const px = (x, y, w, h, color) => {
    g.fillStyle = color;
    g.fillRect(x * CELL, y * CELL, w * CELL, h * CELL);
  };

  const suit = WORKER_TYPES[type]?.작업복 || "#f5a623";

  // ── 머리 위 (안전모 / 고글) ──
  if (type === "연구자") {
    px(2, 0, 6, 2, colors.hair);
    px(2, 3, 6, 1, "#9fd8ff");                 // 보안경
  } else if (type === "품질검사원") {
    px(2, 0, 6, 2, "#ffffff");                 // 흰 캡
    px(1, 2, 8, 1, "#ffffff");
  } else {
    px(2, 0, 6, 2, suit);                      // 안전모
    px(1, 2, 8, 1, suit);
    px(3, 1, 4, 1, "#ffffff");                 // 안전모 하이라이트
  }

  // ── 얼굴 ──
  px(3, 3, 4, 2, colors.skin);
  px(3, 3, 1, 1, "#2c2c3a");
  px(6, 3, 1, 1, "#2c2c3a");

  // ── 몸통 (작업복) ──
  const bodyY = 5, bodyH = 5;
  px(2, bodyY, 6, bodyH, suit);
  px(2, bodyY + 2, 6, 1, "#ffffff");           // 형광 반사띠
  if (type === "연구자") {
    px(2, bodyY, 6, bodyH, "#e8edf2");         // 흰 가운
    px(4, bodyY, 2, bodyH, "#d3dae2");
    px(6, bodyY + 1, 2, 2, "#2fe0c8");         // 가슴 주머니 (시약)
  }
  if (type === "관리자") px(2, bodyY + 1, 2, 2, "#20242e");   // 클립보드
  if (type === "품질검사원") px(6, bodyY + 1, 2, 3, "#ffd23f"); // 시료병
  if (type === "정비원") px(1, bodyY + 2, 2, 2, "#8f98a3");    // 공구
  if (type === "환경담당") px(6, bodyY + 1, 2, 2, "#2ed573");   // 측정기

  // ── 팔 ──
  const armY = bodyY + 1;
  if (frame === 0) {
    px(1, armY, 1, 3, colors.skin);
    px(8, armY + 1, 1, 3, colors.skin);
  } else {
    px(1, armY + 1, 1, 3, colors.skin);
    px(8, armY, 1, 3, colors.skin);
  }

  // ── 다리 (두 동작 = 걷기) ──
  const legY = bodyY + bodyH;
  const legH = GRID_H - legY - 1;
  if (frame === 0) {
    px(3, legY, 2, legH, colors.pants);
    px(5, legY, 2, legH, colors.pants);
    px(3, GRID_H - 1, 2, 1, "#20242e");
    px(5, GRID_H - 1, 2, 1, "#20242e");
  } else {
    px(2, legY, 2, legH, colors.pants);
    px(6, legY, 2, legH, colors.pants);
    px(2, GRID_H - 1, 2, 1, "#20242e");
    px(6, GRID_H - 1, 2, 1, "#20242e");
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.magFilter = THREE.NearestFilter;
  texture.minFilter = THREE.NearestFilter;
  texture.generateMipmaps = false;
  if ("colorSpace" in texture) texture.colorSpace = THREE.SRGBColorSpace;
  return texture;
}

// ── 4. 보행 그래프 ───────────────────────────────────────────────
//    설비는 위(z=-3)와 아래(z=+3) 두 줄로 놓여 있습니다.
//    그 사이 통로(z=0)를 따라 걷고, 설비 앞까지 잠깐 다가갔다 옵니다.
const AISLE_X = [-8.5, -7.0, -5.15, -3.3, -1.5, 0.3, 2.15, 4.0, 5.5];
const EQUIP_X = [-7.0, -3.3, 0.3, 4.0];
const STUB_Z = 1.7;

const WALK_NODES = [];
const WALK_ADJ = [];

// 통로 노드
AISLE_X.forEach((x) => WALK_NODES.push({ x, z: 0 }));
for (let i = 0; i < AISLE_X.length; i++) {
  const near = [];
  if (i > 0) near.push(i - 1);
  if (i < AISLE_X.length - 1) near.push(i + 1);
  WALK_ADJ.push(near);
}
// 설비 앞 노드 (위/아래)
EQUIP_X.forEach((x) => {
  const aisleIndex = AISLE_X.indexOf(x);
  for (const z of [-STUB_Z, STUB_Z]) {
    const nodeIndex = WALK_NODES.length;
    WALK_NODES.push({ x, z });
    WALK_ADJ.push([aisleIndex]);            // 통로로만 되돌아갑니다
    WALK_ADJ[aisleIndex].push(nodeIndex);
  }
});

// ── 5. 공장 활성화 계산 ──────────────────────────────────────────
const clamp01 = (v) => Math.max(0, Math.min(1, Number.isFinite(v) ? v : 0));

/**
 * 공장이 얼마나 '살아 있는지'를 0~1 로 계산합니다.
 *
 * 잘 만들고(생산량·수율·순도) 안전한(안전·환경) 공장에 사람이 모입니다.
 * 안전지수가 낮으면 사람이 빠지고 걸음도 조심스러워집니다.
 */
export function plantVitality(state) {
  if (!state) return 0.4;
  const output = clamp01((state["생산량"] || 0) / 1600);
  const yieldRate = clamp01(((state["수율"] || 0) - 60) / 40);       // 60~100%
  const purity = clamp01(((state["순도"] || 0) - 88) / 12);          // 88~100%
  const safety = clamp01((state["안전지수"] || 0) / 100);
  const env = clamp01((state["환경지수"] || 0) / 100);

  return clamp01(output * 0.20 + yieldRate * 0.24 + purity * 0.20
                 + safety * 0.24 + env * 0.12);
}

/** 시행한 카드를 보고 어떤 인력이 현장에 나올지 정합니다. */
export function workerMix(state) {
  const installed = new Set(state?.["설비목록"] || []);
  const researching = new Set((state?.["연구중"] || []).map((r) => r["아이디"]));
  const types = [];
  for (const [name, def] of Object.entries(WORKER_TYPES)) {
    if (def.기본) { types.push(name); continue; }
    const need = Array.isArray(def.카드) ? def.카드 : [def.카드];
    const hit = need.some((c) => installed.has(c))
      || (def.연구중포함 && need.some((c) => researching.has(c)));
    if (hit) types.push(name);
  }
  return types;
}

// ── 6. 사람들을 공장에 올린다 ────────────────────────────────────
const MAX_WORKERS = 18;

export function mountWorkers(scene) {
  const group = new THREE.Group();
  group.name = "workers";
  scene.add(group);

  const textureCache = new Map();
  const workers = [];
  let vitality = 0.4;
  let mix = ["관리자"];

  function textureFor(type, colorKey, colors, frame) {
    const key = `${type}|${colorKey}|${frame}`;
    if (!textureCache.has(key)) textureCache.set(key, drawWorker(type, colors, frame));
    return textureCache.get(key);
  }

  function spawn(index, type) {
    const rng = makeRng(index * 7919 + 29);
    const colors = {
      skin: pick(PALETTES.skin, rng),
      hair: pick(PALETTES.hair, rng),
      pants: pick(PALETTES.pants, rng),
    };
    const colorKey = `${colors.skin}${colors.hair}${colors.pants}`;
    const frames = [
      textureFor(type, colorKey, colors, 0),
      textureFor(type, colorKey, colors, 1),
    ];
    const material = new THREE.SpriteMaterial({
      map: frames[0], transparent: true, depthWrite: false,
    });
    const sprite = new THREE.Sprite(material);

    const scale = 0.85;                       // 플랜트가 도시보다 커서 사람도 크게
    sprite.scale.set(scale * (GRID_W / GRID_H), scale, 1);

    const from = Math.floor(rng() * WALK_NODES.length);
    const to = WALK_ADJ[from][Math.floor(rng() * WALK_ADJ[from].length)];

    const worker = {
      type, sprite, frames, material,
      from, to,
      progress: rng(),
      speed: 0.16 + rng() * 0.12,
      frame: 0, frameTimer: rng(),
      height: scale / 2 + 0.05,
      pause: 0,
      rng,
    };
    place(worker);
    group.add(sprite);
    return worker;
  }

  function place(w) {
    const a = WALK_NODES[w.from], b = WALK_NODES[w.to];
    w.sprite.position.set(
      a.x + (b.x - a.x) * w.progress,
      w.height,
      a.z + (b.z - a.z) * w.progress
    );
  }

  /** 인력 수와 종류를 공정 상태에 맞춰 다시 맞춥니다. */
  function update(state) {
    vitality = plantVitality(state);
    mix = workerMix(state);

    const wanted = Math.round(2 + vitality * (MAX_WORKERS - 2));

    while (workers.length < wanted) {
      const index = workers.length;
      const type = index % 2 === 0 ? "관리자" : mix[index % mix.length];
      workers.push(spawn(index, type));
    }
    while (workers.length > wanted) {
      const w = workers.pop();
      group.remove(w.sprite);
      w.material.dispose();
    }
    workers.forEach((w, i) => {
      const wantType = i % 2 === 0 ? "관리자" : mix[i % mix.length];
      if (w.type !== wantType) {
        group.remove(w.sprite);
        w.material.dispose();
        workers[i] = spawn(i, wantType);
      }
    });
  }

  /** 매 프레임 조금씩 움직입니다. */
  function tick(dt) {
    // 위험한 공장에서는 조심스럽게 (느리게) 걷습니다
    const pace = 0.45 + vitality * 0.8;

    for (const w of workers) {
      // 설비 앞에서는 잠깐 멈춰 점검합니다
      if (w.pause > 0) {
        w.pause -= dt;
        continue;
      }
      w.progress += w.speed * pace * dt;

      while (w.progress >= 1) {
        w.progress -= 1;
        const back = w.from;
        w.from = w.to;
        // 설비 앞(z ≠ 0)에 도착했으면 잠시 점검
        if (Math.abs(WALK_NODES[w.from].z) > 0.5) w.pause = 0.6 + w.rng() * 1.4;

        const options = WALK_ADJ[w.from].filter((n) => n !== back);
        const pool = options.length ? options : WALK_ADJ[w.from];
        w.to = pool[Math.floor(w.rng() * pool.length)];
      }
      place(w);

      w.frameTimer += dt * (2.2 + w.speed * 4) * pace;
      if (w.frameTimer >= 1) {
        w.frameTimer = 0;
        w.frame = 1 - w.frame;
        w.material.map = w.frames[w.frame];
        w.material.needsUpdate = true;
      }
    }
  }

  function dispose() {
    workers.forEach((w) => { group.remove(w.sprite); w.material.dispose(); });
    workers.length = 0;
    textureCache.forEach((t) => t.dispose());
    textureCache.clear();
    scene.remove(group);
  }

  return {
    update, tick, dispose,
    get 활력() { return vitality; },
    get 인원() { return workers.length; },
    get 유형() { return mix; },
  };
}
