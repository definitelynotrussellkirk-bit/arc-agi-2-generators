"""Generator for arc_additional_puzzles_21_set17_bundle:E115.

Rule: same-color row/column endpoint pairs; rule fills the straight
zero segment between each pair with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_endpoint, off_axis_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c4d63d8b4567"
VERSION = "1.1.0"
TASK_ID = "c4d63d8b4567"
SUMMARY = "Distinct-color row/column endpoint pairs separated by zeros."

INVARIANTS = [
    "background is 0",
    "each nonzero color appears in exactly two cells",
    "the two cells of each color share one row or one column",
    "all cells between matching endpoints are zero",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_endpoint", "off_axis_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..14"},
    "pair_count":     {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "axis_aligned_pairs",
                       "valid": "axis_aligned_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear(g, cells):
    return all(g[r][c] == 0 for r, c in cells)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        pair_count = ctx.draw_int("pair_count", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 12, 14)
        pair_count = ctx.draw_int("pair_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        pair_count = ctx.draw_int("pair_count", 2, 3)
    colors = ctx.draw_distinct_colors("colors", n=pair_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    for color in colors:
        placed = False
        for _ in range(300):
            horizontal = rng.choice([True, False])
            if horizontal:
                r = rng.randrange(h)
                c1 = rng.randint(0, w - 4)
                c2 = rng.randint(c1 + 3, w - 1)
                cells = [(r, c) for c in range(c1, c2 + 1)]
                endpoints = [(r, c1), (r, c2)]
            else:
                c = rng.randrange(w)
                r1 = rng.randint(0, h - 4)
                r2 = rng.randint(r1 + 3, h - 1)
                cells = [(r, c) for r in range(r1, r2 + 1)]
                endpoints = [(r1, c), (r2, c)]
            if _clear(g, cells):
                for r, c in endpoints:
                    g[r][c] = color
                placed = True
                break
        if not placed:
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule has no endpoint pairs to connect.
        return g
    if name == "single_endpoint":
        # Color appears once — rule's "exactly 2 same-color
        # endpoints" precondition fails.
        g[3][3] = 4
        return g
    if name == "off_axis_pair":
        # Two same-color endpoints not sharing row or column —
        # rule's "straight segment" cannot be formed.
        g[2][2] = 4; g[5][7] = 4
        return g
    return g
