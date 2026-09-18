# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  14주 · 03. 차이 ÷ 퍼짐 ★
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     평균 차이를 표준편차와 견줍니다. 이 한 줄이 통계적 판단의 뼈대입니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     server/app/statistics_lab.py › compare_groups()
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
#     터미널  : cd lab\examples\week14   →   python 03_diff_over_spread.py
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

# %% [1] 준비 (앞 예제와 같습니다)
import csv
import glob


def labeled_rows():
    for f in sorted(glob.glob(os.path.join(LAB, "data", "*.csv"))):
        with open(f, encoding="utf-8-sig", newline="") as fp:
            r = list(csv.DictReader(fp))
        if r and "라벨" in r[0] and {"성공", "실패"} <= {x.get("라벨") for x in r}:
            return r
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


def my_mean(v):
    return sum(v) / len(v)


def my_stdev(v):
    m = my_mean(v)
    return (sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** 0.5


# %% [2] ★ 이 세 줄이 전부입니다
gap = my_mean(good) - my_mean(bad)
spread = (my_stdev(good) + my_stdev(bad)) / 2
ratio = gap / spread

print(f"평균 차이    {gap:>8.2f} %")
print(f"퍼짐         {spread:>8.2f}")
print(f"차이 ÷ 퍼짐  {ratio:>8.2f}")
print()
print("눈에 띄는 차이입니다." if abs(ratio) >= 1
      else "퍼짐에 묻히는 차이입니다 - 우연일 수 있습니다.")

# %% [3] 왜 나누나
print("""
★ 평균이 5 차이 나도, 각 무리가 ±10 씩 흔들리면
  그 차이는 우연히 생겼을 수 있습니다.

  그래서 '얼마나 차이 나는가' 만 보지 않고
  '흔들림에 비해 얼마나 차이 나는가' 를 봅니다.

  이 값이 1보다 크면 대체로 눈에 띄는 차이입니다.
  (전문 용어로는 효과크기라고 하는데, 이름은 몰라도 됩니다)
""")


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week14/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) 차이 ÷ 퍼짐 이 0.3 이면 무엇이라고 말해야 하나요?
#   2) 판 수를 두 배로 늘리면 이 값이 커지나요?


# 여기에 답을 써 보세요

