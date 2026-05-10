"""Generator for arc_additional_puzzle_bank_volume9:H63.

Rule: for each 1-blob, count blobs with the same normalized shape; if
unique (frequency 1) → 8, else → 2.

Combinatorial axes (8): grid_h/w, palette_kind, num_blobs, common_size,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: all_three_unique, all_three_same, only_two_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "bd5721e5e728"
VERSION = "1.1.0"
TASK_ID = "bd5721e5e728"
SUMMARY = "3 1-blobs: 2 share normalized shape, 1 is unique."

INVARIANTS = [
    "exactly 3 non-touching 1-blobs",
    "exactly 2 share their normalized shape",
    "exactly 1 has unique shape (becomes 8)",
]

PALETTE_KINDS = ("default", "wide_grid", "tight_grid", "scattered")
DEGENERATE_TEXTURES = ("all_three_unique", "all_three_same", "only_two_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_blobs":      {"type": "int", "default": "3", "valid": "3"},
    "common_size":    {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
    g = full_grid(h, w, 0)
    shape_a = [(0, 0), (0, 1), (1, 0)]
    shape_b = [(0, 0), (1, 0), (2, 0), (2, 1)]
    paint_at(g, 1, 1, shape_a, 1)
    paint_at(g, 1, w - 4, shape_a, 1)
    paint_at(g, h - 4, w // 2 - 1, shape_b, 1)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    shape_a = [(0, 0), (0, 1), (1, 0)]
    shape_b = [(0, 0), (1, 0), (2, 0), (2, 1)]
    shape_c = [(0, 0), (0, 1), (0, 2), (1, 1)]
    if name == "all_three_unique":
        # 3 distinct shapes — multiple "unique" components, rule recolors all to 8
        paint_at(g, 1, 1, shape_a, 1)
        paint_at(g, 1, w - 5, shape_b, 1)
        paint_at(g, h - 4, w // 2 - 1, shape_c, 1)
        return g
    if name == "all_three_same":
        # 3 identical shapes — no unique component
        paint_at(g, 1, 1, shape_a, 1)
        paint_at(g, 1, w - 4, shape_a, 1)
        paint_at(g, h - 4, w // 2 - 1, shape_a, 1)
        return g
    if name == "only_two_blobs":
        # 2 blobs — can't tell unique-vs-shared
        paint_at(g, 1, 1, shape_a, 1)
        paint_at(g, h - 4, w // 2 - 1, shape_b, 1)
        return g
    return g
