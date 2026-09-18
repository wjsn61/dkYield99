# ════════════════════════════════════════════════════════════════════
#  통계 계산과 해석  (statistics_lab.py)
#
#  게임 기록을 받아 통계량을 계산하고, 그 숫자가 무슨 뜻인지
#  한국어로 설명해 줍니다. 그리고 그 설명의 '근거'가 어디서 왔는지
#  논문·표준 문서를 함께 알려 줍니다.
#
#  ▶ 왜 서버(파이썬)에서 계산하나요?
#     이 게임은 'Python 이 권위'인 구조입니다. 화면은 결과만 그립니다.
#     그리고 9주에 여러분이 직접 만든 평균·표준편차 함수의 답이
#     여기 나온 값과 같은지 맞춰 볼 수 있습니다.
#
#  ※ 이 파일은 외부 라이브러리를 쓰지 않습니다.
#     평균과 표준편차가 '어떻게' 계산되는지 그대로 보이도록 하기 위해서입니다.
#
#  ▶ 직접 실행해 보세요:  python statistics_lab.py
# ════════════════════════════════════════════════════════════════════
from __future__ import annotations

import math

# ── 0. 도우미: 한국어 조사 고르기 ───────────────────────────────────
def particle(word, with_final, without_final):
    """
    받침 유무에 따라 조사를 골라 줍니다.

        particle("순도", "을", "를")   ->  "를"   (도에 받침 없음)
        particle("전환율", "을", "를") ->  "을"   (율에 받침 ㄹ)

    해석 문장이 '순도을(를)' 처럼 어색해지지 않게 하려고 씁니다.
    """
    if not word:
        return without_final
    last = word[-1]
    if "가" <= last <= "힣":                       # 한글 음절인가
        return with_final if (ord(last) - 0xAC00) % 28 else without_final
    return without_final


# ── 1. 기본 통계량 (직접 구현 - 9주에 여러분이 만들 것과 같은 것) ────
def mean(values):
    """평균 = 다 더해서 개수로 나눈다."""
    return sum(values) / len(values)


def median(values):
    """중앙값 = 크기순으로 세워 놓고 한가운데. (반드시 정렬 먼저!)"""
    ordered = sorted(values)
    n = len(ordered)
    middle = n // 2
    if n % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def variance(values, sample=True):
    """
    분산 = 평균에서 얼마나 떨어져 있는지의 제곱 평균.

    나눌 때 n 이 아니라 n-1 을 씁니다(표본분산).
    가진 자료가 세상 전체가 아니라 '표본'이기 때문입니다. - 자유도
    """
    n = len(values)
    if n < 2:
        return 0.0
    m = mean(values)
    total = sum((v - m) ** 2 for v in values)
    return total / (n - 1 if sample else n)


def stdev(values, sample=True):
    """표준편차 = 분산의 제곱근. 원래 단위로 돌아옵니다."""
    return math.sqrt(variance(values, sample))


def cv(values):
    """
    변동계수(%) = 표준편차 ÷ 평균 × 100

    단위가 다른 지표끼리 '어느 쪽이 더 불안정한가'를 비교할 때 씁니다.
    (억 단위 세수와 점수 단위 만족도를 직접 비교할 수는 없으니까요)
    """
    m = mean(values)
    if m == 0:
        return 0.0
    return abs(stdev(values) / m) * 100


def quantile(values, q):
    """사분위수 등을 구합니다 (선형보간)."""
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * q
    low = math.floor(position)
    high = math.ceil(position)
    if low == high:
        return ordered[int(position)]
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def describe(values):
    """한 지표의 기술통계를 한 번에 계산합니다."""
    values = [v for v in values if isinstance(v, (int, float))]
    if not values:
        return None
    q1, q3 = quantile(values, 0.25), quantile(values, 0.75)
    return {
        "개수": len(values),
        "평균": round(mean(values), 3),
        "중앙값": round(median(values), 3),
        "표준편차": round(stdev(values), 3),
        "변동계수": round(cv(values), 2),
        "최소": round(min(values), 3),
        "최대": round(max(values), 3),
        "1사분위": round(q1, 3),
        "3사분위": round(q3, 3),
        "사분위범위": round(q3 - q1, 3),
    }


# ── 2. 분포 (히스토그램 · 이상치) ────────────────────────────────────
def histogram(values, bins=8):
    """값을 구간으로 나눠 몇 개씩 들어 있는지 셉니다."""
    values = [v for v in values if isinstance(v, (int, float))]
    if len(values) < 2:
        return None
    low, high = min(values), max(values)
    if high == low:                        # 전부 같은 값이면 구간을 못 나눕니다
        return {"구간": [f"{low:g}"], "도수": [len(values)], "폭": 0,
                "경고": "값이 전부 같아서 분포를 그릴 수 없습니다."}
    width = (high - low) / bins
    counts = [0] * bins
    for v in values:
        index = min(bins - 1, int((v - low) / width))
        counts[index] += 1
    labels = [f"{low + i * width:.1f}~{low + (i + 1) * width:.1f}" for i in range(bins)]
    return {"구간": labels, "도수": counts, "폭": round(width, 3),
            "시작": round(low, 3), "끝": round(high, 3)}


