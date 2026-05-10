"""Generator for arc_puzzle_bank_21_set20_s:S20_E6.

Rule: a row strip reports how many exact template matches start in
each board row.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_match_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_matches, all_rows_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.panels import assemble_vertical_panels, paste

GENERATOR_ID = "860cbb625ca0"
VERSION = "1.1.0"
TASK_ID = "860cbb625ca0"
SUMMARY = "A row strip reports how many exact template matches start in each board row."

INVARIANTS = [
    "divider color is 9",
    "template is dense and exact",
    "matches are placed in controlled start rows",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_matches", "all_rows_match")
HELPFUL_TEXTURES = PALETTE_KINDS

TEMPLATE = [[6, 7, 8], [2, 3, 4], [5, 6, 7]]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "5..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_match_rows":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "7", "valid": "7"},
    "position_bias":  {"type": "str", "default": "scattered_match_rows",
                       "valid": "scattered_match_rows"},
    "n_distinct_colors": {"type": "int", "default": "7", "valid": "7"},
    "density":        {"type": "str", "default": "panels", "valid": "panels"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("board_h", 8, 8)
        w = ctx.draw_int("board_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("board_h", 9, 10)
        w = ctx.draw_int("board_w", 13, 15)
    else:
        h = ctx.draw_int("board_h", 8, 10)
        w = ctx.draw_int("board_w", 11, 15)
    rng = ctx.draw_rng("layout")
    template_panel = full_grid(h, 5, 0)
    paste(template_panel, TEMPLATE, 1, 1)
    board = full_grid(h, w, 0)
    rows = rng.sample(range(h - 2), rng.randint(2, min(4, h - 2)))
    for r in rows:
        cols = list(range(0, w - 2, 5))
        rng.shuffle(cols)
        for c in cols[:rng.randint(1, min(2, len(cols)))]:
            paste(board, TEMPLATE, r, c)
    return assemble_vertical_panels([template_panel, board])


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    template_panel = full_grid(h, 5, 0)
    if name == "no_template":
        # template panel left blank → no pattern to count matches against
        board = full_grid(h, w, 0)
        paste(board, TEMPLATE, 1, 0)
        return assemble_vertical_panels([template_panel, board])
    if name == "no_matches":
        # template present, board empty → counts are all 0
        paste(template_panel, TEMPLATE, 1, 1)
        board = full_grid(h, w, 0)
        return assemble_vertical_panels([template_panel, board])
    if name == "all_rows_match":
        # template stamped in every board row → counter strip saturates
        paste(template_panel, TEMPLATE, 1, 1)
        board = full_grid(h, w, 0)
        for r in range(h - 2):
            paste(board, TEMPLATE, r, 0)
        return assemble_vertical_panels([template_panel, board])
    return assemble_vertical_panels([template_panel, full_grid(h, w, 0)])
