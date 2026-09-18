# ════════════════════════════════════════════════════════════════════
#  카드 검사기 (card_schema.py)
#  ※ 이 파일은 "규칙을 검사하는 도구"입니다. 학생은 보통 건드리지 않습니다.
#     카드를 바꾸려면 cards_data.py 만 편집하세요.
#  ※ 코드의 함수/변수 이름은 영어, 설명(주석)과 카드 내용은 한국어입니다.
# ════════════════════════════════════════════════════════════════════
"""
하는 일:
  - cards_data.py 의 CARDS 가 규칙에 맞는지 검사합니다.
  - 틀린 곳을 '친절한 한국어'로 알려줍니다.
  - 다른 코드(공정 엔진)는 load_cards() 로 검증된 카드를 가져갑니다.
"""

# -- 카드 분류: 이 5가지 중 하나여야 합니다 --------------------------
ALLOWED_CATEGORIES = {"운전", "설비", "연구", "안전환경", "시장"}

# -- 효과에 쓸 수 있는 지표 이름 (오타 잡기용) -----------------------
ALLOWED_INDICATORS = {
    # 핵심 지표
    "예산", "월이익", "생산량", "수율", "순도", "안전지수", "환경지수",
    # 반응/분리
    "전환율", "선택도", "분리회수율", "촉매활성",
    # 비용
    "에너지비", "원료비", "촉매비", "환경처리비",
    # 설비/기술/시장
    "설비노후도", "기술력", "제품단가", "시장수요",
    # 운전 조건
    "반응기온도", "압력", "체류시간", "환류비", "유량",
}

# -- 반드시 있어야 하는 항목 -----------------------------------------
REQUIRED_FIELDS = ["아이디", "이름", "분류", "비용"]
# -- 있어도 되고 없어도 되는 항목 -----------------------------------
OPTIONAL_FIELDS = ["즉시효과", "부작용", "장기효과", "유지비", "일회성", "연구기간", "성공효과"]

EFFECT_FIELDS = ["즉시효과", "부작용", "장기효과", "성공효과"]


class CardError(Exception):
    """카드 정의가 규칙에 어긋날 때 발생합니다."""
    pass


def validate(cards):
    """
    카드 목록을 검사해서 (errors, warnings) 두 목록을 돌려줍니다.
      - errors  : 게임이 못 돌아가는 문제 (반드시 고쳐야 함)
      - warnings: 오타로 의심되는 것 (게임은 돌아가지만 확인 권장)
    """
    errors, warnings = [], []
    seen_ids = set()

    if not isinstance(cards, list):
        errors.append("CARDS 는 [ ... ] 형태의 목록이어야 합니다.")
        return errors, warnings

    for number, card in enumerate(cards, start=1):
        name = card.get("이름", f"(이름없는 {number}번째 카드)") if isinstance(card, dict) else f"{number}번째"

        if not isinstance(card, dict):
            errors.append(f"{number}번째 카드가 {{ }} 블록 형태가 아닙니다.")
            continue

        # 1) 필수 항목
        for field in REQUIRED_FIELDS:
            if field not in card:
                errors.append(f"[{name}] 필수 항목 '{field}' 이(가) 빠졌습니다.")

        # 2) 아이디 중복
        cid = card.get("아이디")
        if cid:
            if cid in seen_ids:
                errors.append(f"[{name}] 아이디 '{cid}' 가 다른 카드와 겹칩니다.")
            seen_ids.add(cid)

        # 3) 분류
        category = card.get("분류")
        if category is not None and category not in ALLOWED_CATEGORIES:
            errors.append(f"[{name}] 분류 '{category}' 는 쓸 수 없습니다. ({' / '.join(sorted(ALLOWED_CATEGORIES))} 중 하나)")

        # 4) 비용 / 유지비
        for field in ["비용", "유지비"]:
            v = card.get(field)
            if v is not None and (not _is_number(v) or v < 0):
                errors.append(f"[{name}] '{field}' 은(는) 0 이상의 숫자여야 합니다. (지금: {v!r})")

        # 5) 분류별 필수 (연구는 연구기간+성공효과, 그 외는 즉시효과)
        if category == "연구":
            dur = card.get("연구기간")
            if not isinstance(dur, int) or not (1 <= dur <= 12):
                errors.append(f"[{name}] 연구 카드는 '연구기간'(1~12 정수)이 필요합니다. (지금: {dur!r})")
            if not isinstance(card.get("성공효과"), dict):
                errors.append(f"[{name}] 연구 카드는 '성공효과'(딕셔너리)가 필요합니다.")
        elif category in ALLOWED_CATEGORIES:
            if not isinstance(card.get("즉시효과"), dict):
                errors.append(f"[{name}] '{category}' 카드는 '즉시효과'(딕셔너리)가 필요합니다.")

        # 6) 효과 지표 검사
        for ef in EFFECT_FIELDS:
            effect = card.get(ef)
            if effect is None:
                continue
            if not isinstance(effect, dict):
                errors.append(f"[{name}] '{ef}' 은(는) {{지표: 숫자}} 형태여야 합니다.")
                continue
            for indicator, change in effect.items():
                if not _is_number(change):
                    errors.append(f"[{name}] '{ef}' 의 '{indicator}' 값은 숫자여야 합니다. (지금: {change!r})")
                # 지표 이름이 틀리면 그 효과는 '조용히 사라집니다'.
                # 게임은 아무 일 없이 돌아가는데 카드만 효과가 없어서
                # 원인을 찾기가 매우 어렵습니다. 그래서 경고가 아니라 오류입니다.
                if indicator not in ALLOWED_INDICATORS:
                    errors.append(
                        f"[{name}] '{ef}' 의 '{indicator}'"
                        f"{particle(indicator, '은', '는')} 쓸 수 없는 지표 이름입니다."
                        + _did_you_mean(indicator, ALLOWED_INDICATORS))

        # 7) 모르는 항목 경고
        for key in card.keys():
            if key not in REQUIRED_FIELDS and key not in OPTIONAL_FIELDS:
                warnings.append(f"[{name}] '{key}' 라는 항목은 사용되지 않습니다. (오타일 수 있어요)")

    return errors, warnings


