"""Generator for v0_original:easy_06.

Rule: isolated nonzero cells (no 4-neighbor of same component) recolor
to cyan; connected clusters remain unchanged.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, isolated, texture.
Degenerates: no_isolated, all_clusters, all_isolated.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f3a411af02b9"
VERSION = "1.1.0"
TASK_ID = "f3a411af02b9"

SUMMARY = "Isolated nonzero cells recolor to cyan while connected clusters remain unchanged."

INVARIANTS = [
    "background is 0",
    "some nonzero cells are 4-isolated",
    "some nonzero cells belong to components of size at least 2",
    "input avoids cyan isolated cells so recoloring is visible",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_isolated", "all_clusters", "all_isolated")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "4..22"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "4..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "isolated":       {"type": "int", "default": "rng 3..6", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "scattered_isolated_and_clusters",
                       "valid": "scattered_isolated_and_clusters"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "2..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        if not (0 <= r < h and 0 <= c < w):
            return False
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("isolated", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 16)
        w = ctx.draw_int("grid_w", 14, 18)
        target = ctx.draw_int("isolated", 5, 8)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 14)
        target = ctx.draw_int("isolated", 3, 6)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for shape in [[(0, 0), (0, 1), (1, 0)], [(0, 0), (1, 0), (2, 0)]]:
        for _ in range(80):
            r0 = rng.randint(0, h - 3)
            c0 = rng.randint(0, w - 3)
            cells = [(r0 + dr, c0 + dc) for dr, dc in shape]
            if _free(g, cells):
                color = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
                for r, c in cells:
                    g[r][c] = color
                break
    placed = 0
    for _ in range(200):
        if placed >= target:
            break
        r, c = rng.randrange(h), rng.randrange(w)
        if _free(g, [(r, c)]):
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 9])
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_isolated":
        # Only multi-cell clusters, no isolated singletons — rule's
        # "isolated → cyan" branch never fires; output equals input.
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 4
        for r, c in [(5, 6), (5, 7), (6, 6)]: g[r][c] = 6
        return g
    if name == "all_clusters":
        # Same as no_isolated, named differently — every component is
        # multi-cell.
        for r, c in [(2, 2), (3, 2)]: g[r][c] = 4
        for r, c in [(5, 6), (5, 7)]: g[r][c] = 6
        return g
    if name == "all_isolated":
        # Every nonzero cell is isolated — rule's "kept cluster"
        # branch never fires; ALL non-bg cells become cyan,
        # eliminating color information from input.
        g[1][2] = 4; g[3][6] = 6; g[5][3] = 7; g[7][8] = 9
        return g
    return g
