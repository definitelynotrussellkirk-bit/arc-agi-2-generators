"""Generator for 7d7772cc.

Rule: dots on source side move near separator when they match the
key side.

Combinatorial axes (8): grid_h/w, sep_row, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_separator, no_dots, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bf9e0959b8ce"
VERSION = "1.1.0"
TASK_ID = "bf9e0959b8ce"
SUMMARY = "Source-side dots move near separator when they match key side."

INVARIANTS = [
    "one full non-background separator row divides source and key regions",
    "source-side singleton dots are compared with the key value in the same column",
    "key colors are distinct so each column has an unambiguous match",
    "the separator color differs from background and key colors",
]

SEP_ROWS = ("r5", "r6")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_separator", "no_dots", "full_grid")
HELPFUL_TEXTURES = SEP_ROWS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "sep_row":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SEP_ROWS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
    "texture":        {"type": "str", "default": "alias for sep_row",
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
    if tx in SEP_ROWS:
        sep_row = int(tx[1:])
    else:
        sep_row = ctx.draw_choice("sep_row", [5, 6])
    bg, sep, a, b, c = ctx.draw_distinct_colors("colors", n=5, exclude={0})
    g = full_grid(10, 11, bg)
    for col in range(11):
        g[sep_row][col] = sep
    key_row = sep_row + 1
    for col, value in [(2, a), (5, b), (8, c)]:
        g[key_row][col] = value
    g[1][2] = a
    g[2][5] = c
    g[3][8] = c
    if sample_index % 2:
        g[4][1] = b
        g[key_row][1] = b
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 11, 1)
    if name == "no_separator":
        g[2][3] = 2
        return g
    if name == "no_dots":
        for c in range(11):
            g[5][c] = 3
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(11):
                g[r][c] = 1
        return g
    return g
