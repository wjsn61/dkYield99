# ════════════════════════════════════════════════════════════════════
#  dkYield99% 공정 엔진  (process_engine.py)
#
#  이 파일은 "카드를 받아서 화학공정을 바꾸는 두뇌"입니다.
#  동시에 파이썬의 기초가 모두 담긴 '학습용 코드'입니다.
#  (함수/변수 이름은 영어, 설명 주석과 데이터 이름은 한국어)
#
#     변수(variable)   : 공정의 숫자들을 담아둡니다              → new_plant()
#     조건문(if/elif)  : "예산이 충분하면", "순도가 높으면"        → enact_card()
#     순환문(for)      : "모든 효과를 하나씩", "설비를 하나씩"      → apply_effect()
#     함수(def)        : 기능을 이름 붙여 재사용합니다            → 아래 전부
#
#  ▶ 직접 실행해서 공장이 굴러가는 걸 보세요:  python process_engine.py
#  ▶ 숫자나 카드를 바꿔보며 수율이 어떻게 달라지는지 실험하세요!
# ════════════════════════════════════════════════════════════════════


#  ▶ 잡음(변동)을 켜려면 시드를 주세요:  new_plant(seed=20260901)
#     시드가 없으면 예전과 똑같이 '한 치의 오차도 없는' 공장이 됩니다.

# 잡음 엔진을 불러옵니다.
# (이 파일을 직접 실행할 때도 옆에 있는 noise.py 를 찾을 수 있게 두 번 시도합니다)
try:
    from app.engine import noise
except ImportError:      # python process_engine.py 로 직접 실행하는 경우
    import noise


# ── 1. 변수: 0~100 사이로만 움직이는 "비율형" 지표들 ──────────────────
PERCENT_INDICATORS = [
    "전환율", "선택도", "분리회수율", "순도", "수율",
    "안전지수", "환경지수", "촉매활성", "설비노후도", "기술력",
]

# ── 1-1. 순도의 천장 ─────────────────────────────────────────────────
#    100% 순수한 화학제품은 세상에 없습니다. 아무리 잘 만들어도
#    미량의 불순물이 남습니다. 그래서 천장을 99.9% 로 둡니다.
PURITY_CEILING = 99.9
#    체감이 시작되는 기준 순도 (이보다 높아질수록 올리기 어려워집니다)
PURITY_BASE = 90.0

# 지표별로 따로 정한 상·하한 (없으면 비율형 기본 규칙 0~100 을 씁니다)
INDICATOR_LIMITS = {"순도": (0, PURITY_CEILING)}


# ── 2. 함수: 새 공장을 하나 만든다 (변수 모음) ───────────────────────
def new_plant(seed=None):
    """
    게임 시작 시점의 공정 상태입니다. 시나리오 초기값을 여기서 바꿀 수 있어요.

    seed 를 주면 공정이 '진짜 공장처럼' 흔들리기 시작합니다.
      - 전환율·선택도·분리회수율이 매달 조금씩 다르고 (원료 조성·촉매 상태)
      - 그래서 수율도 함께 흔들리고 (세 값의 곱이니까요)
      - 순도는 분석기로 재는 값이라 진짜 순도와 조금 다르게 나옵니다
    같은 시드를 주면 언제 다시 돌려도 똑같은 공장이 나옵니다. (재현성)
    """
    plant = {
        # ▼ 화면에 보이는 핵심 지표 7개
        "예산": 100,         # 억
        "월이익": 12,        # 억 (매 턴 다시 계산됨)
        "생산량": 1000,      # 톤/월
        "수율": 0,           # %  (전환율×선택도×분리회수율로 계산)
        "순도": 94,          # %
        "안전지수": 75,      # 0~100
        "환경지수": 68,      # 0~100
        # ▼ 공정/내부 변수
        "전환율": 78,        # %
        "선택도": 92,        # %
        "분리회수율": 98,    # %
        "에너지비": 18,      # 억/월
        "원료비": 8,         # 억/월
        "촉매비": 1,         # 억/월
        "환경처리비": 1,     # 억/월
        "촉매활성": 80,
        "설비노후도": 18,
        "기술력": 10,
        "제품단가": 6.0,     # 생산량 × 수율 × 제품단가/100 = 매출(억)
        "시장수요": 1200,    # 톤/월
        "반응기온도": 80,    # ℃
        "압력": 1.2,         # bar
        "체류시간": 2.0,     # h
        "환류비": 1.5,
        "유량": 100,
        # ▼ 진행 상태
        "턴": 1,
        "최대턴": 12,
        "누적이익": 0,
        "설비목록": [],      # 설치한 설비 카드(유지비·장기효과)
        "연구중": [],        # 진행 중인 R&D [{카드, 남은턴}]
        "기록": [],
        # ▼ 잡음(변동) 설정
        "난수시드": seed,               # None 이면 잡음 없음
        "잡음버전": noise.NOISE_VERSION,  # 규칙이 바뀌어도 예전 게임을 재현하기 위해
    }
    plant["수율"] = calculate_yield(plant)   # 수율은 계산해서 채운다
    return plant


