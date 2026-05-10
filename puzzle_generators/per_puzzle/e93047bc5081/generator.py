"""Generator for easy_g06: shift the object one step toward the border marker.

Combinatorial axes (8): grid_h, grid_w, palette_kind, object_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_object, marker_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.blobs import grow_blob
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e93047bc5081"
VERSION = "1.1.0"
TASK_ID = "e93047bc5081"
SUMMARY = "One maroon border marker indicates the one-step shift direction for the other object."
INVARIANTS = [
    "exactly one border marker of color 9",
    "one non-marker object",
    "shifted object remains in bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_object", "marker_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "object_size":    {"type": "int", "default": "rng 4..7", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "border_marker_plus_object",
                       "valid": "border_marker_plus_object"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        size = ctx.draw_int("object_size", 4, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        size = ctx.draw_int("object_size", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        size = ctx.draw_int("object_size", 4, 7)
    rng = ctx.draw_rng("layout")
    side = rng.choice(["top", "bottom", "left", "right"])
    g = full_grid(h, w, 0)
    marker = {
        "top": (0, rng.randint(1, w - 2)),
        "bottom": (h - 1, rng.randint(1, w - 2)),
        "left": (rng.randint(1, h - 2), 0),
        "right": (rng.randint(1, h - 2), w - 1),
    }[side]
    g[marker[0]][marker[1]] = 9
    cells = grow_blob(rng, h - 4, w - 4, set(), size)
    if cells is None:
        cells = {(1, 1), (1, 2), (2, 1), (2, 2)}
    color = ctx.draw_color("object_color", exclude={0, 9})
    for r, c in cells:
        g[r + 2][c + 2] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # object without border marker → no shift direction
        g[3][3] = 4; g[3][4] = 4; g[4][3] = 4; g[4][4] = 4
        return g
    if name == "no_object":
        # marker without object → nothing to shift
        g[0][3] = 9
        return g
    if name == "marker_at_corner":
        # marker at corner cell → ambiguous side (top vs left)
        g[0][0] = 9
        g[3][3] = 4; g[3][4] = 4; g[4][3] = 4; g[4][4] = 4
        return g
    return g
