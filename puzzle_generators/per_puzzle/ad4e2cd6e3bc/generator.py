"""Generator for arc_additional_puzzle_bank_volume2:H8 — Flood-fill bg from red seed (no connectivity arg).

Rule: connected-region from red seed through cells where v∈{0,2}.
Paint bg cells in the region with 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, wall_pct,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_seed, seed_in_wall.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ad4e2cd6e3bc"
VERSION = "1.1.0"
TASK_ID = "ad4e2cd6e3bc"
SUMMARY = "Maze-like compartments with gray walls; red seed inside; flood the bg compartment with 8."

INVARIANTS = [
    "outer border all gray(5)",
    "internal gray walls form a maze with non-trivial reachable region",
    "exactly one red(2) seed inside",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_seed", "seed_in_wall")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "wall_pct":       {"type": "float", "default": "rng 0.15..0.30", "valid": "0..0.4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "border_walls_with_interior_seed",
                       "valid": "border_walls_with_interior_seed"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "varied", "valid": "varied"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 12)
    g = full_grid(h, w, 5)
    rng = ctx.draw_rng("layout")
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            if rng.random() < 0.7:
                g[r][c] = 0
    interior = [(r, c) for r in range(1, h - 1) for c in range(1, w - 1) if g[r][c] == 0]
    if not interior:
        for r in range(1, h - 1):
            for c in range(1, w - 1):
                g[r][c] = 0
        interior = [(r, c) for r in range(1, h - 1) for c in range(1, w - 1)]
    sr, sc = rng.choice(interior)
    g[sr][sc] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    if name == "no_walls":
        # no internal walls (no border at all) → seed reaches all cells, fill is uniform
        g = full_grid(h, w, 0)
        g[3][4] = 2
        return g
    if name == "no_seed":
        # walled maze but no red seed → rule has no anchor to flood from
        g = full_grid(h, w, 5)
        for r in range(1, h - 1):
            for c in range(1, w - 1):
                g[r][c] = 0
        # internal wall
        for c in range(2, 6): g[3][c] = 5
        return g
    if name == "seed_in_wall":
        # seed is on a gray wall cell → connected-region predicate v∈{0,2} fails at start
        g = full_grid(h, w, 5)
        for r in range(1, h - 1):
            for c in range(1, w - 1):
                g[r][c] = 0
        g[0][3] = 2  # seed sits in border wall
        return g
    return full_grid(h, w, 0)
