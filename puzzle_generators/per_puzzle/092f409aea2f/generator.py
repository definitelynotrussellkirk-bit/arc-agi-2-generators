"""Generator for arc_puzzle_bank_sixteenth21:E106.

Each active color appears as one vertical endpoint pair to bridge.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_bridges,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_endpoints, single_endpoint, horizontal_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "092f409aea2f"
VERSION = "1.1.0"
TASK_ID = "092f409aea2f"

SUMMARY = "Each active color appears as one vertical endpoint pair to bridge."

INVARIANTS = [
    "background is 0",
    "each bridge color appears exactly twice",
    "the two cells for a bridge color share a column",
    "all cells between bridge endpoints are initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_endpoints", "single_endpoint", "horizontal_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_bridges":      {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "vertical_endpoint_pairs",
                       "valid": "vertical_endpoint_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("n_bridges", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("n_bridges", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("n_bridges", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(colors)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    for color in colors:
        if placed >= target:
            break
        for _ in range(80):
            c = rng.randrange(w)
            r0 = rng.randint(0, h - 3)
            r1 = rng.randint(r0 + 2, h - 1)
            cells = {(r, c) for r in range(r0, r1 + 1)}
            if cells & reserved:
                continue
            g[r0][c] = color
            g[r1][c] = color
            reserved.update(cells)
            placed += 1
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_endpoints":
        # blank → no endpoint pairs to bridge
        return g
    if name == "single_endpoint":
        # only one cell of a color → no pair to bridge between
        g[1][3] = 4
        g[2][6] = 6
        return g
    if name == "horizontal_pair":
        # pair shares row instead of column → vertical-bridge precondition fails
        g[3][1] = 4; g[3][6] = 4
        return g
    return g
