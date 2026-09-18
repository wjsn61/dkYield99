// ════════════════════════════════════════════════════════════════
//  통계 지표 다이얼로그 · 저장/불러오기 다이얼로그
//
//  ※ 계산은 전부 서버(파이썬)가 합니다. 여기서는 받은 결과를 그릴 뿐입니다.
//     9주에 여러분이 직접 만든 평균·표준편차 함수의 답이
//     여기 나온 값과 같은지 맞춰 보세요.
// ════════════════════════════════════════════════════════════════
import { api } from "./api.js";

const $ = (s) => document.querySelector(s);
const CSS = (name) => getComputedStyle(document.body).getPropertyValue(name).trim();

let ctxGame = { id: null, toast: () => {}, onLoaded: null };
let statsData = null;
let activeTab = 0;

export function initPanels({ getGameId, toast, onLoaded }) {
  ctxGame = { getGameId, toast, onLoaded };
  wireStats();
  wireSaves();
}

// ════════════════════════════════════════════════════════════════
//  엑셀 모습의 표
//
//  그래프는 요약입니다. 요약만 보면 무엇이 요약됐는지 알 수 없으므로,
//  그 그래프를 만든 실제 숫자를 스프레드시트 모양 그대로 함께 보여 줍니다.
//  열 머리(A·B·C)와 행 번호를 붙이는 이유는, 학생이 이 화면과 엑셀을
//  나란히 놓고 "3행 B열" 같은 말로 같은 칸을 가리킬 수 있게 하기 위해서입니다.
// ════════════════════════════════════════════════════════════════
const colLetter = (i) => {
  let s = "";
  for (i += 1; i > 0; i = Math.floor((i - 1) / 26)) s = String.fromCharCode(65 + ((i - 1) % 26)) + s;
  return s;
};

const cellText = (v) =>
  v === null || v === undefined || v === "" ? ""
    : typeof v === "number" ? (Number.isInteger(v) ? String(v) : v.toFixed(3).replace(/\.?0+$/, ""))
    : String(v);

/** 표를 탭 구분 텍스트로 - 엑셀에 그대로 붙여넣을 수 있는 모양입니다. */
function sheetToTSV(columns, rows) {
  return [columns.join("\t"),
          ...rows.map((r) => columns.map((c) => cellText(r[c])).join("\t"))].join("\n");
}

/**
 * 스프레드시트 모양의 표를 그립니다.
 *  - caption : 이 표가 무엇인지
 *  - columns : 열 이름들
 *  - rows    : 행(객체) 목록
 *  - opts.highlight : 강조할 열 이름 (지금 보고 있는 지표)
 *  - opts.limit     : 화면에 펼칠 최대 행 수 (넘으면 접습니다)
 */
function renderSheet(host, caption, columns, rows, opts = {}) {
  const { highlight: hi = "", limit = 14 } = opts;
  const wrap = document.createElement("div");
  wrap.className = "sheet-block";

  const shown = rows.length > limit ? rows.slice(0, limit) : rows;
  const head = columns.map((c, i) =>
    `<th class="${c === hi ? "hi" : ""}"><span class="cl">${colLetter(i)}</span>${c}</th>`).join("");
  const body = shown.map((r, ri) =>
    `<tr><th class="rn">${ri + 2}</th>` +
    columns.map((c) => `<td class="${c === hi ? "hi" : ""}">${cellText(r[c])}</td>`).join("") +
    `</tr>`).join("");

  wrap.innerHTML = `
    <div class="sheet-head">
      <span class="sh-title">📋 ${caption}</span>
      <span class="sh-size">${rows.length}행 × ${columns.length}열</span>
      <button class="sheet-copy" type="button">엑셀로 복사</button>
    </div>
    <div class="sheet-scroll">
      <table class="sheet">
        <thead><tr><th class="rn corner">1</th>${head}</tr></thead>
        <tbody>${body}</tbody>
      </table>
    </div>
    ${rows.length > shown.length
      ? `<div class="sheet-more">아래 ${rows.length - shown.length}행은 접혀 있습니다 -
         <b>엑셀로 복사</b>를 누르면 전부 복사됩니다.</div>` : ""}`;

  wrap.querySelector(".sheet-copy").addEventListener("click", async (e) => {
    const tsv = sheetToTSV(columns, rows);
    try {
      await navigator.clipboard.writeText(tsv);
      e.target.textContent = "복사됨 · 엑셀에 붙여넣기";
      setTimeout(() => (e.target.textContent = "엑셀로 복사"), 2200);
    } catch {
      ctxGame.toast("복사에 실패했습니다. 📥 엑셀용 CSV 를 쓰세요.", "bad");
    }
  });
  host.appendChild(wrap);
  return wrap;
}

// ════════════════════════════════════════════════════════════════
//  화면이 한 계산을, 학생이 그대로 돌려 볼 수 있는 파이썬 파일로
//
//  화면의 숫자를 그냥 베끼면 아무것도 남지 않습니다.
//  그래서 내려받는 파일에는 '화면에 나와 있던 값'을 함께 적어 둡니다.
//  학생이 직접 계산한 값과 그 값이 같은지 파일이 스스로 확인해 줍니다.
// ════════════════════════════════════════════════════════════════
/** 받침이 있으면 '을/이/은', 없으면 '를/가/는'. 어색한 조사는 교재의 신뢰를 깎습니다. */
function particle(word, withFinal, withoutFinal) {
  const ch = (word || "").trim().slice(-1);
  const code = ch.charCodeAt(0);
  if (!(code >= 0xac00 && code <= 0xd7a3)) return withFinal;   // 한글이 아니면 안전한 쪽
  return (code - 0xac00) % 28 ? withFinal : withoutFinal;
}

function csvPathOf() {
  const s = statsData.요약 || {};
  if (!s.데이터폴더) return "";
  const sep = s.데이터폴더.includes("\\") ? "\\" : "/";
  return `${s.데이터폴더}${sep}${s.파일이름}`;
}

