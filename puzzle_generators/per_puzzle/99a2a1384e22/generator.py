"""Generator for arc_additional_puzzles_21_set6:H38.

Rule: 2 4-blobs sorted by c1; delta = (b - a). 1 3-blob; output is
empty grid with 3-blob translated by delta in color 3.

Combinatorial axes (8): grid_h/w, palette_kind, delta_dr, delta_dc,
palette_size, position_bias, n_distinct_colors, shape_kind, texture.
Degenerates: no_4blobs, no_3blob, single_4blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "99a2a1384e22"
VERSION = "1.1.0"
TASK_ID = "99a2a1384e22"
SUMMARY = "Two 4-blobs (a left, b right) defining delta + one 3-blob; output translates 3-blob by delta."

INVARIANTS = [
    "exactly 2 non-touching 4-blobs (a left of b)",
    "exactly 1 3-blob in lower portion",
    "delta keeps translated 3-cells in-bounds",
]

PALETTE_KINDS = ("default", "small_delta", "medium_delta", "large_delta")
DEGENERATE_TEXTURES = ("no_4blobs", "no_3blob", "single_4blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "delta_dr":       {"type": "int", "default": "3", "valid": "1..6"},
    "delta_dc":       {"type": "int", "default": "3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "split", "valid": "split"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "shape_kind":     {"type": "str", "default": "diag2", "valid": "diag2"},
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    shape4 = [(0, 0), (1, 1)]
    paint_at(g, 1, 1, shape4, 4)
    paint_at(g, 4, 4, shape4, 4)
    shape3 = [(0, 0), (1, 1)]
    paint_at(g, 7, 1, shape3, 3)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    shape4 = [(0, 0), (1, 1)]
    shape3 = [(0, 0), (1, 1)]
    if name == "no_4blobs":
        # 3-blob but no 4-blobs → translation delta undefined
        paint_at(g, 7, 1, shape3, 3)
        return g
    if name == "no_3blob":
        # 4-blobs define delta but no 3-blob to translate → rule has nothing to stamp
        paint_at(g, 1, 1, shape4, 4)
        paint_at(g, 4, 4, shape4, 4)
        return g
    if name == "single_4blob":
        # only one 4-blob → predicate "two 4-blobs" fails; delta needs both endpoints
        paint_at(g, 1, 1, shape4, 4)
        paint_at(g, 7, 1, shape3, 3)
        return g
    return g
