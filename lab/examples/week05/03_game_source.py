# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  5주 · 03. 게임 소스 읽기 - apply_effect( ) 의 for
# ──────────────────────────────────────────────────────────────────────
#
#  ▣ 이 파일이 하는 일
#     효과를 지표에 하나씩 더하는 게임 소스를 그대로 옮겨 왔습니다. for 가 무엇을 꺼내 도는지 확인하고, 같은 것을
#     직접 만들어 봅니다.
#
#  ▣ 이 코드는 게임의 어느 소스와 관련 있나
#     server/app/engine/process_engine.py › apply_effect()
#     (VS Code 에서 그 파일을 열어 나란히 놓고 보세요)
#
#  ▣ 앞에서 배운 것 중 여기서 다시 쓰는 것
#     · 1주 print( ) - 화면에 찍기
#     · 1주 f"..." - 값을 끼워 넣는 문자열
#     · 1주 round( ) - 반올림
#     · 2주 len( ) - 개수 세기
#     · 2주 for - 하나씩 꺼내 반복
#     · 2주 .items( ) - 이름표와 값을 짝지어
#
#  ▣ 어떻게 돌리나
#     VS Code : `# %%` 아래에 커서를 두고  Shift + Enter  (그 칸만 실행)
#     터미널  : cd lab\examples\week05   →   python 03_game_source.py
#
#  ▣ 바로 아래 [0] 준비 블록에 대하여
#     윈도우에서 한글이 깨지지 않게 하고, 게임 엔진을 찾아갈 길을 알려
#     주는 부분입니다. 어느 예제든 똑같으니 외울 필요 없습니다.
#     여러분이 새 파일을 만들 때는 그대로 복사해서 쓰면 됩니다.
#
#     이 주의 목표·실습·과제는 같은 폴더의 README.md 에 있습니다.
# ──────────────────────────────────────────────────────────────────────

# %% [0] 준비 - ★ 외우지 마세요. 새 파일에 그대로 복사해 쓰면 됩니다.
#      윈도우에서 한글이 깨지지 않게 하는 것이 전부입니다.
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# %% [1] 게임의 진짜 소스
#
#     ┌────────────────────────────────────────────────────────────┐
#     │ def apply_effect(plant, effect, reason=""):
#     │     # 효과에 적힌 지표를 하나씩 꺼냅니다
#     │     for indicator, change in effect.items():
#     │         if indicator not in plant:
#     │             plant[indicator] = 0
#     │         plant[indicator] = plant[indicator] + change
#     └────────────────────────────────────────────────────────────┘

# %% [2] 같은 것을 직접 만들어 봅니다
plant = {"수율": 80, "순도": 58}
effect = {"수율": 5, "순도": 8}

for indicator, change in effect.items():          # .items( ) : 이름표와 값을 짝지어
    plant[indicator] = plant[indicator] + change
    print(f"  {indicator} +{change}  →  {plant[indicator]}")

print(plant)

# %% [3] 없는 지표가 나오면
effect2 = {"새지표": 3}
for indicator, change in effect2.items():
    if indicator not in plant:               # not in : 없는가
        plant[indicator] = 0                  # 0에서 시작하게 만들어 주기
    plant[indicator] = plant[indicator] + change
print(plant)

# %% [4] 12개월 동안 쌓인다면
plant = {"수율": 80}
history = []
for turn in range(1, 12 + 1):
    plant["수율"] = plant["수율"] + 0.3        # 매 달 조금씩
    history.append(round(plant["수율"], 2))

print(f"{len(history)}달 기록")
print("처음 5개:", history[:5])
print("합계 ÷ 개수 =", round(sum(history) / len(history), 2))


# %% [퀴즈] ✏️ 직접 해 보기
#      아래 물음에 코드로 답해 보세요. 이 아래에 그대로 쓰면 됩니다.
#      정답은  lab/answers/week05/  에 있습니다. (먼저 풀어 보고 여세요)
#
#   1) 효과에 마이너스 값을 넣으면 어떻게 되나요? 직접 해 보세요.
#   2) 매 턴 0.3 이 아니라 0.3 씩 커지다가 100 을 넘지 않게 하려면?


# 여기에 답을 써 보세요

