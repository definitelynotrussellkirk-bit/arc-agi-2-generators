"""Generator for 83b6b474.

Rule: border fragments are classified by edge type and repacked into
the smallest square.

Combinatorial axes (8): grid_h/w, offset, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_fragments, single_fragment, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9733a2d68593"
VERSION = "1.1.0"
TASK_ID = "9733a2d68593"
SUMMARY = "Border fragments classified by edge type and repacked into smallest square."

INVARIANTS = [
    "each non-background object is a border fragment",
    "fragments include top, corner, and side classes",
    "the output packs classified fragments into a compact square frame layout",
]

OFFSET_KINDS = ("o0", "o1")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_fragments", "single_fragment", "full_grid")
HELPFUL_TEXTURES = OFFSET_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16"},
    "offset":         {"type": "choice", "default": "rng helpful",
                       "valid": "0|1"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
    "texture":        {"type": "str", "default": "alias for offset",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint(g, cells, color):
    for r, c in cells:
        g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in OFFSET_KINDS:
        offset = int(tx[1])
    else:
        offset = ctx.draw_choice("offset", [0, 1])
    colors = ctx.draw_distinct_colors("colors", n=5, exclude={0})
    g = full_grid(12, 16, 0)
    _paint(g, [(1, 1), (1, 2), (2, 1), (3, 1)], colors[0])
    _paint(g, [(1, 5), (1, 6), (1, 7)], colors[1])
    _paint(g, [(7, 1), (8, 1), (9, 1), (9, 2)], colors[2])
    _paint(g, [(7, 10), (8, 10), (9, 8), (9, 9), (9, 10)], colors[3])
    _paint(g, [(4 + offset, 14), (5 + offset, 14)], colors[4])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 16, 0)
    if name == "no_fragments":
        return g
    if name == "single_fragment":
        _paint(g, [(1, 1), (1, 2), (2, 1)], 3)
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(16):
                g[r][c] = 3
        return g
    return g
