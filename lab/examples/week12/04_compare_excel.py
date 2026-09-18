# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  12주 · 04. my_cv( ) - 엑셀 값과 대조 ★
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     11주에 엑셀로 구한 값과 방금 코드로 구한 값을 나란히 놓고 대조합니다. 이 대조가 이번 학기의 핵심 장면입니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     lab/w12_basic.py · lab/check.py
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 1주 f"..." - 값을 끼워 넣는 문자열
#     · 2주 len( ) - 개수 세기
#     · 2주 for - 하나씩 꺼내 반복
#     · 2주 .items( ) - 이름표와 값을 짝지어
#     · 4주 in - 안에 있나 묻기
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week12   →   python 04_compare_excel.py
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

# %% [1] 내 계산
from w12_basic import load_csv, column
#    └ lab/w12_basic.py 를 불러옵니다

values = column(load_csv(), "수율")


def my_mean(v):
    return sum(v) / len(v)


def my_stdev(v):
    m = my_mean(v)
    return (sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** 0.5


def my_cv(v):
    """변동계수(%) - 단위가 다른 두 지표의 불안정함을 견줄 때 씁니다."""
    return my_stdev(v) / my_mean(v) * 100


mine_values = {"개수": len(values), "평균": my_mean(values),
        "표준편차": my_stdev(values), "변동계수": my_cv(values)}
for k, v in mine_values.items():
    print(f"{k:<10} {v:.4f}")

# %% [2] ✏️ 11주에 엑셀에서 구한 값을 적으세요
excel_values = {
    "평균": 0.0,        # ✏️ =AVERAGE
    "표준편차": 0.0,     # ✏️ =STDEV.S
}

for k, excel in excel_values.items():
    mine = mine_values[k]
    same = abs(mine - excel) < 0.01
    print(f"{k:<10} 내 {mine:>10.4f}   엑셀 {excel:>10.4f}   "
          f"{'같음' if same else '★ 다름'}")

# %% [3] 다르면
print("""
확인할 것
  · n 이 아니라 n-1 로 나눴나요?  (엑셀은 =STDEV.S)
  · 엑셀에서 같은 컬럼을 보고 있나요?
  · 빈 칸이 섞여 있지 않나요?
  · 게임의 📊 통계 지표 보기 값과도 비교해 보세요 (셋이 같아야 합니다)
""")


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week12/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) 변동계수는 왜 % 인가요? 언제 쓰나요?
#   2) 엑셀 값과 0.01 이상 차이 나면 무엇부터 확인하나요?


# 여기에 답을 써 보세요

