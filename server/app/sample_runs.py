# ════════════════════════════════════════════════════════════════════
#  예시 데이터 만들기 (sample_runs.py)
#
#  잘 운영한 공장과 잘못 운영한 공장을 여러 개 자동으로 만들어 저장합니다.
#
#  ▶ 왜 필요한가요?
#     통계는 '여러 개'가 있어야 시작됩니다.
#     한 판만 돌려서는 평균도 표준편차도 비교도 할 수 없습니다.
#     수업 시간에 20판을 직접 운전할 수는 없으니 미리 만들어 두고,
#     그것으로 분석하는 법을 먼저 배웁니다.
#
#  ▶ 무엇이 만들어지나요?
#     성공 라벨 - 수율과 순도를 함께 관리한 운전
#     실패 라벨 - 한쪽만 쫓다가 규격을 놓친 운전
#
#     "성공한 공장의 순도가 정말 더 높은가, 아니면 운이 좋았을 뿐인가?"
#     → 13주 이표본 비교
#
#  ▶ 직접 실행:  server 폴더에서  python -m app.sample_runs
# ════════════════════════════════════════════════════════════════════
from __future__ import annotations

from app.engine.process_engine import (
    new_plant, enact_card, end_turn, evaluate_ending,
)
from app.cards import load_cards
from app.persistence import create_save, list_saves

MAX_TURN = 12

CARD_BY_ID = {c["아이디"]: c for c in load_cards()}


# ════════════════════════════════════════════════════════════════════
#  운전 방식 - 잘한 쪽과 잘못한 쪽
# ════════════════════════════════════════════════════════════════════
GOOD_PLANS = {
    "균형 운전": {
        1: "molar_ratio", 2: "reflux_up", 3: "heat_recovery",
        5: "high_selectivity_catalyst", 9: "condition_opt", 11: "online_analyzer",
    },
    "수율·순도 병행": {
        1: "high_selectivity_catalyst", 2: "molar_ratio", 4: "reactor_temp_up",
        5: "reflux_up", 6: "coolant_up", 8: "condition_opt", 10: "residence_up",
    },
    "품질 우선 운전": {
        1: "reflux_up", 2: "hx_clean", 3: "online_analyzer",
        5: "qc_sampling", 7: "high_purity_product", 10: "molar_ratio",
    },
    "에너지 절감 + 품질": {
        1: "heat_recovery", 2: "reflux_up", 4: "hx_clean",
        6: "condition_opt", 9: "molar_ratio", 11: "preventive_maint",
    },
}

BAD_PLANS = {
    "아무것도 안 함": {},
    "생산량만 늘림": {
        1: "feed_up", 3: "feed_up", 6: "reactor_temp_up", 9: "feed_up",
    },
    "비용만 깎음": {
        1: "hx_clean", 2: "heat_recovery", 4: "reflux_down",
        6: "condition_opt", 9: "hx_clean",
    },
    "온도만 계속 올림": {
        1: "reactor_temp_up", 3: "reactor_temp_up", 5: "pressure_up",
        8: "reactor_temp_up",
    },
}


# ── 한 판을 끝까지 돌린다 ────────────────────────────────────────────
def play(plan, seed, turns=MAX_TURN):
    """정해진 계획대로 12개월을 자동 운전하고 기록을 돌려줍니다."""
    from app.main import snapshot            # 기록 컬럼 정의를 그대로 씁니다

    plant = new_plant(seed=seed)
    game = {"plant": plant, "history": [snapshot(plant)], "actions": []}

    for turn in range(1, turns + 1):
        cid = plan.get(turn)
        if cid:
            ok, _message = enact_card(plant, CARD_BY_ID[cid])
            game["actions"].append({"턴": turn, "아이디": cid, "성공": ok})
        end_turn(plant)
        game["history"].append(snapshot(plant))

    grade, name = evaluate_ending(plant)
    game["ending"] = {"등급": grade, "이름": name}
    return game, grade, name


# ── 여러 판을 만들어 저장한다 ────────────────────────────────────────
def build_samples(count_each=4, base_seed=880000, verbose=False):
    """
    잘된 판과 잘못된 판을 각각 만들어 '성공' / '실패' 라벨로 보관합니다.

    같은 운전 방식이라도 시드를 바꾸면 조업 변동 때문에 결과가 달라집니다.
    그 '조금씩 다름'이 바로 통계로 다룰 대상입니다.
    """
    made = {"성공": [], "실패": []}
    seed = base_seed

    for label, plans in (("성공", GOOD_PLANS), ("실패", BAD_PLANS)):
        for style, plan in plans.items():
            for copy_number in range(count_each):
                seed += 1
                game, grade, name = play(plan, seed)
                plant = game["plant"]
                title = f"{style} #{copy_number + 1}"
                memo = f"{grade}등급 · {name}"
                create_save("sample", game, title, label, memo)
                made[label].append({
                    "이름": title, "시드": seed, "등급": grade,
                    "누적이익": plant["누적이익"], "수율": plant["수율"],
                    "순도": plant["순도"],
                })
                if verbose:
                    print(f"    [{label}] {title:<20} 시드 {seed}  {grade}등급  "
                          f"누적 {plant['누적이익']:>7}억  수율 {plant['수율']:>5}%  "
                          f"순도 {plant['순도']:>6}%  안전 {plant['안전지수']:>5}")
    return made


def has_samples():
    """예시 데이터가 이미 만들어져 있는지 확인합니다."""
    return any("등급" in s["메모"] for s in list_saves())


# ════════════════════════════════════════════════════════════════════
#  데모
# ════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    from app.persistence import init_db
    from app.statistics_lab import describe, compare_groups, interpret_describe

    init_db()

    print("=" * 84)
    print("  예시 데이터 만들기 - 잘 운전한 공장과 잘못 운전한 공장")
    print("=" * 84)
    made = build_samples(count_each=4, verbose=True)
    print(f"\n  성공 {len(made['성공'])}판 / 실패 {len(made['실패'])}판 을 보관했습니다.")

    print("\n" + "-" * 84)
    print("  두 무리를 지표별로 비교하면")
    print("-" * 84)
    for key in ("순도", "수율", "누적이익"):
        good = [row[key] for row in made["성공"]]
        bad = [row[key] for row in made["실패"]]
        r = compare_groups(good, bad, "성공", "실패")
        판정 = "뚜렷이 다름" if r["유의함"] else "판단 보류"
        print(f"\n  [{key}]  성공 {r['평균A']}  vs  실패 {r['평균B']}  "
              f"(차이 {r['평균차']})")
        print(f"        t {r['t값']}  임계값 {r['임계값(95%)']}  "
              f"효과크기 d {r['효과크기']}  ->  {판정}")

    print("\n  [성공 무리의 순도 기술통계]")
    for line in interpret_describe("순도", "%", describe([r["순도"] for r in made["성공"]])):
        print(f"     - {line}")
    print("=" * 84)
