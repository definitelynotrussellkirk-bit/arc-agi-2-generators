"""Generator for arc_puzzle_bank_21_set14_bundle:easy_n02.

Rule: rows contain color-zero-same-color motifs; each one-cell horizontal
gap is filled with the matching color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, gap_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, gap_already_filled, mismatched_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ec9340d27f7e"
VERSION = "1.1.0"
TASK_ID = "ec9340d27f7e"
SUMMARY = "Separated horizontal one-cell gaps between same-color endpoints."

INVARIANTS = [
    "background is 0",
    "each motif is color-zero-same-color in one row",
    "motifs are separated by at least one zero column",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "gap_already_filled", "mismatched_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "gap_count":      {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "horizontal_pair",
                       "valid": "horizontal_pair"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        gap_count = ctx.draw_int("gap_count", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        gap_count = ctx.draw_int("gap_count", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 12)
        gap_count = ctx.draw_int("gap_count", 3, 5)
    colors = ctx.draw_distinct_colors("colors", n=gap_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    placed = 0
    for color in colors:
        for _ in range(300):
            r = rng.randrange(h)
            c = rng.randint(0, w - 3)
            band = range(max(0, c - 1), min(w, c + 4))
            if all(g[r][cc] == 0 for cc in band):
                g[r][c] = color
                g[r][c + 2] = color
                placed += 1
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # scattered single cells, no endpoint pairs → rule has no targets
        for r, c, v in [(1, 2, 4), (3, 5, 5), (5, 7, 6)]:
            g[r][c] = v
        return g
    if name == "gap_already_filled":
        # endpoint pairs but the gap is already non-bg → rule no-op for those gaps
        g[2][1] = 3; g[2][2] = 5; g[2][3] = 3
        g[5][4] = 6; g[5][5] = 7; g[5][6] = 6
        return g
    if name == "mismatched_endpoints":
        # endpoints with different colors → "same color" condition never matches
        g[2][1] = 3; g[2][3] = 5
        g[5][4] = 6; g[5][6] = 7
        return g
    return g
