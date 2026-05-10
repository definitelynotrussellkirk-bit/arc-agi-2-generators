"""Generator for arc_additional_puzzles_21_set19_bundle:E130 — Bbox-crop of reflected non-{0,5} across 5-divider.

Rule: full-width 5-row or full-height 5-col is the divider. Reflect
non-{0,5} cells across; output is bbox-crop of reflected positions.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shape_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_shape, shape_on_divider.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "0a603c9e3e4e"
VERSION = "1.1.0"
TASK_ID = "0a603c9e3e4e"
SUMMARY = "Full 5-divider (row or col) + small shape on one side of single non-5 color."

INVARIANTS = [
    "full row/col of 5s as divider",
    "≥3 cells of one non-{0,5} color on one side, forming a shape",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_shape", "shape_on_divider")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shape_cells":  {"type": "int", "default": "rng 3..4", "valid": "3..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "shape_one_side_of_5_divider",
                       "valid": "shape_one_side_of_5_divider"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    if rng.random() < 0.5:
        gr = h // 2
        for c in range(w):
            g[gr][c] = 5
        shape = rng.choice([
            [(0, 0), (0, 1), (0, 2), (1, 1)],
            [(0, 0), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0)],
        ])
        top = rng.randint(0, gr - 3); left = rng.randint(0, w - 4)
        paint_at(g, top, left, shape, color)
    else:
        gc = w // 2
        for r in range(h):
            g[r][gc] = 5
        shape = rng.choice([
            [(0, 0), (1, 0), (2, 0), (1, 1)],
            [(0, 0), (1, 0), (1, 1)],
        ])
        top = rng.randint(0, h - 4); left = rng.randint(0, gc - 3)
        paint_at(g, top, left, shape, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # shape but no 5-divider → no reflection axis defined
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4
        return g
    if name == "no_shape":
        # divider but no shape cells → nothing to reflect
        for c in range(w): g[h // 2][c] = 5
        return g
    if name == "shape_on_divider":
        # shape cells lie on the 5-divider line itself → reflection identity
        for c in range(w): g[h // 2][c] = 5
        # overwrite some divider cells with the shape color (also a violation, but the point
        # is the rule has no clean reflection target)
        g[h // 2][2] = 4; g[h // 2][3] = 4
        return g
    return g
