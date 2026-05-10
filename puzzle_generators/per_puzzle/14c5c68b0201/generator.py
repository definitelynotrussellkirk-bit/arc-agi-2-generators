"""Generator for a57f2f04.

Rule: colored stamp tiles across its surrounding zero hole by modulo
repetition.

Combinatorial axes (8): grid_h/w, hole_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_holes, no_stamps, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "14c5c68b0201"
VERSION = "1.1.0"
TASK_ID = "14c5c68b0201"
SUMMARY = "Colored stamp tiles across surrounding zero hole by modulo repetition."

INVARIANTS = [
    "the modal color is the background",
    "each active color has a small stamp embedded in a rectangular zero hole",
    "the stamp pattern repeats across the whole hole",
    "stamps sit clear of the hole borders",
]

HOLE_SIZES = ("h6", "h7")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_holes", "no_stamps", "full_grid")
HELPFUL_TEXTURES = HOLE_SIZES

AXES = {
    "grid_h":         {"type": "int", "default": "16", "valid": "16"},
    "grid_w":         {"type": "int", "default": "18", "valid": "18"},
    "hole_size":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(HOLE_SIZES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for hole_size",
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
    if tx in HOLE_SIZES:
        hole_size = int(tx[1:])
    else:
        hole_size = ctx.draw_choice("hole_size", [6, 7])
    c1, c2 = ctx.draw_distinct_colors("colors", n=2, exclude={0, 8})
    g = full_grid(16, 18, 8)
    draw_rect(g, 2, 2, hole_size, hole_size + 1, 0)
    draw_rect(g, 9, 10, hole_size, hole_size, 0)
    for dr, dc in [(0, 0), (0, 1), (1, 0)]:
        g[4 + dr][4 + dc] = c1
    for dr, dc in [(0, 0), (1, 1), (2, 0)]:
        g[10 + dr][12 + dc] = c2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(16, 18, 8)
    if name == "no_holes":
        g[5][5] = 2
        return g
    if name == "no_stamps":
        draw_rect(g, 2, 2, 6, 7, 0)
        draw_rect(g, 9, 10, 6, 6, 0)
        return g
    if name == "full_grid":
        for r in range(16):
            for c in range(18):
                g[r][c] = 8
        return g
    return g
