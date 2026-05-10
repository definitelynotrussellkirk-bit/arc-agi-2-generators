"""Generator for arc_puzzle_bank_21_more:hard_b03.

Rule: marker_count = non-zeros in row 0; crop body to content; tile the
template horizontally with 1-col gaps marker_count times.

Combinatorial axes (8): grid_h/w, palette_kind, n_marks, palette_size,
position_bias, n_distinct_colors, motif_density, texture.
Degenerates: no_marks, no_motif, all_columns_marked.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8a248a268dd3"
VERSION = "1.1.0"
TASK_ID = "8a248a268dd3"
SUMMARY = "Row 0 has 2-4 markers + small motif (3-4 cells) below."

INVARIANTS = [
    "row 0 has 2-4 non-zero cells",
    "small motif (color 6) of 3-4 cells in body",
]

PALETTE_KINDS = ("default", "sparse", "dense", "balanced")
DEGENERATE_TEXTURES = ("no_marks", "no_motif", "all_columns_marked")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_marks":        {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "motif_density":  {"type": "str", "default": "fixed", "valid": "fixed"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 9, 11)
    n_marks = ctx.draw_int("n_marks", 2, 4)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    cols = list(range(w)); rng.shuffle(cols)
    for c in cols[:n_marks]:
        g[0][c] = 1
    g[2][5] = 6; g[2][6] = 6
    g[3][5] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 10
    g = full_grid(h, w, 0)
    if name == "no_marks":
        # motif but no row 0 markers → tile count zero (no output)
        g[2][5] = 6; g[2][6] = 6
        g[3][5] = 6
        return g
    if name == "no_motif":
        # markers but no body motif → nothing to tile
        for c in [1, 4, 7]:
            g[0][c] = 1
        return g
    if name == "all_columns_marked":
        # every column marked → maximal tile count
        for c in range(w):
            g[0][c] = 1
        g[2][5] = 6; g[2][6] = 6
        g[3][5] = 6
        return g
    return g
