"""Generator for arc_puzzle_bank_twentieth_21_bundle:hard_139_build_cross_product_gallery_of_color_and_transform_codes.

Combinatorial axes (8): shape, transforms, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_proto, no_codes, no_colors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1282792eaad1"
VERSION = "1.1.0"
TASK_ID = "1282792eaad1"
SUMMARY = "Build a color-by-transform cross-product gallery from one prototype and two code rows."

INVARIANTS = [
    "rows 0..4 contain a single 5x5 prototype",
    "row 5 columns 0..2 contain transform codes",
    "row 6 columns 0..2 contain output colors",
    "the output grid is the Cartesian product of colors by transformed prototype panels",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_proto", "no_codes", "no_colors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "shape":          {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "transforms":     {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "4", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "header_proto_codes_colors",
                       "valid": "header_proto_codes_colors"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(1, 1), (2, 1), (3, 1), (3, 2)],
    [(1, 1), (1, 2), (2, 2), (3, 2), (3, 3)],
    [(1, 1), (2, 1), (2, 2), (2, 3), (3, 3)],
    [(1, 2), (2, 0), (2, 1), (2, 2), (3, 0)],
    [(0, 1), (1, 1), (2, 1), (2, 2), (3, 2)],
]

_TRANSFORM_ROWS = [
    [0, 1, 4],
    [2, 3, 5],
    [1, 2, 3],
    [4, 0, 5],
    [5, 1, 2],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        shape = ctx.draw_int("shape", 0, 1)
        transforms = ctx.draw_int("transforms", 0, 1)
    elif difficulty == "hard":
        shape = ctx.draw_int("shape", 2, 4)
        transforms = ctx.draw_int("transforms", 2, 4)
    else:
        shape = ctx.draw_int("shape", 0, len(_SHAPES) - 1)
        transforms = ctx.draw_int("transforms", 0, len(_TRANSFORM_ROWS) - 1)
    source_color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    output_colors = rng.sample([c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c != source_color], 3)

    g = full_grid(7, 5, 0)
    for r, c in _SHAPES[shape]:
        g[r][c] = source_color
    for c, code in enumerate(_TRANSFORM_ROWS[transforms]):
        g[5][c] = code
    for c, color in enumerate(output_colors):
        g[6][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 5, 0)
    if name == "no_proto":
        # Rows 0..4 empty — rule has no prototype to transform.
        for c, code in enumerate([1, 2, 3]): g[5][c] = code
        for c, color in enumerate([4, 5, 6]): g[6][c] = color
        return g
    if name == "no_codes":
        # Row 5 empty — rule has no transforms to apply.
        for r, c in _SHAPES[0]: g[r][c] = 8
        for c, color in enumerate([4, 5, 6]): g[6][c] = color
        return g
    if name == "no_colors":
        # Row 6 empty — rule has no output palette to recolor with.
        for r, c in _SHAPES[0]: g[r][c] = 8
        for c, code in enumerate([1, 2, 3]): g[5][c] = code
        return g
    return g
