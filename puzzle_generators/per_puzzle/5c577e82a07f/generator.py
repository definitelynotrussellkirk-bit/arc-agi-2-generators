"""Generator for v3_rich_schema:easy_05_complete_rectangle_borders_from_corners — fill borders from 4 corners.

Rule: 4 cells of the same color form the corners of an axis-aligned
rectangle; output fills the rectangle's border (4 edges) with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_corners, three_corners, collinear_corners.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5c577e82a07f"
VERSION = "1.1.0"
TASK_ID = "5c577e82a07f"

SUMMARY = "1-2 sets of 4 corner cells (each set in a distinct color, defining a rectangle)."

INVARIANTS = [
    "background is 0",
    "1-2 sets of 4 cells in distinct colors; each set forms a non-degenerate rectangle (≥3×3)",
    "the 4 cells of each set are at the corners only",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corners", "three_corners", "collinear_corners")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "n_rects":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "rect_corners",
                       "valid": "rect_corners"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..2"},
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
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 8, 9)
        n = ctx.draw_int("n_rects", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 10, 13)
        n = ctx.draw_int("n_rects", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 10)
        n = ctx.draw_int("n_rects", 1, 2)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
        ok = True
        for color in colors:
            placed = False
            for _ in range(80):
                r1 = rng.randint(0, h - 3); r2 = rng.randint(r1 + 2, h - 1)
                c1 = rng.randint(0, w - 3); c2 = rng.randint(c1 + 2, w - 1)
                if not _free(g, r1, c1, r2, c2): continue
                g[r1][c1] = color
                g[r1][c2] = color
                g[r2][c1] = color
                g[r2][c2] = color
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize layout")


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_corners":
        # No corner markers — rule has nothing to complete; output
        # equals input.
        return g
    if name == "three_corners":
        # 3 corners (missing one) — the 4-corner premise fails;
        # rule's border-fill is undefined.
        g[1][1] = 4; g[1][6] = 4; g[5][1] = 4
        return g
    if name == "collinear_corners":
        # 4 markers all in a single row — they don't define a
        # rectangle; rule's border-fill is degenerate.
        g[3][1] = 4; g[3][3] = 4; g[3][5] = 4; g[3][7] = 4
        return g
    return g
