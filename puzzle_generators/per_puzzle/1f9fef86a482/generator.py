"""Generator for arc_puzzle_bank_21_set12_s:S12_M3.

Rule: a blue-count header chooses which body components to mark by
contact degree.

Combinatorial axes (8): grid_h, grid_w, palette_kind, target_degree,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_match, all_isolated.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1f9fef86a482"
VERSION = "1.1.0"
TASK_ID = "1f9fef86a482"
SUMMARY = "A blue-count header chooses which body components to mark by contact degree."

INVARIANTS = [
    "background is 0",
    "the top row contains exactly k blue cells",
    "body components begin below the header row",
    "at least one body component has contact degree k",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_match", "all_isolated")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..15"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "target_degree":  {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "header_top_components_below",
                       "valid": "header_top_components_below"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 9, 10)
        w = ctx.draw_int("width", 11, 12)
        k = ctx.draw_int("target_degree", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 11, 12)
        w = ctx.draw_int("width", 13, 14)
        k = ctx.draw_int("target_degree", 3, 3)
    else:
        h = ctx.draw_int("height", 9, 12)
        w = ctx.draw_int("width", 11, 14)
        k = ctx.draw_int("target_degree", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    for c in range(k):
        g[0][c] = 1

    r = rng.randint(3, h - 4)
    c = rng.randint(3, w - 5)
    if k == 2:
        cells = [(r, c, 2), (r, c + 1, 3), (r, c + 2, 4)]
    else:
        cells = [(r, c, 3), (r - 1, c, 2), (r, c + 1, 4), (r + 1, c, 6)]
    for rr, cc, color in cells:
        g[rr][cc] = color

    g[h - 2][w - 3] = 7
    g[h - 2][w - 2] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # body components but no blue marker → contact-degree threshold undefined
        cells = [(5, 5, 2), (5, 6, 3), (5, 7, 4)]
        for rr, cc, col in cells: g[rr][cc] = col
        g[h - 2][w - 3] = 7; g[h - 2][w - 2] = 7
        return g
    if name == "no_match":
        # marker says k=2 but no body component has contact degree 2 (all isolated)
        for c in range(2): g[0][c] = 1
        g[3][3] = 2
        g[6][7] = 3
        g[h - 2][w - 3] = 7; g[h - 2][w - 2] = 7
        return g
    if name == "all_isolated":
        # all body components are singletons (degree 0) → none satisfies k>=2
        for c in range(3): g[0][c] = 1
        for r, c in [(3, 3), (5, 7), (7, 2)]: g[r][c] = 4
        return g
    return g
