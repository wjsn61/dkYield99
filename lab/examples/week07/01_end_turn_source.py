# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  7주 · 01. import · inspect - 한 턴의 코드 읽기
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     '달 종료' 버튼 하나가 어떤 함수들을 차례로 부르는지 소스에서 확인합니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     server/app/engine/process_engine.py › end_turn()
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 2주 for - 하나씩 꺼내 반복
#     · 2주 sorted( ) - 줄 세우기
#     · 4주 in - 안에 있나 묻기
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week07   →   python 01_end_turn_source.py
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

# %% [1] 그 함수를 통째로 봅니다
import inspect
from app.engine.process_engine import end_turn
#    └ server/app/engine/process_engine.py 를 불러옵니다 (7주 import)

source_text = inspect.getsource(end_turn)
print(source_text)

# %% [2] 여기서 부르는 이름들만 골라 보기
import re                       # re : 글자 패턴 찾기 도구

called_names = sorted(set(re.findall(r"(\w+)\(", source_text)))   # set( ) : 중복 없애기
print("여기서 ( ) 가 붙은 이름들:")
for name in called_names:
    print(" -", name)

# %% [3] 그중 진짜 함수는
print("""
min, max, round, len 같은 것은 파이썬이 원래 갖고 있는 것입니다.
나머지가 이 게임이 직접 만든 함수입니다.
그 이름들을 순서대로 적어 보세요 - 그게 한 달의 흐름입니다.
""")


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week07/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) 여기서 부르는 이름 중 파이썬이 원래 갖고 있는 것을 골라 보세요.
#   2) import 를 이번 주에 처음 썼습니다. 1~6주에는 왜 안 썼을까요?


# 여기에 답을 써 보세요

