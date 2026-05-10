"""Generator for arc_additional_puzzle_bank_volume15:E99.

Rule: two aligned blue markers with even separation get a red midpoint.

Combinatorial axes (8): grid_h, grid_w, palette_kind, orientation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_marker, odd_separation, non_aligned.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "be3a57da2378"
VERSION = "1.1.0"
TASK_ID = "be3a57da2378"
SUMMARY = "Two aligned blue markers with even separation get a red midpoint."

INVARIANTS = [
    "background is 0",
    "there are exactly two blue markers",
    "the markers share one row or one column",
    "their separation is even and at least two cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_marker", "odd_separation", "non_aligned")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..13", "valid": "3..20"},
    "grid_w":         {"type": "int", "default": "rng 7..13", "valid": "3..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "orientation":    {"type": "str", "default": "rng h|v", "valid": "h|v"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "row_or_col_aligned",
                       "valid": "row_or_col_aligned"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 13)
        w = ctx.draw_int("grid_w", 7, 13)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    if rng.choice([False, True]):
        r = rng.randint(0, h - 1)
        c1 = rng.randint(0, w - 3)
        max_step = (w - 1 - c1) // 2
        c2 = c1 + 2 * rng.randint(1, max_step)
        g[r][c1] = 1
        g[r][c2] = 1
    else:
        c = rng.randint(0, w - 1)
        r1 = rng.randint(0, h - 3)
        max_step = (h - 1 - r1) // 2
        r2 = r1 + 2 * rng.randint(1, max_step)
        g[r1][c] = 1
        g[r2][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "single_marker":
        # one blue → no second marker, no midpoint to compute
        g[3][4] = 1
        return g
    if name == "odd_separation":
        # markers separated by odd cells → no integer midpoint, rule undefined
        g[3][1] = 1; g[3][6] = 1  # separation 5 (odd)
        return g
    if name == "non_aligned":
        # markers not on same row/col → no axis defined
        g[2][2] = 1
        g[5][6] = 1
        return g
    return g
