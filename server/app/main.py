# ════════════════════════════════════════════════════════════════════
#  dkYield99% 게임 서버 (main.py)  -  Python 권위형 서버
#
#  - 공정 상태/규칙/계산은 모두 이 서버(엔진)가 가집니다.
#  - 프론트(web/)는 화면만 그리고, 액션을 이 서버에 보냅니다.
#  - 실행:  server 폴더에서  python run.py   →  http://127.0.0.1:5000
# ════════════════════════════════════════════════════════════════════
from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.engine.process_engine import (
    new_plant,
    enact_card,
    end_turn,
    evaluate_ending,
)
from app.cards import load_cards
from app.persistence import (
    init_db, save_game, load_game, cleanup_old_games,
    create_save, list_saves, load_save, save_meta,
    update_save, delete_save, load_saves_bulk, LABELS,
)
from app import export_csv
from app import statistics_lab as SL

PROJECT_ROOT = Path(__file__).resolve().parents[2]   # .../dkYield99
WEB_DIR = PROJECT_ROOT / "web"
LAB_DATA_DIR = PROJECT_ROOT / "lab" / "data"         # 통계 실습이 CSV를 찾는 곳

CARDS = load_cards()
CARD_BY_ID = {c["아이디"]: c for c in CARDS}

# 기록에 담을 컬럼 (지표 설명서가 정합니다)
SNAPSHOT_COLUMNS = export_csv.wide_columns()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()   # 서버 시작 시 DB 초기화
    yield


app = FastAPI(title="dkYield99%", version="1.1.0", lifespan=lifespan)


# ── 요청 모델 ────────────────────────────────────────────────────────
class CardAction(BaseModel):
    cardId: str


class NewGameOptions(BaseModel):
    """새 게임 설정. 아무것도 안 보내도 되게 전부 선택 사항입니다."""
    seed: int | None = None


class SaveRequest(BaseModel):
    이름: str = ""
    라벨: str = "미정"
    메모: str = ""


class SaveUpdate(BaseModel):
    이름: str | None = None
    라벨: str | None = None
    메모: str | None = None


# ── 도우미 ───────────────────────────────────────────────────────────
def snapshot(p: dict) -> dict:
    """
    이번 달의 모든 지표를 한 줄로 남깁니다.

    예전에는 6개만 남겼지만, 통계 실습을 하려면 분석할 변수가 많아야 합니다.
    (차트는 필요한 컬럼만 골라 쓰므로 컬럼이 늘어도 문제없습니다)
    """
    row = {"턴": p["턴"]}
    for column in SNAPSHOT_COLUMNS:
        if column == "턴" or column not in p:
            continue
        value = p[column]
        if isinstance(value, float):
            value = round(value, 3)
        elif isinstance(value, (list, dict)):
            continue                    # 목록형(순도샘플 등)은 아래에서 따로
        row[column] = value

    # 순도 부분군 5개는 관리도의 재료라 요약값으로 함께 남깁니다
    samples = p.get("순도샘플")
    if isinstance(samples, list) and samples:
        row["순도샘플평균"] = round(sum(samples) / len(samples), 3)
        row["순도샘플범위"] = round(max(samples) - min(samples), 3)
        for i, v in enumerate(samples, start=1):
            row[f"순도샘플{i}"] = v
    return row


def to_client(game: dict) -> dict:
    p = game["plant"]
    out = {k: v for k, v in p.items() if k not in ("설비목록", "연구중", "기록")}
    out["설비목록"] = [s["아이디"] for s in p["설비목록"]]
    out["연구중"] = [
        {"아이디": r["카드"]["아이디"], "이름": r["카드"]["이름"], "남은턴": r["남은턴"]}
        for r in p["연구중"]
    ]
    out["기록"] = p["기록"][-40:]
    out["추이"] = game["history"]
    return out


def get_game(game_id: str) -> dict:
    g = load_game(game_id)
    if g is None:
        raise HTTPException(status_code=404, detail="게임을 찾을 수 없습니다.")
    return g


