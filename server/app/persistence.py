# ════════════════════════════════════════════════════════════════════
#  저장소 (persistence.py)
#
#  두 가지를 저장합니다.
#
#   1) 진행 중인 게임  (games)
#      브라우저를 새로고침해도 이어서 할 수 있게 자동으로 저장됩니다.
#      24시간이 지나면 자동으로 정리됩니다.
#
#   2) 내가 이름 붙여 남긴 판  (saves)          ★ 통계 실습의 재료
#      "성장형 1차", "환경형 2차" 처럼 이름을 붙여 보관합니다.
#      자동으로 지워지지 않습니다.
#
#      ★ 라벨(성공/실패)이 핵심입니다.
#        잘된 판과 잘못된 판을 나눠 두면, 나중에 두 무리를 통계로 비교할 수 있습니다.
#        "성공한 판들의 평균 세수는 실패한 판보다 정말 높은가?" 같은 질문이
#        13주 이표본 t검정 실습이 됩니다.
# ════════════════════════════════════════════════════════════════════
import json
import sqlite3
import uuid
from pathlib import Path

# server/app/data 에 데이터베이스가 생성됩니다.
DB_DIR = Path(__file__).resolve().parent / "data"
DB_FILE = DB_DIR / "dkyield.db"

# 세이브에 붙일 수 있는 라벨 (통계 비교의 그룹 변수가 됩니다)
LABELS = ("성공", "실패", "미정")


def _connect():
    """WAL 모드 + busy_timeout 로 동시 접근에 안전한 연결을 엽니다."""
    conn = sqlite3.connect(str(DB_FILE), timeout=5)
    conn.execute("PRAGMA journal_mode=WAL")    # 읽기/쓰기 동시성 향상
    conn.execute("PRAGMA busy_timeout=5000")   # 잠금 시 최대 5초 대기(즉시 오류 방지)
    return conn


def init_db():
    """데이터베이스 파일과 테이블이 없으면 생성합니다."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = _connect()
    try:
        cursor = conn.cursor()
        # (1) 진행 중인 게임 - 자동 저장, 24시간 뒤 정리
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS games (
                game_id TEXT PRIMARY KEY,
                state_data TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # (2) 이름 붙여 남긴 판 - 자동으로 지워지지 않습니다
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS saves (
                save_id    TEXT PRIMARY KEY,
                game_id    TEXT NOT NULL,
                이름        TEXT NOT NULL,
                라벨        TEXT NOT NULL DEFAULT '미정',
                메모        TEXT NOT NULL DEFAULT '',
                턴          INTEGER,
                시드        INTEGER,
                state_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_saves_label ON saves(라벨)")
        conn.commit()
    finally:
        conn.close()


# ════════════════════════════════════════════════════════════════════
#  진행 중인 게임 (자동 저장)
# ════════════════════════════════════════════════════════════════════
def save_game(game_id: str, game: dict):
    """게임 상태를 데이터베이스에 저장하거나 업데이트합니다."""
    conn = _connect()
    try:
        cursor = conn.cursor()
        state_json = json.dumps(game, ensure_ascii=False)
        cursor.execute("""
            INSERT INTO games (game_id, state_data, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(game_id) DO UPDATE SET
                state_data = excluded.state_data,
                updated_at = CURRENT_TIMESTAMP
        """, (game_id, state_json))
        conn.commit()
    finally:
        conn.close()


def load_game(game_id: str) -> dict | None:
    """게임 ID에 해당하는 상태를 불러옵니다. 없으면 None을 반환합니다."""
    conn = _connect()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT state_data FROM games WHERE game_id = ?", (game_id,))
        row = cursor.fetchone()
        if row:
            return json.loads(row[0])
        return None
    finally:
        conn.close()


def cleanup_old_games():
    """
    24시간 동안 업데이트가 없었던 '진행 중인 게임'을 정리합니다.
    ※ 이름 붙여 저장한 판(saves)은 절대 지우지 않습니다.
    """
    conn = _connect()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM games WHERE updated_at < datetime('now', '-1 day')")
        conn.commit()
    finally:
        conn.close()


# ════════════════════════════════════════════════════════════════════
#  이름 붙여 남긴 판 (세이브 슬롯)  ★ 통계 실습의 재료
# ════════════════════════════════════════════════════════════════════
def create_save(game_id: str, game: dict, 이름: str,
                라벨: str = "미정", 메모: str = "") -> str:
    """
    지금 상태를 이름 붙여 보관합니다. 새 save_id 를 돌려줍니다.

    라벨은 나중에 통계로 두 무리를 비교할 때 쓰는 '그룹 이름'입니다.
    ('성공' 판들과 '실패' 판들의 평균을 비교하는 식으로)
    """
    if 라벨 not in LABELS:
        라벨 = "미정"
    plant = game.get("plant", {})
    save_id = uuid.uuid4().hex[:12]

    conn = _connect()
    try:
        conn.execute("""
            INSERT INTO saves (save_id, game_id, 이름, 라벨, 메모, 턴, 시드, state_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (save_id, game_id, 이름.strip() or "이름 없는 판", 라벨, 메모,
              plant.get("턴"), plant.get("난수시드"),
              json.dumps(game, ensure_ascii=False)))
        conn.commit()
    finally:
        conn.close()
    return save_id


def list_saves() -> list[dict]:
    """
    보관한 판의 목록을 돌려줍니다. (최근에 저장한 것부터)
    무거운 상태 데이터는 빼고, 목록에 보여줄 정보만 담습니다.
    """
    conn = _connect()
    try:
        rows = conn.execute("""
            SELECT save_id, game_id, 이름, 라벨, 메모, 턴, 시드, created_at, state_data
            FROM saves ORDER BY created_at DESC
        """).fetchall()
    finally:
        conn.close()

    out = []
    for (save_id, game_id, name, label, memo, turn, seed, created, state_json) in rows:
        plant = json.loads(state_json).get("plant", {})
        out.append({
            "저장아이디": save_id,
            "이름": name,
            "라벨": label,
            "메모": memo,
            "턴": turn,
            "시드": seed,
            "저장시각": created,
            # 목록에서 한눈에 비교할 수 있게 핵심 지표만 함께 보냅니다
            "요약": {
                "예산": round(plant.get("예산", 0), 1),
                "누적이익": round(plant.get("누적이익", 0), 1),
                "수율": round(plant.get("수율", 0), 1),
                "순도": round(plant.get("순도", 0), 2),
                "안전지수": round(plant.get("안전지수", 0), 1),
                "환경지수": round(plant.get("환경지수", 0), 1),
            },
        })
    return out


def load_save(save_id: str) -> dict | None:
    """보관한 판을 통째로 불러옵니다."""
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT state_data FROM saves WHERE save_id = ?", (save_id,)
        ).fetchone()
    finally:
        conn.close()
    return json.loads(row[0]) if row else None


