# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  11주 · 01. pathlib.Path · .glob( ) - CSV 는 그냥 글자
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     CSV 파일을 열어 글자 그대로 찍어 봅니다. 엑셀도 파이썬도 이 글자를 읽는 도구일 뿐이라는 것을 확인합니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     lab/data/*.csv
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
#     터미널  : cd lab\examples\week11   →   python 01_csv_is_text.py
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

# %% [1] 가장 최근 CSV 를 글자 그대로
from pathlib import Path         # pathlib : 경로를 편하게 다루는 도구

folder = Path(LAB) / "data"        # / 로 경로를 이어붙일 수 있습니다
files = sorted(folder.glob("*.csv"), key=lambda p: p.stat().st_mtime)
# glob("*.csv") : 확장자가 csv 인 것 모두.  st_mtime : 마지막 수정 시각

if not files:
    raise SystemExit("data 폴더에 CSV 가 없습니다.\n"
                     "게임에서 [📊 통계 지표 보기 → 📥 엑셀용 CSV] 를 먼저 누르세요.")

latest = files[-1]
print("파일:", latest.name, "\n")
print(latest.read_text(encoding="utf-8-sig")[:400])   # 앞 400글자만

# %% [2] 첫 줄이 컬럼 이름입니다
header_line = latest.read_text(encoding="utf-8-sig").splitlines()[0]
print(f"컬럼 {len(header_line.split(','))}개:")
for name in header_line.split(","):     # split(",") : 쉼표로 쪼개기
    print(" -", name)

# 엑셀에서 이 파일을 더블클릭하면, 저 쉼표가 칸 나눔이 됩니다.


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week11/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) 컬럼이 몇 개인가요? 그중 숫자 컬럼은 몇 개일까요?
#   2) CSV 를 메모장으로 열어 보세요. 엑셀에서 본 것과 같은 내용인가요?


# 여기에 답을 써 보세요