def csv_response(rows: list[dict], filename: str) -> Response:
    """CSV 를 내려받게 하고, 동시에 lab/data 에도 사본을 남깁니다."""
    text = export_csv.to_csv_text(rows)
    saved_to = ""
    try:
        saved_to = str(export_csv.write_csv(LAB_DATA_DIR / filename, rows))
    except Exception:
        pass
    return Response(
        content=text.encode("utf-8-sig"),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "X-Saved-Path": saved_to.encode("utf-8").hex(),
            "Access-Control-Expose-Headers": "X-Saved-Path",
        },
    )


# ════════════════════════════════════════════════════════════════════
#  API - 게임 진행
# ════════════════════════════════════════════════════════════════════
@app.get("/api/cards")
def list_cards_api():
    return JSONResponse(CARDS)


@app.get("/api/scenario")
def scenario():
    return {
        "이름": "Ester-1 Plant - 에스터 생산 플랜트",
        "반응": "초산 + 에탄올 ⇌ 초산에틸 + 물",
        "설명": "수율 70%, 순도 94%의 불안정한 첫 상업 플랜트. 12개월 안에 수율 90%·순도 98%·누적이익 150억을 달성하라.",
        "초기상태": {
            "예산": 100, "월이익": 12, "생산량": 1000,
            "수율": 70, "순도": 94, "안전지수": 75, "환경지수": 68,
        },
        "목표": ["12개월 내 수율 90% 이상", "제품 순도 98% 이상", "누적 이익 150억 이상",
                 "안전지수 70 이상", "환경지수 65 이상"],
    }


@app.post("/api/game/new")
def create_game(options: NewGameOptions | None = None):
    """
    새 게임을 시작합니다.

    ※ options 를 Optional 로 받는 것이 중요합니다.
       프론트가 본문 없이 POST 하는 경우가 있어서, 필수로 받으면 422 가 납니다.
    """
    options = options or NewGameOptions()
    seed = options.seed
    if seed is None:
        env_seed = os.environ.get("DK_SEED")
        if env_seed and env_seed.strip().lstrip("-").isdigit():
            seed = int(env_seed)

    plant = new_plant(seed=seed)
    game_id = uuid.uuid4().hex[:12]
    game = {"plant": plant, "history": [snapshot(plant)], "actions": []}
    cleanup_old_games()
    save_game(game_id, game)
    return {"gameId": game_id, "state": to_client(game)}


@app.get("/api/game/{game_id}")
def read_state(game_id: str):
    return {"state": to_client(get_game(game_id))}


@app.post("/api/game/{game_id}/card")
def do_card(game_id: str, action: CardAction):
    game = get_game(game_id)
    card = CARD_BY_ID.get(action.cardId)
    if card is None:
        raise HTTPException(status_code=400, detail="알 수 없는 카드입니다.")
    ok, message = enact_card(game["plant"], card)
    game.setdefault("actions", []).append(
        {"턴": game["plant"]["턴"], "아이디": action.cardId, "성공": ok}
    )
    save_game(game_id, game)
    return {"ok": ok, "message": message, "state": to_client(game)}


@app.post("/api/game/{game_id}/end_turn")
def do_end_turn(game_id: str):
    game = get_game(game_id)
    plant = game["plant"]

    end_turn(plant)
    game["history"].append(snapshot(plant))

    ended = plant["턴"] > plant["최대턴"]
    ending = None
    if ended:
        grade, name = evaluate_ending(plant)
        ending = {
            "등급": grade, "이름": name,
            "누적이익": plant["누적이익"], "수율": plant["수율"],
            "순도": plant["순도"], "안전지수": plant["안전지수"], "환경지수": plant["환경지수"],
        }
    save_game(game_id, game)
    return {"state": to_client(game), "ended": ended, "ending": ending}


