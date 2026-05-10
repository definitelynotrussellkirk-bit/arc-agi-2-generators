"""Generator for arc_puzzle_bank_nineteenth21:M132 — mirror colored shape across 9-anchor.

Rule: a 9-cell anchors a point reflection. The colored shape is
reflected through the 9 (cell at (r, c) → (2*9.r - r, 2*9.c - c))
and the reflection is added; original shape stays.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, no_shape, reflection_oob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "b1972482cb43"
VERSION = "1.1.0"
TASK_ID = "b1972482cb43"
SUMMARY = "9-anchor + colored shape (2-4 cells) on one side."

INVARIANTS = [
    "background is 0",
    "exactly one 9-cell (the reflection center)",
    "exactly one connected colored shape (2-4 cells), not touching the 9",
    "the shape's reflection through the 9 stays in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_shape", "reflection_oob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "shape_then_anchor_offset",
                       "valid": "shape_then_anchor_offset"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 1), (1, 0), (1, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 13)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 6, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    color = rng.choice(list(random_palette(rng, 4, exclude={9})))
    shape = rng.choice(_SHAPES)
    sh = max(c[0] for c in shape) + 1
    sw = max(c[1] for c in shape) + 1
    sr = rng.randint(0, max(0, h // 2 - sh))
    sc = rng.randint(0, max(0, w // 2 - sw))
    paint_at(g, sr, sc, shape, color)
    nine_r = sr + sh + rng.randint(0, max(0, (h - sr - sh) // 2 - 1))
    nine_c = sc + sw + rng.randint(0, max(0, (w - sc - sw) // 2 - 1))
    if 0 <= nine_r < h and 0 <= nine_c < w and g[nine_r][nine_c] == 0:
        g[nine_r][nine_c] = 9
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # Shape but no 9-cell — rule has no center to reflect through.
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 3)
        return g
    if name == "no_shape":
        # 9-anchor but no colored shape — rule has nothing to reflect.
        g[3][4] = 9
        return g
    if name == "reflection_oob":
        # Shape and anchor both placed, but reflection lands entirely
        # off-grid — rule's reflected cells have no in-bounds target.
        paint_at(g, 0, 0, [(0, 0), (0, 1), (1, 0)], 4)
        g[1][1] = 9
        return g
    return g
