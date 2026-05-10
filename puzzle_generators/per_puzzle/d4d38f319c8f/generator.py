"""Generator for arc_additional_puzzles_21_set10_bundle:M65 — Per-row right-shift by col-0 value.

Rule: col 0 holds shift counts. For each cell (r, c) with c > 0:
  - src_c = c - shift; if src_c is valid (1 ≤ src_c < cols) and (r, src_c) is non-bg,
    paint that value, else 0. Col 0 is preserved.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: zero_shifts, no_content, all_max_shift.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d4d38f319c8f"
VERSION = "1.1.0"
TASK_ID = "d4d38f319c8f"
SUMMARY = "Col 0 holds per-row shift counts; rule shifts each row's content by that amount."

INVARIANTS = [
    "col 0 holds non-zero values (shift counts) in 1..3",
    "each row has 1..3 non-zero cells in cols 1+ with src-c valid after shift",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("zero_shifts", "no_content", "all_max_shift")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..7", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "col0_shift_with_content",
                       "valid": "col0_shift_with_content"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 4, 7)
        w = ctx.draw_int("grid_w", 6, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    color_rng = ctx.draw_rng("colors")
    for r in range(h):
        shift = rng.randint(1, min(3, w - 2))
        g[r][0] = shift
        n_cells = rng.randint(1, 3)
        cols = list(range(1, max(2, w - shift)))
        rng.shuffle(cols)
        for c in cols[:n_cells]:
            g[r][c] = color_rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 7
    g = full_grid(h, w, 0)
    if name == "zero_shifts":
        # all col-0 shift counts are 0 → rule's shift is identity, no content moves
        for r in range(h):
            g[r][0] = 0
            g[r][2] = (r % 8) + 1
            g[r][4] = (r % 7) + 1
        return g
    if name == "no_content":
        # only shift counts in col 0, no content cells in cols 1+ → rule shifts nothing
        for r in range(h):
            g[r][0] = (r % 3) + 1
        return g
    if name == "all_max_shift":
        # shifts equal to (w-1) → src-c is out of bounds for all cells, output cols 1+ all 0
        for r in range(h):
            g[r][0] = w - 2   # max valid shift
            g[r][1] = (r % 8) + 1   # this content shifts to col w-1, valid
            g[r][2] = (r % 7) + 1   # this content shifts past w, gets dropped
        return g
    return g
