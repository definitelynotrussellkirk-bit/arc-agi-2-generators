"""Generator for arc_puzzle_bank_sixteenth_21_bundle:hard_111_decode_library_sequence_into_strip.

Combinatorial axes (8): library, sequence, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_library, no_sequence, mismatched_indices.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "724578f159f2"
VERSION = "1.1.0"
TASK_ID = "724578f159f2"
SUMMARY = "Read four index/transform pairs and stamp transformed 3x3 library panels into a strip."

INVARIANTS = [
    "three 3x3 library panels occupy columns 0..2, 4..6, and 8..10",
    "row 4 contains four one-based panel indexes paired with transform codes",
    "transform codes use the seven-code dihedral/transpose vocabulary",
    "the output is a 3x15 strip with one blank column between decoded panels",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_library", "no_sequence", "mismatched_indices")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "library":        {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "sequence":       {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "library_panels_then_sequence",
                       "valid": "library_panels_then_sequence"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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

_SEQUENCES = [
    [(1, 1), (2, 2), (3, 3), (1, 4)],
    [(3, 5), (1, 6), (2, 7), (3, 2)],
    [(2, 4), (2, 1), (1, 5), (3, 6)],
    [(1, 7), (3, 3), (2, 2), (1, 6)],
    [(2, 5), (1, 3), (3, 1), (2, 4)],
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
    if difficulty == "easy":
        library = ctx.draw_int("library", 0, 1)
        sequence = ctx.draw_int("sequence", 0, 1)
    elif difficulty == "hard":
        library = ctx.draw_int("library", 2, 3)
        sequence = ctx.draw_int("sequence", 2, 4)
    else:
        library = ctx.draw_int("library", 0, len(_LIBRARIES) - 1)
        sequence = ctx.draw_int("sequence", 0, len(_SEQUENCES) - 1)

    g = full_grid(5, 11, 0)
    for left, panel in zip((0, 4, 8), _LIBRARIES[library]):
        _paste(g, panel, 0, left)
    for left, (index, code) in zip((0, 3, 6, 9), _SEQUENCES[sequence]):
        g[4][left] = index
        g[4][left + 1] = code
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 11, 0)
    if name == "no_library":
        # Library panels empty — rule has no source motifs to stamp.
        for left, (index, code) in zip((0, 3, 6, 9), _SEQUENCES[0]):
            g[4][left] = index
            g[4][left + 1] = code
        return g
    if name == "no_sequence":
        # Library present but sequence row empty — rule has no decode plan.
        for left, panel in zip((0, 4, 8), _LIBRARIES[0]):
            _paste(g, panel, 0, left)
        return g
    if name == "mismatched_indices":
        # Sequence indices reference non-existent panels (e.g., index 5).
        for left, panel in zip((0, 4, 8), _LIBRARIES[0]):
            _paste(g, panel, 0, left)
        for left, (index, code) in zip((0, 3, 6, 9), [(5, 1), (6, 2), (7, 3), (4, 4)]):
            g[4][left] = index
            g[4][left + 1] = code
        return g
    return g
