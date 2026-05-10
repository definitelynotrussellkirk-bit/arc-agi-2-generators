"""Generator for 14b:m94 — fill matching row-column intersections.

Rule: a 5-rectangular frame; the top interior row contains color
markers, and the left interior column contains color markers. For each
top-row marker at column c with color X, and each left-col marker at
row r with color X, the interior cell (r, c) becomes color X.

Combinatorial axes (8): frame_h, frame_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_shared_color, empty_row_header, empty_col_header.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f4725b891d89"
VERSION = "1.1.0"
TASK_ID = "f4725b891d89"
SUMMARY = "5-frame with header row + header column of color markers (some colors repeat)."

INVARIANTS = [
    "background is 0",
    "outer 5-frame, hollow",
    "header row (just inside top) holds 3-4 color markers",
    "header column (just inside left) holds 3-4 color markers",
    "at least 2 colors appear in BOTH headers (so output != input)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_shared_color", "empty_row_header", "empty_col_header")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "frame_h":        {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "frame_w":        {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "header_row_and_column",
                       "valid": "header_row_and_column"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
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
        fh = ctx.draw_int("frame_h", 7, 7)
        fw = ctx.draw_int("frame_w", 7, 7)
    elif difficulty == "hard":
        fh = ctx.draw_int("frame_h", 9, 11)
        fw = ctx.draw_int("frame_w", 9, 11)
    else:
        fh = ctx.draw_int("frame_h", 7, 9)
        fw = ctx.draw_int("frame_w", 7, 9)
    rng = ctx.draw_rng("layout")
    h = fh; w = fw
    g = full_grid(h, w, 0)
    for c in range(w): g[0][c] = 5; g[h - 1][c] = 5
    for r in range(h): g[r][0] = 5; g[r][w - 1] = 5
    while True:
        palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 4)
        n_top = rng.randint(3, 4)
        top_cols = rng.sample(range(2, w - 1), n_top)
        top_colors = [rng.choice(palette) for _ in top_cols]
        n_left = rng.randint(3, 4)
        left_rows = rng.sample(range(2, h - 1), n_left)
        left_colors = [rng.choice(palette) for _ in left_rows]
        shared = set(top_colors) & set(left_colors)
        if len(shared) >= 2:
            for c, col in zip(top_cols, top_colors): g[1][c] = col
            for r, col in zip(left_rows, left_colors): g[r][1] = col
            return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    for c in range(w): g[0][c] = 5; g[h - 1][c] = 5
    for r in range(h): g[r][0] = 5; g[r][w - 1] = 5
    if name == "no_shared_color":
        # Header row + header column have no overlapping colors — rule's
        # match step finds no intersection cells to fill.
        g[1][2] = 3; g[1][4] = 7
        g[3][1] = 4; g[5][1] = 6
        return g
    if name == "empty_row_header":
        # Frame + left-column header but the top-row header is empty —
        # rule has no column targets.
        g[3][1] = 4; g[5][1] = 6
        return g
    if name == "empty_col_header":
        # Frame + top-row header but the left-col header is empty —
        # rule has no row targets.
        g[1][2] = 3; g[1][4] = 7
        return g
    return g
