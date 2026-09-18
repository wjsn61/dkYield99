# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  15주 · 02. 발표 숫자는 내 코드가 낸 것으로
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     최종 데이터에 내 함수를 다시 돌려 숫자를 확정하고, 게임 화면 값과 대조합니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     lab/w12_basic.py
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
#     터미널  : cd lab\examples\week15   →   python 02_my_numbers.py
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

# %% [1] 내 함수로 다시 계산합니다
from w12_basic import load_csv, column
#    └ lab/w12_basic.py 를 불러옵니다


def my_mean(v):
    return sum(v) / len(v)


def my_stdev(v):
    m = my_mean(v)
    return (sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** 0.5


rows = load_csv()
values = column(rows, "수율")
print(f"수율   n={len(values)}")
print(f"  평균      {my_mean(values):.3f} %")
print(f"  표준편차   {my_stdev(values):.3f}")

# %% [2] 게임 화면과 맞춰 보기
screen_mean = 0.0        # ✏️ 📊 통계 지표 보기 에 나온 값
screen_sd = 0.0     # ✏️

for name, mine, screen in (("평균", my_mean(values), screen_mean),
                       ("표준편차", my_stdev(values), screen_sd)):
    ok = abs(mine - screen) < 0.05
    print(f"{name:<8} 내 {mine:>10.3f}   화면 {screen:>10.3f}   "
          f"{'같음' if ok else '★ 확인 필요'}")

print("\n★ 발표에 쓰는 숫자는 '내 코드가 낸 숫자' 여야 합니다.")


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week15/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) 화면 값과 내 코드 값이 다르면 어느 쪽을 발표에 쓰나요?
#   2) 발표에 '내 코드가 낸 숫자' 를 쓰라는 이유는?


# 여기에 답을 써 보세요

