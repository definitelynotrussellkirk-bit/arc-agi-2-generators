"""Generator for arc_additional_puzzle_bank_volume10:E67.

Rule: blue components touching only the top border are recolored green.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_components,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_top_only, all_top_only, no_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "4bf462ff34fb"
VERSION = "1.1.0"
TASK_ID = "4bf462ff34fb"
SUMMARY = "Blue components touching only the top border are recolored green."

INVARIANTS = [
    "background is 0",
    "at least one blue component touches row 0 and no other border",
    "other blue components touch another border or are fully interior",
    "blue components are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_top_only", "all_top_only", "no_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 7..12", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_components":   {"type": "int", "default": "rng 3..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "border_mix", "valid": "border_mix"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 7, 12)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    top_c = rng.randint(2, w - 3)
    draw_rect(g, 0, top_c, 2, 1, 1)
    bottom_c = rng.randint(1, w - 3)
    draw_rect(g, h - 2, bottom_c, 2, 1, 1)
    side_r = rng.randint(3, h - 4)
    draw_rect(g, side_r, 0, 2, 1, 1)
    if w > 7 and h > 7:
        g[h // 2][w // 2] = 1
        g[h // 2][w // 2 + 1] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_top_only":
        # no blue component touches row 0 only → no recolor target
        draw_rect(g, h - 2, 2, 2, 1, 1)
        draw_rect(g, 3, 0, 2, 1, 1)
        return g
    if name == "all_top_only":
        # every blue component touches only the top → entire blue mask becomes green
        draw_rect(g, 0, 1, 2, 1, 1)
        draw_rect(g, 0, 4, 2, 1, 1)
        draw_rect(g, 0, 7, 2, 1, 1)
        return g
    if name == "no_components":
        # empty grid → nothing to filter or recolor
        return g
    return g
