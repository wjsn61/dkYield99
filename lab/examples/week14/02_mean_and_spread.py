# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  14주 · 02. my_mean · my_stdev 를 두 번
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     두 무리의 평균과 표준편차를 나란히 구합니다. 12주에 만든 함수를 두 번 부르는 것이 전부입니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     server/app/statistics_lab.py › describe()
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 1주 f"..." - 값을 끼워 넣는 문자열
#     · 1주 str( ) · float( ) · int( ) - 종류 바꾸기
#     · 1주 round( ) - 반올림
#     · 2주 len( ) - 개수 세기
#     · 2주 for - 하나씩 꺼내 반복
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week14   →   python 02_mean_and_spread.py
#
#  ▣ 바로 아래 [0] 준비 블록에 대하여
#     윈도우에서 한글이 깨지지 않게 하고, 게임 엔진을 찾아갈 길을 알려
#     주는 부분입니다. 어느 예제든 똑같으니 외울 필요 없습니다.
#     여러분이 새 파일을 만들 때는 그대로 복사해서 쓰면 됩니다.
#
#     이 주의 목표·실습·과제는 같은 폴더의 README.md 에 있습니다.
# ──────────────────────────────────────────────────────────────────────

# %% [0] 준비 - ★ 외우지 마세요. 새 파일을 만들 때 그대로 복사해 쓰면 됩니다.
#      하는 일 ① 윈도우에서 한글이 깨지지 않게
#              ② 게임 엔진(server 폴더)을 찾아갈 길을 알려 주기
import os      # os  : 폴더·파일 경로를 다루는 도구 모음
import sys     # sys : 파이썬 자신을 다루는 도구 모음

try:
    sys.stdout.reconfigure(encoding="utf-8")   # 윈도우 한글 깨짐 방지
except Exception:
    pass                                       # 안 되는 환경이면 그냥 넘어감

HERE = os.path.dirname(os.path.abspath(__file__))   # 이 파일이 있는 폴더
LAB = os.path.join(HERE, "..", "..")                # 그 위의 위 = lab 폴더
sys.path.insert(0, os.path.join(LAB, "..", "server"))  # 엔진을 찾을 곳
sys.path.insert(0, LAB)                                # lab 의 파일들

# %% [1] 준비 - 라벨 데이터가 없으면 엔진으로 만들어 씁니다
import csv
import glob


def labeled_rows():
    """라벨 붙은 CSV 를 찾고, 없으면 연습용으로 만들어 돌려줍니다."""
    for f in sorted(glob.glob(os.path.join(LAB, "data", "*.csv"))):
        with open(f, encoding="utf-8-sig", newline="") as fp:
            r = list(csv.DictReader(fp))
        if r and "라벨" in r[0] and {"성공", "실패"} <= {x.get("라벨") for x in r}:
            return r
    print("★ 라벨 붙은 CSV 가 없어 연습용 데이터를 만듭니다.")
    print("  과제에는 직접 저장한 판을 쓰세요.\n")
    from app.engine.process_engine import new_plant, enact_card, end_turn
    from app.cards import load_cards
    by_id = {p["아이디"]: p for p in load_cards()}
    rows = []
    for label, plan in (("성공", ["reactor_temp_up", "pressure_up"]), ("실패", [])):
        for seed in range(1, 11):
            s = new_plant(seed=seed)
            for card_id in plan:
                if card_id in by_id:
                    enact_card(s, by_id[card_id])
            for _ in range(12):
                end_turn(s)
            rows.append({"라벨": label, "최종_수율": round(s["수율"], 3)})
    return rows


rows = labeled_rows()
good = [float(r["최종_수율"]) for r in rows if r["라벨"] == "성공"]
bad = [float(r["최종_수율"]) for r in rows if r["라벨"] == "실패"]

# %% [2] 12주에 만든 함수를 두 번 부르면 끝입니다
def my_mean(v):
    return sum(v) / len(v)


def my_stdev(v):
    m = my_mean(v)
    return (sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** 0.5


print(f"{'':6}{'n':>4}{'평균':>10}{'표준편차':>12}")
print("-" * 34)
for name, value in (("성공", good), ("실패", bad)):
    print(f"{name:6}{len(value):>4}{my_mean(value):>10.2f}{my_stdev(value):>12.2f}")

# ✏️ 해 보기
#    평균만 보면 어느 쪽이 좋아 보이나요? 퍼짐까지 보면 어떤가요?


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week14/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) 평균만 보면 어느 쪽이 좋아 보이나요? 퍼짐까지 보면 어떤가요?
#   2) 두 무리의 표준편차가 크게 다르면 무슨 뜻인가요?


# 여기에 답을 써 보세요

