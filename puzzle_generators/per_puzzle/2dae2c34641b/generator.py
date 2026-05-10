"""Generator for 6b:m37 — connect same-color pairs with L-elbow.

Rule: each color appearing twice (at non-aligned positions) → draw an
L-elbow path between them.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, aligned_pair, single_endpoint.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2dae2c34641b"
VERSION = "1.1.0"
TASK_ID = "2dae2c34641b"
SUMMARY = "2-3 colors each appearing exactly twice at distinct row+col positions."

INVARIANTS = [
    "background is 0",
    "each non-zero color appears exactly twice at strictly different rows AND cols",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "aligned_pair", "single_endpoint")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "diagonal_offset_pairs",
                       "valid": "diagonal_offset_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    for color in palette:
        for _ in range(40):
            r1 = rng.randint(0, h - 1); c1 = rng.randint(0, w - 1)
            r2 = rng.randint(0, h - 1); c2 = rng.randint(0, w - 1)
            if r1 == r2 or c1 == c2: continue
            if g[r1][c1] != 0 or g[r2][c2] != 0: continue
            g[r1][c1] = color; g[r2][c2] = color; break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # singletons only → no pair to L-connect
        g[1][2] = 4
        g[5][7] = 6
        return g
    if name == "aligned_pair":
        # endpoints in same row → L-elbow degenerates to straight line
        g[3][1] = 4; g[3][8] = 4   # same row
        g[5][2] = 6; g[5][7] = 6   # same row
        return g
    if name == "single_endpoint":
        # one color has only 1 endpoint → "appears exactly twice" precondition fails
        g[1][2] = 4; g[5][7] = 4
        g[3][4] = 6   # 6 only once
        return g
    return g
