# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  13주 · 02. .index( ) - 평균은 봉우리 안에 있나
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     가장 높은 칸(봉우리)과 평균·중앙값의 위치를 견줍니다. 평균만 보고할 때 무엇이 가려지는지 확인합니다.
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
#     터미널  : cd lab\examples\week13   →   python 02_mean_vs_peak.py
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

# %% [1] 봉우리 찾기
from w12_basic import load_csv, column
#    └ lab/w12_basic.py 를 불러옵니다

values = column(load_csv(), "수율")
mean_value = sum(values) / len(values)


def histogram(values, bins=8):
    lo, hi = min(values), max(values)
    width = (hi - lo) / bins or 1
    edges = [lo + width * i for i in range(bins + 1)]
    counts = [0] * bins
    for v in values:
        counts[min(int((v - lo) / width), bins - 1)] += 1
    return edges, counts


edges, counts = histogram(values)
peak = counts.index(max(counts))     # .index( ) : 그 값이 몇 번째인지
print(f"가장 높은 칸: {edges[peak]:.2f} ~ {edges[peak + 1]:.2f}  ({max(counts)}개)")
print(f"평균        : {mean_value:.2f}")

# %% [2] 판정
inside = edges[peak] <= mean_value <= edges[peak + 1]   # 파이썬은 이렇게 이어 쓸 수 있습니다
print("평균이 봉우리 안에 있나요?", "예" if inside else "아니요")
if not inside:
    print("→ 한쪽으로 치우친 분포입니다. 평균만 보고하면 인상이 왜곡됩니다.")

# %% [3] 중앙값과도 견줍니다
ordered = sorted(values)
median_value = ordered[len(ordered) // 2]
print(f"평균 {mean_value:.2f}  vs  중앙값 {median_value:.2f}")
if mean_value > median_value:
    print("→ 평균이 더 큽니다. 큰 값 몇 개가 평균을 끌어올렸습니다.")
elif mean_value < median_value:
    print("→ 중앙값이 더 큽니다. 작은 값 몇 개가 평균을 끌어내렸습니다.")


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week13/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) 평균이 중앙값보다 크면 무슨 뜻인가요?
#   2) 평균이 봉우리 밖에 있으면 보고서에 무엇을 함께 적어야 하나요?


# 여기에 답을 써 보세요

