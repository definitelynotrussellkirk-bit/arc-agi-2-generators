"""Generator for arc_additional_puzzles_21_set21_bundle:E146 — Trail seed in cmd direction.

Rule: cmd cell value (1=up, 2=down, 3=left, 4=right) + seed cell of
other color. Paint trail from seed in cmd direction with seed color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, code,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cmd, no_seed, seed_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e8504fcc371b"
VERSION = "1.1.0"
TASK_ID = "e8504fcc371b"
SUMMARY = "1 cmd cell ∈ {1,2,3,4} + 1 seed cell of distinct color."

INVARIANTS = [
    "exactly 1 cmd cell with value in {1, 2, 3, 4}",
    "exactly 1 seed cell with value in {5, 6, 7, 8, 9}",
    "trail in cmd direction from seed has empty space",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cmd", "no_seed", "seed_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "code":           {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "cmd_with_seed",
                       "valid": "cmd_with_seed"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    code = rng.randint(1, 4)
    color = rng.choice([5, 6, 7, 8, 9])
    cr = rng.randint(0, h - 1); cc = rng.randint(0, w - 1)
    g[cr][cc] = code
    while True:
        sr = rng.randint(0, h - 1); sc = rng.randint(0, w - 1)
        if g[sr][sc] == 0 and (sr, sc) != (cr, cc):
            g[sr][sc] = color
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_cmd":
        # only seed, no cmd cell → no direction encoded
        g[2][3] = 6
        return g
    if name == "no_seed":
        # only cmd, no seed → nothing to trail
        g[3][5] = 2
        return g
    if name == "seed_at_edge":
        # seed sits at the edge in the cmd direction → trail length 0
        g[0][0] = 1   # cmd: up
        g[0][3] = 6   # seed already at top row, cannot trail up
        return g
    return g
