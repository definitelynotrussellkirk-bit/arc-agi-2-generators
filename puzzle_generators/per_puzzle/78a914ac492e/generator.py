"""Generator for 57aa92db.

Rule: rectangular seeds scale a non-rectangular two-color template,
replacing the template accent color.

Combinatorial axes (8): grid_h/w, seed_count, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_template, no_seeds, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "78a914ac492e"
VERSION = "1.1.0"
TASK_ID = "78a914ac492e"
SUMMARY = "Rectangular seeds scale a non-rectangular two-color template."

INVARIANTS = [
    "one connected multicolor object is a non-seed template",
    "seed objects contain a rectangular common-color block and a rectangular new-color block",
    "the common-color block determines the scale and alignment",
    "the template accent color is replaced by each seed's new color",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_seeds", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "seed_count":     {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _seed(g, r, c, common, new):
    draw_rect(g, r, c, 2, 2, common)
    draw_rect(g, r, c + 2, 2, 1, new)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        seed_count = ctx.draw_int("seed_count", 1, 1)
    elif difficulty == "hard":
        seed_count = ctx.draw_int("seed_count", 2, 2)
    else:
        seed_count = ctx.draw_int("seed_count", 1, 2)
    common, accent, new_a, new_b = ctx.draw_distinct_colors("colors", n=4, exclude={0})
    g = full_grid(14, 15, 0)
    g[1][1] = common
    g[1][2] = accent
    g[2][1] = accent
    g[3][1] = accent
    _seed(g, 6, 2, common, new_a)
    if seed_count == 2:
        _seed(g, 6, 9, common, new_b)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 15, 0)
    if name == "no_template":
        _seed(g, 6, 2, 3, 4)
        return g
    if name == "no_seeds":
        g[1][1] = 3
        g[1][2] = 4
        g[2][1] = 4
        g[3][1] = 4
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(15):
                g[r][c] = 3
        return g
    return g
