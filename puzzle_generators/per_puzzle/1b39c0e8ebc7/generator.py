"""Generator for arc_additional_puzzles_21_set2:H12 — offset 3-cells onto 4-cells.

Rule: the 8-to-9 vector maps source color-3 cells onto color-4 cells,
producing 7s there.

Combinatorial axes (8): grid_h, grid_w, palette_kind, vector,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_vector_markers, no_3_4_pairs, mismatched_pairs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1b39c0e8ebc7"
VERSION = "1.1.0"
TASK_ID = "1b39c0e8ebc7"
SUMMARY = "The 8-to-9 vector maps source color-3 cells onto color-4 cells, producing 7s there."

INVARIANTS = [
    "one 8 marker and one 9 marker define the vector",
    "at least two color-3 source cells have matching color-4 targets",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_vector_markers", "no_3_4_pairs", "mismatched_pairs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "vector":         {"type": "str", "default": "rng vec",
                       "valid": "(1,2)|(2,1)|(-1,2)|(2,-1)"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "vector_with_pairs",
                       "valid": "vector_with_pairs"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
    rng = ctx.draw_rng("layout")
    dr, dc = rng.choice([(1, 2), (2, 1), (-1, 2), (2, -1)])
    g = full_grid(h, w, 0)
    base_r = 1 if dr >= 0 else 3
    base_c = 1 if dc >= 0 else w - 3
    g[base_r][base_c] = 8
    g[base_r + dr][base_c + dc] = 9
    occupied = {(base_r, base_c), (base_r + dr, base_c + dc)}
    candidates = [
        (r, c)
        for r in range(1, h - 1)
        for c in range(1, w - 1)
        if (r, c) not in occupied
        and (r + dr, c + dc) not in occupied
        and 0 <= r + dr < h
        and 0 <= c + dc < w
    ]
    rng.shuffle(candidates)
    for r, c in candidates[:3]:
        g[r][c] = 3
        g[r + dr][c + dc] = 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_vector_markers":
        # 3/4 pairs but no 8/9 markers → no vector defined
        g[2][2] = 3; g[3][4] = 4
        g[5][5] = 3; g[6][7] = 4
        return g
    if name == "no_3_4_pairs":
        # 8/9 vector defined but no 3-cells → nothing maps to 7
        g[1][1] = 8
        g[3][3] = 9
        return g
    if name == "mismatched_pairs":
        # 3-cells exist but their (r+dr, c+dc) targets are NOT color 4
        g[1][1] = 8; g[3][3] = 9   # vector = (2,2)
        g[2][2] = 3                  # target (4,4) is bg, not 4
        g[5][5] = 3                  # target (7,7) is bg, not 4
        return g
    return g
