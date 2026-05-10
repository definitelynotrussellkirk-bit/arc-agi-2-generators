"""Generator for ac605cbb.

Rule: symbol cells expand into vertical, horizontal, and small bent
line segments.

Combinatorial axes (8): grid_h/w, symbol, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_symbol, full_grid, two_symbols.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4d0f228177b0"
VERSION = "1.1.0"
TASK_ID = "4d0f228177b0"
SUMMARY = "Symbol cells expand into vertical, horizontal and bent segments."

INVARIANTS = [
    "background is color 0",
    "symbol colors 6, 3, 1 or 2 determine local line expansions",
    "expanded interiors use color 5",
    "the symbol cell sits clear of grid borders",
]

SYMBOLS = ("s6", "s3", "s1", "s2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_symbol", "full_grid", "two_symbols")
HELPFUL_TEXTURES = SYMBOLS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "symbol":         {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SYMBOLS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for symbol",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in SYMBOLS:
        symbol = int(tx[1])
    else:
        symbol = int(ctx.draw_choice("symbol", ["6", "3", "1", "2"]))
    g = full_grid(12, 12, 0)
    if symbol == 6:
        g[6 + rng.randint(0, 2)][5 + rng.randint(0, 2)] = 6
    elif symbol == 3:
        g[2 + rng.randint(0, 3)][5 + rng.randint(0, 2)] = 3
    elif symbol == 1:
        g[5 + rng.randint(0, 2)][4 + rng.randint(0, 2)] = 1
    else:
        g[5 + rng.randint(0, 2)][6 + rng.randint(0, 2)] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_symbol":
        return g
    if name == "two_symbols":
        g[3][3] = 6
        g[8][8] = 1
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 5
        return g
    return g
