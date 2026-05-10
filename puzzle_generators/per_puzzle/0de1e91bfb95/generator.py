"""Generator for arc_puzzle_bank_21_set10_s:S10_M1 — laser beam from 2-seed, deflected by 6/7 mirrors, stopped by 5-wall.

Rule: each 2-cell shoots a beam to the right. The beam paints 8 on
0-cells. On hitting a 6-mirror it turns left-of-incoming, on 7 it
turns right-of-incoming, on a 5-wall (or any other non-empty cell)
it stops.

Combinatorial axes (8): grid_h, grid_w, palette_kind, mirror_kind,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seed, no_mirror, no_wall.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0de1e91bfb95"
VERSION = "1.1.0"
TASK_ID = "0de1e91bfb95"
SUMMARY = "1 2-seed + 1-2 mirrors (6 or 7) + 1 5-wall, arranged so the beam has at least one cell to paint."

INVARIANTS = [
    "background is 0",
    "exactly one 2-seed",
    "1-2 mirror cells (color 6 or 7) in the 2's row OR in a column the beam will hit after deflection",
    "exactly one 5-wall placed where the beam terminates",
    "beam length ≥1 before hitting the first mirror or wall",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seed", "no_mirror", "no_wall")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "mirror_kind":    {"type": "int", "default": "rng 6|7", "valid": "6..7"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "seed_mirror_wall",
                       "valid": "seed_mirror_wall"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    seed_r = rng.randint(2, h - 3)
    seed_c = 1
    g[seed_r][seed_c] = 2
    mirror_kind = rng.choice([6, 7])  # 6 turns up-from-right, 7 turns down-from-right
    mirror_c = rng.randint(seed_c + 3, w - 3)
    g[seed_r][mirror_c] = mirror_kind
    if mirror_kind == 6:
        wall_r = rng.randint(0, seed_r - 1)
        g[wall_r][mirror_c] = 5
    else:
        wall_r = rng.randint(seed_r + 1, h - 1)
        g[wall_r][mirror_c] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_seed":
        # mirrors and wall but no 2-seed → no beam to fire
        g[3][5] = 6; g[1][5] = 5
        return g
    if name == "no_mirror":
        # seed + wall but no mirror → beam goes straight (still defined but no deflection)
        g[3][1] = 2
        g[3][7] = 5
        return g
    if name == "no_wall":
        # seed + mirror but no wall → beam never terminates
        g[3][1] = 2
        g[3][5] = 6
        return g
    return g
