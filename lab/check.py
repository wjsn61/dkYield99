# ════════════════════════════════════════════════════════════════════
#  채점기 (check.py)
#  ※ 이 파일은 "여러분이 만든 함수를 검사하는 도구"입니다. 안 만져도 됩니다.
#
#  틀렸다고만 말하지 않고, 무엇이 어긋났는지 짚어 줍니다.
#  (policy_schema.py 와 같은 방식입니다)
# ════════════════════════════════════════════════════════════════════
import math
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ── 손으로 검산할 수 있는 아주 작은 자료 ────────────────────────────
#    합계 = 50, 개수 = 5, 평균 = 10
#    편차 = -4, -2, 0, 2, 4  →  제곱합 = 16+4+0+4+16 = 40
#    표본분산 = 40 / 4 = 10  →  표준편차 = √10 ≒ 3.1623
SAMPLE = [6, 8, 10, 12, 14]
ANSWER_MEAN = 10.0
ANSWER_STDEV_SAMPLE = math.sqrt(10)        # n-1 로 나눈 값 (정답)
ANSWER_STDEV_POP = math.sqrt(8)            # n 으로 나눈 값 (흔한 실수)
ANSWER_CV = ANSWER_STDEV_SAMPLE / ANSWER_MEAN * 100

# 값이 뒤바뀌면 티가 나도록 일부러 순서를 섞은 자료
SHUFFLED = [12, 6, 14, 8, 10]


def _close(a, b, tol=1e-6):
    return a is not None and abs(a - b) < tol


def _run(fn, values):
    """학생 함수를 안전하게 실행합니다. 오류가 나면 메시지로 돌려줍니다."""
    try:
        return fn(list(values)), None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


# ── 개별 검사 ────────────────────────────────────────────────────────
def check_mean(fn):
    got, err = _run(fn, SAMPLE)
    if err:
        return False, f"실행 중 오류가 났습니다 - {err}"
    if got is None:
        return False, "아직 만들지 않았습니다. (pass 를 지우고 return 을 쓰세요)"
    if _close(got, ANSWER_MEAN):
        return True, f"평균 {got} - 정답입니다."
    if _close(got, sum(SAMPLE)):
        return False, (f"{got} 는 '합계'입니다. 개수({len(SAMPLE)})로 나누는 것을 잊었습니다.")
    return False, (f"{got} 가 나왔습니다. 정답은 {ANSWER_MEAN} 입니다.\n"
                   f"        {SAMPLE} 를 모두 더하면 {sum(SAMPLE)}, "
                   f"개수는 {len(SAMPLE)} 입니다.")


def check_stdev(fn):
    got, err = _run(fn, SAMPLE)
    if err:
        return False, f"실행 중 오류가 났습니다 - {err}"
    if got is None:
        return False, "아직 만들지 않았습니다."
    if _close(got, ANSWER_STDEV_SAMPLE, 1e-4):
        return True, f"표준편차 {got:.4f} - 정답입니다."
    if _close(got, ANSWER_STDEV_POP, 1e-4):
        return False, (f"{got:.4f} 가 나왔습니다. 아주 가깝습니다!\n"
                       f"        n({len(SAMPLE)}) 이 아니라 "
                       f"n-1({len(SAMPLE)-1}) 로 나누어야 합니다. (자유도)\n"
                       f"        정답은 {ANSWER_STDEV_SAMPLE:.4f} 입니다. "
                       f"엑셀의 =STDEV.S() 와 같은 값입니다.")
    if _close(got, 10.0, 1e-4):
        return False, (f"{got} 는 '분산'입니다. 마지막에 제곱근을 씌우세요. "
                       f"( ** 0.5 )")
    return False, (f"{got} 가 나왔습니다. 정답은 {ANSWER_STDEV_SAMPLE:.4f} 입니다.\n"
                   f"        순서: 평균({ANSWER_MEAN}) → 각 값에서 빼고 제곱해서 더하기(40)\n"
                   f"              → n-1({len(SAMPLE)-1})로 나누기(10) → 제곱근")


