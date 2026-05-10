"""Generator for arc_additional_puzzle_bank_volume15:H105 — XOR of largest 1-shape and largest 2-shape, painted 8.

Rule: take largest 1-blob and largest 2-blob; normalize cells; XOR
sets; bbox-crop output painted as 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_pair,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blobs, identical_shapes, only_one_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "d1dd527dba87"
VERSION = "1.1.0"
TASK_ID = "d1dd527dba87"
SUMMARY = "Two blobs (color 1 and color 2) at different locations; their normalized shapes XOR-differ."

INVARIANTS = [
    "exactly one largest 1-blob and one largest 2-blob",
    "their normalized cells are not identical",
    "tiny decoration (color 5) for noise",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blobs", "identical_shapes", "only_one_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_pair":     {"type": "int", "default": "rng 0..5", "valid": "0..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "two_distinct_blobs_plus_decoration",
                       "valid": "two_distinct_blobs_plus_decoration"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    shapes = [
        [(0, 0), (0, 1), (0, 2), (1, 1)],
        [(0, 0), (1, 0), (0, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (1, 0), (1, 1)],
        [(0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (0, 1), (0, 2)],
    ]
    s1 = rng.choice(shapes); s2 = rng.choice(shapes)
    while sorted(s1) == sorted(s2):
        s2 = rng.choice(shapes)
    r1 = rng.randint(0, 2); c1 = rng.randint(1, 3)
    r2 = rng.randint(4, h - 3); c2 = rng.randint(w - 5, w - 3)
    paint_at(g, r1, c1, s1, 1)
    paint_at(g, r2, c2, s2, 2)
    g[h - 1][w - 1] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_blobs":
        # blank → no blobs to XOR
        return g
    if name == "identical_shapes":
        # both blobs share same normalized shape → XOR is empty (rule output blank)
        cells = [(0, 0), (0, 1), (1, 0), (1, 1)]
        paint_at(g, 1, 1, cells, 1)
        paint_at(g, 5, 8, cells, 2)
        g[h - 1][w - 1] = 5
        return g
    if name == "only_one_color":
        # only one of {1, 2} present → "largest of each color" precondition fails
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 1)
        return g
    return g
