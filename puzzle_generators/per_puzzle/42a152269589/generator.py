"""Generator for b7cb93ac.

Rule: pack three separated 1x4 bars into the canonical 3x4 output.

Combinatorial axes (8): grid_h/w, layout_gap, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_bars, single_bar, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "42a152269589"
VERSION = "1.1.0"
TASK_ID = "42a152269589"
SUMMARY = "Three separated 1x4 bars exactly tile the canonical 3x4 output."

INVARIANTS = [
    "background is 0",
    "three disconnected color bars each have four cells",
    "the three bars have distinct colors and total area 12",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_bars", "single_bar", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "varied", "valid": "varied"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "layout_gap":     {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
        gap = ctx.draw_int("layout_gap", 1, 1)
    elif difficulty == "hard":
        gap = ctx.draw_int("layout_gap", 2, 2)
    else:
        gap = ctx.draw_int("layout_gap", 1, 2)
    colors = list(ctx.draw_distinct_colors("colors", n=3, exclude={0}))
    h = 3 + 2 * gap
    w = 12
    g = full_grid(h, w, 0)
    rows = [0, gap + 1, 2 * gap + 2]
    rng.shuffle(rows)
    for color, r in zip(colors, rows):
        c0 = rng.randint(0, w - 4)
        for dc in range(4):
            g[r][c0 + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 12, 0)
    if name == "no_bars":
        return g
    if name == "single_bar":
        for dc in range(4):
            g[2][4 + dc] = 3
        return g
    if name == "full_grid":
        for r in range(5):
            for c in range(12):
                g[r][c] = 3
        return g
    return g
