"""Generator for 18b:hard_122 — overlay rays until block, count map.

Rule: cells with values 1/2/3/4 are emitters (1=up, 2=right, 3=down,
4=left). Each casts a ray in its direction until hitting value 5 or
the boundary. Output sums ray-hit counts at each cell.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_emitters,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_emitters, no_walls, all_same_direction.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "be6269bef667"
VERSION = "1.1.0"
TASK_ID = "be6269bef667"
SUMMARY = "2-4 directional emitters (1/2/3/4) + 1-3 wall cells (5)."

INVARIANTS = [
    "background is 0",
    "2-4 emitters with values in {1, 2, 3, 4}",
    "1-3 wall cells of value 5",
    "no cell holds two emitters or an emitter on a wall",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_emitters", "no_walls", "all_same_direction")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_emitters":     {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "emitters_with_walls",
                       "valid": "emitters_with_walls"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used: set[tuple[int, int]] = set()
    n_walls = rng.randint(1, 3)
    for _ in range(n_walls):
        for _ in range(40):
            r = rng.randint(1, h - 2); c = rng.randint(1, w - 2)
            if (r, c) in used: continue
            g[r][c] = 5; used.add((r, c)); break
    n_emitters = rng.randint(2, 4)
    for _ in range(n_emitters):
        for _ in range(40):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            if (r, c) in used: continue
            g[r][c] = rng.randint(1, 4); used.add((r, c)); break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "no_emitters":
        # walls but no emitters → no rays cast, output empty count map
        g[3][3] = 5; g[3][4] = 5
        return g
    if name == "no_walls":
        # emitters but no walls → rays travel to grid boundary unobstructed
        g[2][3] = 1; g[5][2] = 2; g[1][6] = 4
        return g
    if name == "all_same_direction":
        # all emitters point up → degenerate, no crossings to count
        g[5][1] = 1; g[5][3] = 1; g[5][5] = 1
        return g
    return g
