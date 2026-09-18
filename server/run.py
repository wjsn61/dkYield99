# ════════════════════════════════════════════════════════════════════
#  dkYield99 launcher (run.py) - Chemical Process Tycoon
#  Run:  from the 'server' folder  ->  python run.py
#  Then open http://127.0.0.1:5000 in your browser.
# ════════════════════════════════════════════════════════════════════
import os
import sys

# Make the 'app' package importable even under bundled (embeddable) Python,
# whose ._pth pins sys.path and does not add the script folder automatically.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("  Starting dkYield99 - Chemical Process Tycoon ...")
    print("  Open http://127.0.0.1:5000 in your browser.")
    print("  (Press Ctrl + C in this window to stop)")
    print("=" * 60)
    uvicorn.run("app.main:app", host="127.0.0.1", port=5000, reload=False)
