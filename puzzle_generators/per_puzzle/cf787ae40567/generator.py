"""Generator for arc_puzzle_bank_21_set17_s:S17_E7.

Rule: plus-growth area is encoded as a one-row run of 8s.

Combinatorial axes (8): grid_h/w, seed_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_seeds, full_seeds, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cf787ae40567"
VERSION = "1.1.0"
TASK_ID = "cf787ae40567"
SUMMARY = "Plus-growth area is encoded as a one-row run of 8s."

INVARIANTS = [
    "input contains two to four seed cells",
    "the output width equals the number of cells in the union of plus-growth masks",
    "the output is a single row of 8s",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seeds", "full_seeds", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 6..8", "valid": "3..14"},
    "width":          {"type": "int", "default": "rng 6..8", "valid": "3..14"},
    "seed_count":     {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "position_bias":  {"type": "str", "default": "interior", "valid": "interior"},
    "n_distinct_colors":{"type": "int", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 6, 6)
        w = ctx.draw_int("width", 6, 7)
        n = ctx.draw_int("seed_count", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 7, 8)
        w = ctx.draw_int("width", 7, 8)
        n = ctx.draw_int("seed_count", 3, 4)
    else:
        h = ctx.draw_int("height", 6, 8)
        w = ctx.draw_int("width", 6, 8)
        n = ctx.draw_int("seed_count", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cells = [(r, c) for r in range(1, h - 1) for c in range(1, w - 1)]
    for idx, (r, c) in enumerate(rng.sample(cells, n)):
        g[r][c] = 2 + idx
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 7, 0)
    if name == "no_seeds":
        return g
    if name == "full_seeds":
        for r in range(1, 6):
            for c in range(1, 6):
                if (r + c) % 2 == 0:
                    g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(7):
                g[r][c] = 2
        return g
    return g
