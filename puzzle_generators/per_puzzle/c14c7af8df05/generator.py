"""Generator for arc_puzzle_bank_tenth21:E69.

Two-cell diagonal color chains extend one more step.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_cell_chains, three_cell_chains.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c14c7af8df05"
VERSION = "1.1.0"
TASK_ID = "c14c7af8df05"

SUMMARY = "Two-cell diagonal color chains extend one more step."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "the two cells form a one-step diagonal",
    "the continuation cell is in bounds and initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_cell_chains", "three_cell_chains")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "diagonal_pairs",
                       "valid": "diagonal_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
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
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("n_pairs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("n_pairs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("n_pairs", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(colors)
    used: set[tuple[int, int]] = set()
    placed = 0
    for color in colors:
        if placed >= target:
            break
        for _ in range(100):
            dr = 1
            dc = rng.choice([-1, 1])
            r = rng.randint(0, h - 3)
            c = rng.randint(2 if dc < 0 else 0, w - 3 if dc > 0 else w - 1)
            cells = [(r, c), (r + dr, c + dc), (r + 2 * dr, c + 2 * dc)]
            if any(p in used for p in cells):
                continue
            g[cells[0][0]][cells[0][1]] = color
            g[cells[1][0]][cells[1][1]] = color
            used.update(cells)
            placed += 1
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no diagonal chains to extend
        return g
    if name == "single_cell_chains":
        # only one cell of color → "appears exactly twice" precondition fails
        g[2][2] = 4
        g[5][5] = 6
        return g
    if name == "three_cell_chains":
        # 3 cells of same color → "exactly twice" precondition fails (continuation already exists)
        g[1][1] = 4; g[2][2] = 4; g[3][3] = 4
        return g
    return g
