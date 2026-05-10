"""Generator for puzzle c7d4e6ad.

Rule: `(rule! (lambda (g) (cellmap g (r c v) (if (= v 5) (at g r 0) v))))`.
Column 0 of each row contains a marker color; gray(5) cells anywhere
in that row get recolored to the marker (the row's col-0 value).

Combinatorial axes:
  * grid_h / grid_w        — outer canvas size
  * n_grays                — how many gray(5) cells to plant
  * gray_layout            — random / cluster / one_per_row / column /
                             diagonal / scattered
  * marker_diversity       — same / mixed / all_distinct (controls how
                             the col-0 markers vary across rows)
  * decor_palette_size     — extra cells of other colors that don't
                             change (must not be 5 or 0)
  * caller-opt-in degenerates: no_grays (rule no-op), all_grays_one_row
                               (visually trivial), col0_all_same
                               (output ambiguous with "fill with X")
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7190532509b9"
VERSION = "1.1.0"  # bumped: deeper combinatorial axes added
TASK_ID = "7190532509b9"
SUMMARY = "Each row's col-0 is a marker color; gray cells in the row get that color."

INVARIANTS = [
    "every row has a non-bg, non-gray color at column 0",
    "≥1 gray(5) cell in columns 1..w-1",
    "different rows may have different marker colors",
]

GRAY_LAYOUTS = (
    "random", "cluster", "one_per_row", "column", "diagonal", "scattered",
)
MARKER_DIVERSITIES = ("same", "mixed", "all_distinct")
DEGENERATE_TEXTURES = ("no_grays", "all_grays_one_row", "col0_all_same")
HELPFUL_TEXTURES = GRAY_LAYOUTS

AXES = {
    "grid_h":              {"type": "int", "default": "rng 5..14",  "valid": "4..18"},
    "grid_w":              {"type": "int", "default": "rng 5..14",  "valid": "4..18"},
    "n_grays":              {"type": "int", "default": "rng 3..12", "valid": "1..30"},
    "gray_layout":         {"type": "str", "default": "rng helpful",
                            "valid": "|".join(GRAY_LAYOUTS)},
    "marker_diversity":    {"type": "str", "default": "rng same|mixed|all_distinct",
                            "valid": "|".join(MARKER_DIVERSITIES)},
    "decor_palette_size":  {"type": "int", "default": "rng 0..3",   "valid": "0..6"},
    "texture":             {"type": "str", "default": "alias for gray_layout",
                            "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)

    if difficulty == "easy":
        h_lo, h_hi, n_lo, n_hi = 5, 7, 2, 5
    elif difficulty == "hard":
        h_lo, h_hi, n_lo, n_hi = 12, 14, 8, 12
    else:
        h_lo, h_hi, n_lo, n_hi = 5, 14, 3, 10

    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("placement")

    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)

    n_grays = int(overrides.get("n_grays",
                                ctx.draw_int("n_grays", n_lo, n_hi)))
    layout = (overrides.get("texture")
              or overrides.get("gray_layout")
              or ctx.draw_choice("gray_layout", list(GRAY_LAYOUTS)))
    diversity = overrides.get(
        "marker_diversity",
        ctx.draw_choice("marker_diversity", list(MARKER_DIVERSITIES)))
    n_decor = int(overrides.get("decor_palette_size",
                                ctx.draw_int("decor_palette_size", 0, 3)))

    g = full_grid(h, w, 0)
    palette = [c for c in range(1, 10) if c != 5]
    rng.shuffle(palette)
    if diversity == "same":
        marker = palette[0]
        for r in range(h):
            g[r][0] = marker
    elif diversity == "all_distinct":
        markers = palette[:h] if len(palette) >= h else \
                  palette + [palette[0]] * (h - len(palette))
        for r in range(h):
            g[r][0] = markers[r]
    else:  # mixed
        for r in range(h):
            g[r][0] = rng.choice(palette)

    gray_positions = _gray_layout(layout, h, w, n_grays, rng)
    for r, c in gray_positions:
        if c >= 1 and 0 <= r < h:  # never overwrite col 0
            g[r][c] = 5

    decor_palette = [c for c in palette if c != g[0][0]][:n_decor]
    if decor_palette:
        for r in range(h):
            for c in range(1, w):
                if g[r][c] == 0 and rng.random() < 0.15:
                    g[r][c] = rng.choice(decor_palette)

    if not any(g[r][c] == 5 for r in range(h) for c in range(1, w)):
        g[0][1] = 5
    return g


def _gray_layout(layout, h, w, n, rng):
    if layout == "cluster":
        cr = rng.randint(0, h - 1); cc = rng.randint(1, w - 1)
        cells = [(r, c) for r in range(h) for c in range(1, w)]
        cells.sort(key=lambda rc: abs(rc[0] - cr) + abs(rc[1] - cc))
        return cells[:n]
    if layout == "one_per_row":
        out = []
        for r in range(min(h, n)):
            c = rng.randint(1, w - 1)
            out.append((r, c))
        return out
    if layout == "column":
        c = rng.randint(1, w - 1)
        cells = [(r, c) for r in range(h)]
        rng.shuffle(cells)
        return cells[:n]
    if layout == "diagonal":
        return [(k, k + 1) for k in range(min(h, w - 1))][:n]
    if layout == "scattered":
        cells = [(r, c) for r in range(0, h, 2) for c in range(1, w, 2)]
        rng.shuffle(cells)
        return cells[:n]
    cells = [(r, c) for r in range(h) for c in range(1, w)]
    rng.shuffle(cells)
    return cells[:n]


def _draw_from_degenerate(name, h, w, rng):
    """Edge-case where the col-0-marker signal collapses.

    no_grays           — input has no 5s; rule is no-op (output == input).
    all_grays_one_row  — only one row has 5s; output looks like that
                          single row repeating its marker.
    col0_all_same      — every row's col-0 is the same color; output is
                          ambiguous with "fill 5 → X" (no per-row signal).
    """
    g = full_grid(h, w, 0)
    palette = [c for c in range(1, 10) if c != 5]
    rng.shuffle(palette)
    if name == "no_grays":
        for r in range(h):
            g[r][0] = rng.choice(palette)
        for r in range(h):
            for c in range(1, w):
                if rng.random() < 0.3:
                    g[r][c] = rng.choice(palette[:3])
        return g
    if name == "all_grays_one_row":
        for r in range(h):
            g[r][0] = rng.choice(palette)
        target_row = rng.randint(0, h - 1)
        for c in range(1, w):
            g[target_row][c] = 5
        return g
    if name == "col0_all_same":
        marker = palette[0]
        for r in range(h):
            g[r][0] = marker
        for r in range(h):
            for c in range(1, w):
                if rng.random() < 0.3:
                    g[r][c] = 5
        return g
    return g
