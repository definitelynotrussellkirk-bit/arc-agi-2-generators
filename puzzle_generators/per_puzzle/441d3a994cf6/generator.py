"""Generator for arc_puzzle_bank_21_set16_bundle:easy_p05.

Rule: matching vertical endpoints with one zero between them are completed
by filling the middle cell.

Combinatorial axes (8): grid_h, grid_w, palette_kind, gap_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, gap_already_filled, mismatched_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "441d3a994cf6"
VERSION = "1.1.0"
TASK_ID = "441d3a994cf6"
SUMMARY = "Separated vertical one-cell gaps between matching endpoints."

INVARIANTS = [
    "background is 0",
    "each motif is color-zero-same-color in one column",
    "motifs are separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "gap_already_filled", "mismatched_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "gap_count":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "vertical_pair",
                       "valid": "vertical_pair"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        gap_count = ctx.draw_int("gap_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        gap_count = ctx.draw_int("gap_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        gap_count = ctx.draw_int("gap_count", 2, 4)
    colors = ctx.draw_distinct_colors("colors", n=gap_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    for color in colors:
        for _ in range(300):
            r = rng.randint(0, h - 3)
            c = rng.randrange(w)
            rows = range(max(0, r - 1), min(h, r + 4))
            if all(g[rr][c] == 0 for rr in rows):
                g[r][c] = color
                g[r + 2][c] = color
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # scattered single cells, no vertical endpoint pairs → rule has no targets
        for r, c, v in [(1, 2, 4), (3, 5, 5), (5, 7, 6)]:
            g[r][c] = v
        return g
    if name == "gap_already_filled":
        # vertical endpoint pairs but the gap is already non-bg → rule no-op
        g[1][2] = 3; g[2][2] = 5; g[3][2] = 3
        g[5][6] = 6; g[6][6] = 7; g[7][6] = 6
        return g
    if name == "mismatched_endpoints":
        # endpoints with different colors → "same color" condition never matches
        g[1][2] = 3; g[3][2] = 5
        g[5][6] = 6; g[7][6] = 7
        return g
    return g
