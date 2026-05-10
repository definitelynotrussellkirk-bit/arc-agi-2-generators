"""Generator for arc_puzzle_bank_fifth_21_bundle:easy_29_shoot_rays_to_walls.

Rule: color-2 emitters cast orthogonal rays through open space until
they hit color-5 walls.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, no_walls, seeds_on_walls.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8dd23f285c61"
VERSION = "1.1.0"
TASK_ID = "8dd23f285c61"
SUMMARY = "Color-2 emitters cast orthogonal rays through open space until 5-walls."

INVARIANTS = [
    "background is 0",
    "wall cells are color 5",
    "at least one color-2 seed has open space before a wall",
    "seeds do not sit on walls",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "no_walls", "seeds_on_walls")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "walls_with_seeds",
                       "valid": "walls_with_seeds"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        w = ctx.draw_int("grid_w", 9, 10)
        n_seeds = ctx.draw_int("n_seeds", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        n_seeds = ctx.draw_int("n_seeds", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 13)
        n_seeds = ctx.draw_int("n_seeds", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    wall_c = rng.randint(3, w - 4)
    for r in range(h):
        g[r][wall_c] = 5
    wall_r = rng.randint(2, h - 3)
    for c in range(wall_c + 2, w - 1):
        g[wall_r][c] = 5
    candidates = [(r, c) for r in range(1, h - 1) for c in range(1, w - 1)
                  if g[r][c] == 0]
    rng.shuffle(candidates)
    for r, c in candidates[:n_seeds]:
        g[r][c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # walls but no emitters → no rays cast
        for r in range(h): g[r][5] = 5
        for c in range(7, w - 1): g[3][c] = 5
        return g
    if name == "no_walls":
        # emitters but no walls → rays would shoot off-grid
        g[2][2] = 2
        g[5][3] = 2
        return g
    if name == "seeds_on_walls":
        # emitters sit on wall cells → ambiguous emitter/wall cell
        for r in range(h): g[r][5] = 5
        g[3][5] = 2  # seed on wall
        g[6][5] = 2
        return g
    return g
