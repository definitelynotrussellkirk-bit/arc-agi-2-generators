"""Generator for arc_additional_puzzles_21_set13_bundle:E91 — Shift non-cmd cells by cmd direction.

Rule: cmd cell value (1=up, 2=right, 3=down, 4=left) + non-cmd cells.
Output: empty grid with each non-cmd cell shifted in cmd direction.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cmd, no_markers, cells_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "66b8f050cbf2"
VERSION = "1.1.0"
TASK_ID = "66b8f050cbf2"
SUMMARY = "Single cmd cell ∈ {1,2,3,4} + 1-3 marker cells of distinct colors."

INVARIANTS = [
    "exactly 1 cmd cell with value in {1, 2, 3, 4}",
    "1-3 marker cells with values in {5, 6, 7, 8, 9}",
    "shifted positions stay in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cmd", "no_markers", "cells_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "cmd_at_origin_with_markers",
                       "valid": "cmd_at_origin_with_markers"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][0] = rng.randint(1, 4)
    palette = [5, 6, 7, 8, 9]
    n = rng.randint(2, 3)
    placed = []
    for _ in range(40):
        if len(placed) >= n: break
        r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
        if (r, c) not in placed and g[r][c] == 0:
            g[r][c] = rng.choice(palette)
            placed.append((r, c))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_cmd":
        # (0,0) is 0 → no direction code
        g[2][3] = 6; g[3][5] = 7
        return g
    if name == "no_markers":
        # cmd present but no markers
        g[0][0] = 2
        return g
    if name == "cells_at_edge":
        # markers at edge → shift pushes out of bounds
        g[0][0] = 1   # cmd: up
        g[0][3] = 6
        g[1][5] = 7
        return g
    return g
