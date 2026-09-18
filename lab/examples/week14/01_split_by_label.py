# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  14주 · 01. glob( ) - 라벨로 두 무리 나누기
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     성공/실패 라벨이 붙은 CSV 를 찾아 두 리스트로 나눕니다. 라벨이 없으면 어떻게 만드는지 안내합니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     server/app/persistence.py (라벨)
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 1주 f"..." - 값을 끼워 넣는 문자열
#     · 1주 str( ) · float( ) · int( ) - 종류 바꾸기
#     · 2주 len( ) - 개수 세기
#     · 2주 for - 하나씩 꺼내 반복
#     · 2주 sorted( ) - 줄 세우기
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week14   →   python 01_split_by_label.py
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

# %% [1] 라벨이 붙은 CSV 찾기
import csv
import glob                    # glob : 이름 패턴으로 파일 찾기

candidates = []
for f in sorted(glob.glob(os.path.join(LAB, "data", "*.csv"))):
    with open(f, encoding="utf-8-sig", newline="") as fp:
        r = list(csv.DictReader(fp))
    # 라벨 컬럼이 있고, 성공과 실패가 둘 다 들어 있는 파일만
    if r and "라벨" in r[0] and {"성공", "실패"} <= {x.get("라벨") for x in r}:
        candidates.append((f, r))     # <= 는 '왼쪽이 오른쪽에 다 들어 있나'

if candidates:
    path, rows = candidates[-1]
    print("쓸 파일:", os.path.basename(path), f"({len(rows)}판)")
else:
    print("""★ 라벨 붙은 CSV 가 없습니다.

  게임 → 💾 저장·불러오기 → 🧪 예시 데이터 만들기
       → 📥 판별 요약 CSV

  (과제에는 반드시 여러분이 직접 저장한 판을 쓰세요)""")
    rows = []

# %% [2] 두 리스트로 나눕니다
def pick_values(rows, label, name):
    out = []
    for r in rows:
        if r.get("라벨") != label:      # != 는 '같지 않다'
            continue
        for c in (name, f"최종_{name}", f"평균_{name}"):
            if c in r:
                try:
                    out.append(float(r[c]))
                except (TypeError, ValueError):
                    pass                 # 숫자로 못 읽으면 그냥 넘어감
                break
    return out


good = pick_values(rows, "성공", "수율")
bad = pick_values(rows, "실패", "수율")
print(f"성공 {len(good)}판, 실패 {len(bad)}판")


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week14/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) 라벨이 '미정' 인 판은 왜 비교에서 빼나요?
#   2) 성공과 실패의 판 수가 크게 다르면 무엇을 조심해야 하나요?


# 여기에 답을 써 보세요

