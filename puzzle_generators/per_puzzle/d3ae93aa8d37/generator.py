"""Generator for arc_additional_puzzle_bank_volume10:M70.

Rule: a red start and green goal on a clear row are connected by a
cyan path.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_walls,
palette_size, position_bias, n_distinct_colors, distance, texture.
Degenerates: no_red, no_green, blocked_path.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d3ae93aa8d37"
VERSION = "1.1.0"
TASK_ID = "d3ae93aa8d37"
SUMMARY = "A red start and green goal on a clear row are connected by a cyan path."

INVARIANTS = [
    "background is 0",
    "gray cells are optional walls away from the direct path",
    "there is exactly one red start and one green goal",
    "the shortest path is the straight horizontal segment between endpoints",
]

PALETTE_KINDS = ("default", "sparse_walls", "medium_walls", "dense_walls")
DEGENERATE_TEXTURES = ("no_red", "no_green", "blocked_path")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "4..24"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_walls":        {"type": "int", "default": "rng 2..5", "valid": "0..8"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "row_aligned", "valid": "row_aligned"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "distance":       {"type": "str", "default": "≥3", "valid": "≥3"},
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
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 8, 14)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    r = rng.randint(1, h - 2)
    c1 = rng.randint(0, w - 5)
    c2 = rng.randint(c1 + 3, w - 1)
    g[r][c1] = 2
    g[r][c2] = 3
    for _ in range(rng.randint(2, 5)):
        wr = rng.choice([x for x in range(h) if x != r])
        wc = rng.randint(0, w - 1)
        g[wr][wc] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    r = 4
    if name == "no_red":
        # only goal — start undefined
        g[r][8] = 3
        return g
    if name == "no_green":
        # only start — goal undefined
        g[r][2] = 2
        return g
    if name == "blocked_path":
        # start + goal but a wall on their row → straight horizontal segment is broken
        g[r][2] = 2
        g[r][8] = 3
        g[r][5] = 5
        return g
    return g
