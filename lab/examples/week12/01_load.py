# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  12주 · 01. load_csv( ) · column( ) - CSV 를 숫자로
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     lab 폴더의 도구(w12_basic)를 써서 CSV 를 읽고, 어떤 숫자 컬럼이 있는지 확인합니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     lab/w12_basic.py
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 1주 f"..." - 값을 끼워 넣는 문자열
#     · 1주 round( ) - 반올림
#     · 2주 len( ) - 개수 세기
#     · 2주 for - 하나씩 꺼내 반복
#     · 2주 리스트 컴프리헨션 - [ ... for ... ]
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week12   →   python 01_load.py
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

# %% [1] lab 의 도구를 그대로 씁니다
from w12_basic import load_csv, column, numeric_columns
#    └ lab/w12_basic.py 를 불러옵니다
# load_csv( )       : data 폴더의 가장 최근 CSV 를 읽어 줍니다
# column(행들,이름) : 한 컬럼을 숫자 리스트로
# numeric_columns( ): 숫자로 읽히는 컬럼 목록

rows = load_csv()
print(f"{len(rows)}행")

# %% [2] 어떤 숫자 컬럼이 있나
print(numeric_columns(rows))

# %% [3] 한 컬럼만 뽑기
values = column(rows, "수율")
print(f"수율  {len(values)}개")
print([round(v, 2) for v in values[:8]], "…")

# ※ 파일 종류에 따라 컬럼 이름이 "수율" 이기도 하고 "최종_수율" 이기도 합니다.
#   column( ) 이 알아서 둘 다 찾아 줍니다.


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week12/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) numeric_columns( ) 에 안 나오는 컬럼은 왜 빠졌을까요?
#   2) 다른 컬럼을 뽑아 개수를 세어 보세요.


# 여기에 답을 써 보세요

