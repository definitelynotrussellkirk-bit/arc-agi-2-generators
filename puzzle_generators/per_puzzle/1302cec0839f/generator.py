"""Generator for 5b:hard_32 — shape match matrix.

Rule: components sorted by (col, row). Output NxN: cell (r, c) = 8 iff
shape r and shape c have identical normalized binary masks, else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, all_same_shape, all_distinct_shapes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1302cec0839f"
VERSION = "1.1.0"
TASK_ID = "1302cec0839f"
SUMMARY = "3 components in distinct colors; one pair has identical shape."

INVARIANTS = [
    "background is 0",
    "exactly 3 isolated components in distinct colors",
    "exactly one pair has identical normalized binary shape (so output isn't all-identity)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "all_same_shape", "all_distinct_shapes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "12..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "three_isolated_components",
                       "valid": "three_isolated_components"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place(g, rng, shape, color):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(40):
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 15, 18)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 13, 15)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 3)
    base_shapes = [
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1)],
    ]
    base = rng.choice(base_shapes)
    other = rng.choice([s for s in base_shapes if s != base])
    shapes = [base, base, other]
    rng.shuffle(shapes)
    for color, shape in zip(palette, shapes):
        _place(g, rng, shape, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 14
    g = full_grid(h, w, 0)
    same = [(0, 0), (0, 1), (1, 0)]
    distinct = [(0, 0), (1, 0), (1, 1), (2, 1)]
    if name == "no_components":
        # Empty grid — output matrix is 0x0, ill-defined.
        return g
    if name == "all_same_shape":
        # All 3 components have the same shape — output matrix is all-8.
        for dr, dc in same: g[1 + dr][1 + dc] = 4
        for dr, dc in same: g[1 + dr][6 + dc] = 5
        for dr, dc in same: g[5 + dr][1 + dc] = 6
        return g
    if name == "all_distinct_shapes":
        # All 3 distinct shapes — output matrix is identity (no off-diagonal matches).
        for dr, dc in same: g[1 + dr][1 + dc] = 4
        for dr, dc in distinct: g[1 + dr][6 + dc] = 5
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 1)]: g[5 + dr][1 + dc] = 6
        return g
    return g
