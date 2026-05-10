"""Generator for arc_additional_puzzles_21_set13_bundle:M90 — Flood single-color compartments.

Rule: 1-walls divide grid. For each 0-region, if it has exactly one
non-{0,1} color cell adjacent (or inside), fill the region with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_compartments,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_seeds, multiple_seeds_per_compartment.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "35b93111c742"
VERSION = "1.1.0"
TASK_ID = "35b93111c742"
SUMMARY = "1-walls form 3 compartments; each has 1 marker of distinct non-{0,1} color."

INVARIANTS = [
    "1-walls form a regular grid",
    "each compartment has exactly one marker of distinct non-{0,1} color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_seeds", "multiple_seeds_per_compartment")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "derived", "valid": "11..17"},
    "grid_w":         {"type": "int", "default": "derived", "valid": "11..17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rows":         {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "n_cols":         {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "rng 4..9", "valid": "4..9"},
    "position_bias":  {"type": "str", "default": "1_walls_with_seeds",
                       "valid": "1_walls_with_seeds"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..9", "valid": "4..9"},
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
        n_rows = ctx.draw_int("n_rows", 2, 2)
        n_cols = ctx.draw_int("n_cols", 2, 2)
    elif difficulty == "hard":
        n_rows = ctx.draw_int("n_rows", 3, 3)
        n_cols = ctx.draw_int("n_cols", 3, 3)
    else:
        n_rows = ctx.draw_int("n_rows", 2, 3)
        n_cols = ctx.draw_int("n_cols", 2, 3)
    cell_h = 4; cell_w = 4
    h = n_rows * cell_h + (n_rows + 1)
    w = n_cols * cell_w + (n_cols + 1)
    g = full_grid(h, w, 1)
    rng = ctx.draw_rng("layout")
    palette = [c for c in range(2, 10)]; rng.shuffle(palette)
    idx = 0
    for ri in range(n_rows):
        for ci in range(n_cols):
            r0 = 1 + ri * (cell_h + 1)
            c0 = 1 + ci * (cell_w + 1)
            for r in range(r0, r0 + cell_h):
                for c in range(c0, c0 + cell_w):
                    g[r][c] = 0
            sr = rng.randint(r0, r0 + cell_h - 1)
            sc = rng.randint(c0, c0 + cell_w - 1)
            g[sr][sc] = palette[idx % len(palette)]
            idx += 1
    return g


def _draw_from_degenerate(name, rng):
    n_rows, n_cols = 2, 2
    cell_h, cell_w = 4, 4
    h = n_rows * cell_h + (n_rows + 1)
    w = n_cols * cell_w + (n_cols + 1)
    if name == "no_walls":
        # markers without 1-walls → no compartments to fill within
        g = full_grid(h, w, 0)
        g[2][2] = 4; g[2][6] = 6
        g[6][2] = 7; g[6][6] = 8
        return g
    if name == "no_seeds":
        # walls form compartments but no seed markers → nothing to fill
        g = full_grid(h, w, 1)
        for ri in range(n_rows):
            for ci in range(n_cols):
                r0 = 1 + ri * (cell_h + 1)
                c0 = 1 + ci * (cell_w + 1)
                for r in range(r0, r0 + cell_h):
                    for c in range(c0, c0 + cell_w):
                        g[r][c] = 0
        return g
    if name == "multiple_seeds_per_compartment":
        # one compartment has 2 different seeds → "exactly one" precondition fails
        g = full_grid(h, w, 1)
        for ri in range(n_rows):
            for ci in range(n_cols):
                r0 = 1 + ri * (cell_h + 1)
                c0 = 1 + ci * (cell_w + 1)
                for r in range(r0, r0 + cell_h):
                    for c in range(c0, c0 + cell_w):
                        g[r][c] = 0
        g[2][2] = 4; g[3][3] = 6  # both in TL compartment
        g[2][6] = 7
        g[6][2] = 8
        return g
    return full_grid(h, w, 0)
