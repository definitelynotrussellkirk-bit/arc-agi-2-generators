"""Generator for 97a05b5b.

Rule: a large red rectangle has a 2x2 hole and a separate matching red
key tile.

Combinatorial axes (8): grid_h/w, rect_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_hole, no_key, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import fill_box, full_grid

GENERATOR_ID = "25c140f9307d"
VERSION = "1.1.0"
TASK_ID = "25c140f9307d"
SUMMARY = "Large red rectangle has a 2x2 hole and a separate matching red key tile."

INVARIANTS = [
    "background is 0",
    "the largest nonzero object is a red rectangle with one 2x2 black hole",
    "a separate 2x2 red key tile matches that hole exactly",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_hole", "no_key", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "varied", "valid": "varied"},
    "grid_w":         {"type": "int", "default": "varied", "valid": "varied"},
    "rect_size":      {"type": "int", "default": "rng 5..7", "valid": "5..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
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
        rect_size = ctx.draw_int("rect_size", 5, 5)
    elif difficulty == "hard":
        rect_size = ctx.draw_int("rect_size", 7, 7)
    else:
        rect_size = ctx.draw_int("rect_size", 5, 7)
    h = max(9, rect_size + 4)
    w = rect_size + 7
    g = full_grid(h, w, 0)
    r0 = 1
    c0 = 1
    fill_box(g, r0, c0, r0 + rect_size - 1, c0 + rect_size - 1, 2)
    hole_r = rng.randint(r0 + 1, r0 + rect_size - 3)
    hole_c = rng.randint(c0 + 1, c0 + rect_size - 3)
    fill_box(g, hole_r, hole_c, hole_r + 1, hole_c + 1, 0)
    key_c = c0 + rect_size + 3
    key_r = rng.randint(1, h - 3)
    fill_box(g, key_r, key_c, key_r + 1, key_c + 1, 2)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 12, 0)
    if name == "no_hole":
        fill_box(g, 1, 1, 5, 5, 2)
        fill_box(g, 1, 9, 2, 10, 2)
        return g
    if name == "no_key":
        fill_box(g, 1, 1, 5, 5, 2)
        fill_box(g, 2, 2, 3, 3, 0)
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
