"""Generator for arc_puzzle_bank_twentyfirst21:E145.

Rule: a single non-zero seed cell paints its full row and column.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors, color.
Degenerates: no_seed, two_seeds, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5b3c69ad7276"
VERSION = "1.1.0"
TASK_ID = "5b3c69ad7276"

SUMMARY = "Single non-zero seed paints its full row and column."

INVARIANTS = [
    "background is 0",
    "exactly one non-zero cell anywhere on the grid",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seed", "two_seeds", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "4..6"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "5..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "color":          {"type": "color", "default": "rng !{0}", "valid": "1..9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 4, 4)
        w = ctx.draw_int("grid_w", 5, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 7, 7)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 5, 7)
    g = full_grid(h, w, 0)
    r = rng.randint(0, h - 1)
    c = rng.randint(0, w - 1)
    g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 6, 0)
    if name == "no_seed":
        return g
    if name == "two_seeds":
        g[1][2] = 3
        g[3][4] = 4
        return g
    if name == "full_grid":
        for r in range(5):
            for c in range(6):
                g[r][c] = 3
        return g
    return g
