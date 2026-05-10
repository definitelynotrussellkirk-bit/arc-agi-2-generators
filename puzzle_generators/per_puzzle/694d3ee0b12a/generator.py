"""Generator for 4b:hard_27 — frame local intersections with fill key.

Rule: a hollow 7-frame contains row markers (color 2 in col c1+1),
col markers (color 3 in row r1+1), plus interior 'fill key' cells of a
single non-{0,2,3} color (the most frequent). At each (row-mark,
col-mark) intersection inside the frame, place the fill color.

Combinatorial axes (8): frame_h, frame_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_row_markers, no_col_markers, no_fill_key.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "694d3ee0b12a"
VERSION = "1.1.0"
TASK_ID = "694d3ee0b12a"
SUMMARY = "7-frame with row/col markers + 1-3 fill-key cells inside (single non-{0,2,3} color)."

INVARIANTS = [
    "background is 0",
    "outer 7-rectangular frame, hollow",
    "2-3 row markers (color 2) in col c1+1, distinct rows",
    "2-3 col markers (color 3) in row r1+1, distinct cols",
    "1-3 cells of a single fill-key color inside the frame, not on the marker rows/cols",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_row_markers", "no_col_markers", "no_fill_key")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "frame_h":        {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "frame_w":        {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "frame_with_axis_markers",
                       "valid": "frame_with_axis_markers"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        fh = ctx.draw_int("frame_h", 8, 8)
        fw = ctx.draw_int("frame_w", 9, 9)
    elif difficulty == "hard":
        fh = ctx.draw_int("frame_h", 10, 13)
        fw = ctx.draw_int("frame_w", 11, 13)
    else:
        fh = ctx.draw_int("frame_h", 8, 10)
        fw = ctx.draw_int("frame_w", 9, 11)
    rng = ctx.draw_rng("layout")
    h = fh + 2; w = fw + 3
    g = full_grid(h, w, 0)
    r1, c1 = 1, 2
    r2, c2 = r1 + fh - 1, c1 + fw - 1
    for c in range(c1, c2 + 1): g[r1][c] = 7; g[r2][c] = 7
    for r in range(r1, r2 + 1): g[r][c1] = 7; g[r][c2] = 7
    n_rows = rng.randint(2, 3)
    row_marks = rng.sample(range(r1 + 2, r2), n_rows)
    for r in row_marks: g[r][c1 + 1] = 2
    n_cols = rng.randint(2, 3)
    col_marks = rng.sample(range(c1 + 2, c2), n_cols)
    for c in col_marks: g[r1 + 1][c] = 3
    fill_color = rng.choice([4, 5, 6, 8, 9])
    n_fills = rng.randint(2, 4)
    placed = 0; attempts = 0
    while placed < n_fills and attempts < 60:
        attempts += 1
        r = rng.randint(r1 + 2, r2 - 1); c = rng.randint(c1 + 2, c2 - 1)
        if g[r][c] != 0: continue
        if r in row_marks or c in col_marks: continue
        g[r][c] = fill_color; placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    r1, c1, r2, c2 = 1, 2, 8, 10
    for c in range(c1, c2 + 1): g[r1][c] = 7; g[r2][c] = 7
    for r in range(r1, r2 + 1): g[r][c1] = 7; g[r][c2] = 7
    if name == "no_row_markers":
        # Col markers + fill key but no row markers — rule's
        # row×col intersection set is empty.
        g[r1 + 1][c1 + 3] = 3; g[r1 + 1][c1 + 5] = 3
        g[r1 + 3][c1 + 4] = 4
        return g
    if name == "no_col_markers":
        # Row markers + fill key but no col markers — intersection
        # set is empty.
        g[r1 + 3][c1 + 1] = 2; g[r1 + 5][c1 + 1] = 2
        g[r1 + 4][c1 + 4] = 4
        return g
    if name == "no_fill_key":
        # Row + col markers but no fill key — rule has no color to
        # paint at the intersections.
        g[r1 + 3][c1 + 1] = 2; g[r1 + 5][c1 + 1] = 2
        g[r1 + 1][c1 + 3] = 3; g[r1 + 1][c1 + 5] = 3
        return g
    return g
