"""Generator for arc_puzzle_bank_21_set8_s:S8_M7 — infer row period.

Rule: each row has a periodic prefix (1-3 cycle period). Extend the
prefix to fill the entire row.

Combinatorial axes (8): grid_h, grid_w, palette_kind, period_len,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_prefix, full_row_already, single_cell_prefix.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "726ac4a5071a"
VERSION = "1.1.0"
TASK_ID = "726ac4a5071a"
SUMMARY = "Each row has a periodic prefix that hasn't filled to grid width."

INVARIANTS = [
    "background is 0 (only after the prefix)",
    "each row's prefix is at least one full period AND has trailing 0s",
    "period length is 1-3",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_prefix", "full_row_already", "single_cell_prefix")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "period_len":     {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "row_periodic_prefix",
                       "valid": "row_periodic_prefix"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 3, 4)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 3, 5)
        w = ctx.draw_int("grid_w", 10, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in range(h):
        period_len = rng.randint(1, 3)
        period = [rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]) for _ in range(period_len)]
        repeats = rng.randint(2, max(2, (w - 2) // period_len))
        prefix_len = repeats * period_len
        if prefix_len >= w:
            prefix_len = period_len * (w // period_len - 1)
        for i in range(prefix_len):
            g[r][i] = period[i % period_len]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 4, 12
    g = full_grid(h, w, 0)
    if name == "no_prefix":
        # blank rows → no period to extend
        return g
    if name == "full_row_already":
        # row already filled to width → rule is identity (no trailing 0 to fill)
        for c in range(w): g[0][c] = (3 if c % 2 == 0 else 6)
        for c in range(w): g[1][c] = 4
        return g
    if name == "single_cell_prefix":
        # only one cell of color → period unrecoverable (no full period to detect)
        g[0][0] = 4
        g[2][0] = 6
        return g
    return g
