"""Generate a /samples directory with rendered (input, output) pairs
for a hand-picked diverse subset of generators. Used for the public
README + SAMPLES.md.

Run:
    python3 scripts/build_samples.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from PIL import Image, ImageDraw

from puzzle_generators import runner

# ARC palette (standard hex codes used across ARC tooling).
ARC_COLORS = [
    "#000000",  # 0 black
    "#1E93FF",  # 1 blue
    "#F93C31",  # 2 red
    "#4FCC30",  # 3 green
    "#FFDC00",  # 4 yellow
    "#999999",  # 5 gray
    "#E53AA3",  # 6 magenta
    "#FF851B",  # 7 orange
    "#87D8F1",  # 8 cyan
    "#921231",  # 9 maroon
]

# Hand-picked subset — variety of bank, rule type, grid size.
SAMPLES = [
    ("ecc04b33119c",
     "Tile 3×3 alternating original / LR-mirror by row block"),
    ("c4ab07496ad4",
     "Small shape determines big shape's color: plus→2, bottom-full→3, top-full→7"),
    ("ad5998ad11d6",
     "Fill all enclosed regions with yellow(4)"),
    ("a9f315ca9cc7",
     "Self-tile 3×3: each cell of the input determines whether that "
     "tile-position copies the input or stays blank"),
    ("c739fcbc6cbd",
     "Repeat a vertical color marker across all columns at the same "
     "spacing"),
]


def render_grid(grid: list[list[int]], cell: int = 24,
                padding: int = 2) -> Image.Image:
    h = len(grid)
    w = len(grid[0]) if h else 0
    img_w = w * cell + 2 * padding
    img_h = h * cell + 2 * padding
    img = Image.new("RGB", (img_w, img_h), "#1a1a1a")
    draw = ImageDraw.Draw(img)
    for r in range(h):
        for c in range(w):
            v = grid[r][c]
            color = ARC_COLORS[v] if 0 <= v < 10 else "#ff00ff"
            x0 = padding + c * cell
            y0 = padding + r * cell
            draw.rectangle([x0, y0, x0 + cell - 1, y0 + cell - 1],
                           fill=color, outline="#1a1a1a")
    return img


def render_pair(input_grid, output_grid, cell: int = 24,
                gap: int = 30, label_h: int = 24) -> Image.Image:
    in_img = render_grid(input_grid, cell)
    out_img = render_grid(output_grid, cell)
    total_w = in_img.width + gap + out_img.width
    total_h = max(in_img.height, out_img.height) + label_h
    img = Image.new("RGB", (total_w, total_h), "#0d0d0d")
    img.paste(in_img, (0, label_h))
    img.paste(out_img, (in_img.width + gap, label_h))
    draw = ImageDraw.Draw(img)
    draw.text((4, 4), "input", fill="#bbbbbb")
    draw.text((in_img.width + gap + 4, 4), "output", fill="#bbbbbb")
    # Arrow between
    arrow_y = label_h + max(in_img.height, out_img.height) // 2
    arrow_x = in_img.width + gap // 2
    draw.text((arrow_x - 3, arrow_y - 8), "→", fill="#888888")
    return img


def main():
    out_dir = ROOT / "samples"
    out_dir.mkdir(exist_ok=True)
    md_lines = ["# Samples", ""]
    md_lines.append("Hand-picked input → output pairs from the corpus, "
                    "rendered with the standard ARC color palette.")
    md_lines.append("")
    md_lines.append("Each pair is one `(input, output)` instance the "
                    "generator produced; the rule was applied via the "
                    "Racket runner. Re-running `python3 "
                    "scripts/build_samples.py` re-rolls them with the "
                    "same seeds.")
    md_lines.append("")

    for tid, summary in SAMPLES:
        try:
            result = runner.run_one(tid, seed=0, sample_index=0)
        except Exception as e:
            print(f"[skip] {tid}: {type(e).__name__}: {e}")
            continue

        train = result.get("train", [])
        if not train:
            print(f"[skip] {tid}: no train pairs")
            continue

        # Render the first 2 train pairs; this keeps SAMPLES.md compact.
        n_to_render = min(2, len(train))
        sample_dir = out_dir / tid
        sample_dir.mkdir(exist_ok=True)
        md_lines.append(f"## `{tid}`")
        md_lines.append("")
        md_lines.append(f"**Rule:** {summary}")
        md_lines.append("")
        for i in range(n_to_render):
            pair = train[i]
            img = render_pair(pair["input"], pair["output"])
            png_path = sample_dir / f"train_{i}.png"
            img.save(png_path)
            md_lines.append(
                f"![{tid} train {i}](samples/{tid}/train_{i}.png)")
            md_lines.append("")
        if result.get("test"):
            test = result["test"][0]
            img = render_pair(test["input"], test["output"])
            png_path = sample_dir / "test_0.png"
            img.save(png_path)
            md_lines.append(f"*test instance:*")
            md_lines.append("")
            md_lines.append(f"![{tid} test 0](samples/{tid}/test_0.png)")
            md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        print(f"[ok]   {tid}: {n_to_render} train + "
              f"{len(result.get('test', []))} test rendered")

    md_lines.append("")
    md_lines.append("To regenerate: `python3 scripts/build_samples.py`")
    (ROOT / "SAMPLES.md").write_text("\n".join(md_lines))
    print(f"\nwrote {ROOT / 'SAMPLES.md'} and PNGs under {out_dir}/")


if __name__ == "__main__":
    main()
