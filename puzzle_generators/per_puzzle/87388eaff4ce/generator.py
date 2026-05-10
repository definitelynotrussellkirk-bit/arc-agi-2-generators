"""Generator for arc_puzzle_bank_21_set10_e:medium_j12 — sort by rows DESC, pack vertically.

Rule: extract every connected non-bg object's bbox crop. Sort by
crop height (rows) descending; tiebreak by color ascending. Stack
crops vertically with 1-row gap, output width = max cols.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_objs, texture.
Degenerates: no_objects, single_object, all_same_height.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "87388eaff4ce"
VERSION = "1.1.0"
TASK_ID = "87388eaff4ce"
SUMMARY = "2-3 connected non-bg objects with distinct bbox heights."

INVARIANTS = [
    "background is 0",
    "2-3 4-connected non-bg objects, each a distinct color",
    "each object has a distinct bbox height (so the row-sort is unambiguous)",
    "objects don't touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "all_same_height")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objs":         {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "= n_objs", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "distinct_height_objects",
                       "valid": "distinct_height_objects"},
    "n_distinct_colors": {"type": "int", "default": "= n_objs", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES_BY_H = {
    1: [[(0, 0), (0, 1)], [(0, 0), (0, 1), (0, 2)]],
    2: [[(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0), (0, 1), (0, 2), (1, 1)]],
    3: [[(0, 0), (1, 0), (1, 1), (2, 0)], [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)]],
    4: [[(0, 0), (1, 0), (2, 0), (3, 0)], [(0, 0), (0, 1), (1, 0), (2, 0), (3, 0)]],
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
        n = ctx.draw_int("n_objs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 16, 19)
        n = ctx.draw_int("n_objs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 12, 16)
        n = ctx.draw_int("n_objs", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    heights = rng.sample(list(_SHAPES_BY_H.keys()), n)
    palette = list(random_palette(rng, n))
    placed: list[tuple[int, int, int, int]] = []
    for sh_h, color in zip(heights, palette):
        shape = rng.choice(_SHAPES_BY_H[sh_h])
        sh = max(c[0] for c in shape) + 1
        sw = max(c[1] for c in shape) + 1
        for _ in range(80):
            r0 = rng.randint(0, h - sh)
            c0 = rng.randint(0, w - sw)
            bb_pad = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
            if any(bbox_overlaps(bb_pad, p) for p in placed): continue
            paint_at(g, r0, c0, shape, color)
            placed.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # Empty grid — rule has no objects to sort.
        return g
    if name == "single_object":
        # Only one object — rule's vertical stack has just one entry;
        # sort signal degenerates.
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 4
        return g
    if name == "all_same_height":
        # All objects share the same bbox height — rule's
        # height-DESC ordering is ambiguous.
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 4
        for r, c in [(2, 7), (2, 8), (3, 7)]: g[r][c] = 6
        for r, c in [(7, 4), (7, 5), (8, 4)]: g[r][c] = 7
        return g
    return g
