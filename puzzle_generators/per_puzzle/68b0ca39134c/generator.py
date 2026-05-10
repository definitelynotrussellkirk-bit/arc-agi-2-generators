"""Generator for arc_puzzle_bank_fifteenth21:E102 — keep only largest, erase rest.

Rule: keep the largest connected component; erase smaller ones.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, single_object, all_same_size.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "68b0ca39134c"
VERSION = "1.1.0"
TASK_ID = "68b0ca39134c"

SUMMARY = "Create several separated components with one unique largest component."

INVARIANTS = [
    "background is 0",
    "nonzero objects are separated 4-connected components",
    "one component is uniquely largest",
    "smaller components are erased by the rule",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "all_same_size")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..16"},
    "small_objects":  {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "scattered_components",
                       "valid": "scattered_components"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0)],
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)],
]


def _free(g, cells, top, left):
    h, w = len(g), len(g[0])
    coords = [(top + r, left + c) for r, c in cells]
    if any(r < 0 or c < 0 or r >= h or c >= w for r, c in coords):
        return False
    for r, c in coords:
        for rr in range(max(0, r - 1), min(h, r + 2)):
            for cc in range(max(0, c - 1), min(w, c + 2)):
                if g[rr][cc] != 0:
                    return False
    return True


def _paint(g, cells, top, left, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        small = ctx.draw_int("small_objects", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 11, 15)
        small = ctx.draw_int("small_objects", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 11)
        small = ctx.draw_int("small_objects", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shapes = [_SHAPES[-1]] + rng.sample(_SHAPES[:-1], k=min(small, len(_SHAPES) - 1))
    placed = 0
    for _ in range(500):
        if placed >= len(shapes):
            break
        shape = shapes[placed]
        max_r = max(r for r, _ in shape)
        max_c = max(c for _, c in shape)
        top = rng.randint(0, h - max_r - 1)
        left = rng.randint(0, w - max_c - 1)
        if _free(g, shape, top, left):
            _paint(g, shape, top, left, rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]))
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # Empty grid — rule's "keep largest" has no candidates.
        return g
    if name == "single_object":
        # Only one object — rule's selection is trivial; erase
        # branch never fires.
        for r, c in [(3, 3), (3, 4), (3, 5), (4, 3), (5, 3)]: g[r][c] = 4
        return g
    if name == "all_same_size":
        # Two objects of equal size — rule's "uniquely largest"
        # tie-break ambiguous; selection undefined.
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 4
        for r, c in [(6, 7), (6, 8), (7, 7)]: g[r][c] = 6
        return g
    return g
