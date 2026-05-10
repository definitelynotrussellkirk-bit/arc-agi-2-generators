"""Generator for arc_puzzle_bank_21_set20_s:S20_E1.

Exact 3x3 template matches are marked at their centers.

Combinatorial axes (8): grid_h, grid_w, palette_kind, match_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_matches, single_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.panels import assemble_vertical_panels, paste

GENERATOR_ID = "fd9ad93c2cc8"
VERSION = "1.1.0"
TASK_ID = "fd9ad93c2cc8"
SUMMARY = "Exact 3x3 template matches are marked at their centers."

INVARIANTS = [
    "divider color is 9",
    "left panel contains the template",
    "right panel contains isolated exact template matches",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_matches", "single_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "derived", "valid": "13..28"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "match_count":    {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "7", "valid": "7..7"},
    "position_bias":  {"type": "str", "default": "9col_template_then_board",
                       "valid": "9col_template_then_board"},
    "n_distinct_colors": {"type": "int", "default": "7", "valid": "7..7"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

TEMPLATE = [[2, 3, 4], [5, 6, 7], [8, 2, 3]]


def _place_matches(rng, h, w, count):
    board = full_grid(h, w, 0)
    anchors = [(r, c) for r in range(0, h - 2) for c in range(0, w - 2)]
    rng.shuffle(anchors)
    used: set[tuple[int, int]] = set()
    placed = 0
    for r, c in anchors:
        footprint = {(rr, cc) for rr in range(r - 1, r + 4) for cc in range(c - 1, c + 4)}
        if footprint & used:
            continue
        paste(board, TEMPLATE, r, c)
        used |= footprint
        placed += 1
        if placed >= count:
            break
    return board


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
    board = _place_matches(rng, h, w, count)
    return assemble_vertical_panels([template_panel, board])


def _draw_from_degenerate(name, rng):
    h = 8
    if name == "no_template":
        # board with matches but no template panel → no shape to compare against
        board = full_grid(h, 9, 0)
        paste(board, TEMPLATE, 2, 2)
        return board
    if name == "no_matches":
        # template + empty board → no match centers to mark
        template_panel = full_grid(h, 5, 0)
        paste(template_panel, TEMPLATE, 1, 1)
        board = full_grid(h, 9, 0)
        return assemble_vertical_panels([template_panel, board])
    if name == "single_match":
        # template + 1 match → trivial output, no contrast
        template_panel = full_grid(h, 5, 0)
        paste(template_panel, TEMPLATE, 1, 1)
        board = full_grid(h, 9, 0)
        paste(board, TEMPLATE, 2, 2)
        return assemble_vertical_panels([template_panel, board])
    return full_grid(h, 9, 0)
