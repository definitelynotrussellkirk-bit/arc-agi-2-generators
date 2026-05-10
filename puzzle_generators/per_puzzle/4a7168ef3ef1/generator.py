"""Generator for arc_puzzle_bank_21_set18_bundle:hard_p07 — even-distance halo per seed.

Rule: each non-{0, 5} cell is a seed. BFS shortest distance to each 0-cell
(through 0-cells, blocked by 5-walls). Cells at even BFS distance get painted
with that seed's color. 5-walls and seeds preserved.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds, n_walls,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, walled_off, no_zero_room.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4a7168ef3ef1"
VERSION = "1.1.0"
TASK_ID = "4a7168ef3ef1"

SUMMARY = "1-2 colored seeds + sparse 5-walls; output paints even-distance halos."

INVARIANTS = [
    "background is 0",
    "1-2 single-cell seeds in distinct non-{0, 5} colors",
    "0-3 sparse color-5 wall cells",
    "seeds are not adjacent to walls (so halos can spread)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "walled_off", "no_zero_room")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "n_walls":        {"type": "int", "default": "rng 0..3", "valid": "0..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "seeds_with_sparse_walls",
                       "valid": "seeds_with_sparse_walls"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
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
        n_seeds = ctx.draw_int("n_seeds", 1, 1)
        n_walls = ctx.draw_int("n_walls", 0, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 11, 13)
        n_seeds = ctx.draw_int("n_seeds", 2, 2)
        n_walls = ctx.draw_int("n_walls", 2, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
        n_seeds = ctx.draw_int("n_seeds", 1, 2)
        n_walls = ctx.draw_int("n_walls", 0, 3)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        seed_colors = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_seeds)
        seed_pos = []
        ok = True
        for color in seed_colors:
            placed = False
            for _ in range(120):
                r = rng.randint(1, h - 2)
                c = rng.randint(1, w - 2)
                if g[r][c] != 0: continue
                if any(abs(r - sr) + abs(c - sc) < 3 for sr, sc in seed_pos): continue
                g[r][c] = color
                seed_pos.append((r, c))
                placed = True; break
            if not placed: ok = False; break
        if not ok:
            continue
        for _ in range(n_walls):
            for _t in range(40):
                r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                if g[r][c] != 0: continue
                if any(abs(r - sr) + abs(c - sc) <= 1 for sr, sc in seed_pos): continue
                g[r][c] = 5
                break
        return g
    raise ValueError("could not realize hard_l21 layout")


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # Walls but no seeds — rule has no halos to project.
        for c in range(2, 5): g[3][c] = 5
        return g
    if name == "walled_off":
        # Seed surrounded by walls — halo cannot spread.
        g[4][4] = 4
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]: g[4 + dr][4 + dc] = 5
        return g
    if name == "no_zero_room":
        # Grid completely full of walls + seed — no 0-cells to color.
        for r in range(h):
            for c in range(w): g[r][c] = 5
        g[4][4] = 4
        return g
    return g
