"""Generator for arc_puzzle_bank_twelfth_21_bundle:hard_84_decode_sequence_of_transformed_library_shapes.

Rule: rows 0..2 hold sparse index/transform/color code columns; three 4x4
library panels start at row 4. Each program triple selects one panel + a
transform + a target color; output concatenates the transformed recolored
crops with one-cell gaps.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_program (rows 0..2 empty → no codes to decode);
no_library (panel area empty → rule's lookup returns nothing);
identity_transform (every transform code is 1 (identity) → output =
recolored panels unchanged).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "982c2905b543"
VERSION = "1.1.0"
TASK_ID = "982c2905b543"
SUMMARY = "Decode three indexed library shapes, transform each, recolor, and pack as a strip."

INVARIANTS = [
    "rows 0..2 hold sparse index, transform, and output-color code columns",
    "three 4x4 library panels start at row 4 and columns 0, 5, and 10",
    "each code column selects one panel, one transform, and one target color",
    "the output concatenates the transformed recolored crops with one-cell gaps",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_program", "no_library", "identity_transform")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "library":           {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "program":           {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 6..6", "valid": "6..6"},
    "position_bias":     {"type": "str", "default": "fixed_program_plus_library",
                          "valid": "fixed_program_plus_library"},
    "n_distinct_colors": {"type": "int", "default": "rng 6..6", "valid": "6..6"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_LIBRARIES = [
    [
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(0, 1), (1, 1), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    ],
    [
        [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1)],
        [(0, 2), (1, 0), (1, 1), (1, 2), (2, 0)],
        [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
    ],
    [
        [(0, 1), (1, 1), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
    ],
    [
        [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)],
        [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (3, 2)],
        [(0, 1), (1, 0), (1, 1), (2, 1), (3, 1)],
    ],
]

_PROGRAMS = [
    [(1, 1), (2, 2), (3, 3)],
    [(3, 4), (1, 5), (2, 3)],
    [(2, 1), (2, 4), (1, 2)],
    [(1, 5), (3, 1), (1, 4)],
    [(3, 3), (2, 2), (1, 1)],
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
    library = ctx.draw_int("library", 0, len(_LIBRARIES) - 1)
    program = ctx.draw_int("program", 0, len(_PROGRAMS) - 1)
    source_colors = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)
    output_colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)

    g = full_grid(8, 14, 0)
    for col, (idx, code), color in zip((0, 2, 4), _PROGRAMS[program], output_colors):
        g[0][col] = idx
        g[1][col] = code
        g[2][col] = color
    for left, cells, color in zip((0, 5, 10), _LIBRARIES[library], source_colors):
        _paint(g, 4, left, cells, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 14, 0)
    if name == "no_program":
        # Rows 0..2 empty — no codes to decode.
        for left, cells, color in zip((0, 5, 10), _LIBRARIES[0], [3, 4, 5]):
            _paint(g, 4, left, cells, color)
        return g
    if name == "no_library":
        # Library area empty — rule's lookup returns nothing.
        for col, (idx, code), color in zip((0, 2, 4), _PROGRAMS[0], [3, 4, 5]):
            g[0][col] = idx
            g[1][col] = code
            g[2][col] = color
        return g
    if name == "identity_transform":
        # All transform codes = 1 (identity).
        for col, idx, color in zip((0, 2, 4), [1, 2, 3], [3, 4, 5]):
            g[0][col] = idx
            g[1][col] = 1   # all identity
            g[2][col] = color
        for left, cells, color in zip((0, 5, 10), _LIBRARIES[0], [3, 4, 5]):
            _paint(g, 4, left, cells, color)
        return g
    return g
