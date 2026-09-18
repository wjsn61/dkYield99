# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  10주 · 01. csv.DictWriter - CSV 로 남기기
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     프로그램이 만든 값을 파일로 저장합니다. csv 모듈로 쓰고, 왜 utf-8-sig 로 저장해야 하는지 확인합니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     server/app/export_csv.py
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 2주 for - 하나씩 꺼내 반복
#     · 2주 리스트 컴프리헨션 - [ ... for ... ]
#     · 4주 in - 안에 있나 묻기
#     · 5주 range( ) - 정해진 횟수만큼
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week10   →   python 01_write_csv.py
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

# %% [1] 프로그램이 만든 값은 끄면 사라집니다
values = [1, 2, 3]
print("지금은 있습니다:", values)
print("창을 닫으면 사라집니다. 남기려면 파일로 써야 합니다.")

# %% [2] 파일로 씁니다
import csv                             # csv : 쉼표로 나뉜 표 파일 다루기

out_path = os.path.join(HERE, "_out", "연습.csv")
os.makedirs(os.path.dirname(out_path), exist_ok=True)   # 폴더가 없으면 만들기

rows = [{"달": t, "수율": 80 + t * 0.5} for t in range(1, 6)]

with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
    # "w" : 새로 쓰기 (기존 내용은 지워집니다). "a" 는 뒤에 덧붙이기
    # utf-8-sig : 엑셀이 한글을 알아보게 하는 표시(BOM)를 붙여 저장
    # newline="" : 윈도우에서 빈 줄이 끼는 것을 막습니다
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()                    # 첫 줄 = 컬럼 이름
    w.writerows(rows)

print("저장:", out_path)

# %% [3] 어디에 저장했나 - 중요합니다
print("""
★ lab/data 가 아니라 examples/_out 에 썼습니다.

  lab/data          게임이 만든 '진짜 데이터' 자리
  examples/_out     예제가 연습으로 만든 것 (지워도 됨)

  연습 파일을 data 에 두면, 12주에 load_csv( ) 가
  그 연습 파일을 집어서 엉뚱한 숫자로 과제를 하게 됩니다.
""")


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week10/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) utf-8-sig 대신 utf-8 로 저장하면 엑셀에서 어떻게 되나요?
#   2) 행을 10개로 늘려 저장해 보세요.


# 여기에 답을 써 보세요