# ════════════════════════════════════════════════════════════════════
#  API - 저장하기 · 불러오기  (★ 통계 실습의 재료를 모으는 곳)
# ════════════════════════════════════════════════════════════════════
@app.get("/api/labels")
def labels():
    return {"라벨": list(LABELS)}


@app.post("/api/game/{game_id}/save")
def save_slot(game_id: str, body: SaveRequest | None = None):
    """
    지금 상태를 이름 붙여 보관합니다.

    라벨('성공' / '실패' / '미정')이 중요합니다.
    나중에 잘 운전한 판과 잘못 운전한 판을 무리지어 비교할 때 쓰는 그룹 이름입니다.
    """
    body = body or SaveRequest()
    game = get_game(game_id)
    plant = game["plant"]
    name = body.이름.strip() or f"{plant['턴']}개월차 · 수율 {plant['수율']}%"
    save_id = create_save(game_id, game, name, body.라벨, body.메모)

    # ★ 저장한 이름과 '같은 이름'으로 CSV 도 함께 남깁니다.
    #   "고순도 운전 1차" 로 저장하면 lab/data/고순도 운전 1차.csv 가 생깁니다.
    #   나중에 "그 판 데이터가 어느 파일이지?" 를 헤매지 않게 하기 위해서입니다.
    csv_path = ""
    try:
        rows = export_csv.rows_wide(game)
        if rows:
            filename = export_csv.safe_filename(name) + ".csv"
            csv_path = str(export_csv.write_csv(LAB_DATA_DIR / filename, rows))
    except Exception:
        pass                    # CSV 를 못 써도 저장 자체는 성공해야 합니다

    message = f"'{name}' 으로 보관했습니다."
    if csv_path:
        message += f"  ·  데이터: {csv_path}"
    return {"저장아이디": save_id, "메시지": message,
            "CSV경로": csv_path, "목록": list_saves()}


@app.get("/api/saves")
def get_saves():
    return {"목록": list_saves()}


@app.post("/api/saves/samples")
def make_samples(count_each: int = 4):
    """★ 잘 운전한 공장과 잘못 운전한 공장을 자동으로 만들어 보관합니다."""
    from app.sample_runs import build_samples, GOOD_PLANS, BAD_PLANS

    count_each = max(1, min(10, count_each))
    made = build_samples(count_each=count_each)
    return {
        "성공": len(made["성공"]), "실패": len(made["실패"]),
        "메시지": f"성공 {len(made['성공'])}판, 실패 {len(made['실패'])}판을 만들었습니다. "
                  "이제 '성공 vs 실패 비교'를 눌러 보세요.",
        "운영방식": {"성공": list(GOOD_PLANS), "실패": list(BAD_PLANS)},
        "목록": list_saves(),
    }


@app.post("/api/saves/{save_id}/load")
def load_slot(save_id: str):
    """
    보관한 판을 불러와 '이어서' 운전합니다.

    원본은 그대로 두고 복사본으로 이어갑니다.
    같은 지점에서 여러 갈래로 실험해 볼 수 있습니다.
      → "여기서 온도를 올렸다면?" vs "안 올렸다면?"  (14주 DOE)
    """
    game = load_save(save_id)
    if game is None:
        raise HTTPException(status_code=404, detail="보관한 판을 찾을 수 없습니다.")
    meta = save_meta(save_id) or {}
    game_id = uuid.uuid4().hex[:12]
    save_game(game_id, game)
    return {"gameId": game_id, "state": to_client(game),
            "메시지": f"'{meta.get('이름', '')}' 에서 이어서 시작합니다."}


@app.patch("/api/saves/{save_id}")
def edit_save(save_id: str, body: SaveUpdate):
    ok = update_save(save_id, body.이름, body.라벨, body.메모)
    if not ok:
        raise HTTPException(status_code=404, detail="보관한 판을 찾을 수 없습니다.")
    return {"ok": True, "목록": list_saves()}


@app.delete("/api/saves/{save_id}")
def remove_save(save_id: str):
    if not delete_save(save_id):
        raise HTTPException(status_code=404, detail="보관한 판을 찾을 수 없습니다.")
    return {"ok": True, "목록": list_saves()}


