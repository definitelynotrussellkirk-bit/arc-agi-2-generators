"""Generator for next_b:m08 — complete rectangle borders from diagonal corners.

Rule: each pair of same-color diagonal corner cells defines a
rectangle. Each rectangle's outline (border only) is drawn in the
corner color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_corners, single_corner, collinear_corners.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f06b9f1a5114"
VERSION = "1.1.0"
TASK_ID = "f06b9f1a5114"
SUMMARY = "2 same-color corner pairs at diagonal positions; rule draws their outlines."

INVARIANTS = [
    "background is 0",
    "2 pairs of cells; each pair is same color and at diagonal-corner positions",
    "the 2 rectangles do not overlap",
    "each rectangle is at least 3x3 so its outline differs from the 2-corner input",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corners", "single_corner", "collinear_corners")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "diagonal_corner_pairs",
                       "valid": "diagonal_corner_pairs"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 2)
    used_cells = set()
    for color in palette:
        for _ in range(60):
            r1 = rng.randint(0, h - 4)
            r2 = rng.randint(r1 + 3, min(h - 1, r1 + 5))
            c1 = rng.randint(0, w - 4)
            c2 = rng.randint(c1 + 3, min(w - 1, c1 + 5))
            cells = {(r, c) for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)}
            if cells & used_cells: continue
            if rng.random() < 0.5:
                g[r1][c1] = color; g[r2][c2] = color
            else:
                g[r1][c2] = color; g[r2][c1] = color
            used_cells |= cells
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 12
    g = full_grid(h, w, 0)
    if name == "no_corners":
        # Empty grid — no diagonal corner pair to expand.
        return g
    if name == "single_corner":
        # Only one cell of each color — no pair, so no rectangle is
        # implied and the rule has nothing to outline.
        g[2][2] = 4
        g[7][8] = 6
        return g
    if name == "collinear_corners":
        # Same-color cells on the same row (not diagonal) — no rectangle
        # is defined, just a line, so the rule's outline is degenerate.
        g[2][1] = 4; g[2][6] = 4
        g[7][2] = 6; g[7][8] = 6
        return g
    return g
