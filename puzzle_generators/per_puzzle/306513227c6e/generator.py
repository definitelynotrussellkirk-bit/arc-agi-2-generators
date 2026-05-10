"""Generator for arc_additional_puzzles_21_set3:H18 — move 4-shape by marker vector.

Rule: markers 2 and 3 define a vector; color-4 cells are kept and
copied by that vector as 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, vector,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, zero_vector, no_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "306513227c6e"
VERSION = "1.1.0"
TASK_ID = "306513227c6e"
SUMMARY = "Markers 2 and 3 define a vector; color-4 cells are kept and copied by that vector as 8."

INVARIANTS = [
    "one color-2 marker and one color-3 marker define a nonzero vector",
    "the color-4 motif has in-bounds shifted copies",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "zero_vector", "no_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "vector":         {"type": "str", "default": "rng vec",
                       "valid": "(1,2)|(2,1)|(-1,2)|(2,-1)"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "markers_with_motif",
                       "valid": "markers_with_motif"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
    g[base_r][base_c] = 2
    g[base_r + dr][base_c + dc] = 3
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
    for r, c in candidates[:4]:
        g[r][c] = 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # motif-4 cells but no 2/3 markers → no vector defined
        g[3][3] = 4; g[5][5] = 4; g[6][2] = 4
        return g
    if name == "zero_vector":
        # both markers at the same cell (impossible to draw) — emulate by placing them
        # at the same color → degenerate marker vector of length 0; rule has no shift
        g[2][2] = 2; g[2][2] = 3
        g[5][5] = 4; g[6][3] = 4
        return g
    if name == "no_motif":
        # markers define a vector but no color-4 cells → nothing to copy
        g[1][1] = 2
        g[3][3] = 3
        return g
    return g