/**
 * 파이썬 소스를 아주 얕게 색칠합니다.
 *
 * ※ 치환을 여러 번 겹쳐 돌리면 안 됩니다 - 먼저 만든 `class="c"` 의 따옴표를
 *   다음 치환이 문자열로 다시 잡아먹습니다. 그래서 한 번만 훑으면서
 *   토큰과 토큰 사이의 원본만 이스케이프해 이어 붙입니다.
 */
function pyHighlight(src) {
  const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const RE = /(#[^\n]*)|("""[\s\S]*?"""|"(?:[^"\\\n]|\\.)*")|\b(import|from|def|return|for|in|if|not|else|with|as|raise|and|or|True|False|None)\b/g;
  let out = "", last = 0, m;
  while ((m = RE.exec(src)) !== null) {
    out += esc(src.slice(last, m.index));
    out += `<span class="${m[1] ? "c" : m[2] ? "s" : "k"}">${esc(m[0])}</span>`;
    last = m.index + m[0].length;
  }
  return out + esc(src.slice(last));
}

/**
 * 코드 카드 - 보여 주고 · 내려받고 · 어떻게 돌리는지 알려 줍니다.
 * host 아래에 붙입니다.
 */
function renderCodeCard(host, { title, filename, code, why }) {
  const card = document.createElement("div");
  card.className = "code-card";
  card.innerHTML = `
    <div class="cc-head">
      <span class="cc-title">🐍 ${title}</span>
      <span class="cc-file">${filename}</span>
      <button class="cc-copy" type="button">복사</button>
      <button class="cc-down" type="button">⬇ .py 내려받기</button>
    </div>
    <div class="cc-why">${why}</div>
    <pre class="cc-code"><code>${pyHighlight(code)}</code></pre>
    <div class="cc-run">
      내려받은 파일을 <b>lab</b> 폴더에 넣고, VS Code 터미널에서
      <code>cd lab</code> → <code>python ${filename}</code>
    </div>`;

  card.querySelector(".cc-copy").addEventListener("click", async (e) => {
    try {
      await navigator.clipboard.writeText(code);
      e.target.textContent = "복사됨";
      setTimeout(() => (e.target.textContent = "복사"), 2000);
    } catch { ctxGame.toast("복사에 실패했습니다.", "bad"); }
  });

  card.querySelector(".cc-down").addEventListener("click", () => {
    // BOM 을 붙여야 메모장으로 열어도 한글이 깨지지 않습니다.
    const blob = new Blob(["﻿" + code], { type: "text/x-python;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    ctxGame.toast(`${filename} 내려받음 - lab 폴더에 옮겨 실행하세요`, "good");
  });

  host.appendChild(card);
}

/** 공통 머리말 - 모든 내려받기 파일에 같은 문장이 들어갑니다. */
function pyHeader(title, filename) {
  return `# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
#  ${title}
#
#  「📊 통계 지표 보기」 화면에서 내려받은 파일입니다.
#  화면의 숫자를 베끼지 마세요. 이 파일이 여러분의 계산과
#  화면의 값을 나란히 찍어 줍니다. 두 값이 같아야 합니다.
#
#  실행:  cd lab  →  python ${filename}
#  ※ 외부 라이브러리가 필요 없습니다 (동봉된 파이썬으로 그냥 돕니다).
# ─────────────────────────────────────────────────────────────
import csv
from pathlib import Path
`;
}

/** CSV 를 읽어 한 컬럼을 숫자 리스트로 - 모든 파일이 공유하는 부분입니다. */
const PY_LOADER = `
def load_column(path, name):
    """CSV 에서 한 컬럼을 숫자만 뽑아 리스트로 돌려줍니다."""
    if not path.exists():
        raise SystemExit(
            f"CSV 를 찾지 못했습니다:\\n  {path}\\n\\n"
            "게임 화면에서 [📥 엑셀용 CSV] 를 먼저 눌러 주세요.")
    # utf-8-sig 로 열어야 엑셀이 넣은 BOM 이 컬럼 이름에 붙지 않습니다.
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise SystemExit("CSV 에 줄이 없습니다.")
    # 파일 종류에 따라 컬럼 이름이 조금 다릅니다 (턴별 / 판별요약)
    for c in (name, f"최종_{name}", f"평균_{name}"):
        if c in rows[0]:
            name = c
            break
    else:
        raise SystemExit(f"'{name}' 컬럼이 없습니다.\\n있는 컬럼: {list(rows[0])[:12]}")
    values = []
    for row in rows:
        try:
            values.append(float(row[name]))
        except (TypeError, ValueError):
            pass
    return name, values
`;

/** 화면값과 내 계산을 나란히 찍는 부분 - 이 과목의 핵심 장면입니다. */
const PY_COMPARE = `
def compare(mine, screen):
    """내 계산과 화면 값을 나란히 찍습니다. 이게 이 파일의 목적입니다."""
    print(f"{'':<12}{'내 계산':>12}{'화면':>12}   같나요?")
    print("-" * 52)
    ok = True
    for key, shown in screen.items():
        got = mine[key]
        same = abs(got - shown) < 0.05
        ok = ok and same
        print(f"{key:<12}{got:>12.3f}{shown:>12.3f}   {'예' if same else '★ 다릅니다'}")
    print()
    print("모두 같습니다. 이제 이 숫자를 믿어도 됩니다." if ok else
          "값이 다릅니다. 어느 쪽이 틀렸는지 찾는 것이 오늘 과제입니다.\\n"
          "  · 표준편차는 n 이 아니라 n-1 로 나눴나요?\\n"
          "  · 화면과 같은 컬럼을 읽고 있나요?")
`;

/** 이 판의 데이터가 어느 파일에 있는지 알려 줍니다. */
function renderDataPath(host) {
  const s = statsData.요약 || {};
  if (!s.데이터폴더) return;
  const sep = s.데이터폴더.includes("\\") ? "\\" : "/";
  const full = `${s.데이터폴더}${sep}${s.파일이름}`;
  const div = document.createElement("div");
  div.className = "data-path";
  div.innerHTML = `
    <span class="dp-k">데이터 위치</span>
    <code class="dp-v">${full}</code>
    <span class="dp-state ${s.파일있음 ? "on" : ""}">${s.파일있음 ? "파일 있음" : "아직 없음"}</span>
    <span class="dp-hint">${s.파일있음
      ? "이 파일을 엑셀에서 열면 위 표와 똑같습니다."
      : "위 <b>📥 엑셀용 CSV</b> 를 누르면 이 경로에 만들어집니다."}</span>
    <span class="dp-hint">판을 <b>이름 붙여 저장</b>하면 <code>${s.데이터폴더}${sep}&lt;그 이름&gt;.csv</code> 도 함께 생깁니다.</span>`;
  host.appendChild(div);
}

// ════════════════════════════════════════════════════════════════
//  그래프 그리기 (작은 캔버스 유틸)
// ════════════════════════════════════════════════════════════════
function makeCanvas(host, height = 170) {
  const canvas = document.createElement("canvas");
  canvas.className = "mini-chart";
  host.appendChild(canvas);
  const ratio = window.devicePixelRatio || 1;
  const width = host.clientWidth || 520;
  canvas.width = width * ratio;
  canvas.height = height * ratio;
  canvas.style.width = "100%";
  canvas.style.height = height + "px";
  const ctx = canvas.getContext("2d");
  ctx.scale(ratio, ratio);
  return { ctx, w: width, h: height };
}

function axes(ctx, w, h, pad) {
  ctx.strokeStyle = "rgba(126,152,191,.28)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(pad.l, pad.t);
  ctx.lineTo(pad.l, h - pad.b);
  ctx.lineTo(w - pad.r, h - pad.b);
  ctx.stroke();
}

function label(ctx, text, x, y, color = "#8696b2", align = "left", size = 10) {
  ctx.fillStyle = color;
  ctx.font = `${size}px "IBM Plex Mono", monospace`;
  ctx.textAlign = align;
  ctx.fillText(text, x, y);
}

/** 히스토그램 - 값이 어느 구간에 몰려 있는가 */
function drawHistogram(host, hist, color) {
  if (!hist || !hist.도수) return;
  const { ctx, w, h } = makeCanvas(host, 170);
  const pad = { l: 34, r: 12, t: 14, b: 34 };
  axes(ctx, w, h, pad);

  const max = Math.max(...hist.도수, 1);
  const innerW = w - pad.l - pad.r;
  const innerH = h - pad.t - pad.b;
  const barW = innerW / hist.도수.length;

  hist.도수.forEach((count, i) => {
    const barH = (count / max) * innerH;
    ctx.fillStyle = color;
    ctx.globalAlpha = 0.75;
    ctx.fillRect(pad.l + i * barW + 2, h - pad.b - barH, barW - 4, barH);
    ctx.globalAlpha = 1;
    if (count > 0) label(ctx, count, pad.l + i * barW + barW / 2, h - pad.b - barH - 4, "#e9eff8", "center");
  });

  label(ctx, hist.시작, pad.l, h - pad.b + 16, "#5d6c86", "left");
  label(ctx, hist.끝, w - pad.r, h - pad.b + 16, "#5d6c86", "right");
  label(ctx, "값의 분포 (가로: 값 구간 / 세로: 몇 번)", pad.l, h - 6, "#5d6c86", "left", 9);
}

/** 관리도 - 이 변화가 우연인가, 신호인가 */
function drawControlChart(host, values, turns, limits, color) {
  if (!limits || values.length < 2) return;
  const { ctx, w, h } = makeCanvas(host, 190);
  const pad = { l: 44, r: 14, t: 14, b: 30 };
  const innerW = w - pad.l - pad.r;
  const innerH = h - pad.t - pad.b;

  const lo = Math.min(limits.관리하한, ...values);
  const hi = Math.max(limits.관리상한, ...values);
  const span = hi - lo || 1;
  const X = (i) => pad.l + (i / Math.max(1, values.length - 1)) * innerW;
  const Y = (v) => pad.t + innerH - ((v - lo) / span) * innerH;

  // 관리한계 띠
  ctx.fillStyle = "rgba(88,220,139,.07)";
  ctx.fillRect(pad.l, Y(limits.관리상한), innerW, Y(limits.관리하한) - Y(limits.관리상한));

  // 한계선 · 중심선
  const lines = [
    [limits.관리상한, "#ff5d6c", [5, 4], "UCL"],
    [limits.중심선, "#8696b2", [], "CL"],
    [limits.관리하한, "#ff5d6c", [5, 4], "LCL"],
  ];
  for (const [v, c, dash, name] of lines) {
    ctx.strokeStyle = c;
    ctx.setLineDash(dash);
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(pad.l, Y(v));
    ctx.lineTo(w - pad.r, Y(v));
    ctx.stroke();
    ctx.setLineDash([]);
    label(ctx, `${name} ${v}`, pad.l - 4, Y(v) + 3, c, "right", 9);
  }

  // 값 선
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.8;
  ctx.beginPath();
  values.forEach((v, i) => (i ? ctx.lineTo(X(i), Y(v)) : ctx.moveTo(X(i), Y(v))));
  ctx.stroke();

  // 점 (이탈점은 빨갛게 크게)
  values.forEach((v, i) => {
    const out = v > limits.관리상한 || v < limits.관리하한;
    ctx.fillStyle = out ? "#ff5d6c" : color;
    ctx.beginPath();
    ctx.arc(X(i), Y(v), out ? 4.5 : 2.4, 0, Math.PI * 2);
    ctx.fill();
    if (out) label(ctx, `${turns[i]}턴`, X(i), Y(v) - 9, "#ff5d6c", "center", 9);
  });

  label(ctx, "관리도 (가로: 턴 / 붉은 점: 우연으로 보기 어려운 값)", pad.l, h - 8, "#5d6c86", "left", 9);
}

/** 상자그림 - 사분위와 이상치 */
function drawBox(host, stats, color) {
  const { ctx, w, h } = makeCanvas(host, 90);
  const pad = { l: 40, r: 40, t: 26, b: 30 };
  const innerW = w - pad.l - pad.r;
  const lo = stats.최소, hi = stats.최대;
  const span = hi - lo || 1;
  const X = (v) => pad.l + ((v - lo) / span) * innerW;
  const midY = pad.t + 14;

  // 수염
  ctx.strokeStyle = "rgba(126,152,191,.5)";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(X(lo), midY); ctx.lineTo(X(hi), midY);
  ctx.stroke();

  // 상자
  ctx.fillStyle = color;
  ctx.globalAlpha = 0.3;
  ctx.fillRect(X(stats["1사분위"]), midY - 13, X(stats["3사분위"]) - X(stats["1사분위"]), 26);
  ctx.globalAlpha = 1;
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.4;
  ctx.strokeRect(X(stats["1사분위"]), midY - 13, X(stats["3사분위"]) - X(stats["1사분위"]), 26);

  // 중앙값
  ctx.strokeStyle = "#e9eff8";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(X(stats.중앙값), midY - 13); ctx.lineTo(X(stats.중앙값), midY + 13);
  ctx.stroke();

  label(ctx, `최소 ${stats.최소}`, X(lo), midY + 30, "#5d6c86", "center", 9);
  label(ctx, `최대 ${stats.최대}`, X(hi), midY + 30, "#5d6c86", "center", 9);
  label(ctx, `중앙값 ${stats.중앙값}`, X(stats.중앙값), pad.t - 8, "#e9eff8", "center", 9);
  label(ctx, "상자그림 (상자 = 가운데 절반이 모인 곳)", pad.l, h - 6, "#5d6c86", "left", 9);
}

// ════════════════════════════════════════════════════════════════
//  통계 다이얼로그
// ════════════════════════════════════════════════════════════════
const STAT_COLORS = ["#f5934a", "#58dc8b", "#51a6ff", "#38d6c0", "#f3b13c"];

function wireStats() {
  $("#stats-btn").addEventListener("click", openStats);
  $("#stats-close").addEventListener("click", () => $("#stats-modal").classList.remove("show"));
  $("#stats-modal").addEventListener("click", (e) => {
    if (e.target.id === "stats-modal") $("#stats-modal").classList.remove("show");
  });
  $("#stats-csv-btn").addEventListener("click", async () => {
    try {
      const path = await api.exportGame(ctxGame.getGameId(), "wide");
      ctxGame.toast(path ? `CSV 저장 완료 · ${path}` : "CSV를 내려받았습니다.", "good");
    } catch (err) {
      ctxGame.toast(err.message, "bad");
    }
  });
}

async function openStats() {
  const id = ctxGame.getGameId();
  if (!id) return;
  try {
    statsData = await api.stats(id);
  } catch (err) {
    return ctxGame.toast(err.message, "bad");
  }
  activeTab = 0;
  const s = statsData.요약;
  $("#stats-meta").innerHTML =
    `${s.턴수}턴 기록 · ` +
    (s.잡음켜짐
      ? `시드 <b>${s.시드}</b> - 같은 시드로 다시 돌리면 똑같은 도시가 나옵니다`
      : `시드 없음 - <b>흔들림이 꺼져 있습니다</b>. 새 게임에서 시드를 주면 통계가 살아납니다`);
  renderStatsTabs();
  renderStatsBody();
  renderRefs();
  $("#stats-modal").classList.add("show");
}

function renderStatsTabs() {
  // ※ '지표 사이의 관계'(상관·회귀) 탭은 일부러 두지 않습니다.
  //   상관계수는 제대로 설명하려면 인과·교란·표본크기까지 함께 다뤄야 하는데,
  //   그만한 시간을 쓰느니 평균·표준편차·분포를 확실히 하는 편이 낫다고 판단했습니다.
  let tabs = statsData.지표.map((m, i) =>
    `<button data-i="${i}" class="${i === activeTab ? "on" : ""}">${m.이름}</button>`).join("");
  // 공정능력 탭은 규격이 정의된 프로젝트(dkYield99)에서만 나타납니다.
  if (statsData.품질) {
    tabs += `<button data-i="qual" class="${activeTab === "qual" ? "on" : ""}">품질 · 공정능력</button>`;
  }
  // 턴별 원본을 컬럼 하나 빠짐없이 한 시트로 - 엑셀에서 열 것과 똑같은 표입니다.
  tabs += `<button data-i="data" class="${activeTab === "data" ? "on" : ""}">🗂 전체 데이터 보기</button>`;
  const host = $("#stats-tabs");
  host.innerHTML = tabs;
  host.querySelectorAll("button").forEach((b) =>
    b.addEventListener("click", () => {
      const v = b.dataset.i;
      activeTab = (v === "qual" || v === "data") ? v : Number(v);
      renderStatsTabs();
      renderStatsBody();
      renderRefs();
    }));
}

function statRow(k, v, unit = "") {
  return `<div class="sv"><span class="k">${k}</span><span class="v">${v}${unit}</span></div>`;
}

function renderStatsBody() {
  const host = $("#stats-body");
  host.innerHTML = "";

  if (activeTab === "qual") return renderQuality(host);
  if (activeTab === "data") return renderAllData(host);

  const metric = statsData.지표[activeTab];
  if (!metric) return;
  const color = STAT_COLORS[activeTab % STAT_COLORS.length];
  const t = metric.기술통계;
  const unit = metric.단위;

  const block = document.createElement("div");
  block.innerHTML = `
    <div class="stat-values">
      ${statRow("개수", t.개수, "개")}
      ${statRow("평균", t.평균, unit)}
      ${statRow("중앙값", t.중앙값, unit)}
      ${statRow("표준편차", t.표준편차, unit)}
      ${statRow("변동계수", t.변동계수, "%")}
      ${statRow("최소", t.최소, unit)}
      ${statRow("최대", t.최대, unit)}
      ${statRow("사분위범위", t.사분위범위, unit)}
    </div>
    <div class="hand-check">
      ✋ <b>직접 확인해 보세요.</b>
      평균 = 모든 값을 더해 ${t.개수}로 나눈 값입니다.
      표준편차는 <b>${t.개수}가 아니라 ${t.개수 - 1}</b>로 나눕니다(자유도).
      엑셀에서는 <code>=AVERAGE(범위)</code> · <code>=STDEV.S(범위)</code>.
    </div>
    <div class="ai-check">
      🤖 <b>이 숫자를 그대로 베끼지 마세요.</b>
      이 화면은 정답이 아니라 <b>맞춰 볼 참고표</b>입니다.
      여러분이 만든 데이터를 <b>직접 코딩해서 계산해 보고</b>, AI에게도 같은 것을 시켜 보세요.
      <b>내 코드 · 이 화면 · AI</b> - 셋이 맞아떨어질 때 비로소 그 숫자를 믿을 수 있습니다.
      AI는 모르는 것을 모른다고 말하지 않기 때문입니다.
    </div>`;
  host.appendChild(block);

  const grid = document.createElement("div");
  grid.className = "chart-grid";
  host.appendChild(grid);

  const boxA = document.createElement("div"); boxA.className = "chart-box"; grid.appendChild(boxA);
  const boxB = document.createElement("div"); boxB.className = "chart-box"; grid.appendChild(boxB);
  drawHistogram(boxA, metric.히스토그램, color);
  drawBox(boxB, t, color);

  const boxC = document.createElement("div"); boxC.className = "chart-box wide"; host.appendChild(boxC);
  drawControlChart(boxC, metric.값, metric.턴, metric.관리도, color);

  // ★ 위 그래프를 만든 숫자 그대로 - 엑셀 모습으로
  const rows = metric.턴.map((t, i) => ({ 턴: t, [metric.이름]: metric.값[i] }));
  renderSheet(host, `위 그래프의 원본 숫자 - ${metric.이름}`,
              ["턴", metric.이름], rows, { highlight: metric.이름 });
  renderDataPath(host);

  if (metric.신뢰구간) {
    const ci = metric.신뢰구간;
    const div = document.createElement("div");
    div.className = "ci-band";
    div.innerHTML =
      `<b>95% 신뢰구간</b> ${ci.하한} ~ ${ci.상한}${unit}
       <span class="ci-margin">(오차범위 ±${ci.오차범위}${unit})</span>`;
    host.appendChild(div);
  }

  const notes = document.createElement("div");
  notes.className = "interpret";
  notes.innerHTML = `<h4>수치 해석</h4>` +
    metric.해석.map((line) => `<p>${highlight(line)}</p>`).join("");
  host.appendChild(notes);

  renderMetricCode(host, metric);
}

/** 지금 보고 있는 지표를 그대로 계산하는 파이썬 파일 (12·13주) */
function renderMetricCode(host, metric) {
  const t = metric.기술통계;
  const key = metric.키;
  const filename = `stat_${key}.py`;
  const code =
`${pyHeader(`${metric.이름} - 평균 · 표준편차 · 변동계수 · 도수분포표`, filename)}
CSV = Path(r"${csvPathOf()}")
COLUMN = "${key}"

# 화면에 나와 있던 값 - 내 계산과 맞춰 볼 참고표입니다 (정답표가 아닙니다)
SCREEN = {
    "개수": ${t.개수},
    "평균": ${t.평균},
    "표준편차": ${t.표준편차},
    "변동계수": ${t.변동계수},
}
${PY_LOADER}
# ═══ ✏️ 여기부터가 여러분이 만드는 부분입니다 ═══════════════

def my_mean(values):
    """평균 = 모두 더해서 개수로 나눈다."""
    return sum(values) / len(values)


def my_stdev(values):
    """표준편차 - n 이 아니라 n-1 로 나눕니다 (자유도)."""
    m = my_mean(values)
    var = sum((v - m) ** 2 for v in values) / (len(values) - 1)
    return var ** 0.5


def my_cv(values):
    """변동계수(%) = 표준편차 ÷ 평균 × 100.
       단위가 다른 두 지표 중 무엇이 더 불안정한지 비교할 때 씁니다."""
    return my_stdev(values) / my_mean(values) * 100

# ═══ 여기까지 ═══════════════════════════════════════════════
${PY_COMPARE}

def histogram(values, bins=8):
    """도수분포표 - 구간을 나눠 세는 것이 전부입니다. (13주)"""
    lo, hi = min(values), max(values)
    width = (hi - lo) / bins or 1
    # 경계는 한 번만 계산해 둡니다. lo+3*w+w 와 lo+4*w 는 소수점 아래에서
    # 값이 살짝 달라서, 그대로 찍으면 앞 칸의 끝과 뒷 칸의 시작이 어긋납니다.
    edges = [lo + width * i for i in range(bins + 1)]
    counts = [0] * bins
    for v in values:
        i = min(int((v - lo) / width), bins - 1)
        counts[i] += 1
    return edges, counts


column_used, values = load_column(CSV, COLUMN)
print(f"파일: {CSV.name}")
print(f"컬럼: {column_used}   {len(values)}개\\n")

mine = {
    "개수": len(values),
    "평균": my_mean(values),
    "표준편차": my_stdev(values),
    "변동계수": my_cv(values),
}
compare(mine, SCREEN)

print("\\n도수분포표 - 화면의 히스토그램과 모양이 같아야 합니다")
edges, counts = histogram(values)
for i, n in enumerate(counts):
    print(f"{edges[i]:8.1f} ~ {edges[i + 1]:8.1f}  {'■' * n:<20} {n}")
`;

  renderCodeCard(host, {
    title: `${metric.이름}${particle(metric.이름, "을", "를")} 직접 계산하는 코드`,
    filename, code,
    why: "위 표와 그래프를 만든 계산을 <b>그대로</b> 담았습니다. " +
         "세 함수를 직접 채워 보고, 화면 값과 같은지 파일이 스스로 확인하게 하세요.",
  });
}

/** 🗂 전체 데이터 - 턴별 원본을 컬럼 하나 빠짐없이 한 시트로 */
function renderAllData(host) {
  const 표 = statsData.표;
  if (!표 || !표.행 || !표.행.length) {
    host.innerHTML = `<div class="hand-check">아직 기록이 없습니다. 몇 턴 더 진행해 보세요.</div>`;
    return;
  }
  // 값이 한 번도 안 채워진 컬럼은 표를 넓히기만 하므로 뺍니다.
  const columns = 표.컬럼.filter((c) =>
    표.행.some((r) => r[c] !== undefined && r[c] !== null && r[c] !== ""));

  const intro = document.createElement("div");
  intro.className = "hand-check";
  intro.innerHTML =
    `✋ <b>이것이 원본입니다.</b> 지표 탭의 그래프와 숫자는 전부 이 표에서 나왔습니다.
     <b>한 줄이 한 턴</b>이고, 컬럼 ${columns.length}개가 그 턴의 모든 지표입니다.
     엑셀에서 CSV를 열면 <b>글자 하나까지 이 표와 같습니다.</b>`;
  host.appendChild(intro);

  renderSheet(host, "턴별 전체 기록 (원본)", columns, 표.행, { limit: 20 });
  renderDataPath(host);

  const filename = "explore_data.py";
  const code =
`${pyHeader("전체 데이터 살펴보기 - 어떤 컬럼이 있고, 각 컬럼이 어떤 값인지", filename)}
CSV = Path(r"${csvPathOf()}")


def load_rows(path):
    if not path.exists():
        raise SystemExit(
            f"CSV 를 찾지 못했습니다:\\n  {path}\\n\\n"
            "게임 화면에서 [📥 엑셀용 CSV] 를 먼저 눌러 주세요.")
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def as_number(text):
    """숫자로 읽히면 숫자로, 아니면 None."""
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


rows = load_rows(CSV)
print(f"파일: {CSV.name}")
print(f"{len(rows)}행 × {len(rows[0])}열\\n")

print(f"{'컬럼':<16}{'개수':>6}{'최소':>12}{'평균':>12}{'최대':>12}")
print("-" * 58)
for name in rows[0]:
    nums = [n for n in (as_number(r[name]) for r in rows) if n is not None]
    if not nums:
        print(f"{name:<16}{'-':>6}{'(숫자 아님)':>38}")
        continue
    mean = sum(nums) / len(nums)
    print(f"{name:<16}{len(nums):>6}{min(nums):>12.2f}{mean:>12.2f}{max(nums):>12.2f}")

print("\\n※ 컬럼이 이렇게 많은 이유: 분석할 것이 많아야 통계를 배울 수 있기 때문입니다.")
print("   이 중 어떤 것이 서로 맞물려 있는지는 여러분이 찾아야 합니다.")
`;

  renderCodeCard(host, {
    title: "전체 데이터를 훑어보는 코드",
    filename, code,
    why: "컬럼이 많을 때 <b>가장 먼저 하는 일</b>입니다 - 어떤 컬럼이 있고, " +
         "각각 몇 개이고, 어느 범위인지 한눈에 봅니다.",
  });
}

/** 품질 탭 - 공정능력(Cp/Cpk)과 부분군 관리도 */
function renderQuality(host) {
  const q = statsData.품질;
  if (!q) return;
  const cap = q.공정능력;

  if (cap) {
    const 등급 = cap.Cpk >= 1.33 ? "good" : cap.Cpk >= 1.0 ? "warn" : "bad";
    host.innerHTML = `
      <div class="stat-values">
        ${statRow("평균", cap.평균, q.단위)}
        ${statRow("표준편차", cap.표준편차, q.단위)}
        ${statRow("규격하한", cap.규격하한 ?? "-", q.단위)}
        ${statRow("Cp", cap.Cp ?? "-")}
        ${statRow("Cpk", cap.Cpk)}
        ${statRow("규격이탈률", cap.규격이탈률, "%")}
        ${statRow("백만개당", cap.백만개당.toLocaleString(), "개")}
      </div>
      <div class="ci-band">
        <b>공정능력지수 Cpk = ${cap.Cpk}</b>
        <span class="badge ${등급}">${
          cap.Cpk >= 1.33 ? "아주 좋음" : cap.Cpk >= 1.0 ? "보통" : "부족"}</span>
        <span class="ci-margin">1.33 이상이면 대부분의 고객이 요구하는 수준입니다</span>
      </div>`;
  } else {
    host.innerHTML = "";
  }

  // 부분군 관리도 (X-bar / R)
  const ch = q.관리도;
  if (ch) {
    const note = document.createElement("div");
    note.className = "hand-check";
    note.innerHTML =
      `✋ <b>한 번에 ${ch.부분군크기}개씩 재는 이유.</b>
       한 개만 재면 '값이 튄 것'인지 '공정이 변한 것'인지 알 수 없습니다.
       묶어서 재야 <b>평균이 움직였는지</b>(X-bar)와
       <b>흔들림이 커졌는지</b>(R)를 따로 볼 수 있습니다.`;
    host.appendChild(note);

    const boxA = document.createElement("div");
    boxA.className = "chart-box wide";
    host.appendChild(boxA);
    drawControlChart(boxA, ch.부분군평균,
      ch.부분군평균.map((_, i) => i + 1),
      { 중심선: ch.Xbar중심선, 관리상한: ch.Xbar관리상한,
        관리하한: ch.Xbar관리하한, 표준편차: 0, 이탈점: ch.Xbar이탈 },
      "#2fe0c8");

    const boxB = document.createElement("div");
    boxB.className = "chart-box wide";
    host.appendChild(boxB);
    drawControlChart(boxB, ch.부분군범위,
      ch.부분군범위.map((_, i) => i + 1),
      { 중심선: ch.R중심선, 관리상한: ch.R관리상한,
        관리하한: ch.R관리하한, 표준편차: 0, 이탈점: ch.R이탈 },
      "#ffb049");

    // ★ 위 두 관리도를 만든 숫자 - 엑셀 모습으로
    renderSheet(host, "위 관리도의 원본 숫자 - 부분군별",
      ["부분군", "평균", "범위"],
      ch.부분군평균.map((m, i) => ({ 부분군: i + 1, 평균: m, 범위: ch.부분군범위[i] })),
      { highlight: "평균" });
  }

  const notes = document.createElement("div");
  notes.className = "interpret";
  notes.innerHTML = `<h4>수치 해석</h4>`
    + q.해석.map((l) => `<p>${highlight(l)}</p>`).join("");
  host.appendChild(notes);
  renderDataPath(host);

  // 관리도·Cp 는 새 통계가 아닙니다 - 평균과 표준편차로 만들어집니다.
  const cap2 = q.공정능력;
  if (cap2) {
    const filename = "stat_quality.py";
    const code =
`${pyHeader("관리도와 공정능력 - 평균과 표준편차만으로 만들어집니다", filename)}
CSV = Path(r"${csvPathOf()}")
COLUMN = "${q.키 || "순도"}"

LSL = ${cap2.규격하한 ?? "None"}      # 규격하한
USL = ${cap2.규격상한 ?? "None"}      # 규격상한

SCREEN = {"평균": ${cap2.평균}, "표준편차": ${cap2.표준편차}}
${PY_LOADER}

def my_mean(values):
    return sum(values) / len(values)


def my_stdev(values):
    m = my_mean(values)
    return (sum((v - m) ** 2 for v in values) / (len(values) - 1)) ** 0.5

${PY_COMPARE}

column_used, values = load_column(CSV, COLUMN)
mean, sd = my_mean(values), my_stdev(values)
compare({"평균": mean, "표준편차": sd}, SCREEN)

# ── 관리도의 선은 이게 전부입니다 ────────────────────────────
print(f"\\n관리 상한 = 평균 + 3 x 표준편차 = {mean + 3 * sd:.3f}")
print(f"중심선    = 평균                 = {mean:.3f}")
print(f"관리 하한 = 평균 - 3 x 표준편차 = {mean - 3 * sd:.3f}")

밖 = [v for v in values if abs(v - mean) > 3 * sd]
print(f"관리선을 벗어난 값: {len(밖)}개 {밖 if 밖 else ''}")

# ── 공정능력도 표준편차 하나에서 나옵니다 ────────────────────
if LSL is not None and USL is not None:
    Cp = (USL - LSL) / (6 * sd)
    Cpk = min(USL - mean, mean - LSL) / (3 * sd)
    print(f"\\nCp  = (규격상한 - 규격하한) / (6 x 표준편차) = {Cp:.3f}")
    print(f"Cpk = 가까운 쪽 여유 / (3 x 표준편차)        = {Cpk:.3f}")
    print("Cpk 가 Cp 보다 작으면, 퍼짐이 아니라 '평균이 한쪽으로 치우친' 것입니다.")
`;
    renderCodeCard(host, {
      title: "관리도·Cp/Cpk 를 직접 계산하는 코드",
      filename, code,
      why: "관리선은 <b>평균 ± 3×표준편차</b>이고 Cp 는 <b>규격폭 ÷ (6×표준편차)</b>입니다. " +
           "새로 배울 통계가 아니라, 12주에 만든 표준편차의 응용입니다.",
    });
  }
}

/** ★ 나 ⚠️ 로 시작하는 문장은 눈에 띄게 */
function highlight(line) {
  if (line.startsWith("★")) return `<span class="hi-star">${line}</span>`;
  if (line.startsWith("⚠️")) return `<span class="hi-warn">${line}</span>`;
  return line;
}

function renderRefs() {
  // 지금 보고 있는 탭에 맞는 문헌만 골라 보여줍니다.
  const groups = activeTab === "qual"
    ? ["공정능력", "관리도", "측정오차"]
    : ["기술통계", "분포", "관리도", "신뢰구간"];
  const refs = statsData.근거;
  $("#stats-refs").innerHTML = groups
    .filter((g) => refs[g])
    .map((g) => `
      <div class="ref-group">
        <div class="ref-group-name">${g}</div>
        ${refs[g].map((r) => `
          <div class="ref">
            <a href="${r.url}" target="_blank" rel="noopener">${r.제목}</a>
            <div class="ref-author">${r.저자}</div>
            <div class="ref-desc">${r.설명}</div>
            <div class="ref-url">${r.url}</div>
          </div>`).join("")}
      </div>`).join("");
}

// ════════════════════════════════════════════════════════════════
//  저장 · 불러오기 다이얼로그
// ════════════════════════════════════════════════════════════════
function wireSaves() {
  $("#saves-btn").addEventListener("click", openSaves);
  $("#saves-close").addEventListener("click", () => $("#saves-modal").classList.remove("show"));
  $("#saves-modal").addEventListener("click", (e) => {
    if (e.target.id === "saves-modal") $("#saves-modal").classList.remove("show");
  });

  $("#save-now-btn").addEventListener("click", async () => {
    try {
      const r = await api.save(ctxGame.getGameId(), {
        이름: $("#save-name").value,
        라벨: $("#save-label").value,
        메모: $("#save-memo").value,
      });
      $("#save-name").value = "";
      $("#save-memo").value = "";
      ctxGame.toast(r.메시지, "good");
      renderSaveList(r.목록);
    } catch (err) { ctxGame.toast(err.message, "bad"); }
  });

  document.querySelectorAll("[data-export]").forEach((b) =>
    b.addEventListener("click", async () => {
      try {
        const path = await api.exportSaves(b.dataset.export);
        ctxGame.toast(path ? `CSV 저장 완료 · ${path}` : "CSV를 내려받았습니다.", "good");
      } catch (err) { ctxGame.toast(err.message, "bad"); }
    }));

  $("#compare-btn").addEventListener("click", compareGroups);

  $("#samples-btn").addEventListener("click", async () => {
    const btn = $("#samples-btn");
    btn.disabled = true;
    btn.textContent = "🧪 만드는 중...";
    try {
      const r = await api.makeSamples(4);
      ctxGame.toast(r.메시지, "good");
      renderSaveList(r.목록);
      $("#compare-result").innerHTML = `<div class="cmp-hint">
        <b>잘 운영한 판 ${r.성공}개</b> (${r.운영방식.성공.join(" · ")})<br />
        <b>잘못 운영한 판 ${r.실패}개</b> (${r.운영방식.실패.join(" · ")})<br /><br />
        같은 운영 방식이라도 시드가 다르면 결과가 조금씩 다릅니다.
        그 '조금씩 다름'이 통계로 다룰 대상입니다.<br />
        이제 <b>⚖ 성공 vs 실패 비교</b> 를 눌러 보세요.
      </div>`;
    } catch (err) {
      ctxGame.toast(err.message, "bad");
    } finally {
      btn.disabled = false;
      btn.textContent = "🧪 예시 데이터 만들기";
    }
  });
}

async function openSaves() {
  try {
    renderSaveList((await api.saves()).목록);
    $("#saves-modal").classList.add("show");
  } catch (err) { ctxGame.toast(err.message, "bad"); }
}

function renderSaveList(list) {
  const host = $("#save-list");
  if (!list.length) {
    host.innerHTML = `<div class="save-empty">
      아직 저장한 판이 없습니다.<br />
      판을 여러 개 남기고 <b>성공 / 실패</b> 라벨을 붙이면,
      두 무리를 통계로 비교할 수 있습니다.</div>`;
    return;
  }
  host.innerHTML = list.map((s) => {
    const q = s.요약;
    return `<div class="save-row" data-id="${s.저장아이디}">
      <div class="save-main">
        <div class="save-name">${s.이름}
          <span class="save-badge ${s.라벨}">${s.라벨}</span>
        </div>
        <div class="save-sub">${s.턴}턴 · 시드 ${s.시드 ?? "없음"} · ${s.저장시각}</div>
        <div class="save-file" title="이 판의 데이터가 저장된 파일입니다">
          📄 lab\\data\\${s.이름}.csv
        </div>
        ${s.메모 ? `<div class="save-memo">${s.메모}</div>` : ""}
        <div class="save-figs">
          예산 ${q.예산} · 세수 ${q.세수} · 인구 ${q.인구} ·
          만족 ${q.주민만족} · 건강 ${q.도시건강도} · Lv.${q.도시레벨}
        </div>
      </div>
      <div class="save-acts">
        <select data-act="label">
          <option ${s.라벨 === "미정" ? "selected" : ""}>미정</option>
          <option ${s.라벨 === "성공" ? "selected" : ""}>성공</option>
          <option ${s.라벨 === "실패" ? "selected" : ""}>실패</option>
        </select>
        <button data-act="load" class="tool-btn">이어하기</button>
        <button data-act="del" class="tool-btn danger">삭제</button>
      </div>
    </div>`;
  }).join("");

  host.querySelectorAll(".save-row").forEach((row) => {
    const id = row.dataset.id;
    row.querySelector('[data-act="label"]').addEventListener("change", async (e) => {
      try {
        const r = await api.editSave(id, { 라벨: e.target.value });
        ctxGame.toast(`라벨을 '${e.target.value}' 로 바꿨습니다.`, "good");
        renderSaveList(r.목록);
      } catch (err) { ctxGame.toast(err.message, "bad"); }
    });
    row.querySelector('[data-act="load"]').addEventListener("click", async () => {
      try {
        const r = await api.loadSave(id);
        ctxGame.toast(r.메시지, "good");
        $("#saves-modal").classList.remove("show");
        ctxGame.onLoaded(r.gameId, r.state);
      } catch (err) { ctxGame.toast(err.message, "bad"); }
    });
    row.querySelector('[data-act="del"]').addEventListener("click", async () => {
      try {
        const r = await api.deleteSave(id);
        renderSaveList(r.목록);
      } catch (err) { ctxGame.toast(err.message, "bad"); }
    });
  });
}

async function compareGroups() {
  const host = $("#compare-result");
  host.innerHTML = `<div class="cmp-hint">비교하는 중...</div>`;
  try {
    const r = await api.compare("성공", "실패");
    const rows = r.결과.map((x) => {
      const c = x.비교;
      return `<tr class="${c.유의함 ? "sig" : "nosig"}">
        <td class="k">${x.지표}</td>
        <td>${c.평균A}<i>${x.단위}</i></td>
        <td>${c.평균B}<i>${x.단위}</i></td>
        <td class="gap">${c.평균차 > 0 ? "+" : ""}${c.평균차}</td>
        <td>${c.t값}</td>
        <td>${c["임계값(95%)"]}</td>
        <td>${c.효과크기}</td>
        <td><span class="badge ${c.유의함 ? "good" : "warn"}">
          ${c.유의함 ? "뚜렷이 다름" : "판단 보류"}</span></td>
      </tr>`;
    }).join("");

    host.innerHTML = `
      <div class="cmp-head">
        <b>${r.무리.A} ${r.결과[0].비교.개수A}판</b>
        <i>vs</i>
        <b>${r.무리.B} ${r.결과[0].비교.개수B}판</b>
        <span class="cmp-gap">지표 ${r.결과.length}개로 비교</span>
      </div>
      <table class="cmp-table">
        <thead><tr>
          <th>지표</th><th>${r.무리.A} 평균</th><th>${r.무리.B} 평균</th>
          <th>차이</th><th>t</th><th>임계값</th><th>d</th><th>판정</th>
        </tr></thead>
        <tbody>${rows}</tbody>
      </table>
      <div class="interpret">${r.총평.map((l) => `<p>${highlight(l)}</p>`).join("")}</div>
      <div class="cmp-refs">${r.근거.map((x) =>
        `<a href="${x.url}" target="_blank" rel="noopener">${x.제목}</a>`).join("")}</div>`;
  } catch (err) {
    host.innerHTML = `<div class="cmp-hint">${err.message}</div>`;
  }
}
