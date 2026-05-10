"""Generator for arc_additional_puzzles_21_set15_bundle:M105.

Rule: bottom-row commands recolor copies of the cropped motif,
concatenated with one blank column between.

Combinatorial axes (8): grid_h, grid_w, palette_kind, commands,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_motif, no_commands, single_command.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "18e652e005b1"
VERSION = "1.1.0"
TASK_ID = "18e652e005b1"
SUMMARY = "Bottom-row commands recolor copies of the cropped motif, concatenated with one blank column between."

INVARIANTS = [
    "the motif lies above the final command row",
    "the last row contains at least two nonzero command colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motif", "no_commands", "single_command")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "commands":       {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "motif_top_commands_bottom",
                       "valid": "motif_top_commands_bottom"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        n = ctx.draw_int("commands", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 12)
        n = ctx.draw_int("commands", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        n = ctx.draw_int("commands", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    motif = [(0, 0), (0, 1), (1, 1), (2, 0)]
    top = rng.randint(1, h - 5)
    left = rng.randint(1, w - 4)
    for dr, dc in motif:
        g[top + dr][left + dc] = rng.choice([2, 3, 4])
    colors = list(ctx.draw_distinct_colors("cmd_colors", n=n, exclude=[0]))
    for i, color in enumerate(colors):
        g[h - 1][i] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_motif":
        # commands but no motif above → rule has nothing to copy
        for i, color in enumerate([4, 6, 7]):
            g[h - 1][i] = color
        return g
    if name == "no_commands":
        # motif but no command row → rule has no recolor instructions
        motif = [(0, 0), (0, 1), (1, 1), (2, 0)]
        for dr, dc in motif:
            g[2 + dr][2 + dc] = 3
        return g
    if name == "single_command":
        # one command → only one motif copy, invariant says ≥2
        motif = [(0, 0), (0, 1), (1, 1), (2, 0)]
        for dr, dc in motif:
            g[2 + dr][2 + dc] = 3
        g[h - 1][0] = 4
        return g
    return g
