# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  10주 · 02. csv.DictReader · float( ) - 다시 읽기
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     저장한 CSV 를 다시 읽습니다. 읽으면 모두 '글자' 라서 숫자로 바꿔야 계산된다는 것을 확인합니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     server/app/export_csv.py
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 1주 type( ) - 무슨 종류인지
#     · 1주 str( ) · float( ) · int( ) - 종류 바꾸기
#     · 2주 len( ) - 개수 세기
#     · 2주 for - 하나씩 꺼내 반복
#     · 4주 if / else - 조건에 따라 갈라지기
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week10   →   python 02_read_csv.py
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

# %% [1] 방금 쓴 파일을 읽습니다
import csv

path = os.path.join(HERE, "_out", "연습.csv")
if not os.path.exists(path):
    raise SystemExit("01_write_csv.py 를 먼저 실행하세요.")

with open(path, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))     # 한 줄이 딕셔너리 하나가 됩니다

for row in rows:
    print(row)

# %% [2] ★ 읽으면 전부 '글자' 입니다
first_value = rows[0]["수율"]
print(first_value, type(first_value))               # str - 따옴표가 붙은 글자
print(float(first_value), type(float(first_value)))  # float( ) 로 숫자로 바꿔야 계산됩니다

# %% [3] 한 컬럼을 숫자 리스트로
values = [float(row["수율"]) for row in rows]
print(values)
print("합계 ÷ 개수 =", sum(values) / len(values))

# %% [4] float( ) 을 빼면
try:
    text_values = [row["수율"] for row in rows]
    print(sum(text_values))
except TypeError as e:
    print("에러:", e)
    print("→ 글자는 더할 수 없습니다. 12주에 이 실수를 많이 합니다.")


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week10/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) float( ) 을 빼고 sum( ) 을 하면 어떤 에러가 나나요?
#   2) 읽어 온 값의 최대·최소를 구해 보세요.


# 여기에 답을 써 보세요

