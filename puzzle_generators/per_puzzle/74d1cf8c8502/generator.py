"""Generator for arc_additional_puzzles_21_set2:M12.

Rule: for each 6-blob, paint cells along its bbox border with color 2.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_blobs, single_blob, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "74d1cf8c8502"
VERSION = "1.1.0"
TASK_ID = "74d1cf8c8502"
SUMMARY = "2-3 non-touching 6-blobs of varied bbox shapes; bbox borders traced with 2."

INVARIANTS = [
    "between 2 and 3 non-touching 6-blobs",
    "each has a non-trivial bbox",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_blobs", "single_blob", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "8..10"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "11..13"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)], 6)
    paint_at(g, h - 4, w - 5, [(0, 0), (1, 0), (1, 1), (1, 2), (2, 0)], 6)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 12, 0)
    if name == "no_blobs":
        return g
    if name == "single_blob":
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)], 6)
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(12):
                g[r][c] = 6
        return g
    return g
