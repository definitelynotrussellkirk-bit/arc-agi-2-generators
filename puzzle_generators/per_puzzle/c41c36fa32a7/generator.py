"""Generator for arc_puzzle_bank_21_set18_bundle:easy_p02.

Matching endpoints with an odd-length clear segment fill only their midpoint.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, pair_count, texture.
Degenerates: no_pairs, odd_distance, no_clear_segment.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c41c36fa32a7"
VERSION = "1.1.0"
TASK_ID = "c41c36fa32a7"
SUMMARY = "Separated horizontal and vertical clear segments with exact midpoints."

INVARIANTS = [
    "background is 0",
    "each color appears in one matching aligned endpoint pair",
    "endpoint distance is even and the interior segment is zero",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "odd_distance", "no_clear_segment")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "pair_count":     {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "= pair_count", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_even_distance_pairs",
                       "valid": "scattered_even_distance_pairs"},
    "n_distinct_colors": {"type": "int", "default": "= pair_count", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 8, 10)
        pair_count = ctx.draw_int("pair_count", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 12, 14)
        pair_count = ctx.draw_int("pair_count", 5, 7)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        pair_count = ctx.draw_int("pair_count", 3, 5)
    colors = ctx.draw_distinct_colors("colors", n=pair_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    for color in colors:
        for _ in range(300):
            horizontal = rng.choice([True, False])
            dist = rng.choice([2, 4, 6])
            if horizontal:
                if dist >= w:
                    continue
                r = rng.randrange(h)
                c1 = rng.randint(0, w - dist - 1)
                cells = [(r, c) for c in range(c1, c1 + dist + 1)]
                endpoints = [(r, c1), (r, c1 + dist)]
            else:
                if dist >= h:
                    continue
                c = rng.randrange(w)
                r1 = rng.randint(0, h - dist - 1)
                cells = [(r, c) for r in range(r1, r1 + dist + 1)]
                endpoints = [(r1, c), (r1 + dist, c)]
            if _clear(g, cells):
                for r, c in endpoints:
                    g[r][c] = color
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        return g
    if name == "odd_distance":
        # Endpoints at odd distance (e.g., 3 apart) — rule's "even
        # distance, exact midpoint" precondition fails; midpoint is
        # not a single cell.
        g[3][1] = 4; g[3][4] = 4
        return g
    if name == "no_clear_segment":
        # Endpoints aligned but interior cell already non-zero —
        # rule's "interior segment is zero" precondition fails.
        g[3][1] = 4; g[3][3] = 4
        g[3][2] = 6
        return g
    return g