# ── 3. 함수: 수율을 계산한다 (핵심 공식) ─────────────────────────────
def calculate_yield(plant, actual=None):
    """
    수율 = 전환율 × 선택도 × 분리회수율  (각 %, ÷10000)

    actual 을 주면 그 '실측값'으로 계산합니다.
    안 주면 설정값 그대로 계산합니다 (예전과 완전히 같은 동작).
    """
    src = actual or plant
    y = src["전환율"] * src["선택도"] * src["분리회수율"] / 10000
    return round(min(100, max(0, y)), 1)


# ── 4. 함수: 순도를 올리는 일은 갈수록 어려워진다 ────────────────────
def purity_gain(current, change):
    """
    순도 94% → 95% 는 쉽지만, 99% → 99.5% 는 훨씬 어렵습니다.
    남아 있는 여유(천장까지의 거리)에 비례해서만 올라가게 만듭니다.

    분리공정의 핵심이 여기 있습니다:
        마지막 1% 를 올리는 데 드는 비용이 가장 비싸다.

    (순도가 떨어질 때는 체감 없이 그대로 떨어집니다 - 망가지는 건 쉽습니다)
    """
    if change <= 0:
        return change
    room = PURITY_CEILING - current          # 천장까지 남은 거리
    if room <= 0:
        return 0
    return round(change * room / (PURITY_CEILING - PURITY_BASE), 2)


# ── 4-1. 함수: 효과 하나를 공정에 반영한다 (순환문 + 조건문) ──────────
def apply_effect(plant, effect, reason=""):
    """effect 는 {"전환율": +5, "안전지수": -3} 같은 모양입니다."""
    # 순환문(for): 효과에 적힌 지표를 하나씩 꺼냅니다.
    for indicator, change in effect.items():

        # 조건문(if): 처음 보는 지표라면 0에서 시작하게 만들어 줍니다.
        if indicator not in plant:
            plant[indicator] = 0

        # 조건문(if): 순도만 특별합니다 - 높을수록 올리기 어렵습니다.
        if indicator == "순도":
            change = purity_gain(plant["순도"], change)

        plant[indicator] = round(plant[indicator] + change, 2)

        # 조건문(if): 따로 정한 상·하한이 있으면 그것을 먼저 씁니다.
        if indicator in INDICATOR_LIMITS:
            low, high = INDICATOR_LIMITS[indicator]
            plant[indicator] = max(low, min(high, plant[indicator]))
        # 조건문(if): 나머지 비율형 지표는 0~100을 벗어나지 않게 묶어 둡니다.
        elif indicator in PERCENT_INDICATORS:
            if plant[indicator] > 100:
                plant[indicator] = 100
            elif plant[indicator] < 0:
                plant[indicator] = 0

    if reason:
        plant["기록"].append(f"{reason} -> {effect}")


# ── 5. 함수: 카드 하나를 시행한다 (조건문이 핵심) ────────────────────
def enact_card(plant, card):
    """카드를 시행할 수 있으면 시행하고, 안 되면 이유를 알려줍니다."""

    # 조건문(if): 일회성 설비는 이미 설치했으면 다시 못 함
    if card.get("일회성") and card["아이디"] in [s["아이디"] for s in plant["설비목록"]]:
        return False, f"'{card['이름']}'은(는) 이미 설치되어 있습니다."

    # 조건문(if): 예산이 모자라면 시행 불가
    if plant["예산"] < card["비용"]:
        return False, f"예산이 부족합니다. (필요 {card['비용']}억 / 보유 {round(plant['예산'],1)}억)"

    # 돈을 쓴다
    plant["예산"] = round(plant["예산"] - card["비용"], 1)

    # 조건문(if): 연구 카드면 '연구중' 목록에 넣고 끝 (성공효과는 나중에)
    if card["분류"] == "연구":
        plant["연구중"].append({"카드": card, "남은턴": card["연구기간"]})
        plant["기록"].append(f"[R&D 시작] {card['이름']} ({card['연구기간']}턴 소요)")
        return True, f"R&D 시작: '{card['이름']}' ({card['연구기간']}턴)"

    # 운전/설비/안전환경/시장 카드: 즉시효과 + 부작용 반영
    apply_effect(plant, card.get("즉시효과", {}), reason=f"[{card['이름']}] 즉시효과")
    if "부작용" in card:
        apply_effect(plant, card["부작용"], reason=f"[{card['이름']}] 부작용")

    # 조건문(if): 설비(유지비/일회성/장기효과 보유)는 설비목록에 등록
    if card.get("유지비") or card.get("일회성") or "장기효과" in card:
        plant["설비목록"].append(card)

    # 운전 변경으로 전환율/선택도/회수율이 바뀌면 수율을 다시 계산
    plant["수율"] = calculate_yield(plant)
    return True, f"'{card['이름']}' 시행 완료!"


