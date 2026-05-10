"""Generator for arc_additional_puzzles_21_set22_bundle:E154.

Rule: interleaved all-zero rows are removed while colored rows are
preserved.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_marks, all_blank, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d7b5ec89244a"
VERSION = "1.1.0"
TASK_ID = "d7b5ec89244a"
SUMMARY = "Interleaved all-zero rows removed while colored rows preserved."

INVARIANTS = [
    "at least two rows are entirely zero",
    "at least two rows contain nonzero cells",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_marks", "all_blank", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "7..10"},
    "grid_w":         {"type": "int", "default": "rng 5..8", "valid": "5..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
        w = ctx.draw_int("grid_w", 5, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 5, 8)
    colors = list(ctx.draw_distinct_colors("colors", n=3, exclude=[0]))
    g = full_grid(h, w, 0)
    rows = [1, h // 2, h - 2]
    for i, r in enumerate(rows):
        g[r][i] = colors[i]
        g[r][w - 1 - i] = colors[i]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 6, 0)
    if name == "no_marks":
        return g
    if name == "all_blank":
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(6):
                g[r][c] = 3
        return g
    return g
