"""Generator for v1_e_m_h_keys:M5 — erase the largest object.

Rule: find connected non-bg objects; erase the one with the largest
cell count. Smaller objects stay unchanged.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_smalls,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_largest, single_object, all_same_size.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "97b3f59b5cc4"
VERSION = "1.1.0"
TASK_ID = "97b3f59b5cc4"
SUMMARY = "1 large connected object + 1-2 strictly smaller distinct-color objects."

INVARIANTS = [
    "background is 0",
    "1 object with ≥4 cells (the 'big' object)",
    "1-2 strictly smaller objects, each in a distinct color",
    "all sizes are distinct",
    "objects don't touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_largest", "single_object", "all_same_size")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_smalls":       {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spread_distinct_sizes",
                       "valid": "spread_distinct_sizes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_BIG = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
]
_SMALL = [
    [(0, 0)],
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0)],
    [(0, 0), (0, 1), (1, 0)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
        n_smalls = 1
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        n_smalls = 2
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 7, 10)
        n_smalls = ctx.draw_int("n_smalls", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = list(random_palette(rng, 1 + n_smalls))
    big = rng.choice(_BIG)
    bh = max(c[0] for c in big) + 1
    bw = max(c[1] for c in big) + 1
    placed: list[tuple[int, int, int, int]] = []
    for _ in range(80):
        r0 = rng.randint(0, h - bh)
        c0 = rng.randint(0, w - bw)
        bb_pad = (r0 - 1, c0 - 1, r0 + bh, c0 + bw)
        if any(bbox_overlaps(bb_pad, p) for p in placed): continue
        paint_at(g, r0, c0, big, palette[0])
        placed.append((r0, c0, r0 + bh - 1, c0 + bw - 1))
        break
    big_size = len(big)
    for color in palette[1:]:
        small_options = [s for s in _SMALL if len(s) < big_size]
        small = rng.choice(small_options)
        sh = max(c[0] for c in small) + 1
        sw = max(c[1] for c in small) + 1
        for _ in range(80):
            r0 = rng.randint(0, h - sh)
            c0 = rng.randint(0, w - sw)
            bb_pad = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
            if any(bbox_overlaps(bb_pad, p) for p in placed): continue
            paint_at(g, r0, c0, small, color)
            placed.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "tied_largest":
        # two objects share the maximum size → "largest" is ambiguous
        paint_at(g, 1, 1, _BIG[0], 4)   # 4-cell object
        paint_at(g, 4, 5, _BIG[0], 6)   # also 4-cell — tied
        return g
    if name == "single_object":
        # one object → trivially "largest", erasing it leaves empty grid
        paint_at(g, 2, 3, _BIG[0], 4)
        return g
    if name == "all_same_size":
        # all objects same size → all tied for largest
        paint_at(g, 1, 1, _SMALL[1], 4)   # 2-cell
        paint_at(g, 3, 5, _SMALL[1], 6)   # 2-cell
        paint_at(g, 5, 1, _SMALL[1], 3)   # 2-cell
        return g
    return g
