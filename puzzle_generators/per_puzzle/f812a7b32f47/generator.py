"""Generator for 5b:m32 — fill frame intersections.

Rule: a hollow 5-rectangular frame; some top-row cells are color 3
(column markers); some left-col cells are color 2 (row markers). At
each (row-marker row, col-marker col) intersection inside the frame,
place a 7.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_top,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_top_markers, no_left_markers, no_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f812a7b32f47"
VERSION = "1.1.0"
TASK_ID = "f812a7b32f47"
SUMMARY = "5-frame with 2-3 col markers (3) on top + 2-3 row markers (2) on left."

INVARIANTS = [
    "background is 0",
    "5-frame at offset (1,2) hollow",
    "2-3 cells of color 3 on the frame top row",
    "2-3 cells of color 2 on the frame left col",
    "frame interior is bg",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_top_markers", "no_left_markers", "no_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "frame_h":        {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "frame_w":        {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_top":          {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "frame_with_markers",
                       "valid": "frame_with_markers"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        fw = ctx.draw_int("frame_w", 8, 9)
    elif difficulty == "hard":
        fh = ctx.draw_int("frame_h", 8, 9)
        fw = ctx.draw_int("frame_w", 9, 10)
    else:
        fh = ctx.draw_int("frame_h", 7, 9)
        fw = ctx.draw_int("frame_w", 8, 10)
    rng = ctx.draw_rng("layout")
    h = fh + 2; w = fw + 4
    g = full_grid(h, w, 0)
    r1, c1 = 1, 2
    r2, c2 = r1 + fh - 1, c1 + fw - 1
    for c in range(c1, c2 + 1): g[r1][c] = 5; g[r2][c] = 5
    for r in range(r1, r2 + 1): g[r][c1] = 5; g[r][c2] = 5
    n_top = rng.randint(2, 3)
    top_cols = rng.sample(range(c1 + 1, c2), n_top)
    for c in top_cols: g[r1][c] = 3
    n_left = rng.randint(2, 3)
    left_rows = rng.sample(range(r1 + 1, r2), n_left)
    for r in left_rows: g[r][c1] = 2
    return g


def _draw_from_degenerate(name, rng):
    fh, fw = 7, 8
    h = fh + 2; w = fw + 4
    g = full_grid(h, w, 0)
    r1, c1 = 1, 2
    r2, c2 = r1 + fh - 1, c1 + fw - 1
    if name == "no_top_markers":
        # frame and left markers but no top markers → no column intersections
        for c in range(c1, c2 + 1): g[r1][c] = 5; g[r2][c] = 5
        for r in range(r1, r2 + 1): g[r][c1] = 5; g[r][c2] = 5
        for r in (r1 + 2, r1 + 4): g[r][c1] = 2
        return g
    if name == "no_left_markers":
        # frame and top markers but no left markers → no row intersections
        for c in range(c1, c2 + 1): g[r1][c] = 5; g[r2][c] = 5
        for r in range(r1, r2 + 1): g[r][c1] = 5; g[r][c2] = 5
        for c in (c1 + 2, c1 + 4): g[r1][c] = 3
        return g
    if name == "no_frame":
        # markers without 5-frame → no boundary defining intersections
        for c in (4, 6): g[1][c] = 3
        for r in (3, 5): g[r][2] = 2
        return g
    return g
