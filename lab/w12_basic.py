# ════════════════════════════════════════════════════════════════════
#  12주 실습 - 파이썬으로 같은 값 만들기   (★ 여기를 채우세요 ★)
#
#  지난주에 엑셀로 평균과 표준편차를 구했습니다.
#  이번 주에는 같은 값을 파이썬으로 직접 만들어 보고,
#  두 값이 정말 같은지 맞춰 봅니다.
#
#  ▶ 왜 직접 만드나요?
#     엑셀의 =AVERAGE() 도, AI가 짜 준 코드도 '어떻게' 계산하는지는
#     보여주지 않습니다. 한 번 직접 만들어 본 사람만
#     나중에 그 답이 맞는지 알아볼 수 있습니다.
#
#  ▶ 실행:  lab 폴더에서   python w12_basic.py
#     (외부 라이브러리가 하나도 필요 없습니다)
# ════════════════════════════════════════════════════════════════════
import csv
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")   # 윈도우 콘솔 한글 깨짐 방지
except Exception:
    pass


# ── 1. 데이터 읽기 ───────────────────────────────────────────────────
def load_csv(filename=None):
    """
    data 폴더에서 CSV 를 읽어 옵니다.

    파일 이름을 안 주면 가장 최근에 내려받은 파일을 알아서 고릅니다.
    (게임에서 「📊 통계 지표 보기 → 엑셀용 CSV」를 누르면 여기 저장됩니다)
    """
    here = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(here, "data")

    if filename is None:
        candidates = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
        if not candidates:
            print("  data 폴더에 CSV 가 없습니다.")
            print("  게임에서 '📊 통계 지표 보기 → 📥 엑셀용 CSV' 를 먼저 누르세요.")
            sys.exit(1)
        # 가장 최근에 저장된 파일
        candidates.sort(key=lambda f: os.path.getmtime(os.path.join(data_dir, f)))
        filename = candidates[-1]

    path = os.path.join(data_dir, filename)
    print(f"  파일: {filename}")

    rows = []
    # utf-8-sig 로 열어야 엑셀이 넣은 BOM 이 컬럼 이름에 붙지 않습니다.
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def column(rows, name):
    """
    한 컬럼만 숫자로 뽑아 옵니다. (빈칸은 건너뜁니다)

    파일에 따라 컬럼 이름이 조금 다릅니다.
      게임에서 내려받은 CSV        →  '수율'      (턴마다 한 줄)
      run_batch.py 판별 요약 CSV   →  '최종_수율'  (판마다 한 줄)
    그래서 몇 가지 이름을 차례로 찾아 봅니다.
    """
    if not rows:
        return []
    candidates = [name, f"최종_{name}", f"평균_{name}"]
    found = next((c for c in candidates if c in rows[0]), None)
    if found is None:
        return []

    values = []
    for row in rows:
        text = row.get(found, "")
        if text == "" or text is None:
            continue
        try:
            values.append(float(text))
        except ValueError:
            continue
    return values


def numeric_columns(rows, limit=12):
    """이 파일에 숫자로 읽을 수 있는 컬럼이 무엇인지 알려 줍니다."""
    if not rows:
        return []
    out = []
    for key, text in rows[0].items():
        try:
            float(text)
            out.append(key)
        except (TypeError, ValueError):
            continue
    return out[:limit]


# ════════════════════════════════════════════════════════════════════
#  ★★★ 여기서부터가 여러분이 채울 부분입니다 ★★★
#
#  아래 세 함수의 pass 를 지우고 직접 만들어 보세요.
#  다 만들면 이 파일을 실행해서 채점을 받습니다.
# ════════════════════════════════════════════════════════════════════

# ── 2. 평균 ─────────────────────────────────────────────────────────
def my_mean(values):
    """
    평균 = 모두 더한 값 ÷ 개수

    힌트:
        total = 0
        for v in values:
            total = total + v
        return total / len(values)

    엑셀에서는  =AVERAGE(범위)
    """
    # ✏️ 여기를 채우세요
    pass


