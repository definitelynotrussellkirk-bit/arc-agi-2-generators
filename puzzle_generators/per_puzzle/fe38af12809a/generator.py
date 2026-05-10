"""Generator for arc_additional_puzzle_bank_volume11:M72 -- red-distance ring.

Rule: a top-row code gives Manhattan radius 1 or 3; zeros/red cells at
that radius become 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, radius,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_code, no_red_seed, code_radius_too_large.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fe38af12809a"
VERSION = "1.1.0"
TASK_ID = "fe38af12809a"
SUMMARY = "A top-row code gives Manhattan radius 1 or 3; zeros/red cells at that radius become 8."

INVARIANTS = [
    "the first 1/2/3 in row 0 is the distance code",
    "a separate red seed exists away from the code row",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_code", "no_red_seed", "code_radius_too_large")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "5..15"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "radius":         {"type": "choice", "default": "rng {1,3}", "valid": "1 or 3"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "code_row0_with_red_seed",
                       "valid": "code_row0_with_red_seed"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 7, 11)
    radius = ctx.draw_choice("radius", [1, 3])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][rng.randint(0, min(2, w - 1))] = radius

    sr = rng.randint(radius + 1, h - radius - 1)
    sc = rng.randint(radius + 1, w - radius - 1)
    g[sr][sc] = 2

    for _ in range(rng.randint(1, 4)):
        r = rng.randint(1, h - 1)
        c = rng.randint(0, w - 1)
        if abs(r - sr) + abs(c - sc) != radius and g[r][c] == 0:
            g[r][c] = rng.choice([4, 5, 6, 7, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_code":
        # row 0 empty → no radius code, ring undefined
        g[4][4] = 2
        return g
    if name == "no_red_seed":
        # code present but no red seed → no center for the ring
        g[0][1] = 3
        return g
    if name == "code_radius_too_large":
        # radius too large → ring extends beyond grid (mostly out-of-bounds)
        g[0][1] = 3
        g[1][1] = 2   # red seed near edge — ring at distance 3 mostly out
        return g
    return g
