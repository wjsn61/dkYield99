# ════════════════════════════════════════════════════════════════════
#  잡음(변동) 엔진  (noise.py)
#
#  이 파일은 "세상은 정확하지 않다"를 게임 안에 넣어 주는 곳입니다.
#
#  ▶ 왜 필요한가요?
#     같은 정책을 쓰면 항상 같은 결과가 나오는 세상에서는
#     평균도 표준편차도 신뢰구간도 의미가 없습니다.
#     통계는 '흔들리는 값'에서 무언가를 알아내는 기술이니까요.
#
#  ▶ 두 가지 흔들림을 구분합니다 (이 구분이 이 수업의 절반입니다)
#
#       설정값 ─── 공정변동 ──▶ 진값 ─── 측정오차 ──▶ 관측값
#       (정책이           (실제로            (우리가
#        정한 값)          일어난 일)          보는 값)
#
#     공정변동: 값 자체가 흔들립니다.   (징수 실적, 전입·전출)
#     측정오차: 값은 그대로인데 재는 게 흔들립니다. (설문조사, 분석기)
#
#     ★ 측정오차는 진값을 절대 바꾸지 않습니다. 관측 칸에만 적습니다.
#        그래서 우리는 "진짜 값을 모른 채 관측값으로 추측"하게 됩니다.
#        이게 통계의 본질이고, 이 게임이 그걸 그대로 흉내 냅니다.
#
#  ▶ 시드(seed)가 있으면 흔들림이 '재현'됩니다.
#     같은 시드 = 같은 평행우주. 그래서 비교 실험을 할 수 있습니다.
#     시드가 없으면(None) 잡음이 아예 꺼집니다 - 예전과 똑같이 동작합니다.
#
#  ※ 이 파일은 학생이 편집하지 않습니다.
#     잡음의 크기(표준편차)를 바꾸려면 indicators_data.py 를 고치세요.
# ════════════════════════════════════════════════════════════════════
from __future__ import annotations

import hashlib
import math
import random

# 잡음 규칙의 판 번호.
# 표준편차나 계산 방식을 바꾸면 이 숫자를 올리세요.
# 그러면 예전에 저장된 게임은 예전 방식 그대로 재현됩니다.
NOISE_VERSION = 1


# ── 1. 함수: 이 턴, 이 지표만을 위한 난수기를 만든다 ──────────────────
def turn_rng(seed, turn, stream):
    """
    (시드, 턴, 지표) 세 가지로 난수기를 만듭니다.

    왜 이렇게 할까요? 난수기를 하나 만들어 계속 쓰면,
    정책을 몇 개 썼는지에 따라 난수 순서가 밀려서
    "같은 시드인데 결과가 다른" 일이 생깁니다.
    턴과 지표마다 따로 만들면 그런 일이 없습니다.
    저장했다 불러와도, 정책 순서를 바꿔도 같은 값이 나옵니다.
    """
    key = f"{seed}|{turn}|{stream}|v{NOISE_VERSION}"
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    return random.Random(int.from_bytes(digest[:8], "big"))


# ── 2. 함수: 지금 잡음이 켜져 있나? ──────────────────────────────────
def noise_on(state):
    """시드가 없으면 잡음은 꺼집니다 (예전과 똑같이 동작)."""
    return state.get("난수시드") is not None


# ── 3. 도우미: 지표 설명서를 가져온다 ───────────────────────────────
_CATALOGUE = None


def catalogue():
    """indicators_data.py 의 지표 설명서를 (한 번만) 읽어 옵니다."""
    global _CATALOGUE
    if _CATALOGUE is None:
        try:
            _CATALOGUE = _load_catalogue()
        except Exception:
            _CATALOGUE = {}          # 설명서를 못 읽어도 게임은 돌아가야 합니다
    return _CATALOGUE


