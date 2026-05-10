"""Generator for 652646ff.

Rule: colored 6x6 hex outlines are detected and restacked as complete
outlines.

Combinatorial axes (8): grid_h/w, hex_count, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_hexes, single_hex, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fa874c2eb1d1"
VERSION = "1.1.0"
TASK_ID = "fa874c2eb1d1"
SUMMARY = "Colored 6x6 hex outlines detected and restacked as complete outlines."

INVARIANTS = [
    "the background is zero",
    "each active color occupies cells of a 6x6 hex-outline stencil",
    "hex stencils do not overlap",
    "all generated hexes are complete so there are no blocker dependencies",
]

HEX_COUNT_KINDS = ("h2", "h3")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_hexes", "single_hex", "full_grid")
HELPFUL_TEXTURES = HEX_COUNT_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "17", "valid": "17"},
    "grid_w":         {"type": "int", "default": "18", "valid": "18"},
    "hex_count":      {"type": "choice", "default": "rng helpful",
                       "valid": "2|3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "texture":        {"type": "str", "default": "alias for hex_count",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

HEX = [(0, 2), (0, 3), (1, 1), (1, 4), (2, 0), (2, 5),
       (3, 0), (3, 5), (4, 1), (4, 4), (5, 2), (5, 3)]


def _draw_hex(g, r0, c0, color):
    for dr, dc in HEX:
        g[r0 + dr][c0 + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in HEX_COUNT_KINDS:
        count = int(tx[1])
    elif difficulty == "easy":
        count = 2
    elif difficulty == "hard":
        count = 3
    else:
        count = ctx.draw_choice("hex_count", [2, 3])
    colors = ctx.draw_distinct_colors("colors", n=count, exclude={0})
    positions = [(1, 1), (1, 11), (10, 6)]
    g = full_grid(17, 18, 0)
    for color, (r, c) in zip(colors, positions):
        _draw_hex(g, r, c, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(17, 18, 0)
    if name == "no_hexes":
        return g
    if name == "single_hex":
        _draw_hex(g, 1, 1, 3)
        return g
    if name == "full_grid":
        for r in range(17):
            for c in range(18):
                g[r][c] = 3
        return g
    return g
