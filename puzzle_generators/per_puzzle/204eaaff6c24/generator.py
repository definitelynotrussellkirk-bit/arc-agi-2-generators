"""Generator for puzzle d631b094.

Rule: find the first non-zero color, count its occurrences (n), output
a 1 × n grid all in that color.

Combinatorial axes: grid_h/w, fg_color, n_cells (= output width),
fg_layout, decoy_density (only matters if there are 0s — but rule only
counts the first non-zero color, others act as decoys).
Degenerates: all_zero (empty input → 1×0 — invalid), single_color_grid
(N = h*w), no_fg.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "204eaaff6c24"
VERSION = "1.1.0"
TASK_ID = "204eaaff6c24"
SUMMARY = "Sparse cells of one non-zero color; rule outputs a 1×N bar of that color (N = cell count)."

INVARIANTS = [
    "background is 0",
    "input has exactly one non-zero color",
    "≥1 non-zero cell so output is at least 1×1",
    "≤30 non-zero cells so the output bar fits within ARC limits",
]

FG_LAYOUTS = ("random", "cluster", "row", "column", "diagonal", "blob", "scattered")
DEGENERATE_TEXTURES = ("single_cell", "all_filled", "monochrome_no_bg")
HELPFUL_TEXTURES = FG_LAYOUTS

AXES = {
    "grid_h":     {"type": "int", "default": "rng 3..10", "valid": "1..30"},
    "grid_w":     {"type": "int", "default": "rng 3..10", "valid": "1..30"},
    "fg_color":   {"type": "color", "default": "rng (≠0)", "valid": "1..9"},
    "n_cells":    {"type": "int", "default": "rng 1..min(15,h*w//2)",
                   "valid": "1..30"},
    "fg_layout":  {"type": "str", "default": "rng helpful",
                   "valid": "|".join(FG_LAYOUTS)},
    "texture":    {"type": "str", "default": "alias for fg_layout",
                   "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 3, 5
    elif difficulty == "hard":
        h_lo, h_hi = 8, 10
    else:
        h_lo, h_hi = 3, 10
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    fg = int(overrides.get("fg_color", ctx.draw_color("fg_color", exclude={0})))
    max_n = max(1, min(15, h * w // 2))
    n = int(overrides.get("n_cells", ctx.draw_int("n_cells", 1, max_n)))
    n = max(1, min(h * w, n, 30))
    layout = (overrides.get("texture") or overrides.get("fg_layout")
              or ctx.draw_choice("fg_layout", list(FG_LAYOUTS)))
    g = full_grid(h, w, 0)
    cells = _layout_cells(layout, h, w, n, rng)
    for (r, c) in cells:
        g[r][c] = fg
    return g


def _layout_cells(layout, h, w, n, rng):
    if layout == "cluster":
        cr = rng.randint(0, h - 1); cc = rng.randint(0, w - 1)
        cells = [(r, c) for r in range(h) for c in range(w)]
        cells.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return cells[:n]
    if layout == "row":
        r = rng.randint(0, h - 1)
        cells = [(r, c) for c in range(w)]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "column":
        c = rng.randint(0, w - 1)
        cells = [(r, c) for r in range(h)]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "diagonal":
        return [(k, k) for k in range(min(h, w))][:n]
    if layout == "blob":
        cr = rng.randint(0, h - 1); cc = rng.randint(0, w - 1)
        cells = [(r, c) for r in range(h) for c in range(w)]
        cells.sort(key=lambda rc: max(abs(rc[0] - cr), abs(rc[1] - cc)))
        return cells[:n]
    if layout == "scattered":
        cells = [(r, c) for r in range(0, h, 2) for c in range(0, w, 2)]
        rng.shuffle(cells)
        if len(cells) < n:
            extras = [(r, c) for r in range(h) for c in range(w) if (r + c) % 2 != 0]
            rng.shuffle(extras)
            cells = cells + extras
        return cells[:n]
    cells = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(cells)
    return cells[:n]


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    fg = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "single_cell":
        g[rng.randint(0, h - 1)][rng.randint(0, w - 1)] = fg
        return g
    if name == "all_filled":
        n = min(30, h * w)
        cells = [(r, c) for r in range(h) for c in range(w)]
        rng.shuffle(cells)
        for r, c in cells[:n]:
            g[r][c] = fg
        return g
    if name == "monochrome_no_bg":
        # No bg cells at all — every cell is fg. Output bar = h*w cells.
        n = min(30, h * w)
        cells = [(r, c) for r in range(h) for c in range(w)]
        rng.shuffle(cells)
        for r, c in cells[:n]:
            g[r][c] = fg
        return g
    return g
