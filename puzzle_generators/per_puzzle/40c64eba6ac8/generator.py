"""Generator for 8b:hard_54 — boolean ops panel.

Rule: two shapes (color 2 and 3) of equal bbox dimensions. Output is a
2x2 grid (with 1-cell gaps) of {union, intersection, 2-minus-3,
3-minus-2}, each painted color 8 where the boolean predicate holds.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: identical_shapes (cells_a == cells_b → union == intersect
== both, A-minus-B == B-minus-A == empty; rule's 4-op contrast collapses),
disjoint_shapes (cells_a ∩ cells_b == ∅ → intersection is empty,
2-minus-3 == 2 and 3-minus-2 == 3, no contrast between ops),
unequal_bboxes (color-2 and color-3 shapes have different bbox dims →
rule's "equal-bbox" precondition fails).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "40c64eba6ac8"
VERSION = "1.1.0"
TASK_ID = "40c64eba6ac8"
SUMMARY = "Two equal-bbox shapes in colors 2 and 3, isolated."

INVARIANTS = [
    "background is 0",
    "exactly two connected components: one in color 2, one in color 3",
    "their bbox dimensions are identical",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("identical_shapes", "disjoint_shapes", "unequal_bboxes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "shape_h":           {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "shape_w":           {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "position_bias":     {"type": "str", "default": "two_equal_bbox_shapes",
                          "valid": "two_equal_bbox_shapes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..2", "valid": "2..2"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        sh = ctx.draw_int("shape_h", 3, 3)
        sw = ctx.draw_int("shape_w", 3, 3)
    elif difficulty == "hard":
        sh = ctx.draw_int("shape_h", 4, 4)
        sw = ctx.draw_int("shape_w", 4, 4)
    else:
        sh = ctx.draw_int("shape_h", 3, 4)
        sw = ctx.draw_int("shape_w", 3, 4)
    rng = ctx.draw_rng("layout")
    h = sh * 2 + 4
    w = sw * 2 + 4
    for _ in range(40):
        g = full_grid(h, w, 0)
        cells_a = set()
        cells_b = set()
        for cells, _ in [(cells_a, 'A'), (cells_b, 'B')]:
            cells.add((0, 0))
            cur = [(0, 0)]
            target = rng.randint(max(3, sh * sw // 2), sh * sw)
            attempts = 0
            while len(cells) < target and attempts < 100:
                attempts += 1
                r, c = rng.choice(list(cells))
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < sh and 0 <= nc < sw and (nr, nc) not in cells:
                        cells.add((nr, nc))
                        if len(cells) >= target: break
        if cells_a == cells_b: continue
        ar = 1; ac = 1
        if not _free(g, ar, ac, ar + sh - 1, ac + sw - 1): continue
        for dr, dc in cells_a: g[ar + dr][ac + dc] = 2
        br = sh + 3; bc = sw + 3
        if not _free(g, br, bc, br + sh - 1, bc + sw - 1): continue
        for dr, dc in cells_b: g[br + dr][bc + dc] = 3
        return g
    return g


def _draw_from_degenerate(name, rng):
    sh, sw = 3, 3
    h = sh * 2 + 4
    w = sw * 2 + 4
    g = full_grid(h, w, 0)
    if name == "identical_shapes":
        # cells_a == cells_b → all 4 ops collapse: union == intersect == both,
        # A-B == B-A == empty.
        cells = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1)]
        for dr, dc in cells: g[1 + dr][1 + dc] = 2
        for dr, dc in cells: g[sh + 3 + dr][sw + 3 + dc] = 3
        return g
    if name == "disjoint_shapes":
        # cells_a ∩ cells_b = ∅ — intersection empty, A-B==A, B-A==B.
        for dr, dc in [(0, 0), (1, 0), (2, 0)]: g[1 + dr][1 + dc] = 2
        for dr, dc in [(0, 1), (0, 2), (1, 2)]: g[sh + 3 + dr][sw + 3 + dc] = 3
        return g
    if name == "unequal_bboxes":
        # A is 3x3, B is 2x2 — equal-bbox precondition fails.
        for dr, dc in [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)]: g[1 + dr][1 + dc] = 2
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]: g[sh + 3 + dr][sw + 3 + dc] = 3
        return g
    return g
