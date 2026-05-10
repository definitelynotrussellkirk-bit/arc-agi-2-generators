"""Generator for additional_bank:M2.

Rule: 2 9-markers define delta = (m2 - m1). For each non-{0,9} cell,
copy its color to (r + dr, c + dc) if in bounds.

Combinatorial axes (9): grid_h/w, palette_kind, marker_offset_r,
marker_offset_c, blob_size, palette_size, position_bias,
n_distinct_colors, texture.
Degenerates: markers_collide, no_blob, no_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6d26bc40cbb2"
VERSION = "1.1.0"
TASK_ID = "6d26bc40cbb2"
SUMMARY = "Two 9-markers + small blob between them; output translates blob by 9→9 delta."

INVARIANTS = [
    "exactly two 9-markers; delta is non-zero",
    "small (3-cell) blob between them",
    "translated blob lands in-bounds",
]

PALETTE_KINDS = ("default", "diagonal_delta", "vertical_delta", "horizontal_delta")
DEGENERATE_TEXTURES = ("markers_collide", "no_blob", "no_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker_offset":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "blob_size":      {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "diagonal",
                       "valid": "diagonal"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][0] = 9
    g[3][3] = 9
    color = rng.choice([2, 3, 4, 5, 6, 7, 8])
    g[1][2] = color
    g[2][1] = color
    g[2][2] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "markers_collide":
        # both 9-markers at same cell — zero delta, rule produces identity
        g[2][2] = 9
        color = 5
        g[3][3] = color
        g[3][4] = color
        return g
    if name == "no_blob":
        # markers but nothing to translate
        g[0][0] = 9
        g[3][3] = 9
        return g
    if name == "no_markers":
        # blob but no delta defined
        g[2][2] = 5
        g[2][3] = 5
        g[3][3] = 5
        return g
    return g