def outliers(values):
    """
    이상치 = 1사분위/3사분위에서 사분위범위의 1.5배 밖으로 나간 값.
    (Tukey 의 상자그림 규칙)
    """
    values = [v for v in values if isinstance(v, (int, float))]
    if len(values) < 4:
        return []
    q1, q3 = quantile(values, 0.25), quantile(values, 0.75)
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return [round(v, 3) for v in values if v < low or v > high]


# ── 3. 관리도 (이 변화가 우연인가, 신호인가) ────────────────────────
def control_limits(values, k=3):
    """
    관리도의 중심선과 위·아래 한계선을 구합니다.

    평균에서 ±3표준편차. 왜 하필 3일까요?
    정규분포라면 3σ 밖으로 나갈 확률이 약 0.27% 입니다.
    거의 안 일어나는 일이 일어났다면, 우연이 아니라 '무언가 변한 것'입니다.
    2σ 로 하면 거짓 경보가 약 20배 늘어납니다.
    """
    values = [v for v in values if isinstance(v, (int, float))]
    if len(values) < 2:
        return None
    center = mean(values)
    spread = stdev(values)
    upper, lower = center + k * spread, center - k * spread
    escaped = [{"위치": i + 1, "값": round(v, 3)}
               for i, v in enumerate(values) if v > upper or v < lower]
    return {
        "중심선": round(center, 3),
        "관리상한": round(upper, 3),
        "관리하한": round(lower, 3),
        "표준편차": round(spread, 3),
        "이탈점": escaped,
    }


# ── 4. 관계 (상관 · 회귀) ────────────────────────────────────────────
def correlation(xs, ys):
    """
    피어슨 상관계수 (-1 ~ +1)

    +1 에 가까우면 한쪽이 오를 때 다른 쪽도 오릅니다.
    ★ 하지만 '그래서 원인'이라는 뜻은 절대 아닙니다.
    """
    pairs = [(x, y) for x, y in zip(xs, ys)
             if isinstance(x, (int, float)) and isinstance(y, (int, float))]
    if len(pairs) < 3:
        return None
    xs2 = [p[0] for p in pairs]
    ys2 = [p[1] for p in pairs]
    mx, my = mean(xs2), mean(ys2)
    top = sum((x - mx) * (y - my) for x, y in pairs)
    bottom = math.sqrt(sum((x - mx) ** 2 for x in xs2) * sum((y - my) ** 2 for y in ys2))
    if bottom == 0:
        return None
    return round(top / bottom, 4)


def linear_regression(xs, ys):
    """최소제곱 직선. y = 기울기 × x + 절편"""
    pairs = [(x, y) for x, y in zip(xs, ys)
             if isinstance(x, (int, float)) and isinstance(y, (int, float))]
    if len(pairs) < 3:
        return None
    xs2 = [p[0] for p in pairs]
    ys2 = [p[1] for p in pairs]
    mx, my = mean(xs2), mean(ys2)
    bottom = sum((x - mx) ** 2 for x in xs2)
    if bottom == 0:
        return None
    slope = sum((x - mx) * (y - my) for x, y in pairs) / bottom
    intercept = my - slope * mx
    ss_total = sum((y - my) ** 2 for y in ys2)
    ss_residual = sum((y - (slope * x + intercept)) ** 2 for x, y in pairs)
    r2 = 1 - ss_residual / ss_total if ss_total else 0.0
    return {"기울기": round(slope, 4), "절편": round(intercept, 3),
            "결정계수": round(r2, 4)}


# ── 5. 신뢰구간 ──────────────────────────────────────────────────────
# 자유도별 t 값 (양쪽 95%). 표를 내장해서 외부 라이브러리 없이 씁니다.
T95 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365,
       8: 2.306, 9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179, 13: 2.160,
       14: 2.145, 15: 2.131, 16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093,
       20: 2.086, 25: 2.060, 30: 2.042, 40: 2.021, 60: 2.000, 120: 1.980}


def t_value(df):
    """자유도에 맞는 t 값을 찾습니다 (표에 없으면 가까운 값)."""
    if df <= 0:
        return 12.706
    if df in T95:
        return T95[df]
    for key in sorted(T95):
        if df <= key:
            return T95[key]
    return 1.96          # 표본이 아주 크면 정규분포 값에 가까워집니다


def confidence_interval(values, conf=0.95):
    """
    평균의 95% 신뢰구간.

    "이 구간 안에 진짜 평균이 있을 것이다" 라고 말할 수 있는 범위입니다.
    표본이 적거나 흔들림이 크면 구간이 넓어집니다 = 잘 모르겠다는 뜻.
    """
    values = [v for v in values if isinstance(v, (int, float))]
    n = len(values)
    if n < 2:
        return None
    m = mean(values)
    standard_error = stdev(values) / math.sqrt(n)
    margin = t_value(n - 1) * standard_error
    return {"평균": round(m, 3), "표준오차": round(standard_error, 4),
            "하한": round(m - margin, 3), "상한": round(m + margin, 3),
            "오차범위": round(margin, 3), "신뢰수준": conf}


