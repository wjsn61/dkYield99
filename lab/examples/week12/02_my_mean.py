# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  12주 · 02. my_mean( ) 직접 만들기 ★
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     평균 함수를 직접 만들고, 파이썬이 갖고 있는 statistics.mean 과 값이 같은지 대조합니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     lab/w12_basic.py › my_mean()
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 1주 f"..." - 값을 끼워 넣는 문자열
#     · 2주 len( ) - 개수 세기
#     · 2주 for - 하나씩 꺼내 반복
#     · 4주 in - 안에 있나 묻기
#     · 5주 sum( ) - 합계
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week12   →   python 02_my_mean.py
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
print(f"{len(values)}개")

# %% [2] ✏️ 직접 만듭니다
def my_mean(values):
    """평균 = 모두 더해서 개수로 나눈다."""
    return sum(values) / len(values)


print("내 계산 :", my_mean(values))

# %% [3] 파이썬이 갖고 있는 것과 대조
import statistics                       # statistics : 파이썬 기본 통계 도구

print("statistics:", statistics.mean(values))
print("같나요?", abs(my_mean(values) - statistics.mean(values)) < 1e-9)
#              abs( ) : 절댓값.  1e-9 = 0.000000001 (소수점 오차 감안)

# %% [4] sum( ) 없이 만들어 보기
def my_mean2(values):
    total = 0
    for v in values:
        total = total + v
    return total / len(values)


print(my_mean2(values), "←  같은 값이어야 합니다")


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week12/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) sum( ) 없이 for 문으로 평균을 구해 보세요.
#   2) statistics.mean 과 값이 다르면 무엇을 의심해야 하나요?


# 여기에 답을 써 보세요

