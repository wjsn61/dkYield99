# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  13주 · 01. histogram( ) 직접 만들기 ★
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     값을 구간으로 나눠 세는 것이 도수분포표이고, 그것을 막대로 세운 것이 히스토그램입니다. 게임 화면의 그림과 모양이
#     같은지 맞춰 봅니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     server/app/statistics_lab.py › histogram()
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 1주 f"..." - 값을 끼워 넣는 문자열
#     · 1주 str( ) · float( ) · int( ) - 종류 바꾸기
#     · 2주 len( ) - 개수 세기
#     · 2주 for - 하나씩 꺼내 반복
#     · 2주 min( ) · max( ) - 가장 작은/큰 것
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week13   →   python 01_histogram.py
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
mean_value = sum(values) / len(values)
print(f"{len(values)}개, 평균 {mean_value:.2f}")

# %% [2] 구간을 나눠 셉니다 - 이게 전부입니다
def histogram(values, bins=8):
    lo, hi = min(values), max(values)
    width = (hi - lo) / bins or 1        # or 1 : 모두 같은 값이면 0이 되니까
    # 경계는 한 번만 계산해 둡니다.
    # lo+3*w+w 와 lo+4*w 는 소수점 아래에서 살짝 달라서, 그대로 찍으면
    # 앞 칸의 끝과 뒷 칸의 시작이 어긋나 보입니다.
    edges = [lo + width * i for i in range(bins + 1)]
    counts = [0] * bins                  # [0,0,0,...] 칸 수만큼
    for v in values:
        i = min(int((v - lo) / width), bins - 1)   # 몇 번째 칸인지
        counts[i] += 1                             # += 는 '더해서 다시 담기'
    return edges, counts


edges, counts = histogram(values)
for i, n in enumerate(counts):
    print(f"{edges[i]:8.2f} ~ {edges[i + 1]:8.2f}  {'■' * n:<20} {n}")

# ★ 게임의 📊 통계 지표 보기 히스토그램과 모양이 같아야 합니다.

# %% [3] 칸 수를 바꿔 보면
for bins in (4, 8, 20):
    _, c = histogram(values, bins)
    print(f"bins={bins:>3}  {c}")
print("\n같은 데이터인데 인상이 달라집니다. 칸 수도 '선택' 입니다.")


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week13/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) bins 를 4 로, 20 으로 바꿔 보고 무엇이 달라지는지 적어 보세요.
#   2) 경계를 edges 로 미리 계산한 이유는?


# 여기에 답을 써 보세요

