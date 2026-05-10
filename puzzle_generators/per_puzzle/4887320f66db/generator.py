"""Generator for arc_additional_puzzles_21_set14_bundle:H92.

Rule: row keys = col 0 values (rows 1+); col keys = row 0 values
(cols 1+). Output 3*N rows × 3*M cols where each tile is motif
(col_key) transformed by row_key.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rows, n_cols,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_row_keys, no_col_keys, all_zero_keys.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4887320f66db"
VERSION = "1.1.0"
TASK_ID = "4887320f66db"
SUMMARY = "Row 0 has 2-3 col-keys (motif ids) + col 0 has 2-3 row-keys (transform codes)."

INVARIANTS = [
    "row 0 (cols 1+) has 2-3 cells of values 2/3/4 (motif ids)",
    "col 0 (rows 1+) has 2-3 cells of values 1/2/3/4 (transform codes)",
]

PALETTE_KINDS = ("default", "few_keys", "many_keys", "varied_keys")
DEGENERATE_TEXTURES = ("no_row_keys", "no_col_keys", "all_zero_keys")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "n_rows+1", "valid": "3..4"},
    "grid_w":         {"type": "int", "default": "n_cols+1", "valid": "3..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rows":         {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "n_cols":         {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "row0_col0", "valid": "row0_col0"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
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
        n_rows = ctx.draw_int("n_rows", 2, 2)
        n_cols = ctx.draw_int("n_cols", 2, 2)
    elif difficulty == "hard":
        n_rows = ctx.draw_int("n_rows", 3, 3)
        n_cols = ctx.draw_int("n_cols", 3, 3)
    else:
        n_rows = ctx.draw_int("n_rows", 2, 3)
        n_cols = ctx.draw_int("n_cols", 2, 3)
    h = n_rows + 1; w = n_cols + 1
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    for c in range(1, w):
        g[0][c] = rng.randint(2, 4)
    for r in range(1, h):
        g[r][0] = rng.randint(1, 4)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 4, 4
    g = full_grid(h, w, 0)
    if name == "no_row_keys":
        # only col-key header — no row-transform codes, output dims undefined
        g[0][1] = 2; g[0][2] = 3; g[0][3] = 4
        return g
    if name == "no_col_keys":
        # only row-transform header — no motif ids, output dims undefined
        g[1][0] = 1; g[2][0] = 2; g[3][0] = 3
        return g
    if name == "all_zero_keys":
        # both headers exist but every key is 0 → no tiles to compose
        return g
    return g
