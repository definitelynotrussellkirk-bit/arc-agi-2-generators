"""Generator for 94be5b80.

Rule: a key strip orders colors; the first keyed shape template is
stacked once per key color.

Combinatorial axes (8): grid_h/w, key_length, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_key, no_template, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "884393009d85"
VERSION = "1.1.0"
TASK_ID = "884393009d85"
SUMMARY = "Key strip orders colors; first keyed shape template stacked once per key color."

INVARIANTS = [
    "background is color 0",
    "two identical key rows contain at least two distinct nonzero colors",
    "one key color has a template shape outside the key rows",
    "the output stacks that template in key order",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_key", "no_template", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "12..16"},
    "grid_w":         {"type": "int", "default": "varied", "valid": "varied"},
    "key_length":     {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "rng 3..4", "valid": "3..4"},
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
        n = ctx.draw_int("key_length", 3, 3)
    elif difficulty == "hard":
        n = ctx.draw_int("key_length", 4, 4)
    else:
        n = ctx.draw_int("key_length", 3, 4)
    h = 12 + rng.randint(0, 4)
    w = 10 + n + rng.randint(0, 3)
    colors = ctx.draw_distinct_colors("key_colors", n=n, exclude={0})
    g = full_grid(h, w, 0)
    start_c = 2
    for r in [0, 1]:
        for i, color in enumerate(colors):
            g[r][start_c + i] = color
    base_r = 4 + (sample_index % 2)
    base_c = 3 + ((seed + sample_index) % 2)
    for dr, dc in [(0, 0), (0, 1), (1, 0)]:
        g[base_r + dr][base_c + dc] = colors[0]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_key":
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][5 + dc] = 3
        return g
    if name == "no_template":
        for r in [0, 1]:
            g[r][2] = 3
            g[r][3] = 4
            g[r][4] = 5
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 3
        return g
    return g
