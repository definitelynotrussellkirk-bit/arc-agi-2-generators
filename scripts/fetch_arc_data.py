"""Fetch the ARC-AGI-2 raw competition data from Kaggle.

Required only if you want to rebuild data/canonical/puzzles.jsonl
from scratch via scripts/build_canonical_puzzles.py. The release
already ships a built canonical, so most users don't need this.

Requires the Kaggle CLI authenticated against your account
(`pip install kaggle && kaggle config view`).
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "raw"
KAGGLE_COMP = "arc-prize-2026-arc-agi-2"


def main():
    if shutil.which("kaggle") is None:
        print("ERROR: `kaggle` CLI not on PATH.")
        print("  pip install kaggle")
        print("  Then put your kaggle.json in ~/.kaggle/")
        sys.exit(1)

    DATA.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {KAGGLE_COMP} into {DATA}")
    r = subprocess.run(
        ["kaggle", "competitions", "download",
         "-c", KAGGLE_COMP, "-p", str(DATA)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print("ERROR: kaggle download failed.")
        print(r.stderr)
        sys.exit(r.returncode)
    # Unzip what was downloaded.
    for z in DATA.glob("*.zip"):
        print(f"  unzipping {z.name}")
        subprocess.run(["unzip", "-o", str(z), "-d", str(DATA)],
                       check=True, capture_output=True)
        z.unlink()
    print()
    print("Done. data/raw/ contents:")
    for f in sorted(DATA.iterdir()):
        if f.is_file():
            print(f"  {f.name}  ({f.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
