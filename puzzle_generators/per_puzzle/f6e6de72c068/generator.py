"""Generator for arc_puzzle_bank_21_set5_e:easy_e02.

Rule: fill row-local A-0-A motif: middle 0 becomes A.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motifs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_motifs, motif_already_filled, mismatched_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f6e6de72c068"
VERSION = "1.1.0"
TASK_ID = "f6e6de72c068"
SUMMARY = "Fill row-local A-0-A gaps."

INVARIANTS = [
    "background is 0",
    "active rows contain A-0-A motifs",
    "each motif fills only its middle zero",
    "nonmatching cells remain unchanged",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motifs", "motif_already_filled", "mismatched_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "3..12"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motifs":         {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "row_motifs",
                       "valid": "row_motifs"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("motifs", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("motifs", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("motifs", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    attempts = 0
    colors = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    while placed < target and attempts < 120:
        attempts += 1
        r = rng.randrange(h)
        c = rng.randint(0, w - 3)
        color = rng.choice(colors)
        if g[r][c] == 0 and g[r][c + 1] == 0 and g[r][c + 2] == 0:
            g[r][c] = color
            g[r][c + 2] = color
            placed += 1
    if placed == 0:
        color = rng.choice(colors)
        g[h // 2][1] = color
        g[h // 2][3] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_motifs":
        # only single colored cells, never an A-0-A triple → rule fires zero times
        g[1][2] = 4; g[3][6] = 6; g[5][1] = 3
        return g
    if name == "motif_already_filled":
        # A-A-A (middle is already A, not 0) → rule has nothing to fill
        g[2][1] = 4; g[2][2] = 4; g[2][3] = 4
        g[4][3] = 6; g[4][4] = 6; g[4][5] = 6
        return g
    if name == "mismatched_endpoints":
        # A-0-B (different colors) → predicate fails, middle stays 0
        g[1][1] = 4; g[1][3] = 6
        g[3][2] = 3; g[3][4] = 8
        return g
    return g
