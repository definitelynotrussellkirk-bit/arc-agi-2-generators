"""Generator for arc_additional_puzzle_bank_volume11:M74.

Rule: red and green chamber markers are joined by a cyan shortest path.

Combinatorial axes (8): grid_h, grid_w, palette_kind, wall_density,
palette_size, position_bias, n_distinct_colors, marker_distance, texture.
Degenerates: no_red, no_green, blocked_path.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8e9198d0ddf3"
VERSION = "1.1.0"
TASK_ID = "8e9198d0ddf3"
SUMMARY = "Red and green chamber markers are joined by a cyan shortest path."

INVARIANTS = [
    "background is 0",
    "there is exactly one red marker and one green marker",
    "gray walls do not block the direct horizontal route",
    "the shortest path has nonzero interior length",
]

PALETTE_KINDS = ("default", "sparse_walls", "medium_walls", "dense_walls")
DEGENERATE_TEXTURES = ("no_red", "no_green", "blocked_path")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "4..24"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "wall_density":   {"type": "str", "default": "mixed", "valid": "mixed"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "row_aligned", "valid": "row_aligned"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "marker_distance": {"type": "str", "default": "≥3", "valid": "≥3"},
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
    for c in range(w):
        if c not in (c1, c2) and rng.random() < 0.18:
            wr = rng.choice([x for x in range(h) if x != r])
            g[wr][c] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    r = 4
    if name == "no_red":
        # only green marker → path source undefined
        g[r][8] = 3
        return g
    if name == "no_green":
        # only red marker → path target undefined
        g[r][2] = 2
        return g
    if name == "blocked_path":
        # red+green plus a wall on the row between them → no horizontal route
        g[r][2] = 2
        g[r][8] = 3
        for rr in range(h):
            g[rr][5] = 5
        return g
    return g
