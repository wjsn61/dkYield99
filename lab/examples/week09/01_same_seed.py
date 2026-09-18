# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  9주 · 01. seed - 같은 씨앗이면 같은 세상
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     seed 를 주면 몇 번을 돌려도 같은 결과가 나온다는 것을 확인합니다. 재현성이 이 과목 평가의 기준이라 가장
#     중요한 개념입니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     server/app/engine/noise.py
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 1주 round( ) - 반올림
#     · 2주 for - 하나씩 꺼내 반복
#     · 4주 in - 안에 있나 묻기
#     · 5주 range( ) - 정해진 횟수만큼
#     · 6주 def - 함수 만들기
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week09   →   python 01_same_seed.py
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

# %% [1] 시작할 때는 시드가 달라도 똑같습니다
from app.engine.process_engine import new_plant
#    └ server/app/engine/process_engine.py 를 불러옵니다 (7주 import)

a = new_plant(seed=7)
b = new_plant(seed=7)
c = new_plant(seed=8)

print("seed 7 vs 7 :", a["수율"] == b["수율"])   # == : 같은지 묻기
print("seed 7 vs 8 :", a["수율"] == c["수율"])

# ★ 둘 다 True 입니다. 놀랐나요? 이게 맞습니다.
#   new_plant( ) 안의 시작 숫자는 그냥 적혀 있는 값이라 시드와 상관없습니다.
#      "전환율": 85,  "선택도": 95,  ...      ← 게임 소스에 그대로 있습니다
#   시드는 "앞으로 흔들릴 방식" 을 정해 둘 뿐, 시작 숫자를 바꾸지 않습니다.
#   그러니 차이는 [2] 처럼 턴을 굴려야 나타납니다.

# %% [2] 끝까지 돌려도 그런가
from app.engine.process_engine import end_turn
#    └ server/app/engine/process_engine.py 를 불러옵니다 (7주 import)


def run_to_end(seed):
    s = new_plant(seed=seed)
    for _ in range(12):
        end_turn(s)
    return round(s["수율"], 4)


print("seed 7 두 번:", run_to_end(7), run_to_end(7))
print("seed 8      :", run_to_end(8))

# %% [3] 왜 중요한가
print("""
★ 시드를 적지 않은 결과는 아무도 다시 확인할 수 없습니다.
  확인할 수 없는 결과는 증거가 아닙니다.

  과제를 낼 때는 반드시 시드를 함께 적으세요.
  (재현 불가 제출물은 해당 과제 최대 70%)
""")


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week09/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) seed 를 안 주면(None) 어떻게 되나요?
#   2) 과제에 시드를 안 적으면 왜 감점인가요?


# 여기에 답을 써 보세요

