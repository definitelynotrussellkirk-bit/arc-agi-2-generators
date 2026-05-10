"""Generator for arc_puzzle_bank_nineteenth_21_bundle:hard_128_decode_prototype_library_with_transform_and_recolor_codes.

Decode three index/transform/color triples from a 3x3 prototype library.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: empty_program (row 4 empty → rule's per-triple loop is
empty, output collapses), all_identity (all transform codes = 1 →
rule's transform stage is invisible), out_of_range_index (index > 3
→ rule's library lookup fails, output undefined for that step).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4a5e76e7a1af"
VERSION = "1.1.0"
TASK_ID = "4a5e76e7a1af"
SUMMARY = "Decode three index/transform/color triples from a 3x3 prototype library."

INVARIANTS = [
    "the first three rows contain three 3x3 prototypes with one blank column between panels",
    "row 4 contains three code triples at columns 0, 4, and 8",
    "each triple encodes prototype index, transform code, and output color",
    "the output is the three transformed and recolored panels packed into a strip",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_program", "all_identity", "out_of_range_index")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "library":        {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "program":        {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "library_plus_program",
                       "valid": "library_plus_program"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "fixed_layout", "valid": "fixed_layout"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_LIBRARIES = [
    [
        [[1, 0, 0], [1, 1, 1], [0, 0, 1]],
        [[0, 2, 0], [2, 2, 2], [0, 2, 0]],
        [[3, 3, 0], [0, 3, 0], [0, 3, 3]],
    ],
    [
        [[4, 0, 4], [4, 4, 0], [0, 4, 0]],
        [[5, 5, 0], [0, 5, 0], [0, 5, 5]],
        [[0, 6, 0], [6, 6, 0], [0, 6, 6]],
    ],
    [
        [[7, 0, 0], [7, 7, 0], [0, 7, 7]],
        [[0, 8, 8], [8, 8, 0], [0, 8, 0]],
        [[9, 9, 9], [0, 9, 0], [0, 9, 0]],
    ],
    [
        [[2, 2, 0], [0, 2, 2], [0, 0, 2]],
        [[0, 3, 0], [3, 3, 3], [3, 0, 0]],
        [[4, 0, 0], [4, 4, 4], [0, 0, 4]],
    ],
]

_PROGRAMS = [
    [(1, 1), (2, 2), (3, 3)],
    [(3, 4), (1, 2), (2, 3)],
    [(2, 1), (2, 4), (1, 3)],
    [(1, 4), (3, 1), (1, 2)],
    [(3, 3), (2, 2), (1, 1)],
]


def _paste(g, panel, top, left):
    for r, row in enumerate(panel):
        for c, value in enumerate(row):
            g[top + r][left + c] = value


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    library = ctx.draw_int("library", 0, len(_LIBRARIES) - 1)
    program = ctx.draw_int("program", 0, len(_PROGRAMS) - 1)
    output_colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)

    g = full_grid(5, 11, 0)
    for left, panel in zip((0, 4, 8), _LIBRARIES[library]):
        _paste(g, panel, 0, left)
    for left, (idx, code), color in zip((0, 4, 8), _PROGRAMS[program], output_colors):
        g[4][left] = idx
        g[4][left + 1] = code
        g[4][left + 2] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 11, 0)
    for left, panel in zip((0, 4, 8), _LIBRARIES[0]):
        _paste(g, panel, 0, left)
    if name == "empty_program":
        # Row 4 empty — rule's per-triple loop is empty; output
        # has no panels to pack.
        return g
    if name == "all_identity":
        # All transform codes = 1 (identity) — rule's transform
        # stage is invisible; output equals selected panels.
        for left, idx in zip((0, 4, 8), (1, 2, 3)):
            g[4][left] = idx
            g[4][left + 1] = 1
            g[4][left + 2] = 5
        return g
    if name == "out_of_range_index":
        # Index 5 — rule's library lookup fails (only 3 panels);
        # output undefined for that step.
        for left, (idx, code, color) in zip((0, 4, 8), [(5, 1, 4), (1, 2, 6), (2, 3, 7)]):
            g[4][left] = idx
            g[4][left + 1] = code
            g[4][left + 2] = color
        return g
    return g