# ── 6. 함수: 매출 / 비용 / 이익 계산 ─────────────────────────────────
def quality_mult(purity):
    """순도에 따른 판매 보정 (시장 요구 순도 98%)."""
    if purity >= 99: return 1.15      # 프리미엄
    if purity >= 98: return 1.08      # 고품질
    if purity >= 94: return 1.00      # 정상 판매
    if purity >= 90: return 0.85      # 할인
    return 0.55                        # 반품 위험

def calculate_revenue(plant):
    """
    매출 = 실제로 만들어 판 제품량 × 제품단가 × 순도 보정

    핵심: 원료를 아무리 많이 넣어도(생산량), 수율이 낮으면 제품은 적게 나옵니다.
          실제 제품량 = 생산량 × 수율
          그래서 '수율 99%'가 이 게임의 제목입니다.
    """
    처리량 = plant.get("생산량_실적", plant["생산량"])
    실제제품량 = 처리량 * plant["수율"] / 100
    return round(실제제품량 * plant["제품단가"] / 100 * quality_mult(plant["순도"]), 1)

def calculate_cost(plant):
    upkeep = sum(s.get("유지비", 0) for s in plant["설비목록"])     # 설비 유지비
    maintenance = round(2 + plant["설비노후도"] * 0.04, 1)         # 설비노후도↑ → 보수비↑
    return round(plant["원료비"] + plant["에너지비"] + plant["촉매비"]
                 + maintenance + plant["환경처리비"] + upkeep, 1)


# ── 7. 함수: R&D를 한 턴 진행시킨다 (순환문 + 조건문) ────────────────
def advance_research(plant):
    done = []
    for r in plant["연구중"]:
        r["남은턴"] -= 1
        if r["남은턴"] <= 0:                       # 연구 완료!
            card = r["카드"]
            apply_effect(plant, card.get("성공효과", {}), reason=f"[R&D 성공] {card['이름']}")
            plant["기술력"] = min(100, plant["기술력"] + 5)
            plant["기록"].append(f"🎉 [R&D 성공] {card['이름']} - 기술력 +5")
            done.append(r)
    for r in done:
        plant["연구중"].remove(r)


# ── 8. 함수: 한 턴을 마무리한다 (순환문 + 조건문) ────────────────────
def end_turn(plant):
    """설비 장기효과·R&D 진행·수율 재계산·이익 정산을 하고 다음 턴으로 갑니다."""

    # 순환문(for): 설치된 설비의 장기효과 적용
    for s in plant["설비목록"]:
        if "장기효과" in s:
            apply_effect(plant, s["장기효과"], reason=f"[{s['이름']}] 장기효과")

    # R&D 진행
    advance_research(plant)

    turn = plant["턴"]

    # 설비는 매 턴 조금씩 노후화
    plant["설비노후도"] = min(100, plant["설비노후도"] + 1)

    # 리스크 드리프트 (조건문): 고온·노후 → 안전 하락 / 에너지 → 환경 하락
    danger = round(plant["설비노후도"] * 0.05 + max(0, plant["반응기온도"] - 90) * 0.2, 1)
    apply_effect(plant, {"안전지수": -danger}) if danger else None
    apply_effect(plant, {"환경지수": -round(plant["에너지비"] * 0.04, 1)})

    # ── 이번 달 실제로 일어난 값 (공정변동) ─────────────────────────
    #   운전 설정은 그대로여도, 원료 조성·촉매 상태·탑 운전은 매달 조금씩 다릅니다.
    #   ★ 세 값을 따로 흔들면, 그 흔들림이 곱해져서 수율의 흔들림이 됩니다.
    #      이것이 '오차 전파'입니다 (14주).
    actual = {
        key: noise.jitter(plant, turn, key, plant[key])
        for key in ("전환율", "선택도", "분리회수율")
    }
    for key, value in actual.items():
        plant[key + "_실측"] = round(value, 2)

    # 수율 다시 계산 - 설정값이 아니라 '이번 달 실측값'으로 계산합니다
    plant["수율"] = calculate_yield(plant, actual=actual)

    # 실제 처리량도 가동률에 따라 흔들립니다
    plant["생산량_실적"] = round(noise.jitter(plant, turn, "생산량", plant["생산량"]), 1)

    # 매출·비용·이익 정산
    revenue = calculate_revenue(plant)
    cost = calculate_cost(plant)
    plant["월이익"] = round(revenue - cost, 1)
    plant["예산"] = round(plant["예산"] + plant["월이익"], 1)
    plant["누적이익"] = round(plant["누적이익"] + plant["월이익"], 1)

    # ── 관측 (분석기·계기로 재기) ───────────────────────────────────
    #   ★ 진값은 건드리지 않습니다. 재서 알아낸 값을 따로 적을 뿐입니다.
    noise.observe(plant, turn)

    #   순도는 한 번만 재지 않고 같은 달에 5개를 뽑습니다.
    #   한 번만 재면 '값이 튄 것'인지 '공정이 변한 것'인지 알 수 없기 때문입니다.
    #   이 5개 묶음(부분군)이 13주 X-bar R 관리도의 재료가 됩니다.
    plant["순도샘플"] = noise.sample_group(plant, turn, "순도", 5)

    # 다음 턴으로
    plant["턴"] += 1


