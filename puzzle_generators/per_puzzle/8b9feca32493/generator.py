"""Generator for arc_additional_puzzle_bank_volume4:H25 — Set difference of normalized 1 vs 2.

Rule: a = normalize(1-cells), b = normalize(2-cells), c = a - b. Crop to
c's bbox; paint to color 3 in fresh grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_1_shape, no_2_shape, equal_shapes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8b9feca32493"
VERSION = "1.1.0"
TASK_ID = "8b9feca32493"
SUMMARY = "1-shape and 2-shape placed apart; normalized 1-cells minus normalized 2-cells is a non-empty set."

INVARIANTS = [
    "exactly one connected blob of color 1 and one of color 2",
    "their normalized cell sets differ (1-shape has cells not in 2-shape)",
    "shapes placed in opposite halves of grid",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_1_shape", "no_2_shape", "equal_shapes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "two_shapes_separated",
                       "valid": "two_shapes_separated"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 12, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    shape1 = [(0, 0)]
    target = rng.randint(4, 6)
    while len(shape1) < target:
        rb, cb = rng.choice(shape1)
        dr, dc = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        nr, nc = rb + dr, cb + dc
        if (nr, nc) not in shape1:
            shape1.append((nr, nc))
    minr = min(r for r, _ in shape1); minc = min(c for _, c in shape1)
    shape1 = [(r - minr, c - minc) for r, c in shape1]
    shape2 = list(shape1)
    n_drop = rng.randint(1, max(1, len(shape1) - 2))
    for _ in range(n_drop):
        if len(shape2) > 1:
            shape2.pop(rng.randint(0, len(shape2) - 1))
    minr2 = min(r for r, _ in shape2); minc2 = min(c for _, c in shape2)
    shape2 = [(r - minr2, c - minc2) for r, c in shape2]
    sh1_h = max(r for r, _ in shape1) + 1; sh1_w = max(c for _, c in shape1) + 1
    sh2_h = max(r for r, _ in shape2) + 1; sh2_w = max(c for _, c in shape2) + 1
    r1 = rng.randint(0, max(0, h // 2 - sh1_h))
    c1 = rng.randint(0, max(0, w // 2 - sh1_w))
    r2 = rng.randint(min(h - sh2_h, h // 2), max(h // 2, h - sh2_h))
    c2 = rng.randint(min(w - sh2_w, w // 2), max(w // 2, w - sh2_w))
    for r, c in shape1: g[r1 + r][c1 + c] = 1
    for r, c in shape2: g[r2 + r][c2 + c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_1_shape":
        # Only 2-shape — rule's "a = normalize(1-cells)" is empty;
        # set difference is empty.
        for r, c in [(5, 7), (6, 7), (6, 8)]: g[r][c] = 2
        return g
    if name == "no_2_shape":
        # Only 1-shape — rule's "c = a - b" yields all of a;
        # output reproduces the 1-shape as 3.
        for r, c in [(2, 2), (3, 2), (3, 3), (4, 3)]: g[r][c] = 1
        return g
    if name == "equal_shapes":
        # 1-shape and 2-shape have identical normalized cells —
        # rule's set difference is empty; output undefined.
        for r, c in [(2, 2), (3, 2), (3, 3)]: g[r][c] = 1
        for r, c in [(6, 8), (7, 8), (7, 9)]: g[r][c] = 2
        return g
    return g
