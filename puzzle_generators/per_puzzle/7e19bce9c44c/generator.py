"""Generator for arc_additional_puzzles_21_set5:E35.

Rule: a nonzero object sits inside black padding; the rule outputs its
tight bounding-box crop.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_object, touches_border, two_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.blobs import grow_blob
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7e19bce9c44c"
VERSION = "1.1.0"
TASK_ID = "7e19bce9c44c"
SUMMARY = "A nonzero object sits inside black padding; the rule outputs its tight bounding-box crop."

INVARIANTS = [
    "nonzero content is away from the border",
    "background padding surrounds the content",
    "colors are preserved",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_object", "touches_border", "two_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_size":     {"type": "int", "default": "rng 5..10", "valid": "1..20"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "interior", "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "density":        {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 10)
        size = ctx.draw_int("shape_size", 4, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        size = ctx.draw_int("shape_size", 8, 10)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
        size = ctx.draw_int("shape_size", 5, 10)
    rng = ctx.draw_rng("layout")
    color = ctx.draw_color("shape_color", exclude={0})
    g = full_grid(h, w, 0)
    cells = grow_blob(rng, h - 4, w - 4, set(), size)
    if cells is None:
        cells = {(1, 1), (1, 2), (2, 1), (2, 2), (3, 2)}
    for r, c in cells:
        g[r + 2][c + 2] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_object":
        # empty grid — bbox is undefined
        return g
    if name == "touches_border":
        # object touching grid border → "padding around content" invariant fails
        for r, c in [(0, 0), (0, 1), (1, 0)]:
            g[r][c] = 4
        return g
    if name == "two_objects":
        # two separated objects → tight bbox spans both, includes empty space
        for r, c in [(2, 2), (2, 3), (3, 2)]:
            g[r][c] = 4
        for r, c in [(6, 6), (6, 7), (7, 7)]:
            g[r][c] = 4
        return g
    return g