# ════════════════════════════════════════════════════════════════════
#  API - 데이터 내보내기
# ════════════════════════════════════════════════════════════════════
@app.get("/api/game/{game_id}/export.csv")
def export_game(game_id: str, format: str = "wide"):
    game = get_game(game_id)
    maker = export_csv.rows_wide if format == "wide" else export_csv.rows_long
    rows = maker(game)
    if not rows:
        raise HTTPException(status_code=400, detail="아직 기록이 없습니다.")
    return csv_response(rows, f"dkyield_{game_id}_{format}.csv")


@app.get("/api/saves/export.csv")
def export_saves(ids: str = "", format: str = "wide", label: str = ""):
    """보관한 여러 판을 한 CSV 로 합쳐서 내려받습니다.  ★ 비교분석의 핵심"""
    if ids.strip():
        wanted = [i.strip() for i in ids.split(",") if i.strip()]
    else:
        wanted = [s["저장아이디"] for s in list_saves()
                  if not label or s["라벨"] == label]
    if not wanted:
        raise HTTPException(status_code=400, detail="내보낼 판이 없습니다. 먼저 저장하세요.")

    saves = load_saves_bulk(wanted)
    if format == "summary":
        rows = export_csv.summary_rows(saves)
        name = "dkyield_판별요약.csv"
    else:
        rows = export_csv.combine(saves, shape=format)
        name = f"dkyield_모음_{format}.csv"
    if not rows:
        raise HTTPException(status_code=400, detail="내보낼 기록이 없습니다.")
    return csv_response(rows, name)


# ════════════════════════════════════════════════════════════════════
#  API - 통계 지표 보기  (★ 9주 도입부에서 쓰는 화면)
# ════════════════════════════════════════════════════════════════════
STAT_TARGETS = [
    ("순도_분석", "제품 순도(분석값)", "%"),
    ("수율", "수율", "%"),
    ("월이익", "월 이익", "억"),
    ("안전지수", "안전지수", "점"),
    ("에너지비", "에너지비", "억"),
]

def build_quality(column):
    """
    규격이 정의된 지표 하나로 공정능력(Cp·Cpk)과 X-bar R 관리도를 만듭니다.

    ★ 새 통계가 아닙니다. 평균과 표준편차로 만들어집니다 (14주).
      규격하한·부분군 크기는 indicators_data.py 에 적혀 있는 값을 그대로 씁니다.
    """
    from app.indicators.indicators_data import INDICATORS

    for ind in INDICATORS:
        chart = ind.get("관리도") or {}
        lsl, usl = chart.get("규격하한"), chart.get("규격상한")
        if lsl is None and usl is None:
            continue
        key = ind.get("관측컬럼") or ind["키"]
        values = column(key)
        cap = SL.capability(values, lsl=lsl, usl=usl)
        if not cap:
            continue

        name, unit = ind["이름"], ind["단위"]
        해석 = SL.interpret_capability(name, unit, cap)

        # 부분군으로 묶어 X-bar R 관리도 - 남는 값은 버립니다
        size = int(chart.get("부분군") or 0)
        관리도 = None
        if size >= 2 and len(values) >= size * 2:
            groups = [values[i:i + size] for i in range(0, len(values) - size + 1, size)]
            관리도 = SL.xbar_r_chart(groups)
            if 관리도:
                해석 = 해석 + SL.interpret_xbar_r(name, unit, 관리도)

        return {"키": key, "이름": name, "단위": unit,
                "공정능력": cap, "관리도": 관리도, "해석": 해석}
    return None


