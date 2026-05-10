"""Generator for arc_additional_puzzles_21_set15_bundle:H101.

Rule: row-0 commands (codes 1..6) transform the same lower motif and
pack the transformed copies horizontally.

Combinatorial axes (8): grid_h/w, palette_kind, command_count,
palette_size, position_bias, n_distinct_colors, motif_color, texture.
Degenerates: no_motif, no_commands, full_grid_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1e597464e3c7"
VERSION = "1.1.0"
TASK_ID = "1e597464e3c7"
SUMMARY = "Row-0 commands transform the same lower motif and pack the transformed copies."

INVARIANTS = [
    "row 0 contains a sequence of nonzero transform commands",
    "the motif is the cropped nonzero content below row 0",
    "each command transforms the motif and all transformed copies are packed horizontally",
]

PALETTE_KINDS = ("default", "wide_motif_color", "rainbow_command", "minimal")
DEGENERATE_TEXTURES = ("no_motif", "no_commands", "full_grid_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "7", "valid": "7"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "command_count":  {"type": "int", "default": "rng 2..4", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        command_count = ctx.draw_int("command_count", 2, 2)
    elif difficulty == "hard":
        command_count = ctx.draw_int("command_count", 3, 4)
    else:
        command_count = ctx.draw_int("command_count", 2, 4)
    color = ctx.draw_color("color", exclude={0, 1, 2, 3, 4, 5, 6})
    g = full_grid(7, 9, 0)
    commands = [1 + ((sample_index + i) % 6) for i in range(command_count)]
    for i, cmd in enumerate(commands):
        g[0][i] = cmd
    for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 1)]:
        g[2 + dr][2 + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 9, 0)
    if name == "no_motif":
        for i in range(3):
            g[0][i] = i + 1
        return g
    if name == "no_commands":
        for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 1)]:
            g[2 + dr][2 + dc] = 7
        return g
    if name == "full_grid_motif":
        for r in range(1, 7):
            for c in range(9):
                g[r][c] = 7
        g[0][0] = 1
        return g
    return g
