"""Generator for next_b:m13 — fill rectangles from diagonal corners.

Rule: each pair of same-color diagonal corner cells defines a
rectangle. Each rectangle is filled solid in the corner color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, collinear, single_endpoint.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b7d9205dd62d"
VERSION = "1.1.0"
TASK_ID = "b7d9205dd62d"
SUMMARY = "2 same-color corner pairs at diagonal positions, distinct colors per pair."

INVARIANTS = [
    "background is 0",
    "2 pairs of cells; each pair is same color and at diagonal-corner positions",
    "the 2 rectangles do not overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "collinear", "single_endpoint")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "non_overlapping",
                       "valid": "non_overlapping"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 2)
    used_cells = set()
    for color in palette:
        for _ in range(60):
            r1 = rng.randint(0, h - 3)
            r2 = rng.randint(r1 + 2, min(h - 1, r1 + 4))
            c1 = rng.randint(0, w - 3)
            c2 = rng.randint(c1 + 2, min(w - 1, c1 + 4))
            # rectangle cells (interior + border)
            cells = {(r, c) for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)}
            if cells & used_cells: continue
            # place corners only (TL+BR or TR+BL)
            if rng.random() < 0.5:
                g[r1][c1] = color; g[r2][c2] = color
            else:
                g[r1][c2] = color; g[r2][c1] = color
            used_cells |= cells
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Lone cells, no diagonal-corner pairs — rule has no rectangles to fill.
        g[2][3] = 4; g[6][8] = 5
        return g
    if name == "collinear":
        # Same-color pair on same row — rectangle would degenerate to a line.
        g[3][2] = 4; g[3][7] = 4
        return g
    if name == "single_endpoint":
        # Only one corner of a pair present — rule has no second anchor.
        g[1][1] = 4
        return g
    return g
