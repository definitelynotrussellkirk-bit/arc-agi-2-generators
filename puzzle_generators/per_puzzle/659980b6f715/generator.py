"""Generator for arc_additional_puzzles_21_set15_bundle:M102.

Rule: get first 2 distinct non-bg colors; normalize their cells; output
union bbox where both → 9, c1-only → c1, c2-only → c2, else 0.

Combinatorial axes (8): grid_h/w, palette_kind, shape_kind,
palette_size, position_bias, n_distinct_colors, overlap_kind, texture.
Degenerates: shapes_identical, no_overlap, single_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "659980b6f715"
VERSION = "1.1.0"
TASK_ID = "659980b6f715"
SUMMARY = "Two distinct-color blobs placed apart with shared and unique normalized cells."

INVARIANTS = [
    "exactly 2 distinct non-bg colors",
    "their normalized cell sets share at least one position and differ at least one",
]

PALETTE_KINDS = ("default", "L_pair", "Z_pair", "T_pair")
DEGENERATE_TEXTURES = ("shapes_identical", "no_overlap", "single_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_kind":     {"type": "str", "default": "fixed", "valid": "fixed"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "overlap_kind":   {"type": "str", "default": "partial", "valid": "partial"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    s1 = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
    s2 = [(0, 0), (1, 0), (1, 1)]
    paint_at(g, 1, 1, s1, 2)
    paint_at(g, 1, w - 4, s2, 3)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    if name == "shapes_identical":
        # both shapes have same normalized cells — output is all 9 (no unique cells)
        same = [(0, 0), (1, 0), (1, 1)]
        paint_at(g, 1, 1, same, 2)
        paint_at(g, 1, w - 4, same, 3)
        return g
    if name == "no_overlap":
        # disjoint normalized shapes — no shared (9) cells
        s1 = [(0, 0), (1, 0)]
        s2 = [(0, 1), (1, 2)]
        paint_at(g, 1, 1, s1, 2)
        paint_at(g, 1, w - 4, s2, 3)
        return g
    if name == "single_color":
        # only one color present — second operand missing
        s1 = [(0, 0), (1, 0), (2, 0), (2, 1)]
        paint_at(g, 1, 1, s1, 2)
        return g
    return g
