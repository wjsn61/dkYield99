# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  13주 · 03. IQR - 혼자 멀리 있는 값
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     사분위와 IQR 로 '보통 범위' 를 정하고 벗어난 값을 찾습니다. 이상치를 지우는 게 아니라 이유를 찾는 것이
#     핵심입니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     server/app/statistics_lab.py › outliers()
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 1주 f"..." - 값을 끼워 넣는 문자열
#     · 1주 round( ) - 반올림
#     · 2주 len( ) - 개수 세기
#     · 2주 for - 하나씩 꺼내 반복
#     · 2주 sorted( ) - 줄 세우기
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week13   →   python 03_outliers.py
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

# %% [1] 사분위 - 줄 세워 4등분한 지점
from w12_basic import load_csv, column
#    └ lab/w12_basic.py 를 불러옵니다

values = column(load_csv(), "수율")
ordered = sorted(values)
n = len(ordered)
Q1 = ordered[n // 4]              # 아래에서 1/4 지점
Q3 = ordered[(3 * n) // 4]        # 아래에서 3/4 지점
IQR = Q3 - Q1                  # 가운데 절반이 차지하는 폭

print(f"Q1 {Q1:.2f}   Q3 {Q3:.2f}   IQR {IQR:.2f}")

# %% [2] 보통 범위 - 관례로 IQR 의 1.5배까지
low_edge, high_edge = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
print(f"보통 범위: {low_edge:.2f} ~ {high_edge:.2f}")

outliers = [v for v in values if v < low_edge or v > high_edge]
print("벗어난 값:", [round(v, 2) for v in outliers] if outliers else "없음")

# %% [3] 그래서 어떻게 하나
print("""
★ 이상치는 지우는 게 아니라 '왜 생겼는지 찾는 것' 입니다.

  · 그때 무엇을 했는지 게임 로그에서 찾아보세요
  · 재는 방법이 잘못됐을 수도 있습니다
  · 진짜로 특별한 일이 있었을 수도 있습니다

  이유를 모른 채 지우면, 그건 데이터 조작입니다.
""")

# ✏️ 해 보기
#    1.5 를 3.0 으로 바꾸면 몇 개가 남나요? 이 숫자도 '선택' 입니다.


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week13/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) 1.5 를 3.0 으로 바꾸면 이상치가 몇 개 남나요?
#   2) 이상치를 지우고 평균을 내면 왜 위험한가요?


# 여기에 답을 써 보세요