@app.get("/api/game/{game_id}/stats")
def game_stats(game_id: str):
    """
    지금까지의 조업 기록으로 통계를 계산하고, 그 숫자가 무슨 뜻인지 설명합니다.

    계산은 전부 파이썬(서버)이 합니다 - 9주에 여러분이 만들 함수와 같은 것입니다.
    """
    game = get_game(game_id)
    history = game.get("history", [])
    if len(history) < 3:
        raise HTTPException(status_code=400,
                            detail="아직 기록이 적습니다. 3개월 이상 운전한 뒤 다시 열어 보세요.")

    def column(key):
        return [row[key] for row in history
                if isinstance(row.get(key), (int, float))]

    지표 = []
    for key, name, unit in STAT_TARGETS:
        values = column(key)
        stats = SL.describe(values)
        if not stats:
            continue
        limits = SL.control_limits(values)
        지표.append({
            "키": key, "이름": name, "단위": unit,
            "값": [round(v, 3) for v in values],
            "턴": [row["턴"] for row in history if isinstance(row.get(key), (int, float))],
            "기술통계": stats,
            "히스토그램": SL.histogram(values),
            "관리도": limits,
            "신뢰구간": SL.confidence_interval(values),
            "이상치": SL.outliers(values),
            "해석": (SL.interpret_describe(name, unit, stats)
                     + (SL.interpret_control(name, unit, limits) if limits else [])),
        })

    # ── 품질 · 공정능력 (dkYield99 전용) ────────────────────────────
    #   규격과 부분군 크기는 indicators_data.py 에 적혀 있습니다.
    #   화면에 숫자를 새로 쓰지 않고 그 파일 하나만 보게 해 둡니다.
    품질 = build_quality(column)

    # ※ 지표 사이의 상관·회귀는 일부러 계산하지 않습니다.
    #   상관계수를 제대로 가르치려면 인과·교란·표본크기를 함께 다뤄야 하는데,
    #   그 시간을 평균·표준편차·분포를 확실히 하는 데 쓰기로 했습니다.
    #   (statistics_lab.correlation() 함수 자체는 남아 있습니다.)

    return {
        "요약": {
            "턴수": len(history),
            "시드": game["plant"].get("난수시드"),
            "잡음켜짐": game["plant"].get("난수시드") is not None,
            # ★ "이 숫자가 어느 파일에 있나"를 화면이 바로 알려 줄 수 있게 경로를 함께 보냅니다.
            "데이터폴더": str(LAB_DATA_DIR),
            "파일이름": f"dkyield_{game_id}_wide.csv",
            "파일있음": (LAB_DATA_DIR / f"dkyield_{game_id}_wide.csv").exists(),
        },
        # ★ 그래프 밑에 '엑셀 모습'으로 그대로 펴 보여 줄 원본 표입니다.
        #   그래프는 요약이고, 이것이 그 요약이 나온 실제 숫자입니다.
        "표": {
            "컬럼": export_csv.wide_columns(),
            "행": export_csv.rows_wide(game),
        },
        "지표": 지표,
        "품질": 품질,
        "근거": SL.REFERENCES,
    }


# 두 무리를 비교할 때 볼 지표들
COMPARE_KEYS = [("순도", "%"), ("수율", "%"), ("누적이익", "억"),
                ("안전지수", "점"), ("환경지수", "점")]


