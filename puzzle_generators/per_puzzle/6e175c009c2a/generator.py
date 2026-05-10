"""Generator for arc_puzzle_bank_21_set13_bundle:easy_m07.

Rule: keep only cells with exactly one same-color orthogonal neighbor
(degree-1 cells in same-color components).

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: only_singletons, only_dense_blobs, no_shapes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6e175c009c2a"
VERSION = "1.1.0"
TASK_ID = "6e175c009c2a"
SUMMARY = "Separated line and L-shaped components for degree-1 filtering."

INVARIANTS = [
    "background is 0",
    "components of the same color do not touch",
    "components include straight lines and L-shapes",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("only_singletons", "only_dense_blobs", "no_shapes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_count":    {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "lines_and_Ls",
                       "valid": "lines_and_Ls"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _cells_clear(g, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        for rr in range(max(0, r - 1), min(h, r + 2)):
            for cc in range(max(0, c - 1), min(w, c + 2)):
                if g[rr][cc] != 0:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        shape_count = ctx.draw_int("shape_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        shape_count = ctx.draw_int("shape_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        shape_count = ctx.draw_int("shape_count", 2, 4)
    colors = ctx.draw_distinct_colors("colors", n=shape_count, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    for i, color in enumerate(colors):
        for _ in range(300):
            if i % 2 == 0:
                length = rng.randint(3, 5)
                horizontal = rng.choice([True, False])
                if horizontal:
                    r = rng.randrange(h)
                    c = rng.randint(0, w - length)
                    cells = [(r, c + dc) for dc in range(length)]
                else:
                    r = rng.randint(0, h - length)
                    c = rng.randrange(w)
                    cells = [(r + dr, c) for dr in range(length)]
            else:
                r = rng.randint(0, h - 3)
                c = rng.randint(0, w - 3)
                cells = [(r, c), (r + 1, c), (r + 2, c), (r + 2, c + 1)]
            if _cells_clear(g, cells):
                for r, c in cells:
                    g[r][c] = color
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "only_singletons":
        # all cells are singletons (degree 0) → predicate "exactly one neighbor" fails everywhere
        g[1][2] = 4; g[3][6] = 6; g[5][1] = 3; g[6][8] = 8
        return g
    if name == "only_dense_blobs":
        # solid 2x2 blobs → every cell has 2 same-color neighbors, none degree-1
        for (r, c) in [(1, 1), (1, 2), (2, 1), (2, 2)]: g[r][c] = 4
        for (r, c) in [(5, 5), (5, 6), (6, 5), (6, 6)]: g[r][c] = 6
        return g
    if name == "no_shapes":
        # blank grid → rule has nothing to filter
        return g
    return g
