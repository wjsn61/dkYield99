# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  7주 · 03. 피드백 루프 찾기
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     두 지표를 12달 나란히 따라가며, 한쪽이 다른 쪽을 밀어 올리는지 봅니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     server/app/engine/process_engine.py › end_turn()
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 1주 f"..." - 값을 끼워 넣는 문자열
#     · 2주 for - 하나씩 꺼내 반복
#     · 4주 in - 안에 있나 묻기
#     · 5주 range( ) - 정해진 횟수만큼
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week07   →   python 03_feedback_loop.py
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

# %% [1] 두 지표를 나란히 따라갑니다
from app.engine.process_engine import new_plant, end_turn
#    └ server/app/engine/process_engine.py 를 불러옵니다 (7주 import)

plant = new_plant(seed=42)
print(f"{'달':>4}{'예산':>12}{'수율':>12}")
print("-" * 28)
for t in range(1, 13):
    end_turn(plant)
    print(f"{t:>4}{plant['예산']:>12.1f}{plant['수율']:>12.2f}")

# %% [2] 변화량으로 보면 더 잘 보입니다
plant = new_plant(seed=42)
prev = (plant["예산"], plant["수율"])
print(f"\n{'달':>4}{'예산 변화':>14}{'수율 변화':>14}")
print("-" * 32)
for t in range(1, 13):
    end_turn(plant)
    now = (plant["예산"], plant["수율"])
    print(f"{t:>4}{now[0] - prev[0]:>+14.2f}{now[1] - prev[1]:>+14.2f}")
    prev = now

# %% [3] 생각해 볼 것
print("""
★ 한쪽이 먼저 움직이고 다른 쪽이 따라가나요? 같이 움직이나요?
  화살표로 그림을 그려 보세요 - 그게 이번 주 과제입니다.
""")


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week07/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) 두 지표 중 어느 쪽이 먼저 움직이나요?
#   2) 화살표 그림을 그린다면 어떤 고리가 되나요?


# 여기에 답을 써 보세요

