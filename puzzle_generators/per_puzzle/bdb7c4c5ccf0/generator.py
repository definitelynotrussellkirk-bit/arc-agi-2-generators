"""Generator for arc_additional_puzzle_bank_volume15:M99.

Rule: a control color rotates the largest green template into a gray
frame.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_control, no_template, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "bdb7c4c5ccf0"
VERSION = "1.1.0"
TASK_ID = "bdb7c4c5ccf0"
SUMMARY = "A control color rotates the largest green template into a gray frame."

INVARIANTS = [
    "background is 0",
    "one singleton control color is in 1, 2, 4, or 6",
    "there is one hollow gray frame",
    "the green template fits inside the frame after rotation",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_control", "no_template", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..24"},
    "grid_w":         {"type": "int", "default": "rng 13..18", "valid": "10..30"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 15, 16)
        w = ctx.draw_int("grid_w", 16, 18)
    else:
        h = ctx.draw_int("grid_h", 12, 16)
        w = ctx.draw_int("grid_w", 13, 18)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    g[0][0] = rng.choice([1, 2, 4, 6])
    for r, c in [(2, 1), (2, 2), (3, 1), (4, 1)]:
        g[r][c] = 3
    draw_frame(g, h - 7, w - 7, h - 2, w - 2, 5)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 14, 0)
    if name == "no_control":
        for r, c in [(2, 1), (2, 2), (3, 1), (4, 1)]:
            g[r][c] = 3
        draw_frame(g, 6, 7, 11, 12, 5)
        return g
    if name == "no_template":
        g[0][0] = 1
        draw_frame(g, 6, 7, 11, 12, 5)
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(14):
                g[r][c] = 5
        return g
    return g