# ── 5-1. 정규분포로 '규격을 벗어날 확률' 구하기 ─────────────────────
def normal_below(x, mean_value, spread):
    """
    정규분포에서 x 보다 작을 확률.

    math.erf 는 파이썬에 기본으로 들어 있어서 따로 설치할 필요가 없습니다.
    (넘파이 없이도 규격이탈률을 계산할 수 있습니다)
    """
    if spread <= 0:
        return 0.0 if x < mean_value else 1.0
    z = (x - mean_value) / (spread * math.sqrt(2))
    return 0.5 * (1 + math.erf(z))


# ── 5-2. 공정능력 Cp · Cpk ──────────────────────────────────────────
def capability(values, lsl=None, usl=None):
    """
    이 공정이 '규격을 지킬 능력'이 있는지 하나의 숫자로 요약합니다.

        Cp  = 규격 폭이 공정 산포(6σ)의 몇 배인가       - 산포만 본다
        Cpk = 평균이 규격 한쪽으로 치우친 것까지 반영    - 치우침도 본다

    ★ Cp 는 좋은데 Cpk 가 나쁘면 "잘 만드는데 목표에서 벗어나 있다"는 뜻입니다.
       산포를 줄일 게 아니라 평균을 가운데로 옮겨야 합니다.

    lsl = 규격하한(lower spec limit), usl = 규격상한(upper spec limit).
    한쪽만 있어도 Cpk 는 구할 수 있습니다. (순도처럼 '98% 이상'만 있는 경우)
    """
    values = [v for v in values if isinstance(v, (int, float))]
    if len(values) < 2 or (lsl is None and usl is None):
        return None
    average = mean(values)
    spread = stdev(values)
    if spread <= 0:
        return None

    cp = None
    if lsl is not None and usl is not None:
        cp = (usl - lsl) / (6 * spread)

    sides = []
    if usl is not None:
        sides.append((usl - average) / (3 * spread))
    if lsl is not None:
        sides.append((average - lsl) / (3 * spread))
    cpk = min(sides)

    # 규격을 벗어날 확률 (정규분포 가정)
    out_low = normal_below(lsl, average, spread) if lsl is not None else 0.0
    out_high = (1 - normal_below(usl, average, spread)) if usl is not None else 0.0
    out_rate = (out_low + out_high) * 100

    return {
        "개수": len(values),
        "평균": round(average, 3),
        "표준편차": round(spread, 4),
        "규격하한": lsl, "규격상한": usl,
        "Cp": round(cp, 3) if cp is not None else None,
        "Cpk": round(cpk, 3),
        "규격이탈률": round(out_rate, 3),
        "백만개당": round(out_rate * 10000),      # ppm
    }


def interpret_capability(name, unit, result):
    """Cp·Cpk 를 읽어 주는 문장들."""
    cpk = result["Cpk"]
    등급 = ("아주 좋음 (1.33 이상 - 대부분의 고객이 요구하는 수준)" if cpk >= 1.33 else
            "보통 (1.0~1.33 - 규격은 지키지만 여유가 없음)" if cpk >= 1.0 else
            "부족 (1.0 미만 - 불량이 꾸준히 나옵니다)")
    lines = [
        f"{name}의 평균은 {result['평균']}{unit}, 표준편차는 {result['표준편차']}{unit} 입니다.",
        f"공정능력지수 Cpk = {cpk} - {등급}",
    ]
    if result["Cp"] is not None and result["Cp"] - cpk > 0.2:
        lines.append(
            f"★ Cp({result['Cp']})는 좋은데 Cpk({cpk})가 낮습니다. "
            "만드는 솜씨(산포)는 괜찮은데 평균이 규격 한쪽으로 치우쳐 있다는 뜻입니다. "
            "산포를 줄이는 것보다 **평균을 가운데로 옮기는 것**이 먼저입니다.")
    lines.append(
        f"이 상태가 계속되면 100개 중 약 {result['규격이탈률']:.2f}개 "
        f"(백만 개당 {result['백만개당']:,}개)가 규격을 벗어납니다.")
    lines.append(
        "⚠️ 이 계산은 값이 정규분포를 따른다고 가정합니다. "
        "히스토그램이 한쪽으로 심하게 치우쳐 있으면 이 숫자를 믿으면 안 됩니다.")
    return lines


# ── 5-3. 부분군 관리도 (X-bar R) ────────────────────────────────────
# 부분군 크기별 관리도 상수 (KS·ISO 표준값)
A2 = {2: 1.880, 3: 1.023, 4: 0.729, 5: 0.577, 6: 0.483, 7: 0.419, 8: 0.373}
D3 = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0.076, 8: 0.136}
D4 = {2: 3.267, 3: 2.574, 4: 2.282, 5: 2.114, 6: 2.004, 7: 1.924, 8: 1.864}


