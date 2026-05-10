"""Generator for arc_additional_puzzles_21_set9:H58.

Copy a framed source motif into target frames using local transform command cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, motif,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_motif, no_targets, no_codes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "ffc1598119d4"
VERSION = "1.1.0"
TASK_ID = "ffc1598119d4"
SUMMARY = "Copy a framed source motif into target frames using local transform command cells."

INVARIANTS = [
    "there is one color-9 source frame containing a nonempty motif",
    "there are two color-8 target frames with empty interiors",
    "each target frame has a command cell above its left border",
    "commands map to identity, rotate 90, rotate 180, or horizontal flip",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motif", "no_targets", "no_codes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12..12"},
    "grid_w":         {"type": "int", "default": "19", "valid": "19..19"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif":          {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "fixed_3frame_layout",
                       "valid": "fixed_3frame_layout"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_MOTIFS = [
    [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 2)],
    [(0, 0), (0, 2), (1, 0), (1, 1), (2, 1)],
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
        motif_idx = ctx.draw_int("motif", 0, 0)
    elif difficulty == "hard":
        motif_idx = ctx.draw_int("motif", 0, len(_MOTIFS) - 1)
    else:
        motif_idx = ctx.draw_int("motif", 0, len(_MOTIFS) - 1)
    code_a = ctx.draw_int("code_a", 1, 4)
    code_b = ctx.draw_int("code_b", 1, 4)
    motif_color = rng.choice([2, 3, 4, 5, 6, 7])

    g = full_grid(12, 19, 0)
    draw_frame(g, 2, 1, 6, 5, 9)
    draw_frame(g, 2, 7, 6, 11, 8)
    draw_frame(g, 2, 13, 6, 17, 8)
    g[1][7] = code_a
    g[1][13] = code_b
    _paint(g, 3, 2, _MOTIFS[motif_idx], motif_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 19, 0)
    if name == "no_motif":
        # source frame empty → no template to copy into targets
        draw_frame(g, 2, 1, 6, 5, 9)
        draw_frame(g, 2, 7, 6, 11, 8)
        draw_frame(g, 2, 13, 6, 17, 8)
        g[1][7] = 1; g[1][13] = 2
        return g
    if name == "no_targets":
        # only source frame with motif → nowhere to copy to
        draw_frame(g, 2, 1, 6, 5, 9)
        _paint(g, 3, 2, _MOTIFS[0], 4)
        return g
    if name == "no_codes":
        # framed motif + targets but no command cells → no transform dispatch
        draw_frame(g, 2, 1, 6, 5, 9)
        draw_frame(g, 2, 7, 6, 11, 8)
        draw_frame(g, 2, 13, 6, 17, 8)
        _paint(g, 3, 2, _MOTIFS[0], 4)
        return g
    return g
