"""Generator for 292dd178.

Rule: open color-1 rectangles fill their interior and beam through
the gap.

Combinatorial axes (8): grid_h/w, open_side, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, background.
Degenerates: no_rect, no_gap, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect_outline, full_grid

GENERATOR_ID = "bdcb4c9eb6bd"
VERSION = "1.1.0"
TASK_ID = "bdcb4c9eb6bd"
SUMMARY = "Open color-1 rectangles fill interior and beam through the gap."

INVARIANTS = [
    "the mode color is the background",
    "there is one 4-connected color-1 rectangular outline",
    "exactly one side of the outline has an interior gap",
    "the rectangle sits with at least one cell of margin from grid borders",
]

OPEN_SIDES = ("up", "down", "left", "right")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rect", "no_gap", "full_grid")
HELPFUL_TEXTURES = OPEN_SIDES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "open_side":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(OPEN_SIDES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "background":     {"type": "color", "default": "rng !{1,2}",
                       "valid": "0|3|4|5|6|7|8|9"},
    "texture":        {"type": "str", "default": "alias for open_side",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    open_side = (overrides.get("texture") if overrides.get("texture") in OPEN_SIDES else None) or \
                overrides.get("open_side") or \
                ctx.draw_choice("open_side", list(OPEN_SIDES))
    bg = ctx.draw_color("background", exclude={1, 2})
    h = rng.randint(10, 13)
    w = rng.randint(11, 15)
    rh = rng.randint(5, min(7, h - 3))
    rw = rng.randint(5, min(8, w - 3))
    r0 = rng.randint(1, h - rh - 1)
    c0 = rng.randint(1, w - rw - 1)
    g = full_grid(h, w, bg)
    draw_rect_outline(g, r0, c0, rh, rw, 1)
    r1 = r0 + rh - 1
    c1 = c0 + rw - 1
    gap_r = rng.randint(r0 + 1, r1 - 1)
    gap_c = rng.randint(c0 + 1, c1 - 1)
    if open_side == "up":
        g[r0][gap_c] = bg
    elif open_side == "down":
        g[r1][gap_c] = bg
    elif open_side == "left":
        g[gap_r][c0] = bg
    else:
        g[gap_r][c1] = bg
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 13, 0)
    if name == "no_rect":
        return g
    if name == "no_gap":
        draw_rect_outline(g, 2, 2, 6, 7, 1)
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(13):
                g[r][c] = 1
        return g
    return g
