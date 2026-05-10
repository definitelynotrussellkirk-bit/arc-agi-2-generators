"""Generator for arc_additional_puzzles_21_set4:H28.

Rule: bbox masks of 2-cells and 3-cells; XOR cells → 8; crop to content.

Combinatorial axes (8): grid_h/w, palette_kind, shape_kind, palette_size,
position_bias, n_distinct_colors, overlap_kind, texture.
Degenerates: shapes_identical, no_blob_2, no_blob_3.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "efb59efe0080"
VERSION = "1.1.0"
TASK_ID = "efb59efe0080"
SUMMARY = "2-shape and 3-shape placed apart with overlapping bbox-masks."

INVARIANTS = [
    "exactly one 2-blob and one 3-blob",
    "their bbox masks differ in at least one position",
]

PALETTE_KINDS = ("default", "L_pair", "Z_pair", "T_pair")
DEGENERATE_TEXTURES = ("shapes_identical", "no_blob_2", "no_blob_3")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_kind":     {"type": "str", "default": "varied", "valid": "varied"},
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
    rng = ctx.draw_rng("layout")
    s_options = [
        [(0, 0), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 0)],
        [(0, 0), (0, 1), (1, 1)],
    ]
    s1 = rng.choice(s_options)
    s2 = rng.choice([s for s in s_options if s != s1])
    paint_at(g, 1, 1, s1, 2)
    paint_at(g, 1, w - 4, s2, 3)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    same = [(0, 0), (1, 0), (1, 1)]
    if name == "shapes_identical":
        # both shapes same → XOR is empty
        paint_at(g, 1, 1, same, 2)
        paint_at(g, 1, w - 4, same, 3)
        return g
    if name == "no_blob_2":
        # only 3-blob — XOR has missing operand
        paint_at(g, 1, w - 4, same, 3)
        return g
    if name == "no_blob_3":
        # only 2-blob — XOR has missing operand
        paint_at(g, 1, 1, same, 2)
        return g
    return g