def save_meta(save_id: str) -> dict | None:
    """보관한 판의 이름·라벨 같은 정보만 가져옵니다."""
    conn = _connect()
    try:
        row = conn.execute("""
            SELECT save_id, 이름, 라벨, 메모, 턴, 시드, created_at
            FROM saves WHERE save_id = ?
        """, (save_id,)).fetchone()
    finally:
        conn.close()
    if not row:
        return None
    return {"저장아이디": row[0], "이름": row[1], "라벨": row[2],
            "메모": row[3], "턴": row[4], "시드": row[5], "저장시각": row[6]}


def update_save(save_id: str, 이름: str = None, 라벨: str = None, 메모: str = None) -> bool:
    """보관한 판의 이름이나 라벨을 고칩니다. (판을 다 하고 나서 성공/실패를 매길 때)"""
    fields, values = [], []
    if 이름 is not None:
        fields.append("이름 = ?")
        values.append(이름.strip() or "이름 없는 판")
    if 라벨 is not None:
        fields.append("라벨 = ?")
        values.append(라벨 if 라벨 in LABELS else "미정")
    if 메모 is not None:
        fields.append("메모 = ?")
        values.append(메모)
    if not fields:
        return False

    values.append(save_id)
    conn = _connect()
    try:
        cursor = conn.execute(f"UPDATE saves SET {', '.join(fields)} WHERE save_id = ?", values)
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def delete_save(save_id: str) -> bool:
    """보관한 판을 지웁니다."""
    conn = _connect()
    try:
        cursor = conn.execute("DELETE FROM saves WHERE save_id = ?", (save_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def load_saves_bulk(save_ids: list[str]) -> list[tuple[dict, dict]]:
    """
    여러 판을 한꺼번에 불러옵니다. [(메타정보, 게임상태), ...]

    ★ 이 함수가 '잘된 판 vs 잘못된 판' 비교분석의 출발점입니다.
       여러 판의 기록을 하나의 표로 합쳐서 통계에 넘깁니다.
    """
    if not save_ids:
        return []
    marks = ",".join("?" for _ in save_ids)
    conn = _connect()
    try:
        rows = conn.execute(f"""
            SELECT save_id, 이름, 라벨, 메모, 턴, 시드, created_at, state_data
            FROM saves WHERE save_id IN ({marks})
            ORDER BY created_at
        """, save_ids).fetchall()
    finally:
        conn.close()

    out = []
    for (save_id, name, label, memo, turn, seed, created, state_json) in rows:
        meta = {"저장아이디": save_id, "이름": name, "라벨": label,
                "메모": memo, "턴": turn, "시드": seed, "저장시각": created}
        out.append((meta, json.loads(state_json)))
    return out
