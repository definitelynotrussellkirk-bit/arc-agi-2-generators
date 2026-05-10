"""Generator for arc_puzzle_bank_eighth_21_bundle:easy_55_move_object_to_marker.

Rule: a small object and a 9 marker; the object is pasted at the marker.

Combinatorial axes (8): grid_h, grid_w, palette_kind, object_color,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_object, multiple_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d172afae0ee5"
VERSION = "1.1.0"
TASK_ID = "d172afae0ee5"
SUMMARY = "A small object and a 9 marker; the object is pasted at the marker."

INVARIANTS = [
    "background is 0",
    "there is exactly one 9 marker",
    "all non-marker nonzero cells form one object bbox",
    "the marker position can fit the object's crop in-bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_object", "multiple_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "object_color":   {"type": "color", "default": "rng", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "object_left_marker_right",
                       "valid": "object_left_marker_right"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 13)
    color = ctx.draw_color("object_color", exclude={0, 9})
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)

    shape = [(0, 0), (1, 0), (2, 0), (2, 1)]
    rr = rng.randint(1, h - 4)
    rc = rng.randint(1, max(1, w // 2 - 2))
    for dr, dc in shape:
        g[rr + dr][rc + dc] = color
    mr = rng.randint(0, h - 3)
    mc = rng.randint(max(w // 2, rc + 3), w - 2)
    g[mr][mc] = 9
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # object only, no 9 marker → no destination position
        for (r, c) in [(2, 1), (3, 1), (4, 1), (4, 2)]: g[r][c] = 4
        return g
    if name == "no_object":
        # marker only, no object → nothing to paste
        g[3][7] = 9
        return g
    if name == "multiple_markers":
        # multiple 9-markers → "the marker" ambiguous
        for (r, c) in [(2, 1), (3, 1), (4, 1), (4, 2)]: g[r][c] = 4
        g[3][6] = 9; g[5][7] = 9; g[6][8] = 9
        return g
    return g
