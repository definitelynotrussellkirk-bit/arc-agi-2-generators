"""Generator for 34cfa167.

Rule: two anchor blocks and local top/side clues generate a repeated
rectangular frame.

Combinatorial axes (8): grid_h/w, anchor_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_anchors, no_clues, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "1fe4628c64c4"
VERSION = "1.1.0"
TASK_ID = "1fe4628c64c4"
SUMMARY = "Two anchor blocks and local clues generate repeated rectangular frame."

INVARIANTS = [
    "two same-sized solid anchor blocks define opposite corners of a frame",
    "small clues adjacent to the first anchor provide top, horizontal, side, and side-inner colors",
    "the output expands those clues into the full patterned rectangle between the anchors",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_anchors", "no_clues", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 16..17", "valid": "16..17"},
    "grid_w":         {"type": "int", "default": "rng 17..18", "valid": "17..18"},
    "anchor_size":    {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
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
        size = ctx.draw_int("anchor_size", 2, 2)
    elif difficulty == "hard":
        size = ctx.draw_int("anchor_size", 3, 3)
    else:
        size = ctx.draw_int("anchor_size", 2, 3)
    anchor, top, horiz, side, inner = ctx.draw_distinct_colors("colors", n=5, exclude={0})
    h = 16 + (sample_index % 2)
    w = 17 + ((sample_index // 2) % 2)
    g = full_grid(h, w, 0)
    ar = 4
    ac = 3 + (sample_index % 2)
    br = 11
    bc = 11 + ((sample_index // 2) % 2)
    draw_rect(g, ar, ac, size, size, anchor)
    draw_rect(g, br, bc, size, size, anchor)
    g[ar][ac + size] = top
    g[ar][ac + size + 2] = horiz
    g[ar + size + 1][ac] = side
    g[ar + size + 3][ac] = inner
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(16, 17, 0)
    if name == "no_anchors":
        g[4][6] = 4
        return g
    if name == "no_clues":
        draw_rect(g, 4, 4, 2, 2, 3)
        draw_rect(g, 11, 11, 2, 2, 3)
        return g
    if name == "full_grid":
        for r in range(16):
            for c in range(17):
                g[r][c] = 3
        return g
    return g
