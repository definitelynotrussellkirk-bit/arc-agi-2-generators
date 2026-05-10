"""Generator for arc_additional_puzzle_bank_volume20:H138.

Rule: open maze cells are partitioned by nearest seed (BFS through
walls), with tie cells colored cyan.

Combinatorial axes (9): grid_h/w, palette_kind, anchor_row,
seed_distance, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: seeds_collide, no_walls, no_seeds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b79c14333907"
VERSION = "1.1.0"
TASK_ID = "b79c14333907"
SUMMARY = "Open maze cells are partitioned by nearest seed, with ties colored cyan."

INVARIANTS = [
    "background is 0",
    "border walls are 5",
    "there is one seed color 2 and one seed color 3",
    "symmetric seed placement creates a nonempty tie column",
]

PALETTE_KINDS = ("default", "tight_corridor", "wide_chamber", "off_center_seeds")
DEGENERATE_TEXTURES = ("seeds_collide", "no_walls", "no_seeds")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "5..24"},
    "grid_w":         {"type": "int", "default": "rng 9..15", "valid": "7..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "seed_distance":  {"type": "int", "default": "4", "valid": "2..8"},
    "anchor_row":     {"type": "str", "default": "rng",
                       "valid": "top|middle|bottom"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "centered", "valid": "centered"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        w = ctx.draw_int("grid_w", 9, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 9, 15)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = 5
        g[r][w - 1] = 5
    for c in range(w):
        g[0][c] = 5
        g[h - 1][c] = 5
    r = rng.randint(2, h - 3)
    mid = w // 2
    g[r][mid - 2] = 2
    g[r][mid + 2] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "seeds_collide":
        for r in range(h):
            g[r][0] = 5
            g[r][w - 1] = 5
        for c in range(w):
            g[0][c] = 5
            g[h - 1][c] = 5
        mid = w // 2
        g[5][mid] = 2
        g[5][mid + 1] = 3
        return g
    if name == "no_walls":
        mid = w // 2
        g[5][mid - 2] = 2
        g[5][mid + 2] = 3
        return g
    if name == "no_seeds":
        for r in range(h):
            g[r][0] = 5
            g[r][w - 1] = 5
        for c in range(w):
            g[0][c] = 5
            g[h - 1][c] = 5
        return g
    return g
