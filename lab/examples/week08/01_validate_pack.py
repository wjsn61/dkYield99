# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  8주 · 01. try / except - 내 팩이 검사를 통과하는지
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     카드 전체를 한 번에 검사하고, 비용이 어떻게 퍼져 있는지 훑어봅니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     server/app/cards/cards_data.py
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 1주 f"..." - 값을 끼워 넣는 문자열
#     · 1주 round( ) - 반올림
#     · 2주 len( ) - 개수 세기
#     · 2주 for - 하나씩 꺼내 반복
#     · 2주 .items( ) - 이름표와 값을 짝지어
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week08   →   python 01_validate_pack.py
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

# %% [1] 통째로 검사
from app.cards import load_cards
#    └ server/app/cards/ 를 불러옵니다 (7주 import)

try:
    deck = load_cards()
    print(f"검사 통과 - 카드 {len(deck)}장")
except Exception as e:
    print("검사에서 걸렸습니다:")
    print(" ", e)
    raise SystemExit                   # 여기서 멈춥니다

# %% [2] 비용이 어떻게 퍼져 있나
costs = sorted(p["비용"] for p in deck)
print("가장 싼  :", costs[0])
print("가장 비싼:", costs[-1])
print("평균     :", round(sum(costs) / len(costs), 1))

# %% [3] 분류별로 몇 장인지
by_category = {}
for p in deck:
    category = p.get("분류", "(없음)")
    by_category[category] = by_category.get(category, 0) + 1     # 없으면 0에서 시작해 +1
for category, n in sorted(by_category.items()):
    print(f"  {category:<10} {n}장")


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week08/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) 가장 비싼 것과 가장 싼 것의 차이는 얼마인가요?
#   2) 비용의 중앙값을 구해 보세요. (평균과 다른가요?)


# 여기에 답을 써 보세요

