# ════════════════════════════════════════════════════════════════════
#  12주 실습 (선택) - 파이썬으로 그림 그리기   (★ 여기를 채우세요 ★)
#
#  지난주에 엑셀로 차트를 만들었습니다.
#  이번에는 같은 그림을 코드로 그려 봅니다.
#
#  ▶ 왜 코드로 그리나요?
#     엑셀은 파일 하나에 3분입니다. 코드는 파일 20개에 3초입니다.
#     한 번 짜 두면 새 데이터가 올 때마다 다시 그릴 필요가 없습니다.
#
#  ▶ 실행 전에 한 번만:  install_stats.bat 을 더블클릭
#     (matplotlib 을 동봉 파이썬에 설치합니다. 게임에는 필요 없습니다)
#
#  ▶ 실행:  lab 폴더에서   python w12_chart.py
#     그림은 lab/figures/ 폴더에 저장됩니다.
# ════════════════════════════════════════════════════════════════════
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(HERE, "figures")


# ── 1. matplotlib 준비 (한글 깨짐·화면 없음 문제를 미리 막습니다) ────
def setup_matplotlib():
    """
    동봉 파이썬에는 창을 띄우는 기능(tkinter)이 없습니다.
    그래서 화면에 띄우지 않고 파일로만 저장하는 방식(Agg)을 씁니다.
    ★ 이 설정은 pyplot 을 불러오기 '전에' 해야 합니다.
    """
    # 폰트 캐시를 lab 폴더 안에 두어 학교 컴퓨터에서도 문제없게 합니다
    os.environ.setdefault("MPLCONFIGDIR", os.path.join(HERE, ".mplcache"))

    try:
        import matplotlib
    except ImportError:
        print("  matplotlib 이 없습니다.")
        print("  프로젝트 폴더의 install_stats.bat 을 먼저 실행하세요.")
        sys.exit(1)

    matplotlib.use("Agg")                    # ★ 창을 띄우지 않고 파일로만
    import matplotlib.pyplot as plt

    # 한글이 네모(두부)로 나오지 않게 폰트를 찾아 줍니다
    for name in ("Malgun Gothic", "NanumGothic", "AppleGothic", "Gulim"):
        try:
            matplotlib.rcParams["font.family"] = name
            plt.figure(); plt.close()        # 실제로 쓸 수 있는지 시험
            break
        except Exception:
            continue
    matplotlib.rcParams["axes.unicode_minus"] = False   # 마이너스 기호도 깨짐 방지
    return plt


def save(plt, name):
    """그림을 figures 폴더에 저장하고 경로를 알려 줍니다."""
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, name)
    plt.savefig(path, dpi=130, bbox_inches="tight")
    plt.close()
    print(f"     저장: {path}")


# ════════════════════════════════════════════════════════════════════
#  ★★★ 여기서부터가 여러분이 채울 부분입니다 ★★★
# ════════════════════════════════════════════════════════════════════

# ── 2. 꺾은선 그래프 - 시간에 따라 어떻게 변했나 ────────────────────
def draw_line(plt, turns, values, label, filename):
    """
    힌트:
        plt.figure(figsize=(8, 3.5))
        plt.plot(turns, values, marker="o")
        plt.title(f"{label} 추이")
        plt.xlabel("턴")
        plt.ylabel(label)
        plt.grid(alpha=0.3)
        save(plt, filename)
    """
    # ✏️ 여기를 채우세요
    pass


# ── 3. 히스토그램 - 값이 어디에 몰려 있나 ───────────────────────────
def draw_histogram(plt, values, label, filename):
    """
    힌트:
        plt.figure(figsize=(6, 3.5))
        plt.hist(values, bins=8, edgecolor="white")
        plt.title(f"{label} 분포")
        plt.xlabel(label)
        plt.ylabel("몇 번")
        save(plt, filename)
    """
    # ✏️ 여기를 채우세요
    pass


# ════════════════════════════════════════════════════════════════════
#  아래는 손대지 않아도 됩니다.
# ════════════════════════════════════════════════════════════════════
def main():
    from w12_basic import load_csv, column, my_mean, my_stdev

    print("=" * 66)
    print("  12주 실습 (선택) - 파이썬으로 그림 그리기")
    print("=" * 66)

    plt = setup_matplotlib()
    rows = load_csv()
    turns = column(rows, "턴")

    made = 0
    for name, fname in (("수율", "수율_추이.png"), ("순도_분석", "순도_추이.png")):
        values = column(rows, name)
        if len(values) < 2:
            continue
        print(f"\n  [{name}]")
        before = len(os.listdir(FIG_DIR)) if os.path.isdir(FIG_DIR) else 0
        draw_line(plt, turns[:len(values)], values, name, fname)
        draw_histogram(plt, values, name, fname.replace("_추이", "_분포"))
        after = len(os.listdir(FIG_DIR)) if os.path.isdir(FIG_DIR) else 0
        if after == before:
            print("     (아직 함수를 채우지 않았습니다 - ✏️ 부분을 완성하세요)")
        else:
            made += after - before

    if made == 0:
        print("\n  -> draw_line() 과 draw_histogram() 을 채운 뒤 다시 실행하세요.")
        return 1

    # ── pandas 맛보기 (두 줄이면 끝납니다) ──────────────────────────
    print("\n" + "-" * 66)
    print("  pandas 맛보기 - 같은 일을 두 줄로")
    print("-" * 66)
    try:
        import pandas as pd
        df = pd.read_csv(_latest_csv(), encoding="utf-8-sig")
        print(df[["수율", "순도_분석", "월이익"]].describe().round(3).to_string())
        print("\n  이게 전부입니다. 여러분이 만든 my_mean() · my_stdev() 가")
        print("  describe() 의 mean · std 와 같은 값인지 확인해 보세요.")
        print("  (std 는 pandas 도 n-1 로 나눕니다)")
    except ImportError:
        print("  pandas 가 없습니다. install_stats.bat 을 실행하면 함께 설치됩니다.")
        print("  없어도 이 수업에는 지장이 없습니다 - 맛보기일 뿐입니다.")

    print("\n" + "-" * 66)
    print("  🤖 AI 에게 \"이 CSV로 히스토그램 그리는 코드 짜 줘\" 라고 해 보세요.")
    print("     그리고 여러분이 짠 코드와 무엇이 다른지 비교해 보세요.")
    print("     읽을 수 있어야 고칠 수 있고, 고칠 수 있어야 쓸 수 있습니다.")
    print("=" * 66)
    return 0


def _latest_csv():
    data_dir = os.path.join(HERE, "data")
    files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
    files.sort(key=lambda f: os.path.getmtime(os.path.join(data_dir, f)))
    return os.path.join(data_dir, files[-1])


if __name__ == "__main__":
    sys.exit(main())
