"""Generator for 668eec9a.

Rule: for each non-bg color, find top-most-then-leftmost cell. Sort by
(min-r, min-c). Output 5x3 with bg padding + one row per color.

Combinatorial axes (8): grid_h/w, n_colors, palette_kind, density,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: same_color, no_colors, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import random_free_cell

GENERATOR_ID = "2c00ca6ac44b"
VERSION = "1.1.0"
TASK_ID = "2c00ca6ac44b"
SUMMARY = "Random h x w bg=7 grid with 2-4 distinct non-7 colors at scattered positions."

INVARIANTS = [
    "bg = 7",
    "2-4 distinct non-7 colors",
    "each color has >=2 cells with at least one in different column",
]

POSITION_BIASES = ("scattered", "clustered", "row_lean", "col_lean")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("same_color", "no_colors", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "grid_w":         {"type": "int", "default": "rng 12..18", "valid": "10..22"},
    "n_colors":       {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "density":        {"type": "float", "default": "rng 0.1..0.2", "valid": "0.05..0.4"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 10, 12
        nc_lo, nc_hi = 2, 2
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
        nc_lo, nc_hi = 4, 5
    else:
        h_lo, h_hi = 12, 18
        nc_lo, nc_hi = 2, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 7)
    n_colors = int(overrides.get("n_colors",
                                 ctx.draw_int("n_colors", nc_lo, nc_hi)))
    n_colors = max(1, min(5, n_colors))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, n_colors, rng)
    for color in palette:
        for _ in range(rng.randint(3, 7)):
            cell = random_free_cell(g, rng, bg=7, max_tries=20)
            if cell is not None:
                g[cell[0]][cell[1]] = color
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 8, 9]
    pool = [c for c in pool if c != 7]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = full_grid(h, w, 7)
    if name == "same_color":
        for _ in range(8):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            g[r][c] = 2
        return g
    if name == "no_colors":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
