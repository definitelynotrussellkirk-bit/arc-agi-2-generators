"""Generator for arc_puzzle_bank_twentyfirst21:M143 — translate shape by 9→9 vector.

Rule: two 9-markers define a translation vector v = (9b.r - 9a.r,
9b.c - 9a.c). Apply v to the colored shape; original shape stays;
9s are erased; out-of-bounds copy cells are silently dropped.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_shape, zero_vector.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "733d5c4a475a"
VERSION = "1.1.0"
TASK_ID = "733d5c4a475a"
SUMMARY = "Two 9-markers (defining a translation vector) + a shape to translate."

INVARIANTS = [
    "background is 0",
    "exactly two 9-cells defining a non-zero translation vector",
    "exactly one connected shape in a third color (3-4 cells)",
    "the translated copy lands at least partly in-bounds (so the rule has effect)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_shape", "zero_vector")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "shape_with_marker_pair",
                       "valid": "shape_with_marker_pair"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 6, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    color = rng.choice(list(random_palette(rng, 4, exclude={9})))
    shape = rng.choice(_SHAPES)
    sh = max(c[0] for c in shape) + 1
    sw = max(c[1] for c in shape) + 1
    sr = rng.randint(0, max(0, h // 2 - sh))
    sc = rng.randint(0, max(0, w // 2 - sw))
    paint_at(g, sr, sc, shape, color)
    nine_a_r = rng.randint(sr, sr + sh - 1)
    nine_a_c = rng.randint(max(0, sc + sw), w - 2)
    if g[nine_a_r][nine_a_c] != 0:
        nine_a_c = min(w - 1, nine_a_c + 1)
    g[nine_a_r][nine_a_c] = 9
    dr = rng.randint(1, max(1, h - nine_a_r - 1))
    dc = rng.randint(-min(2, nine_a_c), min(2, w - nine_a_c - 1))
    if dc == 0: dc = 1
    nine_b_r = nine_a_r + dr
    nine_b_c = nine_a_c + dc
    if 0 <= nine_b_r < h and 0 <= nine_b_c < w and g[nine_b_r][nine_b_c] == 0:
        g[nine_b_r][nine_b_c] = 9
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # Shape but no 9-markers — rule's vector readout fails;
        # translation undefined.
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 4
        return g
    if name == "no_shape":
        # Markers but no shape — rule has nothing to translate.
        g[2][5] = 9; g[5][5] = 9
        return g
    if name == "zero_vector":
        # Both 9-markers at the same position (delta = 0,0) —
        # rule's translation is identity; effect invisible.
        for r, c in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4
        g[3][5] = 9
        return g
    return g
