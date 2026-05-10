"""Generator for arc_puzzle_bank_twentyfirst_21_bundle:easy_147_bridge_one_cell_vertical_gaps.

Rule: one-cell vertical gaps between matching colors are filled.

Combinatorial axes (8): grid_h, grid_w, palette_kind, gaps,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, gap_already_filled, mismatched_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f45070496ffc"
VERSION = "1.1.0"
TASK_ID = "f45070496ffc"
SUMMARY = "One-cell vertical gaps between matching colors are filled."

INVARIANTS = [
    "background is 0",
    "each target is an x 0 x vertical pattern",
    "target colors are nonzero",
    "gap patterns are separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "gap_already_filled", "mismatched_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "4..24"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "3..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "gaps":           {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "vertical_pair",
                       "valid": "vertical_pair"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        for rr in range(max(0, r - 1), min(h, r + 2)):
            for cc in range(max(0, c - 1), min(w, c + 2)):
                if g[rr][cc] != 0:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("gaps", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 10, 11)
        target = ctx.draw_int("gaps", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 7, 11)
        target = ctx.draw_int("gaps", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(160):
        if placed >= target:
            break
        r = rng.randint(0, h - 3)
        c = rng.randrange(w)
        cells = [(r, c), (r + 2, c)]
        if _free(g, cells):
            color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
            g[r][c] = color
            g[r + 2][c] = color
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # scattered single cells, no vertical pairs → rule has no targets
        for r, c, v in [(1, 2, 4), (4, 5, 5), (7, 7, 6)]:
            g[r][c] = v
        return g
    if name == "gap_already_filled":
        # vertical pairs but the gap is already non-bg → rule no-op for those
        g[1][2] = 3; g[2][2] = 5; g[3][2] = 3
        g[5][5] = 6; g[6][5] = 7; g[7][5] = 6
        return g
    if name == "mismatched_endpoints":
        # different-color vertical endpoints → "same color" condition never matches
        g[1][2] = 3; g[3][2] = 5
        g[5][5] = 6; g[7][5] = 7
        return g
    return g
