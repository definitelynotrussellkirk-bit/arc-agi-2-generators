"""Generator for arc_puzzle_bank_21_set19_bundle:hard_p02 — BFS path with portals.

Rule: BFS from color-2 start to color-3 goal, avoiding color-8 walls. Colors
4, 5, 6 form portal pairs (each color appears exactly 2× — entering one teleports
to the other). Path painted color 7 in 0-cells along the route.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_start, no_goal, walls_block_path.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b87dcd3011b1"
VERSION = "1.1.0"
TASK_ID = "b87dcd3011b1"

SUMMARY = "Start (color 2), goal (color 3), 0-3 walls (color 8), optional portal pairs."

INVARIANTS = [
    "background is 0",
    "exactly one color-2 start cell and one color-3 goal cell",
    "0-3 sparse color-8 wall cells",
    "0-1 optional portal pair (color 4) each at distinct positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_start", "no_goal", "walls_block_path")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "n_walls":           {"type": "int", "default": "rng 0..3", "valid": "0..5"},
    "use_portal":        {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "position_bias":     {"type": "str", "default": "start_goal_walls_portals",
                          "valid": "start_goal_walls_portals"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 11)
        n_walls = ctx.draw_int("n_walls", 0, 1)
        use_portal = ctx.draw_int("use_portal", 0, 0)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 13, 13)
        n_walls = ctx.draw_int("n_walls", 2, 3)
        use_portal = ctx.draw_int("use_portal", 1, 1)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        n_walls = ctx.draw_int("n_walls", 0, 3)
        use_portal = ctx.draw_int("use_portal", 0, 1)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        sr = rng.randint(0, h - 1); sc = rng.randint(0, w - 1)
        g[sr][sc] = 2
        for _ in range(120):
            gr = rng.randint(0, h - 1); gc = rng.randint(0, w - 1)
            if (gr, gc) == (sr, sc): continue
            if abs(gr - sr) + abs(gc - sc) < 4: continue
            g[gr][gc] = 3
            break
        else:
            continue
        for _ in range(n_walls):
            for _t in range(40):
                r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                if g[r][c] != 0: continue
                if abs(r - sr) + abs(c - sc) < 2: continue
                if abs(r - gr) + abs(c - gc) < 2: continue
                g[r][c] = 8
                break
        if use_portal:
            placed_p = 0
            portal_color = 4
            while placed_p < 2:
                for _t in range(40):
                    r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                    if g[r][c] != 0: continue
                    g[r][c] = portal_color
                    placed_p += 1
                    break
                else:
                    break
        return g
    raise ValueError("could not realize set19 p02 layout")


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_start":
        g[6][8] = 3
        g[3][3] = 8; g[5][5] = 8
        return g
    if name == "no_goal":
        g[2][2] = 2
        g[5][5] = 8; g[6][7] = 8
        return g
    if name == "walls_block_path":
        g[2][2] = 2
        g[8][9] = 3
        for c in range(0, w):
            g[5][c] = 8
        return g
    return g
