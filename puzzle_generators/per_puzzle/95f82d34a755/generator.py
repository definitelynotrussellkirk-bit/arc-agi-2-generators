"""Generator for arc_additional_puzzles_21_set7:M46 — Cellwise eq of row/col headers.

Rule: row 0 (right of col 0) holds column headers. Col 0 (below row 0)
holds row headers. Output is (h-1) x (w-1) where cell (r, c) is the
value at row-header[r] if it equals col-header[c], else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shared,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_shared, all_shared, corner_marked.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "95f82d34a755"
VERSION = "1.1.0"
TASK_ID = "95f82d34a755"
SUMMARY = "Row/col header values; output cell is row-header if it equals col-header, else 0."

INVARIANTS = [
    "row 0 cells (cols 1+) are non-zero color headers",
    "col 0 cells (rows 1+) are non-zero color headers",
    "(0,0) is zero (would be ambiguous as both header)",
    "at least one matching pair so output isn't all-zero",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_shared", "all_shared", "corner_marked")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..9"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "4..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shared":       {"type": "int", "default": "rng 1..3", "valid": "0..6"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "header_axes",
                       "valid": "header_axes"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..8"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 5, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 5, 7)
    g = full_grid(h, w, 0)

    rng = ctx.draw_rng("headers")
    palette = list(range(1, 10))
    rng.shuffle(palette)
    palette = palette[:rng.randint(3, 5)]

    row_headers = [rng.choice(palette) for _ in range(w - 1)]
    for c, v in enumerate(row_headers):
        g[0][c + 1] = v
    col_headers = [rng.choice(palette) for _ in range(h - 1)]
    for r, v in enumerate(col_headers):
        g[r + 1][0] = v

    if not any(rh == ch for rh in row_headers for ch in col_headers):
        forced = rng.choice(palette)
        g[0][1] = forced
        g[1][0] = forced

    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 6
    g = full_grid(h, w, 0)
    if name == "no_shared":
        # disjoint top/left palettes → output is all zeros, no signal
        for c, v in enumerate([2, 3, 4, 5, 6], start=1):
            if c < w: g[0][c] = v
        for r, v in enumerate([7, 8, 9, 7, 8], start=1):
            if r < h: g[r][0] = v
        return g
    if name == "all_shared":
        # top and left identical → output is full diag, no contrast
        for c in range(1, w):
            g[0][c] = 5
        for r in range(1, h):
            g[r][0] = 5
        return g
    if name == "corner_marked":
        # (0,0) non-zero → "(0,0) is zero" invariant violated, ambiguous header role
        g[0][0] = 4
        for c, v in enumerate([2, 3, 4, 5, 6], start=1):
            if c < w: g[0][c] = v
        for r, v in enumerate([2, 3, 4, 5, 6], start=1):
            if r < h: g[r][0] = v
        return g
    return g
