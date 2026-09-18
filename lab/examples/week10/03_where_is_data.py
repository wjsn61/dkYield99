# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  10주 · 03. os.path - 내 데이터는 어디 있나
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     lab/data 폴더에 무엇이 쌓여 있는지 확인하고, 아직 없다면 어떻게 만드는지 안내합니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     server/app/persistence.py · lab/data/
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
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
#     터미널  : cd lab\examples\week10   →   python 03_where_is_data.py
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

# %% [1] 게임이 만든 CSV 들
data_dir = os.path.join(LAB, "data")
files = sorted(f for f in os.listdir(data_dir) if f.endswith(".csv")) \
    if os.path.isdir(data_dir) else []

print(f"lab/data 에 CSV {len(files)}개")
for f in files[-10:]:
    size = os.path.getsize(os.path.join(data_dir, f))
    print(f"  {f:<40} {size:>8,} B")

# %% [2] 아직 없다면
if not files:
    print("""
게임에서 만들어야 합니다.

  ① 판을 하고  💾 저장 · 불러오기  → 이름·라벨 붙여 저장
     → lab/data/<그 이름>.csv 가 함께 생깁니다
  ② 또는  📊 통계 지표 보기  →  📥 엑셀용 CSV
""")
else:
    print("\n알아볼 수 있는 이름으로 저장하세요. 나중에 그 이름으로 찾습니다.")


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week10/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) CSV 파일 이름만 보고 무슨 판인지 알 수 있나요?
#   2) 가장 큰 CSV 파일을 찾아 보세요.


# 여기에 답을 써 보세요

