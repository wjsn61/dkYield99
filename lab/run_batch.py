# ════════════════════════════════════════════════════════════════════
#  여러 번 돌려 보기 (run_batch.py)
#  ※ 이 파일은 도구입니다. 안 만져도 됩니다. (전략은 strategies.py 에서)
#
#  ▶ 무엇을 하나요?
#     같은 운전 계획을 시드만 바꿔 여러 번 자동으로 돌리고,
#     그 결과를 CSV 한 장으로 모아 줍니다.
#
#  ▶ 왜 필요한가요?                              ← 9주 수업의 핵심
#     한 번 돌려 보고 "이 운전이 좋다"고 말할 수는 없습니다.
#     같은 카드를 써도 조업 변동 때문에 결과가 달라지기 때문입니다.
#     여러 번 돌려 봐야 '카드 때문'과 '그냥 변동'을 구분할 수 있습니다.
#
#  ▶ 쓰는 법
#     python run_batch.py                          무조작 10번
#     python run_batch.py --strategy 품질형 --n 20
#     python run_batch.py --compare 품질형 수율형 --n 20
#     python run_batch.py --strategy 균형형 --level turn      턴별 기록까지
#
#  ※ 외부 라이브러리가 필요 없습니다. 서버를 켜지 않아도 됩니다.
# ════════════════════════════════════════════════════════════════════
import argparse
import csv
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
sys.path.insert(0, os.path.join(HERE, "..", "server"))

from app.engine.process_engine import (         # noqa: E402
    new_plant, enact_card, end_turn, evaluate_ending,
)
from app.cards import load_cards                # noqa: E402
from strategies import STRATEGIES               # noqa: E402

CARD_BY_ID = {c["아이디"]: c for c in load_cards()}
MAX_TURN = 12


# ── 한 판을 끝까지 돌린다 ────────────────────────────────────────────
def play_once(plan, seed, turns=MAX_TURN, quiet=True):
    """정해진 계획대로 자동 운전하고 (공장, 턴별기록) 을 돌려줍니다."""
    plant = new_plant(seed=seed)
    rows = []
    blocked = []

    for turn in range(1, turns + 1):
        cid = plan.get(turn)
        if cid:
            ok, message = enact_card(plant, CARD_BY_ID[cid])
            if not ok:
                blocked.append(f"{turn}턴 {cid}: {message}")
        end_turn(plant)
        if quiet:
            plant["기록"].clear()          # 배치에서는 로그가 낭비입니다

        samples = plant.get("순도샘플") or []
        rows.append({
            "턴": turn,
            "수율": plant["수율"],
            "순도": round(plant["순도"], 2),
            "순도_분석": plant.get("순도_분석"),
            "순도샘플평균": round(sum(samples) / len(samples), 3) if samples else None,
            "순도샘플범위": round(max(samples) - min(samples), 3) if samples else None,
            "월이익": plant["월이익"],
            "누적이익": plant["누적이익"],
            "안전지수": round(plant["안전지수"], 1),
            "환경지수": round(plant["환경지수"], 1),
            "에너지비": round(plant["에너지비"], 1),
            "설비노후도": plant["설비노후도"],
        })

    grade, name = evaluate_ending(plant)
    return plant, rows, grade, name, blocked


# ── 통계 (외부 라이브러리 없이) ─────────────────────────────────────
def mean(values):
    return sum(values) / len(values) if values else 0.0


def stdev(values):
    if len(values) < 2:
        return 0.0
    m = mean(values)
    return (sum((v - m) ** 2 for v in values) / (len(values) - 1)) ** 0.5


# ── 한 전략을 여러 번 ───────────────────────────────────────────────
def run_strategy(name, count, seed_start, turns, level):
    spec = STRATEGIES.get(name)
    if spec is None:
        print(f"  '{name}' 이라는 전략이 없습니다.")
        print(f"  쓸 수 있는 전략: {', '.join(STRATEGIES)}")
        sys.exit(1)

    plan = spec["계획"]
    game_rows, turn_rows = [], []
    warned = False

    for i in range(count):
        seed = seed_start + i
        plant, rows, grade, ending, blocked = play_once(plan, seed, turns)

        if blocked and not warned:
            print("  ⚠️ 시행되지 않은 카드가 있습니다 (예산 부족·이미 설치된 설비):")
            for b in blocked:
                print(f"     - {b}")
            print("     → 계획이 의도대로 돌아가지 않았습니다. strategies.py 를 확인하세요.\n")
            warned = True

        game_rows.append({
            "전략": name, "시드": seed,
            "등급": grade, "등급이름": ending,
            "최종_수율": plant["수율"],
            "최종_순도": round(plant["순도"], 2),
            "최종_누적이익": plant["누적이익"],
            "최종_안전지수": round(plant["안전지수"], 1),
            "최종_환경지수": round(plant["환경지수"], 1),
            # 학생이 직접 만든 my_mean() · my_stdev() 로 검산해 볼 값
            "평균_수율": round(mean([r["수율"] for r in rows]), 3),
            "표준편차_수율": round(stdev([r["수율"] for r in rows]), 3),
        })
        if level == "turn":
            for r in rows:
                turn_rows.append({"전략": name, "시드": seed, **r})

    return game_rows, turn_rows


