"""Generator for 18b:m121 — fill intersections from frame markers.

Rule: an 8-rectangular frame has 2-color markers on its top row and
left column. For each (top-marker column c, left-marker row r), the
interior cell (r, c) becomes color 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_top_markers, no_left_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e505760516d5"
VERSION = "1.1.0"
TASK_ID = "e505760516d5"
SUMMARY = "8-frame with 2-markers on top row + left column."

INVARIANTS = [
    "background is 0",
    "outer 8-frame at offset (1, 2) with size 8x9",
    "2-3 markers (color 2) on top row of frame",
    "2-3 markers (color 2) on left column of frame",
    "frame interior is bg",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_top_markers", "no_left_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "derived", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "derived", "valid": "11..17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "8frame_with_top_left_markers",
                       "valid": "8frame_with_top_left_markers"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        fw = ctx.draw_int("frame_w", 9, 9)
    elif difficulty == "hard":
        fh = ctx.draw_int("frame_h", 8, 9)
        fw = ctx.draw_int("frame_w", 10, 11)
    else:
        fh = ctx.draw_int("frame_h", 7, 9)
        fw = ctx.draw_int("frame_w", 9, 11)
    rng = ctx.draw_rng("layout")
    h = fh + 2
    w = fw + 3
    g = full_grid(h, w, 0)
    r1, c1 = 1, 2
    r2, c2 = r1 + fh - 1, c1 + fw - 1
    for c in range(c1, c2 + 1): g[r1][c] = 8; g[r2][c] = 8
    for r in range(r1, r2 + 1): g[r][c1] = 8; g[r][c2] = 8
    # markers on top row (interior cols)
    n_top = rng.randint(2, 3)
    top_cols = rng.sample(range(c1 + 1, c2), n_top)
    for c in top_cols: g[r1][c] = 2
    # markers on left column (interior rows)
    n_left = rng.randint(2, 3)
    left_rows = rng.sample(range(r1 + 1, r2), n_left)
    for r in left_rows: g[r][c1] = 2
    return g


def _draw_from_degenerate(name, rng):
    fh, fw = 7, 9
    h = fh + 2; w = fw + 3
    g = full_grid(h, w, 0)
    r1, c1 = 1, 2; r2, c2 = r1 + fh - 1, c1 + fw - 1
    if name == "no_frame":
        # markers without an 8-frame → no container to fill intersections inside
        for c in [4, 6]: g[r1][c] = 2
        for r in [3, 5]: g[r][c1] = 2
        return g
    if name == "no_top_markers":
        # frame + left markers but no top markers → no column intersections defined
        for c in range(c1, c2 + 1): g[r1][c] = 8; g[r2][c] = 8
        for r in range(r1, r2 + 1): g[r][c1] = 8; g[r][c2] = 8
        for r in [3, 5]: g[r][c1] = 2
        return g
    if name == "no_left_markers":
        # frame + top markers but no left markers → no row intersections defined
        for c in range(c1, c2 + 1): g[r1][c] = 8; g[r2][c] = 8
        for r in range(r1, r2 + 1): g[r][c1] = 8; g[r][c2] = 8
        for c in [4, 6]: g[r1][c] = 2
        return g
    return g