@app.get("/api/saves/compare")
def compare_saves(label_a: str = "성공", label_b: str = "실패"):
    """
    ★ 잘 운전한 공장과 잘못 운전한 공장을 통계로 비교합니다.

    ★★ 왜 여러 지표를 한 번에 보나요?
        '어떤 지표로 비교하느냐'에 따라 결론이 달라지기 때문입니다.
        지표 하나만 골라 유리한 결과를 보고하는 것을 체리피킹이라고 합니다.
    """
    everything = list_saves()
    group_a_ids = [s["저장아이디"] for s in everything if s["라벨"] == label_a]
    group_b_ids = [s["저장아이디"] for s in everything if s["라벨"] == label_b]
    if len(group_a_ids) < 2 or len(group_b_ids) < 2:
        raise HTTPException(
            status_code=400,
            detail=f"비교하려면 '{label_a}' 와 '{label_b}' 라벨이 각각 2판 이상 필요합니다. "
                   f"(지금 {label_a} {len(group_a_ids)}판 / {label_b} {len(group_b_ids)}판) "
                   "'🧪 예시 데이터 만들기' 를 눌러 보세요.")

    games_a = load_saves_bulk(group_a_ids)
    games_b = load_saves_bulk(group_b_ids)

    def finals(games, key):
        out = []
        for _meta, game in games:
            history = game.get("history", [])
            if history and isinstance(history[-1].get(key), (int, float)):
                out.append(history[-1][key])
        return out

    결과 = []
    for key, unit in COMPARE_KEYS:
        a, b = finals(games_a, key), finals(games_b, key)
        if len(a) < 2 or len(b) < 2:
            continue
        r = SL.compare_groups(a, b, label_a, label_b)
        if r is None:
            continue
        d = abs(r["효과크기"])
        크기 = "큰" if d >= 0.8 else "중간" if d >= 0.5 else "작은"
        결과.append({
            "지표": key, "단위": unit, "비교": r, "효과": 크기,
            "해석": (
                f"'{label_a}' {r['개수A']}판 평균 {r['평균A']}{unit} vs "
                f"'{label_b}' {r['개수B']}판 평균 {r['평균B']}{unit} "
                f"(차이 {r['평균차']}{unit}) - "
                + (f"t {r['t값']} > 임계값 {r['임계값(95%)']}, 우연으로 보기 어렵습니다."
                   if r["유의함"] else
                   f"t {r['t값']} < 임계값 {r['임계값(95%)']}, 지금 자료로는 판단할 수 없습니다.")
                + f" 효과크기 d={r['효과크기']}({크기})"),
        })

    if not 결과:
        raise HTTPException(status_code=400, detail="비교할 값이 부족합니다.")

    갈린다 = len({x["비교"]["유의함"] for x in 결과}) > 1
    총평 = []
    유의한것 = [x["지표"] for x in 결과 if x["비교"]["유의함"]]
    아닌것 = [x["지표"] for x in 결과 if not x["비교"]["유의함"]]
    if 갈린다:
        총평.append(
            f"★ 지표에 따라 결론이 갈립니다. "
            f"{', '.join(유의한것)} 에서는 두 무리가 뚜렷이 다르지만, "
            f"{', '.join(아닌것)} 에서는 '다르다'고 말할 수 없습니다. "
            "어느 지표를 고르느냐가 결론을 바꿉니다 - "
            "자기에게 유리한 지표만 골라 보고하는 것을 체리피킹이라고 합니다. "
            "보고서에는 본 것을 전부 적으세요.")
    elif 유의한것:
        총평.append(f"본 지표 {len(결과)}개 모두에서 두 무리가 뚜렷이 다릅니다.")
    else:
        총평.append("어느 지표에서도 '다르다'고 말할 수 없습니다. 판을 더 모아 보세요.")
    총평.append(
        "⚠️ p값(과 t값)을 '두 무리가 같을 확률'로 읽으면 안 됩니다. "
        "미국통계학회가 2016년 공식 성명으로 경고한 대표적 오해입니다.")
    총평.append(
        "그리고 이 비교는 '라벨을 내가 붙였다'는 한계가 있습니다. "
        "성공/실패를 정한 기준이 무엇이었는지 보고서에 반드시 밝히세요.")

    return {"결과": 결과, "총평": 총평,
            "무리": {"A": label_a, "B": label_b},
            "근거": SL.REFERENCES["신뢰구간"]}


# ── 프론트엔드 ──────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def index():
    idx = WEB_DIR / "index.html"
    if idx.exists():
        headers = {"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
                   "Pragma": "no-cache", "Expires": "0"}
        return FileResponse(idx, headers=headers)
    return HTMLResponse("<h1>dkYield99% API</h1><p>웹 프론트가 아직 없습니다. /api/scenario 로 확인하세요.</p>")


if WEB_DIR.exists():
    app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="web")
