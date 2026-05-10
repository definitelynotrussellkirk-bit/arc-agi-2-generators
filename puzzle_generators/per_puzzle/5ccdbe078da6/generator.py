"""Generator for v0_original:medium_02 — paint rectangle border between same-color pairs.

Rule: for each color that appears exactly 2 times, draw the rectangle border
through those 2 corner cells in that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_pairs, texture.
Degenerates: no_pairs, single_marker, collinear_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5ccdbe078da6"
VERSION = "1.1.0"
TASK_ID = "5ccdbe078da6"

SUMMARY = "1-2 pairs of cells in distinct colors at corner positions of a rectangle."

INVARIANTS = [
    "background is 0",
    "1-2 pairs of cells in distinct colors; each pair forms diagonal corners of a non-degenerate rectangle (≥2×2)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_marker", "collinear_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "= n_pairs", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "scattered_corner_pairs",
                       "valid": "scattered_corner_pairs"},
    "n_distinct_colors": {"type": "int", "default": "= n_pairs", "valid": "1..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
        n = ctx.draw_int("n_pairs", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 11)
        n = ctx.draw_int("n_pairs", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 6, 8)
        n = ctx.draw_int("n_pairs", 1, 2)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
        ok = True
        for color in colors:
            placed = False
            for _ in range(80):
                r1 = rng.randint(0, h - 2); c1 = rng.randint(0, w - 2)
                r2 = rng.randint(r1 + 1, h - 1); c2 = rng.randint(c1 + 1, w - 1)
                if g[r1][c1] != 0 or g[r2][c2] != 0: continue
                g[r1][c1] = color
                g[r2][c2] = color
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 6, 7
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule has no corner pairs to expand into rectangles.
        return g
    if name == "single_marker":
        # Color appears once — rule's "exactly twice" filter excludes;
        # the rectangle is undefined from a single point.
        g[2][2] = 4
        return g
    if name == "collinear_pair":
        # Same color twice on a shared row or column — implied
        # rectangle is 1-D, rule's border degenerates to a line.
        g[3][1] = 4; g[3][5] = 4
        return g
    return g
