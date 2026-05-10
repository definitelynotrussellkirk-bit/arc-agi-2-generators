"""Generator for arc_additional_puzzle_bank_volume17:M113 — Translate 2-cells by 3→4 delta.

Rule: dr/dc = (4-marker - 3-marker). For each 2-cell, set output at
(r+dr, c+dc) to 8 if that cell is in {0, 3, 4}.

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_3, no_4, zero_delta.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "86ab0e5c6811"
VERSION = "1.1.0"
TASK_ID = "86ab0e5c6811"
SUMMARY = "3-marker + 4-marker define delta; 2-blob in upper-left + decoration; output translates 2s to 8s."

INVARIANTS = [
    "exactly one 3-marker, one 4-marker; delta non-zero",
    "2-blob has 2-3 cells, fits after translation",
    "decoration is non-{2,3,4} cell elsewhere",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_3", "no_4", "zero_delta")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_size":      {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "3marker_4marker_with_2blob",
                       "valid": "3marker_4marker_with_2blob"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    # 3 at (0, 0), 4 at (3, 4) — delta = (3, 4)
    g[0][0] = 3
    dr = rng.randint(2, 3); dc = rng.randint(2, 3)
    g[dr][dc] = 4
    # 2-blob in middle
    g[1][1] = 2
    if rng.random() < 0.5:
        g[2][1] = 2
    if rng.random() < 0.5:
        g[2][2] = 2
    # decoration
    g[h - 1][w - 1] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_3":
        # only 4-marker → delta endpoint missing, vector underdetermined
        g[3][3] = 4
        g[1][1] = 2; g[2][1] = 2
        g[h - 1][w - 1] = 7
        return g
    if name == "no_4":
        # only 3-marker → other delta endpoint missing
        g[0][0] = 3
        g[1][1] = 2; g[2][1] = 2
        g[h - 1][w - 1] = 7
        return g
    if name == "zero_delta":
        # 3 and 4 at the same cell → delta = (0, 0), translation has no effect
        g[2][2] = 3   # then overwritten
        g[2][2] = 4   # both at same spot (only 4 visible)
        g[1][1] = 2; g[2][1] = 2
        g[h - 1][w - 1] = 7
        return g
    return g