def xbar_r_chart(subgroups):
    """
    한 번에 여러 개씩 뽑아 재는 자료의 관리도.

    subgroups 는 [[98.1, 98.3, ...], [...], ...] 처럼 묶음의 목록입니다.

    ★ 왜 여러 개씩 뽑을까요?
      한 개만 재면 '값이 튄 것'인지 '공정이 변한 것'인지 알 수 없습니다.
      묶어서 재면 평균이 움직였는지(X-bar)와 흔들림이 커졌는지(R)를
      따로 볼 수 있습니다.
    """
    groups = [g for g in subgroups if isinstance(g, (list, tuple)) and len(g) >= 2]
    if len(groups) < 2:
        return None
    size = len(groups[0])
    if size not in A2:
        return None

    means = [mean(g) for g in groups]
    ranges = [max(g) - min(g) for g in groups]
    center_x, center_r = mean(means), mean(ranges)

    limits = {
        "부분군크기": size, "부분군수": len(groups),
        "Xbar중심선": round(center_x, 3),
        "Xbar관리상한": round(center_x + A2[size] * center_r, 3),
        "Xbar관리하한": round(center_x - A2[size] * center_r, 3),
        "R중심선": round(center_r, 3),
        "R관리상한": round(D4[size] * center_r, 3),
        "R관리하한": round(D3[size] * center_r, 3),
        "부분군평균": [round(m, 3) for m in means],
        "부분군범위": [round(r, 3) for r in ranges],
    }
    limits["Xbar이탈"] = [
        {"위치": i + 1, "값": round(m, 3)} for i, m in enumerate(means)
        if m > limits["Xbar관리상한"] or m < limits["Xbar관리하한"]]
    limits["R이탈"] = [
        {"위치": i + 1, "값": round(r, 3)} for i, r in enumerate(ranges)
        if r > limits["R관리상한"] or r < limits["R관리하한"]]
    return limits


def interpret_xbar_r(name, unit, chart):
    """X-bar R 관리도를 읽어 주는 문장들."""
    lines = [
        f"{name}{particle(name, '을', '를')} 한 번에 {chart['부분군크기']}개씩, "
        f"{chart['부분군수']}번 묶어서 재었습니다.",
        f"평균 관리도: 중심선 {chart['Xbar중심선']}{unit}, "
        f"한계 {chart['Xbar관리하한']} ~ {chart['Xbar관리상한']}{unit}",
        f"범위 관리도: 중심선 {chart['R중심선']}{unit}, "
        f"한계 {chart['R관리하한']} ~ {chart['R관리상한']}{unit}",
    ]
    if chart["Xbar이탈"]:
        위치 = ", ".join(f"{p['위치']}번째({p['값']})" for p in chart["Xbar이탈"][:5])
        lines.append(f"★ 평균이 관리한계를 벗어난 곳: {위치}. "
                     "공정의 '중심'이 옮겨갔다는 신호입니다.")
    if chart["R이탈"]:
        위치 = ", ".join(f"{p['위치']}번째({p['값']})" for p in chart["R이탈"][:5])
        lines.append(f"★ 흔들림이 관리한계를 벗어난 곳: {위치}. "
                     "공정이 '불안정'해졌다는 신호입니다.")
    if not chart["Xbar이탈"] and not chart["R이탈"]:
        lines.append("평균도 흔들림도 관리한계 안에 있습니다. "
                     "예측 가능한 상태로 운전되었다는 뜻입니다.")
    return lines


# ── 5-4. 실험계획법 - 두 인자를 동시에 바꿔 본다 ────────────────────
# '낮음 → 높음' 을 알아볼 수 있는 흔한 표기들 (앞이 낮은 쪽)
LEVEL_ORDER = [("저", "고"), ("낮", "높"), ("low", "high"), ("-", "+"), ("0", "1")]


def _order_levels(found, given=None):
    """
    두 수준 중 어느 쪽이 '낮음'인지 정합니다.

    ★ sorted() 를 쓰면 안 됩니다.
      한글 가나다순으로는 '고' < '저' 라서 高가 낮은 쪽이 되어 버립니다.
      (부호가 통째로 뒤집혀서 "온도를 올리면 수율이 떨어진다"는
       정반대 결론이 나옵니다 - 실제로 이 함수를 만들 때 겪은 버그입니다)

    순서를 정하는 방법:
      1) 호출한 쪽이 알려 준 순서가 있으면 그것을 쓴다
      2) '저/고', 'low/high' 같은 흔한 표기면 그 규칙을 쓴다
      3) 둘 다 아니면 실험표에 먼저 나온 값을 '낮음'으로 본다
    """
    if given and len(given) == 2 and set(given) == set(found):
        return list(given)
    for low_mark, high_mark in LEVEL_ORDER:
        lows = [v for v in found if low_mark in str(v)]
        highs = [v for v in found if high_mark in str(v)]
        if len(lows) == 1 and len(highs) == 1 and lows[0] != highs[0]:
            return [lows[0], highs[0]]
    return list(found)          # 먼저 나온 순서 그대로


