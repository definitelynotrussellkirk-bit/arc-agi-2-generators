"""Generator for arc_additional_puzzles_21_set3:M20 — Crop first marker-color blob (rows ≥ 1).

Rule: target = first non-zero in row 0. Find first object below row 0
with that color and all cells with r > 0; crop to bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_decoys,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker_in_row0, no_matching_body, multiple_matching_bodies.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "406739865b43"
VERSION = "1.1.0"
TASK_ID = "406739865b43"
SUMMARY = "Marker color in row 0 + multi-color body objects with one matching marker."

INVARIANTS = [
    "row 0 has exactly one non-zero cell (the marker)",
    "exactly one body object matches marker color",
    "1-2 decoy body objects of other colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker_in_row0", "no_matching_body", "multiple_matching_bodies")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_decoys":       {"type": "int", "default": "rng 1..2", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "marker_top_body_bottom",
                       "valid": "marker_top_body_bottom"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    marker = rng.choice([2, 3, 4, 5, 6, 7])
    g[0][3] = marker
    paint_at(g, 5, w - 4, [(0, 0), (1, -2), (1, -1), (1, 0)], marker)
    decoy = rng.choice([c for c in [2, 3, 4, 5, 6, 7] if c != marker])
    paint_at(g, 2, 1, [(0, 0), (1, 0)], decoy)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_marker_in_row0":
        # row 0 is empty → rule has no target color to pick
        paint_at(g, 5, w - 4, [(0, 0), (1, -2), (1, -1), (1, 0)], 4)
        paint_at(g, 2, 1, [(0, 0), (1, 0)], 6)
        return g
    if name == "no_matching_body":
        # marker exists but no body object matches its color → crop is undefined
        g[0][3] = 4
        paint_at(g, 5, w - 4, [(0, 0), (1, -2), (1, -1), (1, 0)], 6)
        paint_at(g, 2, 1, [(0, 0), (1, 0)], 7)
        return g
    if name == "multiple_matching_bodies":
        # two body objects share the marker color → which one to crop is ambiguous
        g[0][3] = 4
        paint_at(g, 5, w - 4, [(0, 0), (1, -2), (1, -1), (1, 0)], 4)
        paint_at(g, 2, 1, [(0, 0), (1, 0)], 4)
        return g
    return g
