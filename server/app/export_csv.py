# ════════════════════════════════════════════════════════════════════
#  데이터 내보내기 (export_csv.py)
#
#  게임 기록을 CSV 파일로 만들어 줍니다. 통계 실습의 '원유'입니다.
#
#  ▶ 두 가지 모양으로 내보냅니다
#
#     wide (넓은 표)  - 한 줄에 한 턴. 컬럼이 지표 이름.
#                       턴 | 세수 | 인구 | 주민만족 | ...
#                       9~10주 실습(순수 파이썬)에 씁니다. row["세수"] 로 바로 잡힙니다.
#
#     long (긴 표)    - 한 줄에 (턴, 지표) 하나.
#                       턴 | 지표 | 값 | 유형
#                       11주 pandas 의 pivot_table 연습에 씁니다.
#
#  ▶ 여러 판을 한 파일로 합칠 수도 있습니다  ★ 비교분석
#     '성공' 라벨을 붙인 판들과 '실패' 판들을 한 표로 모으면
#     그대로 이표본 비교(t검정·상자그림)의 재료가 됩니다.
#
#  ※ 한글 엑셀에서 안 깨지도록 반드시 utf-8-sig (BOM) 로 씁니다.
#     이걸 빼면 엑셀에서 헤더가 전부 깨져 보입니다.
# ════════════════════════════════════════════════════════════════════
from __future__ import annotations

import csv
import io
from pathlib import Path

# 판을 구분하는 컬럼 - 여러 판을 합칠 때 맨 앞에 붙습니다
SAVE_COLUMNS = ["저장이름", "라벨", "저장아이디", "시드"]

# 게임 진행 컬럼
BASE_COLUMNS = ["턴"]


def _catalogue():
    """지표 설명서를 읽어 옵니다. 없으면 빈 목록."""
    try:
        from app.indicators import load_indicators
        return load_indicators()
    except Exception:
        return []


def wide_columns() -> list[str]:
    """넓은 표의 컬럼 순서를 정합니다 (지표 설명서 순서를 그대로 따릅니다)."""
    columns = list(BASE_COLUMNS)
    for ind in _catalogue():
        if not ind.get("CSV포함") or ind["키"] in columns:
            continue
        columns.append(ind["키"])
        if ind.get("관측컬럼"):
            columns.append(ind["관측컬럼"])   # 진값 바로 옆에 관측값
    return columns


def rows_wide(game: dict, meta: dict | None = None) -> list[dict]:
    """
    한 판의 기록을 '한 줄에 한 턴' 모양으로 만듭니다.

    meta 를 주면 저장이름·라벨이 앞에 붙습니다 (여러 판을 합칠 때).
    """
    columns = wide_columns()
    head = {}
    if meta:
        head = {
            "저장이름": meta.get("이름", ""),
            "라벨": meta.get("라벨", ""),
            "저장아이디": meta.get("저장아이디", ""),
            "시드": meta.get("시드", ""),
        }

    out = []
    for snapshot in game.get("history", []):
        row = dict(head)
        for column in columns:
            # 옛날에 저장된 기록은 컬럼이 적습니다 - 없으면 빈칸으로 둡니다.
            row[column] = snapshot.get(column, "")
        out.append(row)
    return out


def rows_long(game: dict, meta: dict | None = None) -> list[dict]:
    """한 판의 기록을 '한 줄에 지표 하나' 모양으로 만듭니다."""
    catalogue = {ind["키"]: ind for ind in _catalogue()}
    head = {}
    if meta:
        head = {
            "저장이름": meta.get("이름", ""),
            "라벨": meta.get("라벨", ""),
            "저장아이디": meta.get("저장아이디", ""),
            "시드": meta.get("시드", ""),
        }

    out = []
    for snapshot in game.get("history", []):
        turn = snapshot.get("턴", "")
        for key, value in snapshot.items():
            if key == "턴" or value == "" or value is None:
                continue
            # 관측 컬럼(예: 주민만족_조사)의 설명은 원래 지표에서 가져옵니다.
            base_key = key.split("_")[0]
            ind = catalogue.get(key) or catalogue.get(base_key) or {}
            row = dict(head)
            row.update({
                "턴": turn,
                "지표": key,
                "이름": ind.get("이름", key),
                "값": value,
                "단위": ind.get("단위", ""),
                "유형": "관측값" if key not in catalogue and base_key in catalogue
                        else ind.get("유형", ""),
            })
            out.append(row)
    return out


