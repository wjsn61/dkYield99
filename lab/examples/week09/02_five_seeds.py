# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  9주 · 02. zip( ) - 같은 전략, 시드만 바꿔 5번
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     똑같이 해도 결과가 매번 다르다는 것을 표와 막대로 눈에 보이게 만듭니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     server/app/engine/noise.py
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 1주 f"..." - 값을 끼워 넣는 문자열
#     · 1주 str( ) · float( ) · int( ) - 종류 바꾸기
#     · 2주 for - 하나씩 꺼내 반복
#     · 2주 min( ) · max( ) - 가장 작은/큰 것
#     · 2주 리스트 컴프리헨션 - [ ... for ... ]
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week09   →   python 02_five_seeds.py
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

# %% [1] 다섯 번 돌립니다
from app.engine.process_engine import new_plant, end_turn
#    └ server/app/engine/process_engine.py 를 불러옵니다 (7주 import)


def one_run(seed):
    s = new_plant(seed=seed)
    for _ in range(12):
        end_turn(s)
    return s["수율"]


seeds = [1, 2, 3, 4, 5]
result = [one_run(s) for s in seeds]

for s, v in zip(seeds, result):     # zip( ) : 두 목록을 짝지어 함께 꺼내기
    print(f"  seed {s}  →  {v:.2f} %")

# %% [2] 막대로 그려 보면 차이가 보입니다
lowest = min(result)
for s, v in zip(seeds, result):
    bar = "■" * int((v - lowest) * 4 + 1)     # 차이를 4배 키워 막대 길이로
    print(f"  {s}  {bar:<28} {v:.2f}")

# ✏️ 해 보기
#    시드를 10개로 늘려 보세요.  시드들 = list(range(1, 11))


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week09/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) 시드를 10개로 늘려 보세요. 차이가 더 커지나요?
#   2) 다섯 번의 평균을 구해 보세요.


# 여기에 답을 써 보세요

