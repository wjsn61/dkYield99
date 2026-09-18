# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  12주 · 05. matplotlib - 히스토그램 그리기 (선택)
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     matplotlib 으로 히스토그램을 그려 파일로 저장합니다. install_stats.bat 을 실행하지 않았으면
#     건너뛰어도 됩니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     lab/w12_chart.py
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 6주 try / except - 에러가 나도 멈추지 않게
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week12   →   python 05_chart.py
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

# %% [1] matplotlib 이 있는지 먼저 확인
try:
    import matplotlib
except ImportError:                      # 그 라이브러리가 없을 때 나는 에러
    raise SystemExit("matplotlib 이 없습니다.\n"
                     "프로젝트 폴더의 install_stats.bat 을 실행하세요.\n"
                     "(없어도 12주의 나머지 실습은 전부 됩니다)")

matplotlib.use("Agg")        # 창을 띄우지 않고 파일로만 저장 (★ pyplot 앞에 와야 함)
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Malgun Gothic"   # 한글이 네모로 안 나오게
plt.rcParams["axes.unicode_minus"] = False      # 마이너스 기호가 깨지지 않게

# %% [2] 히스토그램 그리기
from w12_basic import load_csv, column
#    └ lab/w12_basic.py 를 불러옵니다

values = column(load_csv(), "수율")

fig, ax = plt.subplots(figsize=(6, 3.2))   # 그림 한 장과 그 안의 그래프 하나
ax.hist(values, bins=8, edgecolor="white")    # bins : 구간을 몇 칸으로 나눌지
ax.set_title("수율 분포")
ax.set_xlabel("수율 (%)")
ax.set_ylabel("개수")

saved_to = os.path.join(LAB, "figures", "week12_hist.png")
os.makedirs(os.path.dirname(saved_to), exist_ok=True)
fig.tight_layout()                          # 글자가 잘리지 않게 여백 정리
fig.savefig(saved_to, dpi=130)
plt.close(fig)                              # 다 쓴 그림은 닫아 줍니다
print("저장:", saved_to)

# ✏️ 해 보기
#    bins 를 4, 20 으로 바꿔 보세요.
#    같은 데이터인데 인상이 달라집니다 - 13주 이야기입니다.


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week12/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) bins 를 4 와 20 으로 바꿔 보세요. 같은 데이터인데 무엇이 달라지나요?
#   2) matplotlib.use("Agg") 를 pyplot 임포트 뒤로 옮기면 어떻게 되나요?


# 여기에 답을 써 보세요

