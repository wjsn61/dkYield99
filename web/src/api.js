// ════════════════════════════════════════════════════════════════
//  서버와 대화하는 부분 (Python 권위형 서버에 액션을 보냄)
//
//  계산은 전부 서버(파이썬)가 합니다. 여기서는 물어보고 받아 그릴 뿐입니다.
// ════════════════════════════════════════════════════════════════
async function jget(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(await readError(r));
  return r.json();
}
async function jpost(url, body) {
  const r = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : null,
  });
  if (!r.ok) throw new Error(await readError(r));
  return r.json();
}
async function jsend(method, url, body) {
  const r = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : null,
  });
  if (!r.ok) throw new Error(await readError(r));
  return r.json();
}

// 서버가 보내는 한국어 안내문을 그대로 꺼냅니다.
async function readError(response) {
  try {
    const data = await response.json();
    return data.detail || JSON.stringify(data);
  } catch {
    return `서버 오류 (${response.status})`;
  }
}

// CSV 를 내려받습니다. 서버가 lab/data 에도 사본을 남기므로 그 경로를 함께 돌려줍니다.
async function download(url, fallbackName) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(await readError(r));

  const hex = r.headers.get("X-Saved-Path") || "";
  let savedPath = "";
  if (hex) {
    try {
      const bytes = new Uint8Array(hex.match(/.{1,2}/g).map((h) => parseInt(h, 16)));
      savedPath = new TextDecoder("utf-8").decode(bytes);
    } catch { /* 경로 안내는 없어도 내려받기는 됩니다 */ }
  }

  const blob = await r.blob();
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = fallbackName;
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(link.href), 1000);
  return savedPath;
}

export const api = {
  scenario: () => jget("/api/scenario"),
  cards: () => jget("/api/cards"),
  newGame: (options) => jpost("/api/game/new", options || {}),
  enact: (id, cardId) => jpost(`/api/game/${id}/card`, { cardId }),
  endTurn: (id) => jpost(`/api/game/${id}/end_turn`),

  // ── 통계 ──────────────────────────────────────────────────────
  stats: (id) => jget(`/api/game/${id}/stats`),
  compare: (a, b, key) =>
    jget(`/api/saves/compare?label_a=${encodeURIComponent(a)}` +
         `&label_b=${encodeURIComponent(b)}&key=${encodeURIComponent(key)}`),

  // ── 저장 · 불러오기 ───────────────────────────────────────────
  save: (id, body) => jpost(`/api/game/${id}/save`, body),
  saves: () => jget("/api/saves"),
  makeSamples: (n = 4) => jpost(`/api/saves/samples?count_each=${n}`),
  loadSave: (saveId) => jpost(`/api/saves/${saveId}/load`),
  editSave: (saveId, body) => jsend("PATCH", `/api/saves/${saveId}`, body),
  deleteSave: (saveId) => jsend("DELETE", `/api/saves/${saveId}`),

  // ── 데이터 내려받기 ───────────────────────────────────────────
  exportGame: (id, format = "wide") =>
    download(`/api/game/${id}/export.csv?format=${format}`, `dkyield_${id}_${format}.csv`),
  exportSaves: (format = "wide") =>
    download(`/api/saves/export.csv?format=${format}`, `dkyield_모음_${format}.csv`),
};
