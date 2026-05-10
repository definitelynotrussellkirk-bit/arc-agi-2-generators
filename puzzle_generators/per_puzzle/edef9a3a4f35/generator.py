"""Generator for arc_puzzle_bank_fifth21:E33.

Rule: each isolated cell moves one step down-right unless blocked by the edge.

Combinatorial axes (8): grid_h, grid_w, palette_kind, markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_blocked_cell, all_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "edef9a3a4f35"
VERSION = "1.1.0"
TASK_ID = "edef9a3a4f35"

SUMMARY = "Place singleton cells that move one step down-right unless blocked by the edge."

INVARIANTS = [
    "background is 0",
    "all active cells are singletons",
    "most cells have an empty down-right target",
    "at least one cell is edge-blocked and remains in place",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_blocked_cell", "all_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "markers":        {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_with_blocked_cell",
                       "valid": "scattered_with_blocked_cell"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("markers", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("markers", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("markers", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved_in: set[tuple[int, int]] = set()
    reserved_out: set[tuple[int, int]] = set()
    blocked = (rng.randrange(h), w - 1) if rng.randrange(2) else (h - 1, rng.randrange(w))
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    g[blocked[0]][blocked[1]] = color
    reserved_in.add(blocked)
    reserved_out.add(blocked)
    placed = 1
    for _ in range(300):
        if placed >= target:
            break
        r = rng.randint(0, h - 2)
        c = rng.randint(0, w - 2)
        src = (r, c)
        dst = (r + 1, c + 1)
        if src in reserved_in or dst in reserved_in or dst in reserved_out:
            continue
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        reserved_in.add(src)
        reserved_out.add(dst)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # blank → no cells to move, rule has no effect
        return g
    if name == "no_blocked_cell":
        # all cells away from right/bottom edge → all move, no anchor stays
        g[1][1] = 4; g[3][3] = 6; g[5][5] = 3
        return g
    if name == "all_at_edge":
        # all cells at right/bottom edge → all blocked, none move
        g[1][w - 1] = 4
        g[3][w - 1] = 6
        g[h - 1][2] = 3
        g[h - 1][5] = 8
        return g
    return g
