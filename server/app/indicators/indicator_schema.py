# ════════════════════════════════════════════════════════════════════
#  지표 검사기 (indicator_schema.py)
#  ※ 이 파일은 "규칙을 검사하는 도구"입니다. 학생은 보통 건드리지 않습니다.
#     지표를 바꾸려면 indicators_data.py 만 편집하세요.
#  ※ 코드의 함수/변수 이름은 영어, 설명(주석)과 지표 내용은 한국어입니다.
# ════════════════════════════════════════════════════════════════════
"""
하는 일:
  - indicators_data.py 의 INDICATORS 가 규칙에 맞는지 검사합니다.
  - 틀린 곳을 '친절한 한국어'로 알려줍니다.
  - 통계 수업에서 틀리기 쉬운 것도 함께 짚어 줍니다.
      (변동이 0인 지표 / 잡음이 너무 큰 지표 / 계수 자료에 X-bar R 관리도 …)
  - 엔진(city_engine.py)이 실제로 만들지 않는 지표가 섞이지 않았는지도 봅니다.

  ▶ 직접 실행해서 검사해 보세요:  python indicators_data.py
"""

# -- 지표의 '유형': 이 6가지 중 하나여야 합니다 -----------------------
#    진값     : 도시 안에서 실제로 일어난 값
#    관측값   : 조사·측정으로 알아낸 값 (진값과 다를 수 있습니다!)
#    파생값   : 다른 지표들로 계산해 만든 값
#    운전조건 : 정책이 건드리지만 계산에는 안 쓰이는 값
#    비용     : 돈이 나가는 항목
#    진행     : 턴·레벨처럼 게임 진행을 나타내는 값
ALLOWED_TYPES = {"진값", "관측값", "파생값", "운전조건", "비용", "진행"}

# -- 지표의 '척도': 통계에서 제일 먼저 배우는 분류입니다 --------------
#    명목: 이름뿐 (예: 정책 분류)          순서: 순위는 있으나 간격이 무의미
#    등간: 간격은 같으나 0이 '없음'이 아님   비율: 0이 진짜 '없음' (대부분 여기)
ALLOWED_SCALES = {"명목", "순서", "등간", "비율"}

# -- 관리도 종류 ------------------------------------------------------
ALLOWED_CHARTS = {"X-bar R", "X-MR", "c", "p"}

# -- 반드시 있어야 하는 항목 -----------------------------------------
REQUIRED_FIELDS = ["키", "이름", "단위", "유형", "척도", "인과", "CSV포함"]
# -- 있어도 되고 없어도 되는 항목 -----------------------------------
OPTIONAL_FIELDS = ["범위", "관측컬럼", "측정오차", "공정변동", "개선설비",
                   "관리도", "설명"]


class IndicatorError(Exception):
    """지표 정의가 규칙에 어긋날 때 발생합니다."""
    pass