# ── CSV 로 저장 ─────────────────────────────────────────────────────
def write_csv(rows, filename):
    if not rows:
        return None
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(DATA_DIR, filename)
    columns = []
    for row in rows:
        for k in row:
            if k not in columns:
                columns.append(k)
    # utf-8-sig 로 써야 한국어 엑셀에서 컬럼 이름이 안 깨집니다
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    return path


#   여러 지표를 함께 보여 줍니다.
#   ★ 지표에 따라 흔들림이 있기도 하고 없기도 합니다 - 그 자체가 배울 점입니다.
SUMMARY_KEYS = [("최종_수율", "%"), ("최종_순도", "%"),
                ("최종_누적이익", "억"), ("최종_안전지수", "점")]


def summarize(name, rows):
    print(f"\n  [{name}] {len(rows)}판")
    print(f"     {'지표':<16}{'평균':>10}{'표준편차':>10}{'최소':>10}{'최대':>10}")
    flat = []
    for key, unit in SUMMARY_KEYS:
        values = [r[key] for r in rows]
        sd = stdev(values)
        print(f"     {key:<16}{mean(values):>10.2f}{sd:>10.3f}"
              f"{min(values):>10}{max(values):>10}   {unit}")
        if sd == 0:
            flat.append(key)

    if flat:
        print(f"\n     ⓘ {', '.join(flat)} 은(는) 모든 판에서 똑같이 나왔습니다.")
        print("       흔들림이 없는 지표도 있습니다. 왜 그럴까요?")
        print("       - 순도(진값)는 카드로만 바뀝니다. 우리가 보는 건 분석값")
        print("         (순도_분석)이고, 그쪽은 계기 오차 때문에 흔들립니다.")
        print("       ★ 무엇을 보고 판단할지 고르는 것도 분석의 일부입니다.")


# ── 실행부 ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="같은 운전을 시드만 바꿔 여러 번 돌려 봅니다.")
    parser.add_argument("--strategy", default="무조작", help="strategies.py 의 전략 이름")
    parser.add_argument("--compare", nargs=2, metavar=("전략A", "전략B"),
                        help="두 전략을 같은 시드로 비교")
    parser.add_argument("--n", type=int, default=10, help="몇 번 돌릴지 (기본 10)")
    parser.add_argument("--seed-start", type=int, default=1000, help="첫 시드")
    parser.add_argument("--turns", type=int, default=MAX_TURN, help="몇 달까지")
    parser.add_argument("--level", choices=["game", "turn"], default="game",
                        help="game=판별 한 줄 / turn=달별 한 줄")
    parser.add_argument("--out", default=None, help="저장할 파일 이름")
    args = parser.parse_args()

    print("=" * 70)
    print("  여러 번 돌려 보기")
    print("=" * 70)

    names = args.compare if args.compare else [args.strategy]
    all_game, all_turn = [], []

    for name in names:
        # ★ 같은 시드를 두 전략에 똑같이 씁니다.
        #   그래야 조업 변동이 같아지고, 차이가 카드 때문이라고 말할 수 있습니다.
        game_rows, turn_rows = run_strategy(
            name, args.n, args.seed_start, args.turns, args.level)
        all_game.extend(game_rows)
        all_turn.extend(turn_rows)
        summarize(name, game_rows)

    if args.compare:
        key = "최종_누적이익"
        a = [r[key] for r in all_game if r["전략"] == names[0]]
        b = [r[key] for r in all_game if r["전략"] == names[1]]
        gap = mean(a) - mean(b)
        print()
        print(f"  두 전략의 {key} 평균 차이: {gap:+.2f}억")
        print(f"  각 무리의 흔들림(표준편차): {stdev(a):.2f} / {stdev(b):.2f}")
        if abs(gap) < max(stdev(a), stdev(b)):
            print("  ⚠️ 차이가 흔들림보다 작습니다. 이 정도로는 '다르다'고 말하기 어렵습니다.")
            print("     --n 을 늘려 더 많이 돌려 보세요.")
        else:
            print("  차이가 흔들림보다 큽니다. 다만 이것만으로 단정하지는 마세요 -")
            print("     게임의 「⚖ 성공 vs 실패 비교」 화면에서 제대로 된 검정을 볼 수 있습니다.")

    rows = all_turn if args.level == "turn" else all_game
    tag = "-".join(names)
    default = f"batch_{tag}_{args.level}.csv"
    path = write_csv(rows, args.out or default)

    print()
    print("-" * 70)
    print(f"  {len(rows)}줄을 저장했습니다:")
    print(f"     {path}")
    print()
    print("  ▶ 다음 할 일")
    print("     1) 엑셀로 열어서 =AVERAGE() · =STDEV.S() 로 확인")
    print("     2) python w12_basic.py 로 같은 값을 코드로 계산")
    print("     3) 두 값이 같은지 맞춰 보기")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
