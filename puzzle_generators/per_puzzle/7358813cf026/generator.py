"""Generator for arc_puzzle_bank_twelfth21:E80.

Rule: erase singleton-cell components, keep larger components.

Combinatorial axes (8): grid_h, grid_w, palette_kind, singletons,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_singletons, all_singletons, components_touching.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7358813cf026"
VERSION = "1.1.0"
TASK_ID = "7358813cf026"
SUMMARY = "Singleton nonzero noise is erased while larger components remain."

INVARIANTS = [
    "background is 0",
    "some components have size 1",
    "some components have size at least 2",
    "components are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_singletons", "all_singletons", "components_touching")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "4..20"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "4..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "singletons":     {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 8, 9)
        noise = ctx.draw_int("singletons", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
        noise = ctx.draw_int("singletons", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 12)
        noise = ctx.draw_int("singletons", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shapes = [[(0, 0), (0, 1), (1, 0)], [(0, 0), (1, 0), (2, 0)], [(0, 0), (0, 1)]]
    for shape in shapes:
        for _ in range(80):
            r0 = rng.randint(0, h - 3)
            c0 = rng.randint(0, w - 3)
            cells = [(r0 + dr, c0 + dc) for dr, dc in shape]
            if _free(g, cells):
                color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
                for r, c in cells:
                    g[r][c] = color
                break
    placed = 0
    for _ in range(200):
        if placed >= noise:
            break
        r, c = rng.randrange(h), rng.randrange(w)
        if _free(g, [(r, c)]):
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_singletons":
        # only multi-cell components → rule has nothing to erase, identity output
        for r, c in [(2, 2), (2, 3), (3, 2)]:
            g[r][c] = 4
        for r, c in [(5, 5), (5, 6), (6, 5)]:
            g[r][c] = 6
        return g
    if name == "all_singletons":
        # only singleton cells → rule erases everything, output is all-zero
        for r, c, v in [(1, 1, 3), (3, 5, 4), (5, 7, 5), (7, 2, 6)]:
            g[r][c] = v
        return g
    if name == "components_touching":
        # adjacent cells that look like singletons but are actually one component
        for r, c, v in [(2, 2, 3), (2, 3, 4)]:  # touching, mixed colors
            g[r][c] = v
        return g
    return g
