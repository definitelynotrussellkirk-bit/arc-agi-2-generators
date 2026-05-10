"""Generator for arc_puzzle_bank_eighth21:E52 — diagonal length-3 midpoint fill.

Rule: each pair of same-color cells at a length-3 diagonal has its
zero midpoint filled.

Combinatorial axes (8): grid_h, grid_w, palette_kind, bridges,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, axis_aligned, midpoint_blocked.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "56169a1e5c1d"
VERSION = "1.1.0"
TASK_ID = "56169a1e5c1d"

SUMMARY = "Fill the midpoint between matching endpoints of a length-3 diagonal."

INVARIANTS = [
    "background is 0",
    "each active color appears as diagonal endpoints two steps apart",
    "the diagonal midpoint is initially zero",
    "bridge motifs are separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "axis_aligned", "midpoint_blocked")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "bridges":        {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "= bridges", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_diagonal_bridges",
                       "valid": "scattered_diagonal_bridges"},
    "n_distinct_colors": {"type": "int", "default": "= bridges", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear(g, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        for rr in range(max(0, r - 1), min(h, r + 2)):
            for cc in range(max(0, c - 1), min(w, c + 2)):
                if g[rr][cc] != 0:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("bridges", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 14)
        target = ctx.draw_int("bridges", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("bridges", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], target)
    placed = 0
    for color in colors:
        for _ in range(120):
            dr = rng.choice([-1, 1])
            dc = rng.choice([-1, 1])
            r1 = rng.randint(2 if dr < 0 else 0, h - 3 if dr > 0 else h - 1)
            c1 = rng.randint(2 if dc < 0 else 0, w - 3 if dc > 0 else w - 1)
            r2, c2 = r1 + 2 * dr, c1 + 2 * dc
            cells = [(r1, c1), (r1 + dr, c1 + dc), (r2, c2)]
            if _clear(g, cells):
                g[r1][c1] = color
                g[r2][c2] = color
                placed += 1
                break
    if placed == 0:
        raise ValueError("could not place diagonal bridge")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Singletons only — rule has no diagonal pair to bridge.
        g[1][1] = 3; g[3][6] = 4; g[6][2] = 5
        return g
    if name == "axis_aligned":
        # Same-color pairs at distance 2 but axis-aligned (not diagonal)
        # — rule's diagonal filter doesn't match.
        g[2][1] = 3; g[2][3] = 3
        g[5][3] = 5; g[5][5] = 5
        return g
    if name == "midpoint_blocked":
        # Diagonal pair correctly placed, but the midpoint is already
        # non-zero (different color) — rule cannot fill it cleanly.
        g[1][1] = 4; g[3][3] = 4; g[2][2] = 7
        return g
    return g