def check_cv(fn, mean_fn, stdev_fn):
    got, err = _run(fn, SAMPLE)
    if err:
        return False, f"실행 중 오류가 났습니다 - {err}"
    if got is None:
        return False, "아직 만들지 않았습니다."
    if _close(got, ANSWER_CV, 1e-4):
        return True, f"변동계수 {got:.2f}% - 정답입니다."
    if _close(got, ANSWER_CV / 100, 1e-6):
        return False, f"{got:.4f} 가 나왔습니다. 100을 곱해 퍼센트로 만드세요."
    if _close(got, ANSWER_MEAN / ANSWER_STDEV_SAMPLE * 100, 1e-4):
        return False, (f"{got:.2f} 가 나왔습니다. 나누는 순서가 반대입니다.\n"
                       f"        변동계수 = 표준편차 ÷ 평균 × 100 입니다.")
    return False, f"{got} 가 나왔습니다. 정답은 {ANSWER_CV:.2f}% 입니다."


def check_order_independent(fn, name):
    """순서를 바꿔도 같은 답이 나와야 합니다."""
    a, _ = _run(fn, SAMPLE)
    b, _ = _run(fn, SHUFFLED)
    if a is None or b is None:
        return True, ""          # 앞 검사에서 이미 걸렸습니다
    if _close(a, b, 1e-9):
        return True, ""
    return False, (f"{name} 이 자료 순서에 따라 달라집니다 ({a} vs {b}).\n"
                   f"        평균·표준편차는 순서와 상관없이 같아야 합니다.")


# ── 12주 전체 채점 ──────────────────────────────────────────────────
def check_week12(mean_fn, stdev_fn, cv_fn):
    """세 함수를 한 번에 채점합니다. 전부 맞으면 True."""
    print("-" * 66)
    print("  채점 - 손으로 검산할 수 있는 작은 자료로 확인합니다")
    print(f"  자료: {SAMPLE}   (합계 {sum(SAMPLE)}, 개수 {len(SAMPLE)})")
    print("-" * 66)

    results = [
        ("평균 my_mean()", check_mean(mean_fn)),
        ("표준편차 my_stdev()", check_stdev(stdev_fn)),
        ("변동계수 my_cv()", check_cv(cv_fn, mean_fn, stdev_fn)),
    ]
    for label, (ok, message) in results:
        mark = "[O]" if ok else "[X]"
        print(f"  {mark} {label}")
        print(f"        {message}")

    # 순서 무관 검사 (앞이 다 맞았을 때만)
    if all(ok for _, (ok, _) in results):
        for fn, name in ((mean_fn, "평균"), (stdev_fn, "표준편차")):
            ok, message = check_order_independent(fn, name)
            if not ok:
                print(f"  [X] 순서 검사")
                print(f"        {message}")
                results.append(("순서 검사", (False, message)))

    passed = all(ok for _, (ok, _) in results)
    print("-" * 66)
    if passed:
        print("  OK 전부 정답입니다! 이제 진짜 게임 데이터로 계산해 봅시다.")
    else:
        print("  -> 위 안내를 보고 고친 뒤 다시 실행하세요:  python w12_basic.py")
    print("-" * 66)
    return passed


# ── 직접 실행하면 정답 예시를 보여 줍니다 (선생님용) ────────────────
if __name__ == "__main__":
    print("=" * 66)
    print("  채점기 자체 점검 - 정답 함수를 넣으면 전부 통과해야 합니다")
    print("=" * 66)

    def ok_mean(v):
        return sum(v) / len(v)

    def ok_stdev(v):
        m = ok_mean(v)
        return (sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** 0.5

    def ok_cv(v):
        return ok_stdev(v) / ok_mean(v) * 100

    assert check_week12(ok_mean, ok_stdev, ok_cv), "정답 함수가 통과하지 못했습니다!"

    print("\n  흔한 실수도 제대로 잡아내는지 확인합니다")
    print("-" * 66)

    def wrong_stdev(v):                       # n 으로 나눈 경우
        m = ok_mean(v)
        return (sum((x - m) ** 2 for x in v) / len(v)) ** 0.5

    ok, msg = check_stdev(wrong_stdev)
    print(f"  n 으로 나눈 경우 -> {'X 못 잡음' if ok else 'O 잡아냄'}")
    print(f"     {msg}")

    def wrong_mean(v):                        # 합계만 반환
        return sum(v)

    ok, msg = check_mean(wrong_mean)
    print(f"\n  합계만 반환한 경우 -> {'X 못 잡음' if ok else 'O 잡아냄'}")
    print(f"     {msg}")
    print("=" * 66)
