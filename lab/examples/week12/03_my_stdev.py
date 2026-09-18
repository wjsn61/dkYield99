# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  12주 · 03. my_stdev( ) 직접 만들기 ★★  (n-1)
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     표준편차를 한 단계씩 쪼개 만듭니다. n 이 아니라 n-1 로 나누는 이유와 그 차이가 얼마인지 눈으로 확인합니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     lab/w12_basic.py › my_stdev()
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
#     터미널  : cd lab\examples\week12   →   python 03_my_stdev.py
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

# %% [1] 재료
from w12_basic import load_csv, column
#    └ lab/w12_basic.py 를 불러옵니다

values = column(load_csv(), "수율")


def my_mean(v):
    return sum(v) / len(v)


# %% [2] 한 단계씩 - 편차 → 제곱 → 평균 → 제곱근
m = my_mean(values)
deviations = [v - m for v in values]           # 평균에서 얼마나 떨어졌나
squares = [d ** 2 for d in deviations]          # ** 는 거듭제곱. 음수를 없애려고 제곱
variance = sum(squares) / (len(values) - 1)     # ★ n 이 아니라 n-1 (자유도)
sd = variance ** 0.5                 # 0.5 제곱 = 제곱근

print(f"평균      {m:.4f}")
print(f"편차 예시  {[round(d, 2) for d in deviations[:5]]}")
print(f"분산      {variance:.4f}")
print(f"표준편차   {sd:.4f}")

# %% [3] 함수로 묶기
def my_stdev(values):
    m = my_mean(values)
    var = sum((v - m) ** 2 for v in values) / (len(values) - 1)
    return var ** 0.5


print(my_stdev(values))

# %% [4] ★ n 으로 나누면 얼마나 다른가
sd_with_n = (sum((v - m) ** 2 for v in values) / len(values)) ** 0.5
print(f"n-1 로 나눔 : {my_stdev(values):.4f}   ← 엑셀 =STDEV.S")
print(f"n   로 나눔 : {sd_with_n:.4f}   ← 엑셀 =STDEV.P")
print(f"차이       : {my_stdev(values) - sd_with_n:.4f}")
print("\n엑셀 값과 안 맞으면 대개 이것 때문입니다.")

# %% [5] 왜 n-1 인가 (알아만 두기)
print("""
우리가 가진 것은 '전부' 가 아니라 '일부(표본)' 입니다.
표본으로 구한 평균은 그 표본에 맞춰져 있어서, 흩어짐이 실제보다
조금 작게 나옵니다. n 대신 n-1 로 나눠 그만큼을 보정합니다.
  → 이 이유까지는 시험에 내지 않습니다. n-1 을 쓴다는 것만 기억하세요.
""")


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week12/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) n 으로 나눈 값과 n-1 로 나눈 값 중 어느 쪽이 큰가요? 왜일까요?
#   2) 값이 모두 같으면 표준편차가 얼마인가요?


# 여기에 답을 써 보세요

