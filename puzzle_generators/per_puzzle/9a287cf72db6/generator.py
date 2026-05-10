"""Generator for arc_puzzle_bank_eighteenth_21_bundle:hard_121_decode_library_with_transform_codes.

Use index and transform rows to decode a sequence of 4x4 library panels.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: empty_program (no codes in rows 5-6 → rule's per-step
output is empty, no panels packed), all_identity (all transform codes
are identity → rule's transform stage is invisible, output equals
selected panels), out_of_range_index (index > 3 → rule's library
lookup fails; output undefined).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9a287cf72db6"
VERSION = "1.1.0"
TASK_ID = "9a287cf72db6"
SUMMARY = "Use index and transform rows to decode a sequence of 4x4 library panels."

INVARIANTS = [
    "the first four rows contain three 4x4 prototype panels separated by one blank column",
    "row 5 lists one-based prototype indexes at sparse code positions",
    "row 6 lists transform codes at the same positions",
    "the output is the selected transformed panels packed left-to-right with one-cell gaps",
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
        [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
        [(0, 1), (0, 2), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2), (2, 1)],
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
    [(1, 1), (2, 2), (3, 3), (1, 4)],
    [(3, 2), (1, 3), (2, 4)],
    [(2, 1), (2, 3), (3, 4), (1, 2)],
    [(1, 4), (3, 1), (1, 2), (2, 3)],
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
    colors = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)

    g = full_grid(7, 14, 0)
    for left, cells, color in zip((0, 5, 10), _LIBRARIES[library], colors):
        _paint(g, 0, left, cells, color)

    for c, (index, code) in zip((0, 2, 6, 10), _PROGRAMS[program]):
        g[5][c] = index
        g[6][c] = code
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 14, 0)
    library = 0
    for left, cells, color in zip((0, 5, 10), _LIBRARIES[library], (2, 3, 4)):
        _paint(g, 0, left, cells, color)
    if name == "empty_program":
        # Rows 5-6 empty — rule's per-step output loop is empty;
        # no panels are packed.
        return g
    if name == "all_identity":
        # All transform codes are 1 (identity) — rule's transform
        # stage is invisible; output equals selected panels.
        for c, idx in zip((0, 2, 6, 10), (1, 2, 3, 1)):
            g[5][c] = idx
            g[6][c] = 1
        return g
    if name == "out_of_range_index":
        # Index 5 — rule's library lookup fails (only 3 panels);
        # output undefined for that step.
        for c, (idx, code) in zip((0, 2, 6, 10), [(5, 1), (1, 2), (5, 3), (2, 1)]):
            g[5][c] = idx
            g[6][c] = code
        return g
    return g
