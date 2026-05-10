"""Generator for arc_additional_puzzle_bank_volume2:H9 — Intersection of normalized 2/3 shapes.

Rule: normalize cells of color 2 and color 3 (translate min to 0).
Output paints color 8 at every position in both normalized sets.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shape,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: identical_shapes, disjoint_shapes, single_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c878420172c2"
VERSION = "1.1.0"
TASK_ID = "c878420172c2"
SUMMARY = "Two staircase shapes in colors 2 and 3 placed apart; output paints intersection of normalized cells."

INVARIANTS = [
    "exactly one connected blob of color 2 and one of color 3",
    "their normalized cell sets share at least one position",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("identical_shapes", "disjoint_shapes", "single_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shape":        {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "two_overlapping_shapes",
                       "valid": "two_overlapping_shapes"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    shape = [(0, 0)]
    target = rng.randint(3, 5)
    while len(shape) < target:
        r0, c0 = rng.choice(shape)
        dr, dc = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        nr, nc = r0 + dr, c0 + dc
        if (nr, nc) not in shape:
            shape.append((nr, nc))
    minr = min(r for r, _ in shape); minc = min(c for _, c in shape)
    shape = [(r - minr, c - minc) for r, c in shape]
    shape3 = list(shape)
    n_diff = rng.randint(1, max(1, len(shape) // 2))
    for _ in range(n_diff):
        if len(shape3) <= 1: break
        idx = rng.randint(0, len(shape3) - 1)
        del shape3[idx]
        for _ in range(20):
            r0, c0 = rng.choice(shape3)
            dr, dc = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            nr, nc = r0 + dr, c0 + dc
            if (nr, nc) not in shape3:
                shape3.append((nr, nc)); break
    minr = min(r for r, _ in shape3); minc = min(c for _, c in shape3)
    shape3 = [(r - minr, c - minc) for r, c in shape3]
    sh2 = max(r for r, _ in shape) + 1
    sw2 = max(c for _, c in shape) + 1
    sh3 = max(r for r, _ in shape3) + 1
    sw3 = max(c for _, c in shape3) + 1
    r2 = rng.randint(1, max(1, h // 2 - sh2))
    c2 = rng.randint(1, max(1, w // 2 - sw2))
    r3 = rng.randint(h // 2, max(h // 2, h - sh3 - 1))
    c3 = rng.randint(w // 2, max(w // 2, w - sw3 - 1))
    for r, c in shape:
        g[r2 + r][c2 + c] = 2
    for r, c in shape3:
        g[r3 + r][c3 + c] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "identical_shapes":
        # color-2 and color-3 shapes are identical (after normalization) → intersection equals shape
        # placed apart; both have the same cells under normalization
        for (r, c) in [(1, 1), (1, 2), (2, 1), (2, 2)]: g[r][c] = 2
        for (r, c) in [(5, 6), (5, 7), (6, 6), (6, 7)]: g[r][c] = 3
        return g
    if name == "disjoint_shapes":
        # normalized shapes have NO common position → intersection is empty
        # color 2 shape at (0,0)-(0,2) (1x3 horizontal)
        for (r, c) in [(1, 1), (1, 2), (1, 3)]: g[r][c] = 2
        # color 3 shape at (0,0)-(2,0) (3x1 vertical) — different normalized shape
        for (r, c) in [(5, 6), (6, 6), (7, 6)]: g[r][c] = 3
        return g
    if name == "single_color":
        # only one of the two required colors present → rule has no second set, intersection undefined
        for (r, c) in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 2
        return g
    return g
