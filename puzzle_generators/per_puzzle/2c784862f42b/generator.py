"""Generator for arc_puzzle_bank_twentieth_21_bundle:hard_140_decode_transform_sequence_and_stamp_row.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape, sequence,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_prototype, no_sequence, no_target_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2c784862f42b"
VERSION = "1.1.0"
TASK_ID = "2c784862f42b"
SUMMARY = "Apply a four-step transform-code sequence to a prototype and recolor each stamped panel."

INVARIANTS = [
    "rows 0..4 contain a 5x5 prototype shape",
    "row 5 columns 0..3 contain transform codes",
    "row 5 column 4 contains the output color",
    "each code transforms the running prototype before it is recolored and appended to the output strip",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_prototype", "no_sequence", "no_target_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "6", "valid": "6..6"},
    "grid_w":         {"type": "int", "default": "5", "valid": "5..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape":          {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "sequence":       {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "5x5_prototype_plus_codes_row",
                       "valid": "5x5_prototype_plus_codes_row"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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

_SEQUENCES = [
    [1, 2, 4, 3],
    [4, 5, 1, 2],
    [0, 1, 3, 5],
    [2, 2, 4, 1],
    [5, 3, 1, 4],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        shape = ctx.draw_int("shape", 0, 1)
        sequence = ctx.draw_int("sequence", 0, 1)
    elif difficulty == "hard":
        shape = ctx.draw_int("shape", 2, 4)
        sequence = ctx.draw_int("sequence", 2, 4)
    else:
        shape = ctx.draw_int("shape", 0, len(_SHAPES) - 1)
        sequence = ctx.draw_int("sequence", 0, len(_SEQUENCES) - 1)
    source_color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    target_color = rng.choice([c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c != source_color])

    g = full_grid(6, 5, 0)
    for r, c in _SHAPES[shape]:
        g[r][c] = source_color
    for c, code in enumerate(_SEQUENCES[sequence]):
        g[5][c] = code
    g[5][4] = target_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 5, 0)
    if name == "no_prototype":
        # codes + target color but no prototype → nothing to transform
        for c, code in enumerate(_SEQUENCES[0]):
            g[5][c] = code
        g[5][4] = 5
        return g
    if name == "no_sequence":
        # prototype + target color but no transform codes → no operations defined
        for r, c in _SHAPES[0]: g[r][c] = 4
        g[5][4] = 5
        return g
    if name == "no_target_color":
        # prototype + codes but no target color → no recolor color defined
        for r, c in _SHAPES[0]: g[r][c] = 4
        for c, code in enumerate(_SEQUENCES[0]):
            g[5][c] = code
        return g
    return g
