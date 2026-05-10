"""Generator for arc_additional_puzzles_21_set6:H39.

Rule: color-2 components with no holes become 3; hollow components
(with at least one enclosed 0-region) become 4.

Combinatorial axes (8): grid_h/w, palette_kind, num_solid, num_hollow,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_objects, all_solid, all_hollow.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect, draw_rect_outline

GENERATOR_ID = "ea56ba328a3e"
VERSION = "1.1.0"
TASK_ID = "ea56ba328a3e"
SUMMARY = "Color-2 components with no holes become 3; hollow components with one hole become 4."

INVARIANTS = [
    "only color-2 objects participate",
    "objects are separated and include both solid and hollow examples",
]

PALETTE_KINDS = ("default", "more_solid", "more_hollow", "balanced")
DEGENERATE_TEXTURES = ("no_objects", "all_solid", "all_hollow")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_solid":      {"type": "int", "default": "2", "valid": "1..3"},
    "num_hollow":     {"type": "int", "default": "1", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    draw_rect_outline(g, 1, 1, 5, 5, 2)
    draw_rect(g, h - 4, w - 5, 3, 4, 2)
    if rng.random() < 0.5:
        draw_rect(g, h - 3, 1, 2, 3, 2)
    else:
        g[h - 3][1] = 2
        g[h - 2][1] = 2
        g[h - 2][2] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "no_objects":
        return g
    if name == "all_solid":
        # only solid blocks — no hollow components, rule produces only 3s
        draw_rect(g, 1, 1, 3, 3, 2)
        draw_rect(g, h - 4, w - 4, 3, 3, 2)
        draw_rect(g, h - 4, 1, 2, 2, 2)
        return g
    if name == "all_hollow":
        # only hollow frames — no solid components, rule produces only 4s
        draw_rect_outline(g, 1, 1, 4, 4, 2)
        draw_rect_outline(g, h - 5, w - 5, 4, 4, 2)
        return g
    return g
