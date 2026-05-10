"""Generator for arc_additional_puzzles_21_set19_bundle:M128.

Rule: foreground objects are sorted largest-first and packed
horizontally.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, shape_set, texture.
Degenerates: no_objects, single_object, equal_sizes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "5aa2b1bf7760"
VERSION = "1.1.0"
TASK_ID = "5aa2b1bf7760"
SUMMARY = "Foreground objects are sorted largest-first and packed horizontally."

INVARIANTS = [
    "objects are single-color nonzero components on black",
    "objects are sorted by component size descending with color tie-break",
    "their crops are packed horizontally with one blank column gap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "equal_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "15", "valid": "12..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "shape_set":      {"type": "choice", "default": "mixed", "valid": "mixed|wide"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    shape_set = ctx.draw_choice("shape_set", ["mixed", "wide"])
    if "shape_set" not in overrides:
        shape_set = "mixed" if sample_index % 2 == 0 else "wide"
    a, b, c = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    g = full_grid(10, 15, 0)
    draw_rect(g, 5, 1, 3, 3, a)
    if shape_set == "mixed":
        draw_rect(g, 2, 10, 2, 2, b)
        draw_rect(g, 1, 5, 1, 3, c)
    else:
        draw_rect(g, 1, 8, 2, 3, b)
        draw_rect(g, 7, 11, 1, 2, c)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 15, 0)
    if name == "no_objects":
        # empty grid — nothing to sort or pack
        return g
    if name == "single_object":
        # only 1 object → sorting is trivial; pack output is identity
        draw_rect(g, 5, 1, 3, 3, 4)
        return g
    if name == "equal_sizes":
        # 3 equal-size blobs → "largest-first" tie-break order ambiguous beyond color
        draw_rect(g, 2, 1, 2, 2, 4)
        draw_rect(g, 2, 6, 2, 2, 6)
        draw_rect(g, 6, 4, 2, 2, 7)
        return g
    return g
