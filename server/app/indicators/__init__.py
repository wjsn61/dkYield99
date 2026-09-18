# ════════════════════════════════════════════════════════════════════
#  indicators 패키지 - 통계 실습이 지표 설명서를 가져가는 입구
#  ※ 학생은 이 파일을 건드리지 않습니다. indicators_data.py 만 편집하세요.
# ════════════════════════════════════════════════════════════════════
"""
사용 예:

    from app.indicators import load_indicators, by_key

    for ind in load_indicators():          # 검증을 통과한 지표 목록
        print(ind["이름"], ind["단위"])

    print(by_key()["순도"])                # 키로 바로 찾기
"""

from .indicators_data import INDICATORS
from .indicator_schema import validate, check_and_report, IndicatorError


def load_indicators():
    """검증을 통과한 지표 목록을 돌려줍니다. (문제가 있으면 멈춥니다)"""
    errors, _warnings = validate(INDICATORS)
    if errors:
        raise IndicatorError("지표 정의에 문제가 있습니다:\n  - " + "\n  - ".join(errors))
    return INDICATORS


def by_key():
    """키로 바로 찾을 수 있게 사전(dict)으로 정리해 돌려줍니다."""
    return {ind["키"]: ind for ind in load_indicators()}


def csv_columns():
    """데이터를 내려받을 때 쓸 컬럼 이름을 순서대로 돌려줍니다.

    진값 옆에 관측값(예: 주민만족 / 주민만족_조사)을 나란히 놓습니다.
    두 값을 나란히 보는 것이 '관측 ≠ 진실'을 배우는 출발점입니다.
    """
    columns = []
    for ind in load_indicators():
        if not ind.get("CSV포함"):
            continue
        columns.append(ind["키"])
        if ind.get("관측컬럼"):
            columns.append(ind["관측컬럼"])
    return columns


def noisy_indicators():
    """잡음(측정오차·공정변동)이 있는 지표만 골라 돌려줍니다."""
    return [i for i in load_indicators()
            if i.get("측정오차") or i.get("공정변동")]


def confounders():
    """
    교란변수만 골라 돌려줍니다.

    정책이 건드려서 움직이기는 하지만(운전조건) 어떤 계산에도 쓰이지 않는 지표입니다.
    다른 지표와 상관관계가 보여도 원인이 아닙니다 - 11주 '상관 ≠ 인과'의 재료.
    """
    return [i for i in load_indicators()
            if i.get("인과") is False and i.get("유형") == "운전조건"]


__all__ = [
    "load_indicators", "by_key", "csv_columns",
    "noisy_indicators", "confounders",
    "INDICATORS", "validate", "check_and_report", "IndicatorError",
]