def _load_catalogue():
    """엔진 파일을 직접 실행할 때도 설명서를 찾을 수 있게 경로를 맞춰 줍니다."""
    try:
        from app.indicators import by_key
    except ImportError:
        import os
        import sys
        here = os.path.dirname(os.path.abspath(__file__))
        server = os.path.abspath(os.path.join(here, "..", ".."))
        if server not in sys.path:
            sys.path.insert(0, server)
        from app.indicators import by_key
    return by_key()


def spec_of(key, field):
    """어떤 지표의 '공정변동' 또는 '측정오차' 설정을 꺼냅니다."""
    return (catalogue().get(key) or {}).get(field)


# ── 4. 함수: 설치된 설비/정책 아이디 목록 ────────────────────────────
def installed_ids(state):
    """지금 설치된 설비(또는 시행 중인 정책)의 아이디를 모읍니다."""
    ids = set()
    for field in ("설비목록", "시행중정책"):
        for item in state.get(field, []) or []:
            if isinstance(item, dict) and "아이디" in item:
                ids.add(item["아이디"])
            elif isinstance(item, str):
                ids.add(item)
    return ids


# ── 5. 함수: 측정오차의 실제 크기 ───────────────────────────────────
def measurement_sigma(state, key):
    """
    이 지표를 잴 때의 표준편차를 돌려줍니다.

    좋은 계기를 설치했다면 오차가 줄어듭니다.
    ★ 값이 좋아지는 게 아니라, 값을 '더 정확히 알게' 되는 것입니다.
    """
    spec = spec_of(key, "측정오차")
    if not spec:
        return 0.0
    sigma = spec.get("표준편차", 0.0)

    better = (catalogue().get(key) or {}).get("개선설비")
    if better and better.get("아이디") in installed_ids(state):
        sigma = better.get("표준편차", sigma)
    return sigma


# ── 6. 함수: 공정변동을 입힌다 (값 자체가 흔들린다) ──────────────────
def jitter(state, turn, key, base):
    """
    설정값(base)에 이번 턴의 흔들림을 입혀 '진값'을 만듭니다.

    단위기준이 "비율"이면  base × (1 + 흔들림)   ← 세수처럼 % 로 흔들리는 값
    단위기준이 "절대"이면  base + 흔들림          ← 인구처럼 양으로 흔들리는 값

    흔들림은 누적되지 않습니다. 매 턴 설정값 주변에서 새로 흔들립니다.
    (누적시키면 몇 턴 만에 정책 효과가 흔들림에 묻혀 버립니다)
    """
    if not noise_on(state):
        return base
    spec = spec_of(key, "공정변동")
    if not spec:
        return base
    sigma = spec.get("표준편차", 0)
    if not sigma:
        return base

    rng = turn_rng(state["난수시드"], turn, key)
    shake = rng.gauss(0, sigma)
    if spec.get("단위기준") == "비율":
        return base * (1 + shake)
    return base + shake


def jitter_ratio(state, turn, key):
    """
    이번 턴 흔들림의 '배수'만 돌려줍니다. (예: 징수율 1.028)
    학생이 잡음 자체를 눈으로 볼 수 있게 기록해 두는 용도입니다.
    """
    if not noise_on(state):
        return 1.0
    spec = spec_of(key, "공정변동")
    if not spec or not spec.get("표준편차"):
        return 1.0
    rng = turn_rng(state["난수시드"], turn, key)
    return 1 + rng.gauss(0, spec["표준편차"])


# ── 7. 함수: 개수를 세는 값 (포아송분포) ────────────────────────────
def poisson(rng, mean):
    """
    '드문 일이 몇 번 일어났나'를 세는 분포입니다.
    민원 건수, 사고 건수처럼 세는 값은 정규분포가 아닙니다.

    (크누스의 방법 - 외부 라이브러리 없이 계산합니다)
    """
    if mean <= 0:
        return 0
    if mean > 30:
        # 평균이 크면 정규분포로 근사해도 거의 같습니다 (계산도 빠릅니다)
        return max(0, int(round(rng.gauss(mean, math.sqrt(mean)))))
    limit = math.exp(-mean)
    count, product = 0, 1.0
    while True:
        product *= rng.random()
        if product <= limit:
            return count
        count += 1


