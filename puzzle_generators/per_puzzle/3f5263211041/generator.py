"""Generator for arc_puzzle_bank_ninth_21_bundle:hard_62_library_select_transform_gallery.

Combinatorial axes (8): library, program, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_library, no_program, mismatched_keys.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "3f5263211041"
VERSION = "1.1.0"
TASK_ID = "3f5263211041"
SUMMARY = "Use framed library shapes, selector keys, and transform codes to build a decoded gallery strip."

INVARIANTS = [
    "three color-9 library frames sit above the two code rows",
    "a key marker above each frame identifies that framed shape",
    "the penultimate row lists selector keys from the library",
    "the final row lists transform commands 5=id, 6=quarter-turn, and 7=horizontal flip",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_library", "no_program", "mismatched_keys")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "library":        {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "program":        {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "5", "valid": "4..6"},
    "position_bias":  {"type": "str", "default": "library_top_program_bottom",
                       "valid": "library_top_program_bottom"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "4..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_LIBRARIES = [
    [
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
    ],
    [
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
        [(0, 0), (0, 1), (1, 1), (2, 1)],
    ],
    [
        [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (1, 1), (2, 0), (2, 1)],
        [(0, 2), (1, 0), (1, 1), (1, 2), (2, 0)],
    ],
    [
        [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
]

_PROGRAMS = [
    [(0, 5), (1, 6), (2, 7)],
    [(2, 6), (0, 7), (1, 5)],
    [(1, 7), (1, 6), (0, 5)],
    [(0, 6), (2, 5), (0, 7)],
    [(2, 7), (1, 5), (2, 6)],
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
        library = ctx.draw_int("library", 0, 1)
        program = ctx.draw_int("program", 0, 1)
    elif difficulty == "hard":
        library = ctx.draw_int("library", 2, 3)
        program = ctx.draw_int("program", 2, 4)
    else:
        library = ctx.draw_int("library", 0, len(_LIBRARIES) - 1)
        program = ctx.draw_int("program", 0, len(_PROGRAMS) - 1)
    keys = rng.sample([2, 3, 4, 5, 6, 7, 8], 3)

    g = full_grid(15, 21, 0)
    for idx, (left, cells, key) in enumerate(zip((1, 8, 15), _LIBRARIES[library], keys)):
        draw_frame(g, 1, left, 6, left + 4, 9)
        g[0][left + 2] = key
        _paint(g, 2, left + 1, cells, idx + 1)

    for left, (selector_idx, code) in zip((10, 13, 17), _PROGRAMS[program]):
        g[13][left] = keys[selector_idx]
        g[14][left] = code
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 21, 0)
    if name == "no_library":
        # Frames empty — rule has no shapes to select from.
        for left, (selector_idx, code) in zip((10, 13, 17), _PROGRAMS[0]):
            g[13][left] = 5; g[14][left] = code
        return g
    if name == "no_program":
        # Library present but program rows empty — rule has no decode plan.
        keys = [2, 3, 4]
        for idx, (left, cells, key) in enumerate(zip((1, 8, 15), _LIBRARIES[0], keys)):
            draw_frame(g, 1, left, 6, left + 4, 9)
            g[0][left + 2] = key
            _paint(g, 2, left + 1, cells, idx + 1)
        return g
    if name == "mismatched_keys":
        # Selectors reference keys that don't appear in library — rule selects nothing.
        keys = [2, 3, 4]
        for idx, (left, cells, key) in enumerate(zip((1, 8, 15), _LIBRARIES[0], keys)):
            draw_frame(g, 1, left, 6, left + 4, 9)
            g[0][left + 2] = key
            _paint(g, 2, left + 1, cells, idx + 1)
        for left in (10, 13, 17):
            g[13][left] = 9  # not in keys [2,3,4]
            g[14][left] = 5
        return g
    return g
