"""Generator for arc_puzzle_bank_21_set17_s:S17_E3.

Rule: sparse seeds grow into clipped 3x3 square stencils.

Combinatorial axes (8): grid_h/w, height, width, seed_count, palette_kind,
anchor_corner, asymmetry_force, palette_size.
Degenerates: no_seeds, single_seed, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "067f6e037e97"
VERSION = "1.1.0"
TASK_ID = "067f6e037e97"
SUMMARY = "Sparse seeds grow into clipped 3x3 square stencils."

INVARIANTS = [
    "input contains two to three nonzero seed cells",
    "output is the union of 3x3 square neighborhoods around seeds",
    "growth is clipped at borders",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seeds", "single_seed", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "6..8"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "6..8"},
    "height":         {"type": "int", "default": "rng 6..8", "valid": "6..8"},
    "width":          {"type": "int", "default": "rng 6..8", "valid": "6..8"},
    "seed_count":     {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h = ctx.draw_int("height", 6, 6)
        w = ctx.draw_int("width", 6, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 7, 8)
        w = ctx.draw_int("width", 7, 8)
    else:
        h = ctx.draw_int("height", 6, 8)
        w = ctx.draw_int("width", 6, 8)
    n = ctx.draw_int("seed_count", 2, 3)
    g = full_grid(h, w, 0)
    cells = [(r, c) for r in range(h) for c in range(w)]
    for idx, (r, c) in enumerate(rng.sample(cells, n)):
        g[r][c] = 4 + idx
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 7, 0)
    if name == "no_seeds":
        return g
    if name == "single_seed":
        g[3][3] = 4
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(7):
                g[r][c] = 4
        return g
    return g
