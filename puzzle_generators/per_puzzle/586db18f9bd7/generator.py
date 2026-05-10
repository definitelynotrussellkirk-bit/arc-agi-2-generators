"""Generator for 20b:hard_134 — decode library + transform + border codes.

Rule: row 0 cols 0..3 carry (panel-index, transform-code, fill-color,
border-color); rows 1..5 hold three 5x5 library panels separated by
blank columns. Output: selected panel cropped, transformed, recolored
with fill, then wrapped in a 1-cell border of border-color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: header_zero (command/index codes are 0 → may select a
non-existent slot or no-op transform), fill_equals_border (rule's
border highlight collapses into the fill — output looks blank inside),
empty_panel (selected panel has no cells → cropped object is empty,
border wraps a 0x0 region).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "586db18f9bd7"
VERSION = "1.1.0"
TASK_ID = "586db18f9bd7"

SUMMARY = "Select a library panel, transform and recolor its crop, then wrap it in a requested border color."

INVARIANTS = [
    "row 0 columns 0..3 encode panel index, transform code, fill color, and border color",
    "rows 1..5 contain three 5x5 library panels separated by one blank column",
    "the selected panel is crop-normalized before transformation",
    "the output is the recolored transformed object with a one-cell rectangular border",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("header_zero", "fill_equals_border", "empty_panel")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "library":        {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "command":        {"type": "int", "default": "rng 0..5", "valid": "0..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "5", "valid": "4..6"},
    "position_bias":  {"type": "str", "default": "header_plus_3panel_library",
                       "valid": "header_plus_3panel_library"},
    "n_distinct_colors": {"type": "int", "default": "5..6", "valid": "4..7"},
    "density":        {"type": "str", "default": "fixed_layout", "valid": "fixed_layout"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
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
        command = ctx.draw_int("command", 0, 2)
    elif difficulty == "hard":
        library = ctx.draw_int("library", 0, len(_LIBRARIES) - 1)
        command = ctx.draw_int("command", 0, 5)
    else:
        library = ctx.draw_int("library", 0, len(_LIBRARIES) - 1)
        command = ctx.draw_int("command", 0, 5)
    index = 1 + (command % 3)
    fill_color, border_color = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 2)
    source_colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)

    g = full_grid(6, 17, 0)
    g[0][0] = index
    g[0][1] = command
    g[0][2] = fill_color
    g[0][3] = border_color
    for left, cells, color in zip((0, 6, 12), _LIBRARIES[library], source_colors):
        _paint(g, 1, left + 1, cells, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 17, 0)
    library = 0
    if name == "header_zero":
        # All header codes are 0 → rule's "select panel index"
        # branch addresses slot 0 which is the header itself (or
        # otherwise undefined); transform code 0 is no-op.
        g[0][0] = 0; g[0][1] = 0; g[0][2] = 0; g[0][3] = 0
        for left, cells, color in zip((0, 6, 12), _LIBRARIES[library], (1, 2, 3)):
            _paint(g, 1, left + 1, cells, color)
        return g
    if name == "fill_equals_border":
        # Fill color and border color match → rule's border-highlight
        # branch produces no visual contrast; the rectangle is one
        # solid block of fill.
        g[0][0] = 1; g[0][1] = 0; g[0][2] = 5; g[0][3] = 5
        for left, cells, color in zip((0, 6, 12), _LIBRARIES[library], (1, 2, 3)):
            _paint(g, 1, left + 1, cells, color)
        return g
    if name == "empty_panel":
        # Panel index points at a slot whose cells we omit → rule's
        # crop step extracts an empty object, transform is identity
        # on emptiness, border wraps zero content.
        g[0][0] = 2; g[0][1] = 1; g[0][2] = 4; g[0][3] = 7
        # Only place panels for slots 1 and 3.
        for left, cells, color in zip((0, 12), (_LIBRARIES[library][0], _LIBRARIES[library][2]), (1, 3)):
            _paint(g, 1, left + 1, cells, color)
        return g
    return g
