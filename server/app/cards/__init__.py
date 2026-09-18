# ════════════════════════════════════════════════════════════════════
#  cards 패키지 - 공정 엔진이 카드를 가져가는 입구
#  ※ 학생은 이 파일을 건드리지 않습니다. cards_data.py 만 편집하세요.
# ════════════════════════════════════════════════════════════════════
"""
공정 엔진에서 사용 예:

    from app.cards import load_cards

    cards = load_cards()           # 검증을 통과한 카드 목록
    for card in cards:
        print(card["이름"], card["분류"], card["비용"])
"""

from .cards_data import CARDS
from .card_schema import validate, CardError


def load_cards():
    """검증을 통과한 카드 목록을 돌려줍니다. (문제가 있으면 멈춥니다)"""
    errors, _ = validate(CARDS)
    if errors:
        raise CardError("카드 정의에 문제가 있습니다:\n  - " + "\n  - ".join(errors))
    return CARDS


ALL_CARDS = CARDS

__all__ = ["load_cards", "CARDS", "ALL_CARDS", "validate", "CardError"]
