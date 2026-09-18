# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  15주 · 01. 내 데이터는 어떻게 만들어졌나
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     발표 첫 장에 들어갈 내용입니다. 시드·판 수·라벨 기준을 확인하고 한 문단으로 적습니다.
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 1주 f"..." - 값을 끼워 넣는 문자열
#     · 2주 len( ) - 개수 세기
#     · 2주 for - 하나씩 꺼내 반복
#     · 2주 sorted( ) - 줄 세우기
#     · 4주 if / else - 조건에 따라 갈라지기
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week15   →   python 01_dataset_spec.py
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

# %% [1] 무엇으로 말할 것인지 확정합니다
from w12_basic import load_csv, numeric_columns
#    └ lab/w12_basic.py 를 불러옵니다

rows = load_csv()
print(f"행 수      : {len(rows)}")
print(f"숫자 컬럼  : {numeric_columns(rows)[:10]}")

seeds = sorted({r.get("시드") for r in rows if r.get("시드")})
labels = sorted({r.get("라벨") for r in rows if r.get("라벨")})
print(f"시드       : {seeds[:12] if seeds else '(컬럼 없음)'}")
print(f"라벨       : {labels if labels else '(없음)'}")

# %% [2] ✏️ 한 문단으로 적습니다 - 발표 1번 항목
dataset_note = """
"""      # ✏️ 시드 / 판 수 / 라벨 기준 / 무엇을 어떻게 쟀는지

if dataset_note.strip():
    print(dataset_note.strip())
else:
    print("★ 아직 비어 있습니다. 이게 발표 1번 항목입니다.")


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week15/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) 데이터 설명에 반드시 들어가야 할 세 가지는?
#   2) 시드 컬럼이 없는 CSV 를 냈다면 어떻게 되나요?


# 여기에 답을 써 보세요

