"""Generator for arc_puzzle_bank_fifteenth_21_bundle:hard_105_select_by_key_and_apply_transform_sequence.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape, sequence,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_sequence, no_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "98e86aae9095"
VERSION = "1.1.0"
TASK_ID = "98e86aae9095"
SUMMARY = "Select the keyed object and apply the top-row transform-code sequence."

INVARIANTS = [
    "top-row nonzero cells are transform sequence codes in 1..4",
    "the bottom-left cell gives the selected object color",
    "there is one largest component of the selected color",
    "other nonzero components use different colors and are ignored",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_sequence", "no_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8..8"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape":          {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "sequence":       {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "header_seq_plus_keyed_shape",
                       "valid": "header_seq_plus_keyed_shape"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
]
_SEQS = [
    [1, 2],
    [2, 3],
    [4, 1, 2],
    [3, 2, 4],
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
        shape_idx = ctx.draw_int("shape", 0, 1)
        seq_idx = ctx.draw_int("sequence", 0, 1)
    elif difficulty == "hard":
        shape_idx = ctx.draw_int("shape", 2, 3)
        seq_idx = ctx.draw_int("sequence", 2, 3)
    else:
        shape_idx = ctx.draw_int("shape", 0, len(_SHAPES) - 1)
        seq_idx = ctx.draw_int("sequence", 0, len(_SEQS) - 1)
    key = rng.choice([5, 6, 7, 8, 9])
    other = rng.choice([c for c in [2, 3, 4, 5, 6, 7, 8, 9] if c != key])
    g = full_grid(8, 10, 0)
    for c, code in enumerate(_SEQS[seq_idx]):
        g[0][c] = code
    _paint(g, 2, 2, _SHAPES[shape_idx], key)
    _paint(g, 5, 7, [(0, 0), (1, 0)], other)
    g[7][0] = key
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 10, 0)
    if name == "no_key":
        # transform sequence + shape but no bottom-left key → no selection color
        for c, code in enumerate(_SEQS[0]):
            g[0][c] = code
        _paint(g, 2, 2, _SHAPES[0], 5)
        _paint(g, 5, 7, [(0, 0), (1, 0)], 6)
        return g
    if name == "no_sequence":
        # key + shape but no transform sequence → no operation defined
        _paint(g, 2, 2, _SHAPES[0], 5)
        _paint(g, 5, 7, [(0, 0), (1, 0)], 6)
        g[7][0] = 5
        return g
    if name == "no_shape":
        # sequence + key but no shape of key color → nothing to transform
        for c, code in enumerate(_SEQS[0]):
            g[0][c] = code
        _paint(g, 5, 7, [(0, 0), (1, 0)], 6)
        g[7][0] = 5
        return g
    return g