def count_of(state, turn, key, mean):
    """포아송으로 개수를 하나 뽑습니다. 잡음이 꺼져 있으면 평균 그대로."""
    if not noise_on(state):
        return int(round(mean))
    return poisson(turn_rng(state["난수시드"], turn, key), mean)


# ── 8. 함수: 관측한다 (진값을 '재서' 관측 칸에 적는다) ───────────────
def observe(state, turn):
    """
    측정오차가 정의된 모든 지표를 '재서' 관측 칸에 적습니다.

    ★ 진값은 절대 건드리지 않습니다.
       그래서 게임은 정답(진값)을 알고 있고, 학생은 관측값만 봅니다.
       13주에 마지막으로 정답을 공개합니다.
    """
    for key, ind in catalogue().items():
        column = ind.get("관측컬럼")
        if not column or not ind.get("측정오차"):
            continue
        if key not in state:
            continue

        true_value = state[key]
        if not noise_on(state):
            state[column] = true_value          # 잡음이 꺼지면 그대로 베낍니다
            continue

        sigma = measurement_sigma(state, key)
        rng = turn_rng(state["난수시드"], turn, f"측정:{key}")
        state[column] = round(true_value + rng.gauss(0, sigma), 2)


# ── 9. 함수: 같은 턴에 여러 번 재 본다 (부분군) ─────────────────────
def sample_group(state, turn, key, size):
    """
    같은 턴에 같은 값을 여러 번 재 봅니다.

    왜 여러 번 잴까요? 한 번만 재면 그 값이 튄 건지 알 수 없습니다.
    4~5개씩 묶어 재야 '평균이 움직였는지'와 '흔들림이 커졌는지'를
    따로 볼 수 있습니다. 이것이 X-bar R 관리도의 출발점입니다. (13주)
    """
    true_value = state.get(key)
    if true_value is None:
        return []
    if not noise_on(state):
        return [true_value] * size

    sigma = measurement_sigma(state, key)
    rng = turn_rng(state["난수시드"], turn, f"부분군:{key}")
    return [round(true_value + rng.gauss(0, sigma), 2) for _ in range(size)]


# ════════════════════════════════════════════════════════════════════
#  데모: 이 파일을 실행하면 잡음이 어떻게 생겼는지 보여줍니다.
# ════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    print("=" * 70)
    print("  잡음(변동) 살펴보기")
    print("=" * 70)

    print("\n  [1] 같은 시드는 몇 번을 돌려도 같은 값이 나옵니다")
    for _ in range(3):
        rng = turn_rng(20260901, 5, "세수")
        print(f"      시드 20260901, 5턴, 세수  ->  {rng.gauss(0, 0.03):+.5f}")

    print("\n  [2] 시드가 다르면 다른 값이 나옵니다 (다른 평행우주)")
    for seed in (20260901, 20260902, 20260903):
        rng = turn_rng(seed, 5, "세수")
        print(f"      시드 {seed}, 5턴, 세수  ->  {rng.gauss(0, 0.03):+.5f}")

    print("\n  [3] 지표마다 흔들림이 따로 놉니다 (서로 영향 없음)")
    for key in ("세수", "인구", "주민만족"):
        rng = turn_rng(20260901, 5, key)
        print(f"      시드 20260901, 5턴, {key}  ->  {rng.gauss(0, 1):+.5f}")

    print("\n  [4] 개수를 세는 값은 포아송분포입니다 (평균 25, 30번 관측)")
    rng = turn_rng(20260901, 1, "민원건수")
    counts = [poisson(rng, 25) for _ in range(30)]
    print(f"      {counts}")
    mean = sum(counts) / len(counts)
    var = sum((c - mean) ** 2 for c in counts) / (len(counts) - 1)
    print(f"      평균 {mean:.2f}  분산 {var:.2f}")
    print(f"      -> 포아송은 평균과 분산이 (거의) 같습니다. 정규분포와 다른 점입니다.")

    print("=" * 70)
