"""Generator for arc_puzzle_bank_twentysecond21:E150 — gravity down.

Rule: all non-zero cells fall to the bottom (each shifts down by max-row -
maximum cell row).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: already_at_bottom, no_cells, single_row_at_top.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8343e384cd7c"
VERSION = "1.1.0"
TASK_ID = "8343e384cd7c"
SUMMARY = "Sparse non-zero cells in upper half; lower half empty."

INVARIANTS = [
    "background is 0",
    "2-5 non-zero cells in any colors",
    "at least one cell is in the upper half (so the gravity has visible effect)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("already_at_bottom", "no_cells", "single_row_at_top")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "upper_half",
                       "valid": "upper_half"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..5", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 5, 6)
        n = ctx.draw_int("n_cells", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
        n = ctx.draw_int("n_cells", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 5, 7)
        n = ctx.draw_int("n_cells", 2, 5)
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    for _ in range(n):
        for _t in range(40):
            r = rng.randint(0, h // 2)  # upper half
            c = rng.randint(0, w - 1)
            if g[r][c] != 0: continue
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 6
    g = full_grid(h, w, 0)
    if name == "already_at_bottom":
        # cells already on bottom row → gravity is identity
        g[h - 1][1] = 3
        g[h - 1][3] = 5
        g[h - 1][4] = 7
        return g
    if name == "no_cells":
        # empty grid → gravity has nothing to drop
        return g
    if name == "single_row_at_top":
        # all cells on top row only → gravity drops a clean horizontal line
        for c in range(w):
            if c % 2 == 0:
                g[0][c] = (c % 9) + 1
        return g
    return g
