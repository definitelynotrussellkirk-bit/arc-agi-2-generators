"""Generator for arc_additional_puzzles_21_set9:E57 — Rotate non-{0,5} cells 4-fold around 5-pivot.

Rule: pivot = single 5-cell. For each non-{0,5} cell, copy to its
4 rotational positions around the pivot.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pivot, no_cells, pivot_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6b4b56166bfd"
VERSION = "1.1.0"
TASK_ID = "6b4b56166bfd"
SUMMARY = "1 pivot of color 5 + 1-3 cells of distinct non-{0,5} colors near it."

INVARIANTS = [
    "exactly 1 cell of color 5 (pivot)",
    "1-3 non-{0,5} cells with rotated positions in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pivot", "no_cells", "pivot_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "pivot_with_nearby_cells",
                       "valid": "pivot_with_nearby_cells"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..4"},
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
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 6, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 6, 8)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pr = h // 2; pc = w // 2
    g[pr][pc] = 5
    palette = [1, 2, 3, 4, 6, 7, 8, 9]
    n = rng.randint(1, 3)
    placed = []
    for _ in range(40):
        if len(placed) >= n: break
        dr = rng.randint(-2, 2); dc = rng.randint(-2, 2)
        if dr == 0 and dc == 0: continue
        if not (0 <= pr + dr < h and 0 <= pc + dc < w): continue
        rots = [(dr, dc), (dc, -dr), (-dr, -dc), (-dc, dr)]
        if all(0 <= pr + a < h and 0 <= pc + b < w for a, b in rots):
            r = pr + dr; c = pc + dc
            if g[r][c] == 0:
                g[r][c] = rng.choice(palette)
                placed.append((dr, dc))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    if name == "no_pivot":
        # cells without 5-pivot → no rotation center
        g[2][2] = 4
        g[3][3] = 6
        return g
    if name == "no_cells":
        # pivot alone, nothing to rotate
        g[h // 2][w // 2] = 5
        return g
    if name == "pivot_at_corner":
        # pivot at corner → most rotated cells fall out of bounds
        g[0][0] = 5
        g[1][1] = 4  # rotations land at (1,-1), (-1,1), (-1,-1) — all OOB
        return g
    return g
