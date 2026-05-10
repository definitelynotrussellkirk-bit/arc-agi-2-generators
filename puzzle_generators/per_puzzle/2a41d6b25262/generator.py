"""Generator for arc_puzzle_bank_21_set15:S15_M5.

Rule: two template shapes are combined by normalized XOR and stamped at
a blue marker.

Combinatorial axes (8): grid_h, grid_w, palette_kind, variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, single_template, identical_templates.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "2a41d6b25262"
VERSION = "1.1.0"
TASK_ID = "2a41d6b25262"
SUMMARY = "Two template shapes are combined by normalized XOR and stamped at a blue marker."

INVARIANTS = [
    "background is 0",
    "there is exactly one color-2 template object and one color-3 template object",
    "the two template objects have overlapping but non-identical normalized supports",
    "there is exactly one color-1 marker with room for the XOR footprint",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "single_template", "identical_templates")
HELPFUL_TEXTURES = PALETTE_KINDS

A1 = [(0, 0), (1, 0), (1, 1), (2, 1)]
A2 = [(0, 0), (0, 1), (1, 1), (2, 1)]
B1 = [(0, 0), (0, 1), (1, 1), (1, 2)]
B2 = [(0, 1), (1, 0), (1, 1), (1, 2)]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 15..18", "valid": "13..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "variant":        {"type": "enum", "default": "rng a|b", "valid": "a|b"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "templates_top_marker_bottom",
                       "valid": "templates_top_marker_bottom"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 12, 12)
        w = ctx.draw_int("width", 15, 16)
        variant = ctx.draw_choice("variant", ["a"])
    elif difficulty == "hard":
        h = ctx.draw_int("height", 13, 15)
        w = ctx.draw_int("width", 16, 18)
        variant = ctx.draw_choice("variant", ["b"])
    else:
        h = ctx.draw_int("height", 12, 15)
        w = ctx.draw_int("width", 15, 18)
        variant = ctx.draw_choice("variant", ["a", "b"])
    g = full_grid(h, w, 0)

    s1, s2 = (A1, A2) if variant == "a" else (B1, B2)
    paint_at(g, 1, 1, s1, 2)
    paint_at(g, 1, 6, s2, 3)
    g[h - 5][w - 5] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 16
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # templates without color-1 marker → no stamp position
        paint_at(g, 1, 1, A1, 2)
        paint_at(g, 1, 6, A2, 3)
        return g
    if name == "single_template":
        # only one template → XOR is undefined (no second operand)
        paint_at(g, 1, 1, A1, 2)
        g[h - 5][w - 5] = 1
        return g
    if name == "identical_templates":
        # both templates are identical → normalized XOR is empty
        paint_at(g, 1, 1, A1, 2)
        paint_at(g, 1, 6, A1, 3)
        g[h - 5][w - 5] = 1
        return g
    return g
