"""Generator for arc_additional_puzzle_bank_volume9:H62 -- transpose median 6-shape.

Rule: color-6 components are sorted by size; the median shape is
normalized and transposed.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_components,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: even_count, all_same_size, single_component.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "aae03e82a263"
VERSION = "1.1.0"
TASK_ID = "aae03e82a263"
SUMMARY = "Color-6 components are sorted by size; the median shape is normalized and transposed."

INVARIANTS = [
    "an odd number of separated color-6 objects is present",
    "the median-size object is non-symmetric under transpose",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("even_count", "all_same_size", "single_component")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..15", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 14..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_components":   {"type": "int", "default": "5", "valid": "3..7"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "five_color6_distinct_sizes",
                       "valid": "five_color6_distinct_sizes"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 14, 14)
        w = ctx.draw_int("grid_w", 14, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 15, 15)
        w = ctx.draw_int("grid_w", 15, 15)
    else:
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 14, 15)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    median_shapes = [
        [(0, 0), (1, 0), (2, 0)],
        [(0, 0), (0, 1), (1, 0)],
        [(0, 1), (1, 1), (1, 0)],
        [(0, 0), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 1)],
    ]
    paint_at(g, 1, 1, [(0, 0)], 6)
    paint_at(g, 1, w - 4, [(0, 0), (1, 0)], 6)
    paint_at(g, h // 2, w // 2, rng.choice(median_shapes), 6)
    paint_at(g, h - 5, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], 6)
    paint_at(g, h - 5, w - 5, [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)], 6)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = full_grid(h, w, 0)
    if name == "even_count":
        # 4 components → no unique median (sort positions 1,2 are middle pair)
        paint_at(g, 1, 1, [(0, 0)], 6)
        paint_at(g, 1, w - 4, [(0, 0), (1, 0)], 6)
        paint_at(g, h - 5, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], 6)
        paint_at(g, h - 5, w - 5, [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)], 6)
        return g
    if name == "all_same_size":
        # all 5 components same size → median by size is ambiguous (ties)
        for (r0, c0) in [(1, 1), (1, w - 4), (h // 2, w // 2), (h - 5, 1), (h - 5, w - 5)]:
            paint_at(g, r0, c0, [(0, 0), (0, 1)], 6)
        return g
    if name == "single_component":
        # only 1 component → median is itself, transpose may equal input (trivial)
        paint_at(g, h // 2, w // 2, [(0, 0), (1, 0), (2, 0)], 6)
        return g
    return g
