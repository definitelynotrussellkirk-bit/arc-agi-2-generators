"""Generator for arc_additional_puzzles_21_set21_bundle:H147.

Rule: command at (0, 0) plus a row-wise color remap (rows 0/1, cols 2+)
specify a transformation; the object below row 1 is remapped, then
transformed by the command.

Combinatorial axes (8): grid_h/w, palette_kind, command, motif_anchor,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_command, no_remap_pairs, no_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8ef6f191186d"
VERSION = "1.1.0"
TASK_ID = "8ef6f191186d"
SUMMARY = "A command cell transforms a cropped object after a row-wise color remapping."

INVARIANTS = [
    "cell (0,0) is the geometric command",
    "rows 0 and 1 after column 2 define source-to-target color pairs",
    "the object below row 1 is remapped and then transformed by the command",
]

PALETTE_KINDS = ("default", "warm_remap", "cool_remap", "rainbow_remap")
DEGENERATE_TEXTURES = ("no_command", "no_remap_pairs", "no_object")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "command":        {"type": "int", "default": "rng 2..6", "valid": "2..6"},
    "motif_anchor":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        command = ctx.draw_int("command", 2, 3)
    elif difficulty == "hard":
        command = ctx.draw_int("command", 5, 6)
    else:
        command = ctx.draw_int("command", 2, 6)
    src_a, src_b, dst_a, dst_b = ctx.draw_distinct_colors("colors", n=4, exclude={0})
    g = full_grid(8, 9, 0)
    g[0][0] = command
    g[0][2] = src_a
    g[0][3] = src_b
    g[1][2] = dst_a
    g[1][3] = dst_b
    r0 = 3
    c0 = 2 + (sample_index % 2)
    for dr, dc, color in [(0, 0, src_a), (1, 0, src_a), (1, 1, src_b), (2, 1, src_a)]:
        g[r0 + dr][c0 + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 9, 0)
    if name == "no_command":
        # remap pairs and motif but no command — transformation undefined
        g[0][2] = 4; g[0][3] = 5
        g[1][2] = 6; g[1][3] = 7
        for dr, dc, color in [(0, 0, 4), (1, 0, 4), (1, 1, 5), (2, 1, 4)]:
            g[3 + dr][2 + dc] = color
        return g
    if name == "no_remap_pairs":
        # command and motif but no remap header — colors don't change
        g[0][0] = 2
        for dr, dc, color in [(0, 0, 4), (1, 0, 4), (1, 1, 5), (2, 1, 4)]:
            g[3 + dr][2 + dc] = color
        return g
    if name == "no_object":
        # command + remap header but no object below — rule has nothing to transform
        g[0][0] = 2
        g[0][2] = 4; g[0][3] = 5
        g[1][2] = 6; g[1][3] = 7
        return g
    return g