def to_csv_text(rows: list[dict]) -> str:
    """행 목록을 CSV 글자로 바꿉니다. (컬럼 순서는 첫 행을 따릅니다)"""
    if not rows:
        return ""
    # 모든 행에 등장하는 컬럼을 순서를 지켜 모읍니다.
    columns = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, extrasaction="ignore",
                            lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return buffer.getvalue()


#  파일 이름에 쓸 수 없는 글자 (윈도우 기준)
FORBIDDEN = '\\/:*?"<>|'


def safe_filename(name: str, fallback: str = "이름없는판") -> str:
    """
    저장한 판 이름을 그대로 파일 이름으로 쓸 수 있게 다듬습니다.

        "환경형 1차"        ->  "환경형 1차"
        "세금 3/4 인상"     ->  "세금 3_4 인상"      (/ 는 쓸 수 없음)

    ★ 저장 이름과 CSV 파일 이름을 같게 두는 것이 중요합니다.
      나중에 "환경형 1차 판의 데이터가 어느 파일이지?" 를 헤매지 않게.
    """
    cleaned = "".join("_" if ch in FORBIDDEN else ch for ch in (name or ""))
    cleaned = " ".join(cleaned.split())          # 앞뒤·중복 공백 정리
    cleaned = cleaned.strip(". ")                # 윈도우는 끝의 점을 싫어합니다
    if not cleaned:
        cleaned = fallback
    return cleaned[:80]                          # 너무 길면 자릅니다


def write_csv(path: Path, rows: list[dict]) -> Path:
    """
    CSV 파일로 저장합니다.

    encoding="utf-8-sig" 가 중요합니다.
    이걸 빼면 한글 엑셀에서 컬럼 이름이 전부 깨져 보입니다.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(to_csv_text(rows), encoding="utf-8-sig", newline="")
    return path


# ════════════════════════════════════════════════════════════════════
#  ★ 비교분석 - 여러 판을 한 표로 합치기
# ════════════════════════════════════════════════════════════════════
def combine(saves: list[tuple[dict, dict]], shape: str = "wide") -> list[dict]:
    """
    여러 판의 기록을 하나의 표로 합칩니다.

    saves 는 [(메타정보, 게임상태), ...] 입니다. (persistence.load_saves_bulk 의 결과)

    합쳐진 표에는 맨 앞에 '저장이름'과 '라벨' 컬럼이 붙습니다.
    라벨로 무리를 나누면 그대로 통계 비교가 됩니다:

        성공한 판들의 최종 세수 평균  vs  실패한 판들의 최종 세수 평균
        → 차이가 우연일 수 있는 크기인가? (13주 이표본 t검정)
    """
    maker = rows_wide if shape == "wide" else rows_long
    out = []
    for meta, game in saves:
        out.extend(maker(game, meta))
    return out


def summary_rows(saves: list[tuple[dict, dict]]) -> list[dict]:
    """
    판마다 '한 줄 요약'을 만듭니다. (마지막 턴의 결과 + 몇 가지 통계)

    한 줄에 한 판이므로, 판이 20개면 표본 20개짜리 데이터가 됩니다.
    '성공' 무리와 '실패' 무리의 평균을 비교하기에 가장 편한 모양입니다.
    """
    out = []
    for meta, game in saves:
        history = game.get("history", [])
        if not history:
            continue
        last = history[-1]
        row = {
            "저장이름": meta.get("이름", ""),
            "라벨": meta.get("라벨", ""),
            "시드": meta.get("시드", ""),
            "총턴": len(history),
        }
        # 마지막 턴의 값
        for key, value in last.items():
            if key == "턴" or isinstance(value, (list, dict)):
                continue
            row[f"최종_{key}"] = value

        # 판 전체에 걸친 간단한 통계 (학생이 직접 계산한 값과 맞춰 볼 수 있게)
        for key in ("세수", "주민만족", "인구", "도시건강도"):
            values = [h[key] for h in history
                      if isinstance(h.get(key), (int, float))]
            if len(values) >= 2:
                average = sum(values) / len(values)
                spread = (sum((v - average) ** 2 for v in values) / (len(values) - 1)) ** 0.5
                row[f"평균_{key}"] = round(average, 2)
                row[f"표준편차_{key}"] = round(spread, 3)
        out.append(row)
    return out
