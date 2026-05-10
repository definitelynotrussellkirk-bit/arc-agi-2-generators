"""Generator for 7b:m49 — draw rect from same-color diagonal pairs.

Rule: each color appearing twice (at diagonal corners) → fill the
bbox rectangle in that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, collinear_pair, overlapping_bboxes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1713e09a3132"
VERSION = "1.1.0"
TASK_ID = "1713e09a3132"
SUMMARY = "2-3 colors each at diagonal corners of non-overlapping rectangles."

INVARIANTS = [
    "background is 0",
    "each non-zero color appears at 2 diagonal corners of a rectangle",
    "rectangles don't overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "collinear_pair", "overlapping_bboxes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "diagonal_corner_pairs",
                       "valid": "diagonal_corner_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
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
        n = ctx.draw_int("n_pairs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        n = ctx.draw_int("n_pairs", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 13)
        n = ctx.draw_int("n_pairs", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    reserved: set[tuple[int, int]] = set()
    for color in palette:
        for _ in range(40):
            r1 = rng.randint(0, h - 3)
            c1 = rng.randint(0, w - 3)
            r2 = rng.randint(r1 + 2, min(h - 1, r1 + 4))
            c2 = rng.randint(c1 + 2, min(w - 1, c1 + 4))
            cells = {(r, c) for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)}
            if cells & reserved:
                continue
            if rng.random() < 0.5:
                g[r1][c1] = color; g[r2][c2] = color
            else:
                g[r1][c2] = color; g[r2][c1] = color
            reserved |= cells
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # single cells per color → bbox can't be defined
        g[2][2] = 4; g[5][7] = 6
        return g
    if name == "collinear_pair":
        # both cells in same row → degenerate to a line, no rect interior
        g[3][1] = 4; g[3][8] = 4
        return g
    if name == "overlapping_bboxes":
        # two pairs whose rectangles overlap → fill conflict
        g[1][1] = 4; g[6][6] = 4
        g[3][3] = 6; g[8][8] = 6
        return g
    return g
