"""Generator for arc_puzzle_bank_seventh_21_bundle:hard_44_template_tiling_from_code_grid.

Rule: framed monochrome templates form a dictionary; expand a compact
code grid into tiled output by replacing each code cell with its template.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_library, no_codes, code_not_in_library.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "b1fcb840c8ab"
VERSION = "1.1.0"
TASK_ID = "b1fcb840c8ab"
SUMMARY = "Use framed monochrome templates as a dictionary and expand a compact code grid into tiled output."

INVARIANTS = [
    "color-1 frames contain same-sized monochrome template interiors",
    "the template color is also its code value",
    "a separate compact code grid contains only template code colors",
    "the output replaces every code cell with the corresponding template tile",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_library", "no_codes", "code_not_in_library")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "library":        {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "code_grid":      {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "framed_library_with_code",
                       "valid": "framed_library_with_code"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TEMPLATES = [
    [
        [(0, 0), (1, 0), (2, 0)],
        [(0, 0), (0, 1), (0, 2), (1, 1)],
        [(0, 2), (1, 1), (2, 0)],
    ],
    [
        [(0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    ],
    [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 1), (1, 1), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (0, 1), (0, 2), (1, 2)],
    ],
    [
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(0, 2), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (0, 1), (1, 1), (2, 1)],
    ],
]

_CODES = [
    [[2, 3, 4], [4, 2, 3]],
    [[3, 2], [4, 3], [2, 4]],
    [[4, 4, 2], [3, 2, 3]],
    [[2, 4], [3, 2]],
    [[3, 4, 2], [2, 3, 4], [4, 2, 3]],
]


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    library = ctx.draw_int("library", 0, len(_TEMPLATES) - 1)
    if difficulty == "easy":
        code_grid = ctx.draw_int("code_grid", 3, 3)
    elif difficulty == "hard":
        code_grid = ctx.draw_int("code_grid", 4, 4)
    else:
        code_grid = ctx.draw_int("code_grid", 0, len(_CODES) - 1)

    g = full_grid(12, 17, 0)
    for idx, (left, color) in enumerate(zip((0, 6, 12), (2, 3, 4))):
        draw_frame(g, 0, left, 4, left + 4, 1)
        _paint(g, 1, left + 1, _TEMPLATES[library][idx], color)

    codes = _CODES[code_grid]
    top = 7
    left = 1
    for r, row in enumerate(codes):
        for c, value in enumerate(row):
            g[top + r][left + c] = value
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 17, 0)
    if name == "no_library":
        # Code grid present but no framed templates above —
        # rule's lookup has no entries; expand undefined.
        codes = _CODES[0]
        for r, row in enumerate(codes):
            for c, value in enumerate(row):
                g[7 + r][1 + c] = value
        return g
    if name == "no_codes":
        # Library present but no code grid below — rule has no
        # codes to expand; output empty.
        for idx, (left, color) in enumerate(zip((0, 6, 12), (2, 3, 4))):
            draw_frame(g, 0, left, 4, left + 4, 1)
            _paint(g, 1, left + 1, _TEMPLATES[0][idx], color)
        return g
    if name == "code_not_in_library":
        # Code grid uses colors not in the library — rule's
        # lookup misses; expand undefined for those cells.
        for idx, (left, color) in enumerate(zip((0, 6, 12), (2, 3, 4))):
            draw_frame(g, 0, left, 4, left + 4, 1)
            _paint(g, 1, left + 1, _TEMPLATES[0][idx], color)
        for r, row in enumerate([[6, 7, 8], [7, 6, 8]]):
            for c, value in enumerate(row):
                g[7 + r][1 + c] = value
        return g
    return g