# ── 3. 표준편차 ─────────────────────────────────────────────────────
def my_stdev(values):
    """
    표준편차 = '평균에서 얼마나 떨어져 있는지'를 하나의 숫자로

    순서:
        1) 평균을 구한다
        2) 각 값에서 평균을 빼고, 그것을 제곱해서 모두 더한다
        3) 개수보다 1 작은 수로 나눈다        ← ★ n 이 아니라 n-1 !
        4) 제곱근을 씌운다                    ← ** 0.5 를 쓰면 됩니다

    ★ 왜 n 이 아니라 n-1 로 나눌까요?
      우리가 가진 자료는 세상 전체가 아니라 '표본'이기 때문입니다.
      표본으로 계산하면 흔들림을 실제보다 작게 보는 경향이 있어서,
      조금 크게 잡아 주는 것입니다. 이것을 자유도라고 부릅니다.

    엑셀에서는  =STDEV.S(범위)     ← S 는 표본(Sample)의 S 입니다
                =STDEV.P(범위) 는 n 으로 나눕니다. 이 수업에서는 안 씁니다.
    """
    # ✏️ 여기를 채우세요
    pass


# ── 4. 변동계수 ─────────────────────────────────────────────────────
def my_cv(values):
    """
    변동계수(%) = 표준편차 ÷ 평균 × 100

    ★ 왜 필요한가요?
      '%' 단위인 수율과 '억' 단위인 이익은 표준편차를 직접 비교할 수 없습니다.
      변동계수는 단위를 없애 주기 때문에 "어느 쪽이 더 불안정한가"를 비교할 수 있습니다.
    """
    # ✏️ 여기를 채우세요
    pass


# ════════════════════════════════════════════════════════════════════
#  아래는 손대지 않아도 됩니다 - 실행하면 채점해 줍니다.
# ════════════════════════════════════════════════════════════════════
def main():
    print("=" * 66)
    print("  12주 실습 - 파이썬으로 같은 값 만들기")
    print("=" * 66)

    rows = load_csv()
    print(f"  기록 {len(rows)}줄을 읽었습니다.\n")

    # 채점부터 받습니다
    from check import check_week12
    passed = check_week12(my_mean, my_stdev, my_cv)
    if not passed:
        return 1

    # 통과했으면 진짜 게임 데이터로 계산해 봅니다
    print("\n" + "-" * 66)
    print("  내가 만든 함수로 게임 데이터를 계산해 봅니다")
    print("-" * 66)

    shown = 0
    for name in ("수율", "순도_분석", "월이익", "안전지수", "환경지수", "누적이익"):
        values = column(rows, name)
        if len(values) < 2:
            continue
        shown += 1
        print(f"\n  [{name}]  {len(values)}개")
        print(f"     평균      {my_mean(values):.3f}")
        print(f"     표준편차   {my_stdev(values):.3f}")
        print(f"     변동계수   {my_cv(values):.2f}%")

    if shown == 0:
        print("\n  이 파일에서 아는 지표를 찾지 못했습니다.")
        print(f"  숫자로 읽을 수 있는 컬럼: {', '.join(numeric_columns(rows))}")
        print("  위 이름 중 하나를 골라 column(rows, \"이름\") 으로 직접 뽑아 보세요.")
        return 1

    print("\n" + "-" * 66)
    print("  ✋ 이제 엑셀을 열어서 =AVERAGE() 와 =STDEV.S() 로")
    print("     같은 값이 나오는지 확인하세요. 소수점까지 같아야 합니다.")
    print()
    print("  🤖 그리고 AI 에게도 물어보세요.")
    print("     \"이 숫자들의 표준편차를 구해 줘\" 라고 하고,")
    print("     내가 만든 함수의 답과 같은지 맞춰 보세요.")
    print("     AI 는 모르는 것을 모른다고 말하지 않습니다.")
    print("     스스로 계산해 본 사람만 그 답이 맞는지 압니다.")
    print("=" * 66)
    return 0


if __name__ == "__main__":
    sys.exit(main())
