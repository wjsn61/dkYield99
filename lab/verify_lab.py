# ════════════════════════════════════════════════════════════════════
#  실습실 점검 (verify_lab.py)
#  ※ 선생님/조교용. 배포 전에 lab 폴더가 제대로 도는지 확인합니다.
#
#  ▶ 실행:  lab 폴더에서   python verify_lab.py
#  ▶ 순수 파이썬만 확인:   python verify_lab.py --pure-only
#       (matplotlib·pandas 를 설치하지 않은 컴퓨터에서도 도는지 검사)
# ════════════════════════════════════════════════════════════════════
import os
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
PURE_ONLY = "--pure-only" in sys.argv


def run(name, args, expect_zero=True, needs_libs=False):
    """한 파일을 실제로 돌려 보고 결과를 봅니다."""
    if needs_libs and PURE_ONLY:
        return None, "건너뜀 (--pure-only)"

    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    try:
        result = subprocess.run(
            [sys.executable, name] + args,
            cwd=HERE, capture_output=True, env=env, timeout=180)
    except subprocess.TimeoutExpired:
        return False, "180초 안에 끝나지 않았습니다"

    out = result.stdout.decode("utf-8", "replace")
    err = result.stderr.decode("utf-8", "replace")

    # 한글이 깨졌는지
    if "�" in out:
        return False, "출력에 깨진 글자가 있습니다 (인코딩 문제)"
    # matplotlib 한글 폰트 경고 (그림이 두부로 나오는 신호)
    if "findfont" in err:
        return False, "한글 폰트를 못 찾았습니다 - 그림의 글자가 네모로 나옵니다"

    ok = (result.returncode == 0) if expect_zero else True
    detail = f"종료코드 {result.returncode}"
    if not ok and err:
        detail += " | " + err.strip().split("\n")[-1][:120]
    return ok, detail


CHECKS = [
    # (표시 이름, 파일, 인자, 종료코드 0 을 기대하는가, 라이브러리 필요)
    ("채점기 자체 점검",       "check.py",       [], True,  False),
    ("전략 묶음 검사",         "strategies.py",  [], True,  False),
    ("배치 실행 (대조군 3판)", "run_batch.py",   ["--n", "3", "--turns", "12"], True, False),
    ("12주 실습 (미완성 상태)", "w12_basic.py",   [], False, False),   # 안 채웠으면 1이 정상
    ("12주 그림 (미완성 상태)", "w12_chart.py",   [], False, True),
]


def main():
    print("=" * 70)
    print("  실습실 점검" + ("   [순수 파이썬만]" if PURE_ONLY else ""))
    print(f"  파이썬: {sys.version.split()[0]}   {sys.executable}")
    print("=" * 70)

    # data 폴더에 CSV 가 있는지 (실습의 전제)
    data_dir = os.path.join(HERE, "data")
    csvs = [f for f in os.listdir(data_dir) if f.endswith(".csv")] \
        if os.path.isdir(data_dir) else []
    print(f"\n  data/ CSV 파일 {len(csvs)}개")
    if not csvs:
        print("     ⚠️ CSV 가 없습니다. run_batch.py 가 하나 만들어 줄 것입니다.")

    print()
    failures = []
    for label, name, args, expect_zero, needs in CHECKS:
        ok, detail = run(name, args, expect_zero, needs)
        if ok is None:
            print(f"  [ - ] {label:<26} {detail}")
            continue
        mark = "[O]" if ok else "[X]"
        print(f"  {mark} {label:<26} {detail}")
        if not ok:
            failures.append(label)

    # 라이브러리 상태
    print()
    for lib in ("matplotlib", "pandas"):
        try:
            __import__(lib)
            print(f"  [O] {lib} 설치됨")
        except ImportError:
            note = "정상 (순수 파이썬 검사)" if PURE_ONLY else "install_stats.bat 필요"
            print(f"  [ - ] {lib} 없음 - {note}")

    print("\n" + "-" * 70)
    if failures:
        print(f"  실패 {len(failures)}개: {', '.join(failures)}")
    else:
        print("  OK 실습실이 정상입니다.")
    print("=" * 70)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
