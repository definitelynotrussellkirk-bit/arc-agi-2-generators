"""Generator for arc_additional_puzzles_21_set2:H8 — Hstack object crops sorted by size desc.

Rule: extract every connected non-bg object; sort by (size desc, r1 asc,
c1 asc); hstack their bbox crops with 1-col gaps.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes, single_object, no_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "c464f6b94fbb"
VERSION = "1.1.0"
TASK_ID = "c464f6b94fbb"
SUMMARY = "3 distinct-color shapes of distinct sizes, well-separated."

INVARIANTS = [
    "exactly 3 connected non-bg objects",
    "objects have distinct colors and distinct sizes",
    "objects don't touch or overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "single_object", "no_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread",
                       "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 13, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 13, 15)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = rng.sample([2, 3, 4, 6, 7, 8, 9], 3)
    s_big = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)]
    s_med = [(0, 0), (0, 1), (0, 2), (1, 1)]
    s_sml = [(0, 0), (0, 1), (0, 2)]
    paint_at(g, 1, 1, s_big, palette[0])
    paint_at(g, 1, 8, s_med, palette[1])
    paint_at(g, h - 3, 2, s_sml, palette[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 14
    g = full_grid(h, w, 0)
    s_med = [(0, 0), (0, 1), (0, 2), (1, 1)]
    if name == "tied_sizes":
        # two objects same size → sort order by size is ambiguous
        paint_at(g, 1, 1, s_med, 4)
        paint_at(g, 1, 8, s_med, 6)
        paint_at(g, h - 3, 5, [(0, 0), (0, 1)], 7)
        return g
    if name == "single_object":
        # one object → hstack of one is trivial, no comparison
        paint_at(g, 3, 4, s_med, 6)
        return g
    if name == "no_objects":
        # empty grid → nothing to extract or stack
        return g
    return g
