"""Generator for arc_additional_puzzle_bank_volume18:M122 — Flood-fill compartment.

Rule: BFS from the (single) red(2) seed through cells where v ∈ {0, 2}.
Paint all bg(0) cells in the reached region with 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_walls,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_seed, seed_in_wall.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f60cfd11346a"
VERSION = "1.1.0"
TASK_ID = "f60cfd11346a"
SUMMARY = "Gray walls forming compartments; red seed in one; flood-fill its compartment with 8."

INVARIANTS = [
    "outer border all gray(5)",
    "1+ vertical gray walls split the interior into ≥2 compartments",
    "exactly one red(2) seed inside one of them",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_seed", "seed_in_wall")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_walls":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "framed_with_walls",
                       "valid": "framed_with_walls"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 9, 14)
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = 5; g[r][w-1] = 5
    for c in range(w):
        g[0][c] = 5; g[h-1][c] = 5
    rng = ctx.draw_rng("walls")
    n_walls = rng.randint(1, 2)
    cols_used = []
    for _ in range(n_walls):
        for _ in range(20):
            col = rng.randint(2, w - 3)
            if all(abs(col - c) >= 2 for c in cols_used):
                cols_used.append(col)
                for r in range(h):
                    g[r][col] = 5
                break
    seed_r = rng.randint(1, h - 2)
    seed_c = rng.randint(1, min(cols_used) - 1) if cols_used else rng.randint(1, w - 2)
    g[seed_r][seed_c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 11
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = 5; g[r][w - 1] = 5
    for c in range(w):
        g[0][c] = 5; g[h - 1][c] = 5
    if name == "no_walls":
        # bordered grid with no interior walls → flood fills the entire interior with 8
        g[3][5] = 2
        return g
    if name == "no_seed":
        # walls but no red seed → BFS has no source, rule fires zero times
        for r in range(h):
            g[r][4] = 5
        return g
    if name == "seed_in_wall":
        # red seed lands on a wall cell → predicate ambiguous (cell is 5, not 2)
        for r in range(h):
            g[r][4] = 5
        # overwrite a wall cell with 2 → seed embedded in wall
        g[2][4] = 2
        return g
    return g
