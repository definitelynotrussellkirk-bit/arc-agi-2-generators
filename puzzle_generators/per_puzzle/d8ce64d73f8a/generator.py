"""Generator for arc_additional_puzzle_bank_volume12:M81 — Flood-fill from seed inside walls.

Rule: BFS from the (single) red(2) cell, expanding through any cell
whose value isn't 5 (gray walls), 4-connected. Paint the reached
region with 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, wall_col,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seed, no_walls, seed_outside.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d8ce64d73f8a"
VERSION = "1.1.0"
TASK_ID = "d8ce64d73f8a"
SUMMARY = "Gray (5) walls forming compartments; red(2) seed inside one; flood-fills with 8."

INVARIANTS = [
    "outer border is all gray(5)",
    "1+ vertical or horizontal gray walls divide the interior into >=2 compartments",
    "exactly one red(2) seed cell, inside one compartment",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seed", "no_walls", "seed_on_wall")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "wall_col":       {"type": "int", "default": "rng", "valid": "1..w-2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "compartmented",
                       "valid": "compartmented"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
    "density":        {"type": "str", "default": "medium", "valid": "medium"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 14)
    wall_col = ctx.draw_int("wall_col", 3, w - 4)

    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = 5; g[r][w-1] = 5
    for c in range(w):
        g[0][c] = 5; g[h-1][c] = 5
    for r in range(h):
        g[r][wall_col] = 5

    rng = ctx.draw_rng("seed")
    seed_r = rng.randint(1, h - 2)
    seed_c = rng.randint(1, wall_col - 1)
    g[seed_r][seed_c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = 5; g[r][w-1] = 5
    for c in range(w):
        g[0][c] = 5; g[h-1][c] = 5
    if name == "no_seed":
        # walls present but no red seed → flood-fill has no start point, rule no-op
        for r in range(h):
            g[r][5] = 5
        return g
    if name == "no_walls":
        # outer border only, no internal wall → only one compartment, flood fills entire interior
        # (overwrite border to remove the always-present outer wall to make this distinct)
        g2 = full_grid(h, w, 0)
        g2[3][6] = 2
        return g2
    if name == "seed_on_wall":
        # red seed sits on a wall cell → ambiguous which side it belongs to
        for r in range(h):
            g[r][5] = 5
        g[3][5] = 2
        return g
    return g
