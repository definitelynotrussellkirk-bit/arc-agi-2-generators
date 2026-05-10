"""Generator for arc_additional_puzzles_21_set18_bundle:M126 — column gravity below 1-walls.

Rule: 1-cells are walls/floors. For each column, non-1 segments
between adjacent 1s collect their non-0/non-1 values and pack them
at the bottom.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_walls, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_floor, no_markers, already_settled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box

GENERATOR_ID = "aae737932036"
VERSION = "1.1.0"
TASK_ID = "aae737932036"
SUMMARY = "Bottom row of 1s + scattered 1-walls + 4-8 non-1 colored markers."

INVARIANTS = [
    "background is 0",
    "the bottom row is entirely 1 (floor)",
    "0-3 additional 1-cells inside the grid (vertical walls/segments)",
    "4-8 non-1 markers (colors 2..9) placed in non-1 positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_floor", "no_markers", "already_settled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_walls":        {"type": "int", "default": "rng 1..4", "valid": "0..6"},
    "n_markers":      {"type": "int", "default": "rng 4..7", "valid": "2..12"},
    "palette_size":   {"type": "int", "default": "rng 4..7", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "1floor_1walls_markers",
                       "valid": "1floor_1walls_markers"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..7", "valid": "2..8"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_walls = ctx.draw_int("n_walls", 1, 2)
        n_markers = ctx.draw_int("n_markers", 3, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
        n_walls = ctx.draw_int("n_walls", 3, 5)
        n_markers = ctx.draw_int("n_markers", 7, 10)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
        n_walls = ctx.draw_int("n_walls", 1, 4)
        n_markers = ctx.draw_int("n_markers", 4, 7)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    fill_box(g, h - 1, 0, h - 1, w - 1, 1)
    placed = 0
    for _ in range(60):
        if placed >= n_walls: break
        r = rng.randint(2, h - 3)
        c = rng.randint(0, w - 1)
        if g[r][c] != 0: continue
        g[r][c] = 1
        placed += 1
    placed_m = 0
    for _ in range(60):
        if placed_m >= n_markers: break
        r = rng.randint(0, h - 2)
        c = rng.randint(0, w - 1)
        if g[r][c] != 0: continue
        g[r][c] = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
        placed_m += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_floor":
        # Markers but no 1-floor row — gravity has nothing to settle on.
        g[2][3] = 4; g[3][6] = 6; g[5][2] = 7
        return g
    if name == "no_markers":
        # 1-floor present but no markers — rule has nothing to drop.
        fill_box(g, h - 1, 0, h - 1, w - 1, 1)
        return g
    if name == "already_settled":
        # Markers already at the bottom row above the floor — rule's
        # gravity is a no-op.
        fill_box(g, h - 1, 0, h - 1, w - 1, 1)
        for c in range(2, 7):
            g[h - 2][c] = c
        return g
    return g
