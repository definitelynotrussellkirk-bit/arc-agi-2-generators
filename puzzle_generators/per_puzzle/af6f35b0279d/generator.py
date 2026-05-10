"""Generator for arc_puzzle_bank_21_set11_bundle:medium_k08.

Rule: corner-marker = first non-zero corner cell. Color = its value.
Clean corners; output bbox-crop of color-blob.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_decoys,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_corner_marker, no_match, multiple_matches.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "af6f35b0279d"
VERSION = "1.1.0"
TASK_ID = "af6f35b0279d"
SUMMARY = "Corner marker (color C) + 1 blob of color C in body + 1-2 decoys."

INVARIANTS = [
    "exactly one non-zero corner cell (the marker)",
    "exactly one body blob of marker color",
    "1-2 decoy body blobs of other colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corner_marker", "no_match", "multiple_matches")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_decoys":       {"type": "int", "default": "rng 1..2", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "corner_top_left",
                       "valid": "corner_top_left"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    color = rng.choice([2, 3, 4, 6, 7, 8, 9])
    g[0][0] = color
    paint_at(g, 1, 1, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], color)
    decoy = rng.choice([c for c in [2, 3, 4, 6, 7, 8, 9] if c != color])
    paint_at(g, 5, 5, [(0, 0), (0, 1), (0, 2), (1, 1)], decoy)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_corner_marker":
        # all corners empty → no color selector, rule has no anchor
        paint_at(g, 1, 1, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], 4)
        paint_at(g, 5, 5, [(0, 0), (0, 1), (0, 2), (1, 1)], 6)
        return g
    if name == "no_match":
        # corner marker color doesn't appear in body → rule has no blob to crop
        g[0][0] = 4
        paint_at(g, 5, 5, [(0, 0), (0, 1), (0, 2), (1, 1)], 6)
        return g
    if name == "multiple_matches":
        # two body blobs share the marker color → which one to crop is ambiguous
        g[0][0] = 4
        paint_at(g, 1, 1, [(0, 0), (1, 0), (2, 0)], 4)
        paint_at(g, 5, 5, [(0, 0), (0, 1), (0, 2)], 4)
        return g
    return g