def _is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def particle(word, with_final, without_final):
    """
    받침 유무에 따라 한국어 조사를 골라 줍니다.

        particle("전환율", "을", "를")  ->  "을"   (율에 받침 ㄹ)
        particle("선택도", "을", "를")  ->  "를"   (도에 받침 없음)

    안내문이 '전환율를' 처럼 어색해지지 않게 하려고 씁니다.
    """
    if not word:
        return without_final
    last = word[-1]
    if "가" <= last <= "힣":                       # 한글 음절인가
        return with_final if (ord(last) - 0xAC00) % 28 else without_final
    return without_final


def _did_you_mean(wrong, choices):
    """
    틀린 이름과 가장 비슷한 이름을 찾아 '혹시 이거였나요?' 를 붙여 줍니다.

    '전환률' 이라고 잘못 쓰면 '전환율' 을 제안하는 식입니다.
    (difflib 은 파이썬에 기본으로 들어 있어서 따로 설치할 필요가 없습니다)
    """
    import difflib
    close = difflib.get_close_matches(wrong, sorted(choices), n=2, cutoff=0.6)
    if close:
        # 조사는 마지막 후보에만 붙입니다 ("'전환율' 또는 '선택도'를 쓰려던…")
        quoted = [f"'{c}'" for c in close]
        suggestions = " 또는 ".join(quoted) + particle(close[-1], "을", "를")
        return f" 혹시 {suggestions} 쓰려던 건가요?"
    return " (쓸 수 있는 이름은 cards_data.py 맨 위 주석에 있습니다)"


def check_and_report(cards):
    """학생이 파일을 실행했을 때 보기 좋게 결과를 보여줍니다."""
    import sys
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass

    errors, warnings = validate(cards)

    print("-" * 60)
    print(f"  dkYield99% 카드 검사 결과  -  카드 {len(cards)}장")
    print("-" * 60)

    if not errors and not warnings:
        print("  OK 완벽합니다! 모든 카드가 규칙에 맞습니다.")
    if errors:
        print(f"\n  [반드시 고쳐야 할 문제 {len(errors)}개]")
        for m in errors: print(f"     - {m}")
    if warnings:
        print(f"\n  [확인해 보면 좋은 점 {len(warnings)}개]")
        for m in warnings: print(f"     - {m}")

    if not errors:
        print("\n  분류별 카드 수:")
        for c in sorted(ALLOWED_CATEGORIES):
            n = sum(1 for x in cards if x.get("분류") == c)
            if n: print(f"     - {c}: {n}장")

    print("-" * 60)
    print("  -> 위 문제를 고친 뒤 다시 실행하세요:  python cards_data.py" if errors
          else "  -> 게임에서 바로 사용할 수 있습니다. 수고하셨어요!")
    print("-" * 60)


def load_cards():
    """공정 엔진이 호출하는 함수. 검증을 통과한 카드 목록을 돌려줍니다."""
    from cards_data import CARDS
    errors, _ = validate(CARDS)
    if errors:
        raise CardError("카드 정의에 문제가 있습니다:\n  - " + "\n  - ".join(errors))
    return CARDS
