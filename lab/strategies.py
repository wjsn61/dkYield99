# ════════════════════════════════════════════════════════════════════
#  카드 묶음 (strategies.py) - 학생 편집 파일  (★ 여기를 고치세요 ★)
#
#  같은 공장을 여러 번 돌려 볼 때 쓸 '운전 계획표'입니다.
#  {턴: "카드 아이디"} 모양으로, 몇 달째에 무엇을 할지 적습니다.
#
#  ▶ 왜 필요한가요?
#     통계는 '여러 개'가 있어야 시작됩니다.
#     같은 계획을 시드만 바꿔 여러 번 돌리면,
#     "카드 때문에 달라진 것"과 "그냥 조업 변동"을 구분할 수 있습니다.
#
#  ▶ 카드 아이디는 어디서 보나요?
#     server/app/cards/cards_data.py 의 "아이디" 항목
#
#  ▶ ★ '무조작' 을 지우지 마세요.
#     비교할 기준(대조군)이 없으면 어떤 결론도 낼 수 없습니다.
# ════════════════════════════════════════════════════════════════════


STRATEGIES = {

    # ── 대조군 - 아무것도 하지 않는다 ──────────────────────────────
    #    ★ 모든 비교의 기준입니다. 지우지 마세요.
    "무조작": {
        "설명": "아무 카드도 쓰지 않는다 (비교 기준)",
        "계획": {},
    },

    # ── 균형 운전 ─────────────────────────────────────────────────
    "균형형": {
        "설명": "수율과 순도를 함께 관리한다",
        "계획": {
            1: "molar_ratio",                 # 전환율·선택도 ↑
            2: "reflux_up",                   # 순도 ↑ (품질 보정)
            3: "heat_recovery",               # 에너지비 ↓
            5: "high_selectivity_catalyst",   # R&D 선택도
            9: "condition_opt",               # R&D 조건 최적화
            11: "online_analyzer",            # 측정오차 ↓
        },
    },

    # ── 수율 중심 ─────────────────────────────────────────────────
    "수율형": {
        "설명": "전환율과 선택도를 끌어올린다",
        "계획": {
            1: "high_selectivity_catalyst",
            2: "molar_ratio",
            4: "reactor_temp_up",             # 전환율 ↑ (순도 ↓ 주의!)
            6: "coolant_up",                  # 안전 보강
            8: "condition_opt",
            10: "residence_up",
        },
    },

    # ── 품질 중심 ─────────────────────────────────────────────────
    "품질형": {
        "설명": "순도를 최우선으로 한다",
        "계획": {
            1: "reflux_up",
            2: "hx_clean",
            3: "online_analyzer",
            5: "qc_sampling",
            7: "high_purity_product",
            10: "molar_ratio",
        },
    },

    # ── 비용 절감 ─────────────────────────────────────────────────
    "저비용형": {
        "설명": "에너지비를 최대한 줄인다 (품질을 놓치기 쉽다)",
        "계획": {
            1: "hx_clean",
            2: "heat_recovery",
            4: "reflux_down",                 # 에너지 ↓ 그런데 순도도 ↓
            6: "condition_opt",
            9: "hx_clean",
        },
    },

    # ── 안전·환경 중심 ────────────────────────────────────────────
    "안전환경형": {
        "설명": "사고와 규제 위험을 줄인다",
        "계획": {
            1: "coolant_up",
            2: "preventive_maint",
            4: "wastewater",
            6: "runaway_analysis",
            8: "reactor_temp_down",
        },
    },

    # ✏️ 여기에 여러분의 전략을 추가해 보세요.
    # "나의전략": {
    #     "설명": "무엇을 노리는 운전인가요?",
    #     "계획": {1: "reflux_up", 5: "molar_ratio"},
    # },
}


# ════════════════════════════════════════════════════════════════════
#  아래는 손대지 않아도 됩니다 - 실행하면 전략 목록을 확인해 줍니다.
# ════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import os
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(here, "..", "server"))
    try:
        from app.cards import load_cards
        known = {c["아이디"] for c in load_cards()}
    except Exception as e:
        print(f"  (카드 목록을 못 읽었습니다: {e})")
        known = None

    print("-" * 66)
    print(f"  카드 묶음 {len(STRATEGIES)}개")
    print("-" * 66)

    problems = []
    for name, spec in STRATEGIES.items():
        plan = spec.get("계획", {})
        print(f"\n  [{name}] {spec.get('설명', '')}")
        if not plan:
            print("     (아무 카드도 없음 - 대조군)")
            continue
        for turn in sorted(plan):
            cid = plan[turn]
            mark = ""
            if known is not None and cid not in known:
                mark = "   ← ❌ 이런 아이디의 카드가 없습니다"
                problems.append(f"[{name}] {turn}턴 '{cid}'")
            print(f"     {turn:>2}턴  {cid}{mark}")

    print("\n" + "-" * 66)
    if problems:
        print(f"  ❌ 고쳐야 할 곳 {len(problems)}개:")
        for p in problems:
            print(f"     - {p}")
        print("  -> cards_data.py 의 '아이디' 를 확인하세요.")
    else:
        print("  OK 모든 카드 아이디가 올바릅니다.")
        print("  -> python run_batch.py --strategy 품질형 --n 10  으로 돌려 보세요.")
    print("-" * 66)
