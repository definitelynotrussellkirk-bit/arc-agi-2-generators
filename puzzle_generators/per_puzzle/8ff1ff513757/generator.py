"""Generator for arc_puzzle_bank_21_set5_s:S5_M7.

Rule: output = input with every all-zero row removed (column count
unchanged).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_active_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_active_rows, no_active_rows, all_zero_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8ff1ff513757"
VERSION = "1.1.0"
TASK_ID = "8ff1ff513757"
SUMMARY = "Sparse non-zero rows separated by all-zero spacer rows."

INVARIANTS = [
    "background is 0",
    "at least 2 non-zero rows AND at least 1 all-zero row (otherwise rule is identity)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_active_rows", "no_active_rows", "all_zero_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 5..8", "valid": "4..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_active_rows":  {"type": "int", "default": "rng 2..h-2", "valid": "2..10"},
    "palette_size":   {"type": "int", "default": "rng 1..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "row_sparse", "valid": "row_sparse"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..6", "valid": "1..9"},
    "density":        {"type": "str", "default": "mixed", "valid": "mixed"},
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
        w = ctx.draw_int("grid_w", 5, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 5, 8)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_active = rng.randint(2, max(2, h - 2))
    active_rows = sorted(rng.sample(range(h), n_active))
    for r in active_rows:
        n_cells = rng.randint(1, max(1, w // 2))
        cols = rng.sample(range(w), n_cells)
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for c in cols:
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 6
    g = full_grid(h, w, 0)
    if name == "all_active_rows":
        # every row has nonzero cells → rule is trivially identity (no rows to drop)
        for r in range(h):
            g[r][r % w] = ((r % 7) + 1)
        return g
    if name == "no_active_rows":
        # only one nonzero row → predicate "≥2 nonzero rows" fails
        g[3][2] = 5
        return g
    if name == "all_zero_grid":
        # entirely zero grid → rule produces an empty (0×w) output
        return g
    return g