# ── 9. 함수: 최종 평가 (조건문으로 엔딩 등급 결정) ──────────────────
def evaluate_ending(plant):
    y, p, prof = plant["수율"], plant["순도"], plant["누적이익"]
    sf, ev = plant["안전지수"], plant["환경지수"]

    if y >= 99 and p >= 99 and sf >= 80 and ev >= 75:
        grade, name = "S", "Yield Master - 수율의 달인"
    elif y >= 90 and p >= 98 and prof >= 150:
        grade, name = "A", "고효율 플랜트"
    elif y >= 85 and p >= 96 and prof >= 80:
        grade, name = "B", "안정 운영"
    elif prof >= 0 and p >= 90:
        grade, name = "C", "생산은 성공 (비용·품질 과제)"
    elif prof < 0:
        grade, name = "D", "적자 공장"
    else:
        grade, name = "F", "공정 실패"
    return grade, name


# ════════════════════════════════════════════════════════════════════
#  데모: 파일을 실행하면 작은 공장 한 판이 자동으로 돌아갑니다.
# ════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import os, sys
    try: sys.stdout.reconfigure(encoding="utf-8")     # 윈도우 콘솔 한글 깨짐 방지
    except Exception: pass

    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(here, "..", "cards"))
    from cards_data import CARDS

    card_by_id = {c["아이디"]: c for c in CARDS}

    def show(p):
        print(f"  [턴 {p['턴']:>2}] 예산 {p['예산']:>6}억  이익 {p['월이익']:>5}억  "
              f"생산 {p['생산량']:>4}톤  수율 {p['수율']:>5}%  순도 {p['순도']:>4}%  "
              f"안전 {p['안전지수']:>3}  환경 {p['환경지수']:>3}")

    print("=" * 78)
    print("  dkYield99% - 자동 플레이 데모 (에스터 생산 플랜트)")
    print("=" * 78)

    plant = new_plant()
    show(plant)

    # 이번 데모에서 펼칠 카드 계획 (턴 → 시행할 카드 아이디)
    plan = {
        1: "high_selectivity_catalyst",   # R&D 시작 (4턴 뒤 성공)
        2: "reflux_up",                   # 순도↑
        3: "heat_recovery",               # 에너지비↓ 환경↑
        4: "molar_ratio",                 # 전환율↑ 선택도↑
        5: "reactor_temp_up",             # 전환율↑ (부작용 안전↓)
        6: "coolant_up",                  # 안전 보강
        7: "membrane_research",           # R&D 분리
        8: "online_analyzer",             # 순도 안정
        9: "preventive_maint",            # 노후·안전 관리
        10: "condition_opt",              # R&D 조건 최적화
    }

    for turn in range(1, 13):
        cid = plan.get(turn)
        if cid:
            ok, msg = enact_card(plant, card_by_id[cid])
            print(f"    -> {msg}")
        end_turn(plant)
        show(plant)

    print("-" * 78)
    grade, name = evaluate_ending(plant)
    print(f"  최종 등급: {grade}급 - {name}  |  누적이익 {plant['누적이익']}억  수율 {plant['수율']}%  순도 {plant['순도']}%")
    print("=" * 78)
