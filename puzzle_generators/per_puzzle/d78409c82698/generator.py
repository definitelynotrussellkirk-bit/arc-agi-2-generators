"""Generator for arc_additional_puzzle_bank_volume2:E8.

Rule: red cells with no cardinal red neighbor are recolored green.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_singletons,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_singletons, all_singletons, no_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d78409c82698"
VERSION = "1.1.0"
TASK_ID = "d78409c82698"
SUMMARY = "Red cells with no cardinal red neighbor are recolored green."

INVARIANTS = [
    "background is 0",
    "target red cells are cardinally isolated singletons",
    "larger red components are present as non-target distractors",
    "red singletons are separated from all red components",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_singletons", "all_singletons", "no_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_singletons":   {"type": "int", "default": "rng 2..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "singletons_plus_component",
                       "valid": "singletons_plus_component"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
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
        n_singletons = ctx.draw_int("n_singletons", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
        n_singletons = ctx.draw_int("n_singletons", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_singletons = ctx.draw_int("n_singletons", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    cells: list[tuple[int, int]] = []
    for _ in range(220):
        if len(cells) >= n_singletons:
            break
        r = rng.randint(1, h - 4)
        c = rng.randint(3, w - 2)
        if any(abs(r - rr) < 3 and abs(c - cc) < 3 for rr, cc in cells):
            continue
        if g[r][c] == 0:
            g[r][c] = 2
            cells.append((r, c))
    g[h - 2][0] = 2
    g[h - 2][1] = 2
    g[h - 3][0] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_singletons":
        # only multi-cell red component → rule fires zero times, output identical
        g[1][1] = 2; g[1][2] = 2; g[2][1] = 2
        return g
    if name == "all_singletons":
        # all red cells are isolated singletons → all recolored green
        g[1][2] = 2; g[3][5] = 2; g[5][7] = 2; g[7][1] = 2
        return g
    if name == "no_components":
        # blank → no red cells, rule has no effect
        return g
    return g
