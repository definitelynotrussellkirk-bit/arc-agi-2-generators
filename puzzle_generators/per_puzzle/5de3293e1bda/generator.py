"""Generator for arc_additional_puzzle_bank_volume17:M117 — Intersection of normalized 1 and 2 shapes.

Rule: normalize 1-cells, normalize 2-cells, intersect. Output bbox-cropped
intersection in color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: empty_intersection (normalized 1-cells ∩ 2-cells = ∅ →
rule's intersection produces no cells, output is empty), identical_shapes
(1-shape == 2-shape after normalize → intersection equals input shape,
no contrast), missing_color (only 1-shape OR only 2-shape present →
rule's intersection has no second operand, undefined).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5de3293e1bda"
VERSION = "1.1.0"
TASK_ID = "5de3293e1bda"
SUMMARY = "1-shape and 2-shape placed apart; their normalized intersection is non-empty."

INVARIANTS = [
    "exactly one connected blob of color 1 and one of color 2",
    "their normalized cell sets share at least one position",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_intersection", "identical_shapes", "missing_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":            {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "blob_size":         {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "two_overlapping_normalized_shapes",
                          "valid": "two_overlapping_normalized_shapes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
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
        w = ctx.draw_int("grid_w", 9, 10)
        target_lo, target_hi = 3, 4
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        target_lo, target_hi = 4, 5
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
        target_lo, target_hi = 3, 5
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    shape1 = [(0, 0)]
    target = rng.randint(target_lo, target_hi)
    while len(shape1) < target:
        rb, cb = rng.choice(shape1)
        dr, dc = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        nr, nc = rb + dr, cb + dc
        if (nr, nc) not in shape1:
            shape1.append((nr, nc))
    minr = min(r for r, _ in shape1); minc = min(c for _, c in shape1)
    shape1 = [(r - minr, c - minc) for r, c in shape1]
    shape2 = list(shape1)
    n_diff = rng.randint(1, max(1, len(shape1) // 2))
    for _ in range(n_diff):
        if len(shape2) <= 1: break
        idx = rng.randint(0, len(shape2) - 1)
        del shape2[idx]
        for _ in range(20):
            r0, c0 = rng.choice(shape2)
            dr, dc = rng.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            nr, nc = r0 + dr, c0 + dc
            if (nr, nc) not in shape2:
                shape2.append((nr, nc)); break
    minr = min(r for r, _ in shape2); minc = min(c for _, c in shape2)
    shape2 = [(r - minr, c - minc) for r, c in shape2]
    sh1_h = max(r for r, _ in shape1) + 1
    sh1_w = max(c for _, c in shape1) + 1
    sh2_h = max(r for r, _ in shape2) + 1
    sh2_w = max(c for _, c in shape2) + 1
    r1 = rng.randint(1, max(1, h // 2 - sh1_h))
    c1 = rng.randint(1, max(1, w // 2 - sh1_w))
    r2 = rng.randint(min(h - sh2_h - 1, h // 2), max(h // 2, h - sh2_h - 1))
    c2 = rng.randint(min(w - sh2_w - 1, w // 2), max(w // 2, w - sh2_w - 1))
    for r, c in shape1: g[r1 + r][c1 + c] = 1
    for r, c in shape2: g[r2 + r][c2 + c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "empty_intersection":
        # Normalized cells of 1 and 2 share no position — rule's
        # intersection is empty, output has no painted cells.
        # 1-shape: vertical line; 2-shape: horizontal line. Normalized
        # cells: 1 = {(0,0),(1,0),(2,0)}; 2 = {(0,0),(0,1),(0,2)}.
        # Intersection = {(0,0)} — actually one shared. Use shapes
        # whose normalized footprints don't overlap at any cell:
        # 1 = {(0,1),(1,0),(1,1)}, 2 = {(0,0),(1,0)}. Both have (1,0)
        # — share. Use 1 = {(0,0),(1,1)}, 2 = {(0,1),(1,0)}: no shared.
        g[2][2] = 1; g[3][3] = 1   # normalized: (0,0),(1,1)
        g[5][6] = 2; g[6][5] = 2   # normalized: (0,1),(1,0)
        return g
    if name == "identical_shapes":
        # 1-shape == 2-shape after normalize — intersection = whole
        # shape; output has no contrast vs input footprint.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[2 + dr][2 + dc] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][6 + dc] = 2
        return g
    if name == "missing_color":
        # Only 1-shape present, no 2-shape — rule's intersection has
        # no second operand; undefined.
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[3 + dr][3 + dc] = 1
        return g
    return g
