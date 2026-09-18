# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  8주 · 02. continue - 계획대로 끝까지 돌려 보기
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     내 계획대로 카드 을(를) 시행하고 12개월 을(를) 진행시켜 결과를 봅니다. seed 를 고정해야 계획끼리
#     공정하게 비교됩니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     server/app/engine/process_engine.py
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 1주 f"..." - 값을 끼워 넣는 문자열
#     · 1주 round( ) - 반올림
#     · 2주 for - 하나씩 꺼내 반복
#     · 4주 if / else - 조건에 따라 갈라지기
#     · 4주 in - 안에 있나 묻기
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week08   →   python 02_run_full_game.py
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

# %% [1] 내 계획을 적습니다
from app.engine.process_engine import new_plant, enact_card, end_turn
#    └ server/app/engine/process_engine.py 를 불러옵니다 (7주 import)
from app.cards import load_cards
#    └ server/app/cards/ 를 불러옵니다 (7주 import)

deck = load_cards()
by_id = {p["아이디"]: p for p in deck}       # 아이디로 바로 찾을 수 있게
my_plan = ["reactor_temp_up", "pressure_up"]          # ✏️ 내 것으로 바꾸세요

# %% [2] 시행하고 12개월 진행
plant = new_plant(seed=42)                          # seed 고정 = 공정한 비교
for card_id in my_plan:
    if card_id not in by_id:
        print(f"{card_id} - 그런 카드이(가) 없습니다")
        continue                                # continue : 이번 것만 건너뛰기
    good, message = enact_card(plant, by_id[card_id])
    print(f"{card_id:<20} {'OK' if good else 'X '} {message}")

for _ in range(12):
    end_turn(plant)

# %% [3] 결과
print()
for k in ['예산', '생산량', '수율', '순도', '안전지수']:
    print(f"{k:<12} {round(plant[k], 1)}")

# ✏️ 해 보기
#    계획을 바꿔 가며 어느 조합이 좋은지 찾아 보세요.
#    ★ seed 는 42 로 고정해야 '계획 때문' 인지 '운' 인지 구분됩니다.


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week08/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) 계획을 바꾸면 결과가 달라집니다. seed 는 왜 42 로 고정해야 하나요?
#   2) 같은 계획을 seed 43 으로 돌리면 결과가 같나요?


# 여기에 답을 써 보세요

