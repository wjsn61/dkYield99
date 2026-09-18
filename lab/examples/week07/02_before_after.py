# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  7주 · 02. dict comprehension - 한 턴 전후 비교
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     아무 카드 도 쓰지 않고 한 달 만 진행시켜, 저절로 움직이는 값을 봅니다.
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
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week07   →   python 02_before_after.py
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

# %% [1] 진행 전 상태를 적어 둡니다
from app.engine.process_engine import new_plant, end_turn
#    └ server/app/engine/process_engine.py 를 불러옵니다 (7주 import)

plant = new_plant(seed=42)
before = {k: plant[k] for k in ['예산', '생산량', '수율', '순도', '안전지수']}     # 딕셔너리 컴프리헨션 - 필요한 것만 베끼기

# %% [2] 한 달 진행
end_turn(plant)
after = {k: plant[k] for k in ['예산', '생산량', '수율', '순도', '안전지수']}

# %% [3] 나란히 놓고 봅니다
print(f"{'지표':<12}{'전':>10}{'후':>10}{'변화':>10}")
print("-" * 44)
for k in before:
    print(f"{k:<12}{before[k]:>10.1f}{after[k]:>10.1f}{after[k] - before[k]:>+10.2f}")

# ✏️ 해 보기
#    아무것도 안 했는데 왜 값이 변할까요?
#    (촉매 활성 저하 · 원료 변동 · 자연 변동 - 소스에서 찾아보세요)


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week07/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) 아무것도 안 했는데 왜 값이 변하나요? 소스에서 이유를 찾아보세요.
#   2) 두 턴을 진행하면 변화량이 첫 턴과 같은가요?


# 여기에 답을 써 보세요

