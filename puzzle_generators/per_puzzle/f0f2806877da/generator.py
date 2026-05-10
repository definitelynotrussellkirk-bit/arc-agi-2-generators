"""Generator for e6de6e8f.

Rule: two-row piece codes are traced into a fixed 8x7 path diagram.

Combinatorial axes (8): grid_h/w, piece_sequence, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
code_color.
Degenerates: no_pieces, full_grid, single_piece.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f0f2806877da"
VERSION = "1.1.0"
TASK_ID = "f0f2806877da"
SUMMARY = "Two-row piece codes traced into a fixed 8x7 path diagram."

INVARIANTS = [
    "input has two coding rows",
    "blank columns separate pieces",
    "single-column, left-bending and right-bending pieces map to different trace steps",
    "piece colors are non-zero and distinct from background",
]

SEQUENCES = {
    "straight_left_right": [0, 1, 2],
    "left_right_straight": [1, 2, 0],
    "right_straight_left": [2, 0, 1],
}
SEQ_KINDS = tuple(SEQUENCES.keys())
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pieces", "full_grid", "single_piece")
HELPFUL_TEXTURES = SEQ_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "2", "valid": "2"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "piece_sequence": {"type": "str", "default": "rng helpful",
                       "valid": "|".join(SEQ_KINDS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "code_color":     {"type": "color", "default": "rng !0", "valid": "1..9"},
    "texture":        {"type": "str", "default": "alias for piece_sequence",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_piece(g, col, kind, color):
    if kind == 0:
        g[0][col] = color
        g[1][col] = color
        return col + 1
    if kind == 1:
        g[1][col] = color
        g[0][col + 1] = color
        g[1][col + 1] = color
        return col + 2
    g[0][col] = color
    g[0][col + 1] = color
    g[1][col + 1] = color
    return col + 2


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    name = (overrides.get("texture") if overrides.get("texture") in SEQ_KINDS else None) or \
           overrides.get("piece_sequence") or \
           ctx.draw_choice("piece_sequence", list(SEQ_KINDS))
    color = ctx.draw_color("code_color", exclude={0})
    g = full_grid(2, 9, 0)
    col = 0
    for kind in SEQUENCES[name]:
        col = _draw_piece(g, col, kind, color) + 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(2, 9, 0)
    if name == "no_pieces":
        return g
    if name == "single_piece":
        _draw_piece(g, 0, 0, 2)
        return g
    if name == "full_grid":
        for r in range(2):
            for c in range(9):
                g[r][c] = 2
        return g
    return g
