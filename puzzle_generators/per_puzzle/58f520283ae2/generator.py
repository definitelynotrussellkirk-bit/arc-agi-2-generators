"""Generator for arc_additional_puzzles_21_set14_bundle:M94.

Rule: command at (0, 0) selects identity, rotations, transpose, or
flips for the cropped object.

Combinatorial axes (8): grid_h, grid_w, palette_kind, cmd,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_command, no_motif, square_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "58f520283ae2"
VERSION = "1.1.0"
TASK_ID = "58f520283ae2"
SUMMARY = "Command at (0,0) selects identity, rotations, transpose, or flips for the cropped object."

INVARIANTS = [
    "command cell is separate from the motif",
    "motif has a non-square bounding box so transforms are visible",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_command", "no_motif", "square_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cmd":            {"type": "int", "default": "rng 1..7", "valid": "1..7"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "command_top_left",
                       "valid": "command_top_left"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


MOTIFS = (
    ((0, 0, 4), (0, 1, 4), (1, 1, 5), (2, 1, 5)),
    ((0, 2, 6), (1, 0, 7), (1, 1, 7), (1, 2, 6)),
)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
    cmd = ctx.draw_int("cmd", 1, 7)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][0] = cmd
    top = rng.randint(2, h - 4)
    left = rng.randint(2, w - 4)
    for dr, dc, color in rng.choice(MOTIFS):
        g[top + dr][left + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "missing_command":
        # cell (0,0) is bg → no transform code, action undefined
        for dr, dc, color in MOTIFS[0]:
            g[3 + dr][4 + dc] = color
        return g
    if name == "no_motif":
        # command present but no motif → nothing to transform
        g[0][0] = 3
        return g
    if name == "square_motif":
        # motif's bbox is square → cw / transpose / 180 may produce identical results
        g[0][0] = 4
        for dr in range(3):
            for dc in range(3):
                if (dr + dc) % 2 == 0:
                    g[3 + dr][4 + dc] = 6
        return g
    return g
