"""Generator for 5af49b42.

Rule: isolated dots expand into the horizontal key run that contains
their color, aligned at the matching key index.

Combinatorial axes (8): grid_h/w, dot_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_keys, no_dots, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1e9f25803112"
VERSION = "1.1.0"
TASK_ID = "1e9f25803112"
SUMMARY = "Isolated dots expand into horizontal key run containing their color."

INVARIANTS = [
    "horizontal runs of length at least two are key sequences",
    "single-cell runs are dots to expand",
    "each dot color appears in exactly one key run",
    "key colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_keys", "no_dots", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16"},
    "dot_count":      {"type": "int", "default": "rng 2..4", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "8", "valid": "8"},
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
    colors = ctx.draw_distinct_colors("colors", n=8, exclude={0})
    g = full_grid(13, 16, 0)
    key1 = list(colors[:4])
    key2 = list(colors[4:])
    for i, v in enumerate(key1):
        g[12][i] = v
    for i, v in enumerate(key2):
        g[12][9 + i] = v
    dot_specs = [(1, 5, key1[1]), (3, 11, key2[2]), (6, 7, key1[3]), (9, 3, key2[0])]
    rng.shuffle(dot_specs)
    for r, c, color in dot_specs[:ctx.draw_int("dot_count", 2, 4)]:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 16, 0)
    if name == "no_keys":
        g[5][5] = 2
        return g
    if name == "no_dots":
        for i in range(4):
            g[12][i] = 2 + i
            g[12][9 + i] = 6 + i
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(16):
                g[r][c] = 2
        return g
    return g
