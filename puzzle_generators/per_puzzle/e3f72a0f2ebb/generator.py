"""Generator for arc_puzzle_bank_21_set10_e:medium_j09.

Rule: for each object, paint its bbox border (rectangle outline) with
its color in fresh grid.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_blobs, single_blob, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "e3f72a0f2ebb"
VERSION = "1.1.0"
TASK_ID = "e3f72a0f2ebb"
SUMMARY = "2-3 distinct-color non-touching blobs."

INVARIANTS = [
    "between 2 and 3 non-touching blobs",
    "blobs use distinct colors",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_blobs", "single_blob", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = list(range(2, 10)); rng.shuffle(palette)
    paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 1)], palette[0])
    paint_at(g, h - 4, w - 4, [(0, 0), (1, 0), (1, 1), (2, 1)], palette[1])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 11, 0)
    if name == "no_blobs":
        return g
    if name == "single_blob":
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 1)], 3)
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(11):
                g[r][c] = 3
        return g
    return g