def two_factor_doe(runs, levels_a=None, levels_b=None):
    """
    두 가지를 '하나씩' 바꾸지 말고 '동시에' 설계해서 바꿔 봅니다.

    runs 는 네 가지 조건의 결과입니다:
        [{"A": "저", "B": "저", "결과": 70.1},
         {"A": "고", "B": "저", "결과": 74.5}, ...]

    levels_a / levels_b 로 ["낮은쪽", "높은쪽"] 순서를 직접 알려 줄 수 있습니다.
    안 주면 '저/고' 같은 표기나 실험표에 나온 순서로 알아서 정합니다.

    ★ 왜 하나씩 바꾸면 안 될까요?
      A를 바꿔 보고, 그다음 B를 바꿔 보면
      "A와 B를 함께 올렸을 때만 생기는 효과"를 영원히 볼 수 없습니다.
      그것을 교호작용(interaction)이라고 합니다.
    """
    table = {}
    seen_a, seen_b = [], []          # 실험표에 나온 순서를 기억해 둡니다
    for r in runs:
        if not isinstance(r, dict):
            continue
        key = (r.get("A"), r.get("B"))
        value = r.get("결과")
        if key[0] is None or key[1] is None or not _is_number_like(value):
            continue
        if key[0] not in seen_a:
            seen_a.append(key[0])
        if key[1] not in seen_b:
            seen_b.append(key[1])
        table.setdefault(key, []).append(value)
    if len(table) < 4 or len(seen_a) != 2 or len(seen_b) != 2:
        return None

    cells = {k: mean(v) for k, v in table.items()}
    a_low, a_high = _order_levels(seen_a, levels_a)
    b_low, b_high = _order_levels(seen_b, levels_b)
    levels_a, levels_b = [a_low, a_high], [b_low, b_high]

    def cell(a, b):
        return cells.get((a, b))
    if any(cell(a, b) is None for a in levels_a for b in levels_b):
        return None

    # 주효과 = 그 인자를 낮음→높음으로 바꿨을 때 결과가 평균 얼마나 변하나
    main_a = ((cell(a_high, b_low) + cell(a_high, b_high))
              - (cell(a_low, b_low) + cell(a_low, b_high))) / 2
    main_b = ((cell(a_low, b_high) + cell(a_high, b_high))
              - (cell(a_low, b_low) + cell(a_high, b_low))) / 2
    # 교호작용 = "둘을 함께 올렸을 때만" 생기는 몫
    interaction = ((cell(a_high, b_high) - cell(a_low, b_high))
                   - (cell(a_high, b_low) - cell(a_low, b_low))) / 2

    # 교호작용을 사람 말로 설명하려면 '조건부 효과'가 필요합니다.
    #   B가 낮을 때 A의 효과  vs  B가 높을 때 A의 효과
    a_effect_at_b_low = cell(a_high, b_low) - cell(a_low, b_low)
    a_effect_at_b_high = cell(a_high, b_high) - cell(a_low, b_high)

    best = max(cells, key=cells.get)
    return {
        "수준A": [a_low, a_high], "수준B": [b_low, b_high],
        "칸평균": {f"A={k[0]},B={k[1]}": round(v, 3) for k, v in cells.items()},
        "주효과A": round(main_a, 3),
        "주효과B": round(main_b, 3),
        "교호작용": round(interaction, 3),
        "A효과_B낮을때": round(a_effect_at_b_low, 3),
        "A효과_B높을때": round(a_effect_at_b_high, 3),
        "최적조건": {"A": best[0], "B": best[1], "결과": round(cells[best], 3)},
    }


def interpret_doe(name_a, name_b, response, result):
    """실험계획 결과를 읽어 주는 문장들."""
    a, b, x = result["주효과A"], result["주효과B"], result["교호작용"]
    목적어 = lambda w: particle(w, "을", "를")
    주어 = lambda w: particle(w, "이", "가")
    lines = [
        f"{name_a}{목적어(name_a)} {result['수준A'][0]}→{result['수준A'][1]} 로 바꾸면 "
        f"{response}{주어(response)} 평균 {a:+.3f} 움직입니다. (주효과)",
        f"{name_b}{목적어(name_b)} {result['수준B'][0]}→{result['수준B'][1]} 로 바꾸면 "
        f"{response}{주어(response)} 평균 {b:+.3f} 움직입니다. (주효과)",
    ]
    크기 = max(abs(a), abs(b))
    if 크기 > 0 and abs(x) > 크기 * 0.25:
        low, high = result["A효과_B낮을때"], result["A효과_B높을때"]
        lines.append(
            f"★ 교호작용이 {x:+.3f} 로 큽니다. "
            f"{name_a}의 효과가 {name_b}의 값에 따라 달라진다는 뜻입니다 - "
            f"{name_b}{주어(name_b)} {result['수준B'][0]}일 때는 {low:+.1f}인데 "
            f"{result['수준B'][1]}일 때는 {high:+.1f} 입니다. "
            f"{name_b}{목적어(name_b)} 고정해 놓고 {name_a}만 시험했다면 "
            "둘 중 한쪽 답만 보고 잘못 결론지었을 것입니다. "
            "'하나씩 바꿔 보기(OFAT)'가 위험한 이유입니다.")
    else:
        lines.append(
            f"교호작용은 {x:+.3f} 로 작습니다. "
            "두 인자가 서로 방해하지 않으니 따로따로 조정해도 괜찮습니다.")
    best = result["최적조건"]
    lines.append(
        f"네 조건 중 가장 좋았던 것: {name_a}={best['A']}, {name_b}={best['B']} "
        f"→ {response} {best['결과']}")
    lines.append(
        "⚠️ 네 조건을 **같은 시드로** 돌렸을 때만 이 비교가 의미 있습니다. "
        "조업 변동이 다르면 무엇 때문에 달라졌는지 알 수 없습니다.")
    return lines


