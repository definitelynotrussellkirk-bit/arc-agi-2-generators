"""Generator for arc_puzzle_bank_21_set20_s:S20_E2.

Every exact template match window is recolored to 8 at occupied cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, match_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_matches, no_template, single_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.panels import assemble_vertical_panels, paste

GENERATOR_ID = "d50ba3ef0962"
VERSION = "1.1.0"
TASK_ID = "d50ba3ef0962"
SUMMARY = "Every exact template match window is recolored to 8 at occupied cells."

INVARIANTS = [
    "divider color is 9",
    "template is a dense 3x3 pattern",
    "board contains isolated exact matches of the template",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_matches", "no_template", "single_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "derived", "valid": "13..26"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "match_count":    {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "7", "valid": "7..7"},
    "position_bias":  {"type": "str", "default": "9col_separated_template_board",
                       "valid": "9col_separated_template_board"},
    "n_distinct_colors": {"type": "int", "default": "7", "valid": "7..7"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

TEMPLATE = [[3, 4, 5], [6, 7, 8], [2, 3, 4]]


def _board(rng, h, w, count):
    grid = full_grid(h, w, 0)
    anchors = [(r, c) for r in range(h - 2) for c in range(w - 2)]
    rng.shuffle(anchors)
    used = set()
    placed = 0
    for r, c in anchors:
        footprint = {(rr, cc) for rr in range(r - 1, r + 4) for cc in range(c - 1, c + 4)}
        if footprint & used:
            continue
        paste(grid, TEMPLATE, r, c)
        used |= footprint
        placed += 1
        if placed >= count:
            break
    return grid


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("board_h", 8, 9)
        w = ctx.draw_int("board_w", 9, 10)
        count = ctx.draw_int("match_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("board_h", 10, 11)
        w = ctx.draw_int("board_w", 12, 13)
        count = ctx.draw_int("match_count", 3, 4)
    else:
        h = ctx.draw_int("board_h", 8, 11)
        w = ctx.draw_int("board_w", 9, 13)
        count = ctx.draw_int("match_count", 2, 4)
    rng = ctx.draw_rng("layout")
    template_panel = full_grid(h, 5, 0)
    paste(template_panel, TEMPLATE, 1, 1)
    return assemble_vertical_panels([template_panel, _board(rng, h, w, count)])


def _draw_from_degenerate(name, rng):
    h = 8
    if name == "no_matches":
        # template panel + blank board → no matches to recolor
        template_panel = full_grid(h, 5, 0)
        paste(template_panel, TEMPLATE, 1, 1)
        board = full_grid(h, 9, 0)
        return assemble_vertical_panels([template_panel, board])
    if name == "no_template":
        # board with matches but no template panel → nothing to compare against
        board = full_grid(h, 9, 0)
        paste(board, TEMPLATE, 2, 2)
        return board
    if name == "single_match":
        # template + 1 match only → trivial output, no contrast
        template_panel = full_grid(h, 5, 0)
        paste(template_panel, TEMPLATE, 1, 1)
        board = full_grid(h, 9, 0)
        paste(board, TEMPLATE, 2, 2)
        return assemble_vertical_panels([template_panel, board])
    return full_grid(h, 9, 0)
