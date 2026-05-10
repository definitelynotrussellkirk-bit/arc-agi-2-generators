"""Generator for arc_puzzle_bank_21_set7_s:S7_E3.

Rule: two color-4 markers define a rectangle; output is the interior crop.

Combinatorial axes (8): grid_h, grid_w, palette_kind, density,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, single_marker, markers_collinear.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "401aff907774"
VERSION = "1.1.0"
TASK_ID = "401aff907774"
SUMMARY = "Two color-4 markers define a rectangle; the output is the interior crop."

INVARIANTS = [
    "background is 0",
    "there are exactly two color-4 corner markers",
    "the markers have at least one row and column between them",
    "the interior contains a small colored pattern",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "single_marker", "markers_collinear")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "interior_fill":  {"type": "choice", "default": "rng sparse",
                       "valid": "sparse interior pattern"},
    "palette_size":   {"type": "int", "default": "4", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "diag_corners",
                       "valid": "diag_corners"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "2..6"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    r1 = rng.randint(0, h - 4)
    c1 = rng.randint(0, w - 4)
    r2 = rng.randint(r1 + 2, h - 1)
    c2 = rng.randint(c1 + 2, w - 1)
    g[r1][c1] = 4
    g[r2][c2] = 4
    palette = [2, 3, 6, 7]
    for idx, (r, c) in enumerate(rng.sample([(r, c) for r in range(r1 + 1, r2) for c in range(c1 + 1, c2)], min(4, (r2 - r1 - 1) * (c2 - c1 - 1)))):
        g[r][c] = palette[idx % len(palette)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # no color-4 markers → rule has no anchor for cropping
        for r, c, v in [(2, 3, 5), (4, 5, 6), (5, 4, 7)]:
            g[r][c] = v
        return g
    if name == "single_marker":
        # only one color-4 cell → rectangle is undefined (only one corner)
        g[2][2] = 4
        for r, c, v in [(4, 5, 5), (5, 4, 6)]:
            g[r][c] = v
        return g
    if name == "markers_collinear":
        # two markers in same row/col → no interior, rule produces empty/1xN region
        g[3][1] = 4
        g[3][7] = 4
        for r, c, v in [(2, 4, 5), (4, 4, 6)]:
            g[r][c] = v
        return g
    return g