def validate(indicators, engine_keys=None):
    """
    지표 목록을 검사해서 (errors, warnings) 두 목록을 돌려줍니다.
      - errors  (❌): 그대로 두면 게임/실습이 안 돌아가는 문제
      - warnings(⚠️): 돌아가긴 하지만 확인해 보면 좋은 것
    engine_keys 를 주면 "엔진이 만들지 않는 지표"까지 잡아 줍니다.
    """
    errors, warnings = [], []
    seen_keys = set()

    if not isinstance(indicators, list):
        errors.append("INDICATORS 는 [ ... ] 형태의 목록이어야 합니다.")
        return errors, warnings

    # 순환문(for): 지표를 하나씩 검사합니다.
    for number, ind in enumerate(indicators, start=1):
        name = ind.get("이름", f"(이름없는 {number}번째 지표)") if isinstance(ind, dict) else f"{number}번째"

        if not isinstance(ind, dict):
            errors.append(f"{number}번째 지표가 {{ }} 블록 형태가 아닙니다.")
            continue

        # 1) 필수 항목이 다 있는가
        for field in REQUIRED_FIELDS:
            if field not in ind:
                errors.append(f"[{name}] 필수 항목 '{field}' 이(가) 빠졌습니다.")

        # 2) 키 중복 검사
        key = ind.get("키")
        if key:
            if key in seen_keys:
                errors.append(f"[{name}] 키 '{key}' 가 다른 지표와 겹칩니다. (키는 서로 달라야 합니다)")
            seen_keys.add(key)

        # 3) 유형 / 척도가 올바른가
        kind = ind.get("유형")
        if kind is not None and kind not in ALLOWED_TYPES:
            errors.append(f"[{name}] 유형 '{kind}' 는 쓸 수 없습니다. ({' / '.join(sorted(ALLOWED_TYPES))} 중 하나)")
        scale = ind.get("척도")
        if scale is not None and scale not in ALLOWED_SCALES:
            errors.append(f"[{name}] 척도 '{scale}' 는 쓸 수 없습니다. ({' / '.join(sorted(ALLOWED_SCALES))} 중 하나)")

        # 4) 범위는 [작은값, 큰값] 형태여야 함
        span = ind.get("범위")
        if span is not None:
            if not (isinstance(span, (list, tuple)) and len(span) == 2
                    and all(_is_number(v) for v in span)):
                errors.append(f"[{name}] '범위' 는 [최소, 최대] 형태의 숫자 두 개여야 합니다.")
            elif span[0] >= span[1]:
                errors.append(f"[{name}] '범위' 의 최소({span[0]})가 최대({span[1]})보다 크거나 같습니다.")

        # 5) 잡음(측정오차 / 공정변동) 검사 - 통계 수업의 핵심 숫자입니다
        for field in ("측정오차", "공정변동"):
            noise = ind.get(field)
            if noise is None:
                continue
            if not isinstance(noise, dict):
                errors.append(f"[{name}] '{field}' 는 {{분포:…, 표준편차:…}} 형태여야 합니다.")
                continue
            # 포아송은 표준편차를 따로 정하지 않습니다.
            # 개수 자료는 평균(λ)이 정해지면 표준편차도 √λ 로 함께 정해집니다.
            if noise.get("분포") == "포아송":
                continue
            sigma = noise.get("표준편차")
            if sigma is None:
                errors.append(f"[{name}] '{field}' 에 '표준편차' 가 없습니다.")
                continue
            if not _is_number(sigma) or sigma < 0:
                errors.append(f"[{name}] '{field}' 의 표준편차는 0 이상의 숫자여야 합니다. (지금: {sigma!r})")
                continue
            if sigma == 0:
                warnings.append(
                    f"[{name}] '{field}' 의 표준편차가 0 입니다. "
                    "변동이 없으면 표준편차·관리도·신뢰구간을 배울 수 없어요.")
            elif span and _is_number(sigma):
                width = span[1] - span[0]
                if sigma > width * 0.2:
                    warnings.append(
                        f"[{name}] 잡음이 너무 큽니다 (표준편차 {sigma} / 범위 {width}). "
                        "정책 효과가 잡음에 묻혀 버립니다.")

        # 6) 관리도 검사 - 자료의 성격에 맞는 관리도인지 봅니다
        chart = ind.get("관리도")
        if chart is not None:
            if not isinstance(chart, dict) or "종류" not in chart:
                errors.append(f"[{name}] '관리도' 는 {{\"종류\": …}} 형태여야 합니다.")
            else:
                kind_of_chart = chart["종류"]
                if kind_of_chart not in ALLOWED_CHARTS:
                    errors.append(
                        f"[{name}] 관리도 종류 '{kind_of_chart}' 는 쓸 수 없습니다. "
                        f"({' / '.join(sorted(ALLOWED_CHARTS))} 중 하나)")
                # 계수(개수) 자료에 X-bar R 를 쓰면 틀립니다 - 흔한 실수라 짚어 줍니다.
                if ind.get("단위") in ("건", "회") and kind_of_chart in ("X-bar R", "X-MR"):
                    warnings.append(
                        f"[{name}] 는 '개수'를 세는 자료(계수형)라 c관리도가 맞습니다. "
                        f"({kind_of_chart} 는 길이·무게처럼 재는 자료(계량형)에 씁니다)")
                if kind_of_chart == "X-bar R" and not chart.get("부분군"):
                    errors.append(
                        f"[{name}] X-bar R 관리도는 한 번에 여러 개를 뽑아야 합니다. "
                        "'부분군' 크기(보통 4~5)를 적어 주세요.")
                low, high = chart.get("규격하한"), chart.get("규격상한")
                if low is not None and high is not None and low >= high:
                    errors.append(f"[{name}] 규격하한({low})이 규격상한({high})보다 크거나 같습니다.")

        # 7) 관측컬럼 이름이 다른 지표의 키와 부딪히지 않는가
        observed = ind.get("관측컬럼")
        if observed and observed == key:
            errors.append(f"[{name}] '관측컬럼' 이 자기 키와 같습니다. 다른 이름을 쓰세요. (예: {key}_조사)")

        # 8) 모르는 항목 이름 경고 (오타 방지)
        for field in ind.keys():
            if field not in REQUIRED_FIELDS and field not in OPTIONAL_FIELDS:
                warnings.append(f"[{name}] '{field}' 라는 항목은 사용되지 않습니다. (오타일 수 있어요)")

    # 9) ★ 엔진이 실제로 만드는 지표인가 (죽은 지표가 되살아나는 것을 막습니다)
    if engine_keys is not None:
        for ind in indicators:
            if not isinstance(ind, dict):
                continue
            key = ind.get("키")
            if key and key not in engine_keys:
                warnings.append(
                    f"[{ind.get('이름')}] '{key}' 는 엔진이 만들지 않는 지표입니다. "
                    "이름이 틀렸거나, 아직 아무 정책도 이 지표를 건드리지 않습니다.")

    return errors, warnings


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