def _is_number_like(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


# ── 6. 두 무리 비교 (잘된 판 vs 잘못된 판) ──────────────────────────
def compare_groups(group_a, group_b, name_a="성공", name_b="실패"):
    """
    두 무리의 평균이 정말 다른지 봅니다 (웰치의 t검정).

    ★ '성공' 판들과 '실패' 판들을 비교할 때 쓰는 계산입니다.
    """
    a = [v for v in group_a if isinstance(v, (int, float))]
    b = [v for v in group_b if isinstance(v, (int, float))]
    if len(a) < 2 or len(b) < 2:
        return None
    ma, mb = mean(a), mean(b)
    va, vb = variance(a), variance(b)
    na, nb = len(a), len(b)
    se = math.sqrt(va / na + vb / nb)
    if se == 0:
        return None
    t = (ma - mb) / se
    # 웰치-새터스웨이트 자유도
    top = (va / na + vb / nb) ** 2
    bottom = (va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1)
    df = top / bottom if bottom else min(na, nb) - 1

    # 효과크기 (코헨의 d) - '통계적으로 유의' 와 '실무적으로 크다' 는 다릅니다
    pooled = math.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    d = (ma - mb) / pooled if pooled else 0.0

    return {
        "무리A": name_a, "무리B": name_b,
        "개수A": na, "개수B": nb,
        "평균A": round(ma, 3), "평균B": round(mb, 3),
        "평균차": round(ma - mb, 3),
        "t값": round(t, 3), "자유도": round(df, 1),
        "임계값(95%)": t_value(int(df)),
        "유의함": abs(t) > t_value(int(df)),
        "효과크기": round(d, 3),
    }


# ════════════════════════════════════════════════════════════════════
#  근거 문헌
#
#  아래 해석 문구들이 어디서 온 것인지 밝혀 둡니다.
#  "선생님이 그렇게 말했으니까"가 아니라 출처를 확인하는 습관이
#  데이터로 일하는 사람의 기본입니다.
#
#  ※ 링크는 수업 전에 한 번 확인해 보세요. 주소가 바뀌기도 합니다.
# ════════════════════════════════════════════════════════════════════
REFERENCES = {
    "기술통계": [
        {
            "제목": "NIST/SEMATECH e-Handbook of Statistical Methods, 1.3.5 Quantitative Techniques",
            "저자": "NIST/SEMATECH (미국 국립표준기술연구소)",
            "설명": "평균·표준편차·사분위 등 기술통계의 정의와 계산법. 무료 공개 표준 교재.",
            "url": "https://www.itl.nist.gov/div898/handbook/eda/section3/eda35.htm",
        },
        {
            "제목": "Exploratory Data Analysis",
            "저자": "John W. Tukey (1977), Addison-Wesley",
            "설명": "상자그림과 1.5×사분위범위 이상치 규칙의 출처. "
                    "'숫자를 요약하기 전에 먼저 그려 보라'는 원칙을 세운 책.",
            "url": "https://archive.org/details/exploratorydataa0000tuke",
        },
        {
            "제목": "Graphs in Statistical Analysis, The American Statistician 27(1), 17-21",
            "저자": "F. J. Anscombe (1973)",
            "설명": "평균·표준편차·상관계수가 모두 같은데 그림은 전혀 다른 네 자료(앤스콤 4중주). "
                    "요약 숫자만 믿으면 안 되는 이유.",
            "url": "https://doi.org/10.1080/00031305.1973.10478966",
        },
    ],
    "분포": [
        {
            "제목": "NIST/SEMATECH e-Handbook, 1.3.3.14 Histogram",
            "저자": "NIST/SEMATECH",
            "설명": "히스토그램을 읽는 법 - 봉우리·치우침·퍼짐.",
            "url": "https://www.itl.nist.gov/div898/handbook/eda/section3/histogra.htm",
        },
    ],
    "관리도": [
        {
            "제목": "NIST/SEMATECH e-Handbook, 6.3 Univariate and Multivariate Control Charts",
            "저자": "NIST/SEMATECH",
            "설명": "관리도의 3σ 관리한계와 판정 규칙. 이 게임의 관리도 계산이 따르는 기준.",
            "url": "https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc3.htm",
        },
        {
            "제목": "Economic Control of Quality of Manufactured Product",
            "저자": "Walter A. Shewhart (1931), Van Nostrand",
            "설명": "관리도를 처음 만든 책. '우연변동'과 '이상원인'을 나눈 것이 출발점.",
            "url": "https://archive.org/details/in.ernet.dli.2015.150272",
        },
        {
            "제목": "Statistical Quality Control Handbook",
            "저자": "Western Electric Company (1956)",
            "설명": "관리도 판정 규칙(웨스턴일렉트릭 룰)의 원전. "
                    "3σ 이탈 외에 '연속 7점 상승' 같은 패턴 규칙을 정리했습니다.",
            "url": "https://archive.org/details/westernelectricstatisticalqualitycontrolhandbook",
        },
    ],
    "공정능력": [
        {
            "제목": "Process Capability Indices, Journal of Quality Technology 18(1), 41-52",
            "저자": "Victor E. Kane (1986)",
            "설명": "Cp·Cpk 를 널리 알린 논문. 규격을 만족할 능력을 하나의 숫자로 요약하는 법.",
            "url": "https://doi.org/10.1080/00224065.1986.11978984",
        },
        {
            "제목": "NIST/SEMATECH e-Handbook, 6.1.6 What is Process Capability?",
            "저자": "NIST/SEMATECH",
            "설명": "Cp / Cpk 계산식과 해석 기준(1.33 이상 등).",
            "url": "https://www.itl.nist.gov/div898/handbook/pmc/section1/pmc16.htm",
        },
    ],
    "상관과인과": [
        {
            "제목": "NIST/SEMATECH e-Handbook, 1.3.3.26 Scatter Plot",
            "저자": "NIST/SEMATECH",
            "설명": "상관을 눈으로 확인하는 법. 계수만 보지 말고 반드시 그려 보라는 원칙.",
            "url": "https://www.itl.nist.gov/div898/handbook/eda/section3/scatterp.htm",
        },
        {
            "제목": "Experimental and Quasi-Experimental Designs for Generalized Causal Inference",
            "저자": "Shadish, Cook & Campbell (2002), Houghton Mifflin",
            "설명": "상관에서 인과로 넘어가려면 무엇이 필요한가(통제군·반사실). "
                    "증거기반정책의 방법론적 토대.",
            "url": "https://archive.org/details/experimentalquas0000shad",
        },
    ],
    "신뢰구간": [
        {
            "제목": "The Probable Error of a Mean, Biometrika 6(1), 1-25",
            "저자": "'Student' (William S. Gosset, 1908)",
            "설명": "t분포의 원전. 표본이 적을 때 평균을 어떻게 다뤄야 하는지.",
            "url": "https://doi.org/10.1093/biomet/6.1.1",
        },
        {
            "제목": "The ASA Statement on p-Values: Context, Process, and Purpose, "
                    "The American Statistician 70(2), 129-133",
            "저자": "Ronald L. Wasserstein & Nicole A. Lazar (2016), 미국통계학회",
            "설명": "★ p값을 '가설이 틀릴 확률'로 읽으면 안 되는 이유를 학회가 공식 성명으로 밝힌 문서. "
                    "리포트를 쓰기 전에 반드시 읽어야 합니다.",
            "url": "https://doi.org/10.1080/00031305.2016.1154108",
        },
        {
            "제목": "Statistical Power Analysis for the Behavioral Sciences (2nd ed.)",
            "저자": "Jacob Cohen (1988), Routledge",
            "설명": "효과크기(코헨의 d)의 출처. '통계적으로 유의하다'와 "
                    "'실제로 중요하다'는 다르다는 것.",
            "url": "https://doi.org/10.4324/9780203771587",
        },
    ],
    "합성지표": [
        {
            "제목": "Handbook on Constructing Composite Indicators: Methodology and User Guide",
            "저자": "Nardo et al. (2008), OECD / EU JRC",
            "설명": "★ 여러 지표를 하나의 점수로 묶는 법(정규화·가중치)과 그 위험. "
                    "도시건강도와 재선점수가 바로 이런 합성지표입니다. "
                    "가중치를 누가 어떻게 정하는가가 곧 정책적 선택이라는 것.",
            "url": "https://doi.org/10.1787/9789264043466-en",
        },
    ],
    "측정오차": [
        {
            "제목": "Evaluation of measurement data - Guide to the expression of "
                    "uncertainty in measurement (GUM), JCGM 100:2008",
            "저자": "국제도량형국(BIPM) 외 7개 국제기구",
            "설명": "측정에는 반드시 불확도가 따른다는 국제 표준. "
                    "곱셈으로 이어진 값의 오차가 어떻게 전파되는지(수율!)도 여기 있습니다.",
            "url": "https://www.bipm.org/en/committees/jc/jcgm/publications",
        },
    ],
}


# ── 7. 해석: 숫자를 문장으로 바꾼다 ─────────────────────────────────
def interpret_describe(name, unit, stats):
    """기술통계를 읽어 주는 문장들을 만듭니다."""
    lines = []
    average, spread = stats["평균"], stats["표준편차"]
    lines.append(
        f"{stats['개수']}개 기록의 평균은 {average}{unit} 이고, "
        f"대체로 ±{spread}{unit} 만큼 흔들렸습니다.")

    # 변동계수로 안정성을 판단합니다
    coefficient = stats["변동계수"]
    if coefficient < 5:
        lines.append(f"변동계수가 {coefficient}% 로 매우 안정적입니다. "
                     "거의 일정하게 유지되었다는 뜻입니다.")
    elif coefficient < 15:
        lines.append(f"변동계수가 {coefficient}% 입니다. 보통 수준의 흔들림입니다.")
    else:
        lines.append(f"변동계수가 {coefficient}% 로 큽니다. "
                     "평균만 보고 판단하면 위험합니다 - 최악의 경우를 함께 보세요.")

    # 평균과 중앙값의 차이로 치우침을 봅니다
    gap = stats["평균"] - stats["중앙값"]
    if spread > 0 and abs(gap) > spread * 0.3:
        direction = "큰 값들" if gap > 0 else "작은 값들"
        lines.append(
            f"평균({stats['평균']})이 중앙값({stats['중앙값']})과 제법 다릅니다. "
            f"{direction}이 평균을 끌고 갔습니다. 이럴 때는 중앙값이 더 정직합니다.")

    lines.append(f"가장 낮을 때 {stats['최소']}{unit}, 가장 높을 때 {stats['최대']}{unit} "
                 f"까지 갔습니다. (사분위범위 {stats['사분위범위']}{unit})")
    return lines


def interpret_control(name, unit, limits):
    """관리도를 읽어 주는 문장들."""
    lines = [
        f"중심선 {limits['중심선']}{unit}, "
        f"관리한계는 {limits['관리하한']} ~ {limits['관리상한']}{unit} 입니다.",
        "이 범위 안에서 오르내리는 것은 '늘 있는 흔들림'입니다. "
        "여기에 반응해서 정책을 바꾸면 오히려 더 불안정해집니다.",
    ]
    escaped = limits["이탈점"]
    if escaped:
        positions = ", ".join(f"{p['위치']}턴({p['값']})" for p in escaped[:5])
        lines.append(
            f"★ {len(escaped)}번 관리한계를 벗어났습니다: {positions}. "
            "우연이라기엔 너무 드문 일입니다. 그 턴에 무슨 일이 있었는지 "
            "로그를 확인해 보세요 - 원인이 있을 가능성이 높습니다.")
    else:
        lines.append("관리한계를 벗어난 적이 없습니다. "
                     "예측 가능한 상태로 운영되었다는 뜻입니다.")
    return lines


def interpret_correlation(x_name, y_name, r, regression, first_time=True):
    """
    상관·회귀를 읽어 주는 문장들.

    first_time 이 True 인 관계에만 '상관≠인과' 경고를 붙입니다.
    (모든 관계마다 같은 경고를 반복하면 아무도 안 읽게 됩니다)
    """
    strength = ("매우 강한" if abs(r) >= 0.9 else
                "강한" if abs(r) >= 0.7 else
                "뚜렷한" if abs(r) >= 0.4 else
                "약한" if abs(r) >= 0.2 else "거의 없는")
    direction = "같이 오르는" if r > 0 else "반대로 가는"
    lines = [f"{x_name} 와(과) {y_name} 는 상관계수 {r} - {strength} {direction} 관계입니다."]

    if regression:
        lines.append(
            f"직선으로 맞춰 보면 {x_name} 가 1 오를 때 "
            f"{y_name} 는 약 {regression['기울기']} 움직입니다. "
            f"이 직선이 설명하는 몫은 {round(regression['결정계수'] * 100, 1)}% 입니다.")

    if first_time:
        lines.append(
            "★ 이 숫자만으로는 '원인'인지 알 수 없습니다. "
            "두 값이 함께 움직인 것은, 하나의 선택이 둘을 동시에 건드렸기 때문일 수도 있습니다. "
            "아래 각 관계에 '실제 원인'인지 '교란변수'인지 표시해 두었습니다 - "
            "하지만 현실에서는 아무도 알려 주지 않습니다. "
            "그래서 다른 조건을 똑같이 맞춘 비교(통제군)가 필요합니다.")
    return lines


def interpret_confidence(name, unit, interval):
    """신뢰구간을 읽어 주는 문장들."""
    return [
        f"평균 {interval['평균']}{unit}, 95% 신뢰구간은 "
        f"{interval['하한']} ~ {interval['상한']}{unit} 입니다.",
        f"오차범위가 ±{interval['오차범위']}{unit} 이므로, "
        f"이보다 작은 차이는 '달라졌다'고 말하기 어렵습니다.",
        "표본이 늘면 이 구간은 좁아집니다. 더 많이 관찰할수록 더 정확히 알게 됩니다.",
    ]


# ════════════════════════════════════════════════════════════════════
#  데모
# ════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    sample = [80.0, 81.3, 79.4, 84.2, 82.1, 83.9, 78.6, 95.4, 81.0, 82.7, 80.5, 83.1]

    print("=" * 70)
    print("  통계 계산 데모 - 12개월치 세수(억)")
    print("=" * 70)
    print(f"  자료: {sample}")

    stats = describe(sample)
    print("\n  [기술통계]")
    for key, value in stats.items():
        print(f"     {key:<8} {value}")

    print("\n  [해석]")
    for line in interpret_describe("세수", "억", stats):
        print(f"     - {line}")

    print("\n  [관리도]")
    limits = control_limits(sample)
    for line in interpret_control("세수", "억", limits):
        print(f"     - {line}")

    print("\n  [신뢰구간]")
    for line in interpret_confidence("세수", "억", confidence_interval(sample)):
        print(f"     - {line}")

    print("\n  [근거 문헌 - 기술통계]")
    for ref in REFERENCES["기술통계"]:
        print(f"     · {ref['제목']}")
        print(f"       {ref['저자']}")
        print(f"       {ref['url']}")

    print("=" * 70)
