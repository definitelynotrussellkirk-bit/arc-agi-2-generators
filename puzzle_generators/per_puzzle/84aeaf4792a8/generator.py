"""Generator for 8b:hard_52 — shape similarity matrix.

Rule: connected components sorted by (row, col). Output NxN: cell
(r, c) = 5 if r==c, 8 if shape r and shape c are rotation-equivalent,
else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: all_same_shape (all 3 shapes rotation-equivalent → matrix
is all-8 off-diagonal, no rule contrast), all_distinct (no pair
matches → matrix is identity-only, off-diagonal stays 0), single_motif
(only 1 component → matrix is 1x1, no pairwise comparison).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "84aeaf4792a8"
VERSION = "1.1.0"
TASK_ID = "84aeaf4792a8"
SUMMARY = "3 components in distinct colors; one pair rotation-equivalent."

INVARIANTS = [
    "background is 0",
    "exactly 3 isolated components in distinct colors",
    "at least one pair is rotation-equivalent",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_same_shape", "all_distinct", "single_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "12..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "three_components_one_pair_match",
                       "valid": "three_components_one_pair_match"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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


def _rotate_cw(shape):
    rs = [r for r, _ in shape]
    h = max(rs) + 1
    return sorted([(c, h - 1 - r) for r, c in shape])


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 13, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 15, 17)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
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
    rotated = base
    for _ in range(rng.randint(1, 3)):
        rotated = _rotate_cw(rotated)
    other = rng.choice([s for s in base_shapes if s != base])
    shapes = [base, rotated, other]
    rng.shuffle(shapes)
    for color, shape in zip(palette, shapes):
        _place(g, rng, shape, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 14
    g = full_grid(h, w, 0)
    if name == "all_same_shape":
        # All 3 shapes rotation-equivalent → output matrix is
        # all-8 off-diagonal; no rule contrast.
        base = [(0, 0), (0, 1), (1, 0)]
        for dr, dc in base: g[1 + dr][1 + dc] = 1
        for dr, dc in _rotate_cw(base): g[1 + dr][6 + dc] = 3
        for dr, dc in _rotate_cw(_rotate_cw(base)): g[6 + dr][2 + dc] = 4
        return g
    if name == "all_distinct":
        # No pair matches under rotation → output matrix is
        # identity-only; off-diagonals stay 0.
        for dr, dc in [(0, 0), (1, 0), (2, 0)]: g[1 + dr][1 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (0, 2), (0, 3)]: g[1 + dr][5 + dc] = 3
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]: g[5 + dr][2 + dc] = 4
        return g
    if name == "single_motif":
        # Only 1 component — output matrix is 1x1; no pairwise
        # similarity comparison.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]: g[3 + dr][5 + dc] = 6
        return g
    return g
