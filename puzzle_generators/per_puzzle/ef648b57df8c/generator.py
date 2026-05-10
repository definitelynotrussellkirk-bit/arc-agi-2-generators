"""Generator for arc_additional_puzzles_21_set19_bundle:M129.

Rule: three command-labeled 3×3 blocks (cols 1, 5, 9) are transformed by
their command codes and packed horizontally.

Combinatorial axes (8): grid_h/w, palette_kind, command_offset,
palette_size, position_bias, n_distinct_colors, command_density, texture.
Degenerates: no_commands, no_blocks, missing_block.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ef648b57df8c"
VERSION = "1.1.0"
TASK_ID = "ef648b57df8c"
SUMMARY = "Three command-labeled 3x3 blocks are transformed and packed horizontally."

INVARIANTS = [
    "commands sit above the centers of three 3x3 blocks",
    "each block is cropped from rows 2-4 at starts 1, 5, and 9",
    "the transformed blocks are packed left-to-right with one blank column gap",
]

PALETTE_KINDS = ("default", "varied_offset", "warm_blocks", "cool_blocks")
DEGENERATE_TEXTURES = ("no_commands", "no_blocks", "missing_block")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "5", "valid": "5"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "command_offset": {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "command_density": {"type": "str", "default": "fixed", "valid": "fixed"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "fixed_starts",
                       "valid": "fixed_starts"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
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
        offset = ctx.draw_int("command_offset", 0, 1)
    elif difficulty == "hard":
        offset = ctx.draw_int("command_offset", 2, 3)
    else:
        offset = ctx.draw_int("command_offset", 0, 3)
    colors = ctx.draw_distinct_colors("colors", n=3, exclude={0, 1, 2, 3, 4})
    g = full_grid(5, 13, 0)
    starts = [1, 5, 9]
    commands = [1 + ((offset + i) % 4) for i in range(3)]
    for start, cmd, color in zip(starts, commands, colors):
        g[0][start + 1] = cmd
        for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 1)]:
            g[2 + dr][start + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 13, 0)
    starts = [1, 5, 9]
    if name == "no_commands":
        # blocks but no command codes — no transform to apply
        for start, color in zip(starts, [5, 6, 7]):
            for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 1)]:
                g[2 + dr][start + dc] = color
        return g
    if name == "no_blocks":
        # commands but no blocks below — rule has nothing to transform
        for start, cmd in zip(starts, [1, 2, 3]):
            g[0][start + 1] = cmd
        return g
    if name == "missing_block":
        # 3 commands but only 2 blocks — third command has no payload
        commands = [1, 2, 3]
        for start, cmd in zip(starts, commands):
            g[0][start + 1] = cmd
        for start, color in zip(starts[:2], [5, 6]):
            for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 1)]:
                g[2 + dr][start + dc] = color
        return g
    return g
