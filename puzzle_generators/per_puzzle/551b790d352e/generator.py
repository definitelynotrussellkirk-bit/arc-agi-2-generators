"""Generator for arc_puzzle_bank_thirteenth_21_bundle:hard_85_decode_library_shape_transform_and_recolor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, selector,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_library, no_command_row, selector_not_in_library.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "551b790d352e"
VERSION = "1.1.0"
TASK_ID = "551b790d352e"
SUMMARY = "Select a colored library panel, transform its crop, and recolor it to a commanded output color."

INVARIANTS = [
    "the top five rows contain three five-column library panels at offsets 0, 6, and 12",
    "each library panel has a distinct nonzero selector color",
    "row 6 contains selector color, transform code, and output color",
    "the output is the selected crop transformed and recolored",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_library", "no_command_row", "selector_not_in_library")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "7", "valid": "7..7"},
    "grid_w":         {"type": "int", "default": "17", "valid": "17..17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "selector":       {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "3library_panels_with_command_row",
                       "valid": "3library_panels_with_command_row"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 2)],
]


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        selector = ctx.draw_int("selector", 0, 0)
        transform = ctx.draw_int("transform", 1, 2)
    elif difficulty == "hard":
        selector = ctx.draw_int("selector", 0, 2)
        transform = ctx.draw_int("transform", 1, 5)
    else:
        selector = ctx.draw_int("selector", 0, 2)
        transform = ctx.draw_int("transform", 1, 5)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7], 3)
    out_color = rng.choice([c for c in [2, 3, 4, 5, 6, 7, 8, 9] if c not in colors])
    g = full_grid(7, 17, 0)
    for idx, cells in enumerate(_SHAPES):
        _paint(g, 1, idx * 6 + 1, cells, colors[idx])
    g[6][0] = colors[selector]
    g[6][1] = transform
    g[6][2] = out_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 17, 0)
    if name == "no_library":
        # command row but no library panels → no shapes to select
        g[6][0] = 4; g[6][1] = 1; g[6][2] = 7
        return g
    if name == "no_command_row":
        # library panels but no row 6 commands → no selector/transform/recolor
        for idx, cells in enumerate(_SHAPES):
            _paint(g, 1, idx * 6 + 1, cells, [2, 3, 4][idx])
        return g
    if name == "selector_not_in_library":
        # selector color absent from library → no panel matches
        for idx, cells in enumerate(_SHAPES):
            _paint(g, 1, idx * 6 + 1, cells, [2, 3, 4][idx])
        g[6][0] = 9  # not 2/3/4 → no match
        g[6][1] = 1
        g[6][2] = 7
        return g
    return g