# ── 도우미: 엔진이 실제로 만들어 내는 지표 이름을 모읍니다 ────────────
def engine_indicator_keys():
    """
    새 공장 + 모든 카드가 만들어 내는 지표 이름을 전부 모읍니다.
    (검사기가 '엔진에 없는 지표'를 잡아내는 데 씁니다)
    """
    import os
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    server = os.path.abspath(os.path.join(here, "..", ".."))
    if server not in sys.path:
        sys.path.insert(0, server)

    from app.engine.process_engine import new_plant
    from app.cards.cards_data import CARDS

    keys = set(new_plant().keys())
    for card in CARDS:
        for field in ("즉시효과", "장기효과", "부작용", "성공효과"):
            keys.update((card.get(field) or {}).keys())
    return keys


def check_and_report(indicators):
    """학생이 파일을 실행했을 때 보기 좋게 결과를 보여줍니다."""
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    try:
        engine_keys = engine_indicator_keys()
    except Exception:
        engine_keys = None      # 엔진을 못 불러와도 나머지 검사는 계속합니다

    errors, warnings = validate(indicators, engine_keys)

    print("-" * 66)
    print(f"  dkYield99% 지표 검사 결과  -  지표 {len(indicators)}개")
    print("-" * 66)

    if not errors and not warnings:
        print("  OK 완벽합니다! 모든 지표가 규칙에 맞습니다.")
    if errors:
        print(f"\n  [반드시 고쳐야 할 문제 {len(errors)}개]")
        for m in errors:
            print(f"     - {m}")
    if warnings:
        print(f"\n  [확인해 보면 좋은 점 {len(warnings)}개]")
        for m in warnings:
            print(f"     - {m}")

    # 유형별 / 통계용 요약
    if not errors:
        print("\n  유형별 지표 수:")
        for kind in sorted(ALLOWED_TYPES):
            count = sum(1 for i in indicators if i.get("유형") == kind)
            if count:
                print(f"     - {kind}: {count}개")

        noisy = [i for i in indicators if i.get("측정오차") or i.get("공정변동")]
        charted = [i for i in indicators if i.get("관리도")]
        # 교란변수 = 정책이 건드리지만(운전조건) 어떤 계산에도 안 쓰이는 지표
        confounders = [i for i in indicators
                       if i.get("인과") is False and i.get("유형") == "운전조건"]
        print(f"\n  통계 실습용 요약:")
        print(f"     - 잡음이 있는 지표(변동을 관찰할 수 있음): {len(noisy)}개")
        print(f"     - 관리도를 그릴 수 있는 지표: {len(charted)}개")
        print(f"     - 교란변수(움직이지만 원인은 아닌 지표): {len(confounders)}개")
        if confounders:
            print(f"       → {', '.join(i['이름'] for i in confounders)}")
            print(f"       (함께 움직이지만 원인은 아닙니다 - 14주에 다룹니다)")

    print("-" * 66)
    if errors:
        print("  -> 위의 문제를 먼저 고친 뒤 다시 실행해 보세요:  python indicators_data.py")
    else:
        print("  -> 통계 실습에서 바로 사용할 수 있습니다. 수고하셨어요!")
    print("-" * 66)
