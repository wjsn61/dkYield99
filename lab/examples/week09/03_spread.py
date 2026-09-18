# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  9주 · 03. max( ) - min( ) - 얼마나 흩어졌나
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     열 번 돌린 결과의 최대·최소 차이를 봅니다. 이 '흩어짐' 이 후반부의 주제입니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     server/app/engine/noise.py
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 1주 f"..." - 값을 끼워 넣는 문자열
#     · 1주 round( ) - 반올림
#     · 2주 for - 하나씩 꺼내 반복
#     · 2주 min( ) · max( ) - 가장 작은/큰 것
#     · 2주 리스트 컴프리헨션 - [ ... for ... ]
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week09   →   python 03_spread.py
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

# %% [1] 열 번 돌려 모읍니다
from app.engine.process_engine import new_plant, end_turn
#    └ server/app/engine/process_engine.py 를 불러옵니다 (7주 import)


def one_run(seed):
    s = new_plant(seed=seed)
    for _ in range(12):
        end_turn(s)
    return s["수율"]


result = [one_run(s) for s in range(1, 11)]
print([round(v, 2) for v in result])

# %% [2] 가장 크고 작은 값의 차이
print(f"가장 큼   {max(result):.2f}")
print(f"가장 작음 {min(result):.2f}")
print(f"차이      {max(result) - min(result):.2f} %")

# %% [3] 생각해 볼 것
print("""
★ 이만큼이 '운' 이었다면,
  한 번만 돌려 보고 "이 방법이 좋다" 고 말한 친구의 결론을
  믿을 수 있을까요?

  이 흩어짐이 이번 학기 후반부의 주제입니다.
  아직 계산하지 않습니다. 눈으로만 봅니다.
""")


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week09/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) 이 흩어짐 안에서 '가장 좋은 시드' 를 골라 보고하면 왜 안 되나요?
#   2) 평균과 중앙값을 함께 구해 견줘 보세요.


# 여기에 답을 써 보세요

