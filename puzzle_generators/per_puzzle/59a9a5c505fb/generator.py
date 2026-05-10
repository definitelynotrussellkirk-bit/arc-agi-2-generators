"""Generator for arc_additional_puzzles_21_set11_bundle:H73 — Count bbox overlaps.

Rule: per-cell, count how many object bboxes contain it.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_frame, frames_disjoint, frames_identical.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "59a9a5c505fb"
VERSION = "1.1.0"
TASK_ID = "59a9a5c505fb"
SUMMARY = "2-3 nested rectangle frames; output counts bbox-overlap per cell."

INVARIANTS = [
    "between 2 and 3 nested frames",
    "frames are nested (bboxes contain inner ones)",
    "each frame uses a distinct color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_frame", "frames_disjoint", "frames_identical")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "nested_frames",
                       "valid": "nested_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "density":        {"type": "str", "default": "framed", "valid": "framed"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n_frames = ctx.draw_int("n_frames", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
        n_frames = ctx.draw_int("n_frames", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 9, 13)
        n_frames = ctx.draw_int("n_frames", 2, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    color_rng = ctx.draw_rng("colors")
    colors = [c for c in range(2, 10)]
    color_rng.shuffle(colors)
    r1 = rng.randint(0, h // 4)
    c1 = rng.randint(0, w // 4)
    r2 = rng.randint(h - 1 - h // 4, h - 1)
    c2 = rng.randint(w - 1 - w // 4, w - 1)
    for i in range(n_frames):
        col = colors[i]
        for c in range(c1, c2 + 1):
            g[r1][c] = col
            g[r2][c] = col
        for r in range(r1, r2 + 1):
            g[r][c1] = col
            g[r][c2] = col
        if r2 - r1 < 6 or c2 - c1 < 6:
            break
        r1 += 2; c1 += 2; r2 -= 2; c2 -= 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "single_frame":
        # one frame only → counts are all 0 or 1, no nesting depth visible
        for c in range(2, 9):
            g[2][c] = 4; g[8][c] = 4
        for r in range(2, 9):
            g[r][2] = 4; g[r][8] = 4
        return g
    if name == "frames_disjoint":
        # frames don't overlap → each cell is in at most 1 bbox, no count gradient
        for c in range(1, 4):
            g[1][c] = 4; g[3][c] = 4
        for r in range(1, 4):
            g[r][1] = 4; g[r][3] = 4
        for c in range(6, 10):
            g[6][c] = 6; g[9][c] = 6
        for r in range(6, 10):
            g[r][6] = 6; g[r][9] = 6
        return g
    if name == "frames_identical":
        # two frames at the exact same bbox → counts are identical (overlapping but same shape)
        for c in range(2, 9):
            g[2][c] = 4; g[8][c] = 4
        for r in range(2, 9):
            g[r][2] = 4; g[r][8] = 4
        # second frame at same bbox in different color (would draw over)
        for c in range(2, 9):
            g[2][c] = 6; g[8][c] = 6
        for r in range(2, 9):
            g[r][2] = 6; g[r][8] = 6
        return g
    return g
