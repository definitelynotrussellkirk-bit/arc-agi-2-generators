"""Generator for arc_additional_puzzle_bank_volume20:M140 — crop nearest object to red marker.

Rule: the colored object nearest the red marker is cropped out as the
output.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_objects, tied_distances.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4fe33a81bf48"
VERSION = "1.1.0"
TASK_ID = "4fe33a81bf48"
SUMMARY = "The colored object nearest the red marker is cropped out as the output."

INVARIANTS = [
    "background is 0",
    "there is exactly one red marker",
    "non-marker objects are separated colored components",
    "one object is uniquely nearest to the marker",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_objects", "tied_distances")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..14", "valid": "6..24"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "6..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "marker_center_with_distractors",
                       "valid": "marker_center_with_distractors"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 14)
        w = ctx.draw_int("grid_w", 9, 14)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    marker = (h // 2, w // 2)
    g[marker[0]][marker[1]] = 2
    near_color = rng.choice([3, 4, 6, 7, 8, 9])
    nr = marker[0]
    nc = max(0, marker[1] - 3)
    for r, c in [(nr, nc), (nr, nc + 1), (nr + 1, nc)]:
        g[r][c] = near_color
    far_specs = [
        (1, 1, 5, [(0, 0), (0, 1), (1, 1)]),
        (h - 3, w - 3, 1, [(0, 0), (1, 0), (1, 1), (1, 2)]),
    ]
    for r0, c0, color, cells in far_specs:
        if color == near_color:
            color = 6 if near_color != 6 else 7
        for dr, dc in cells:
            g[r0 + dr][c0 + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # objects but no red marker → no anchor for "nearest" calculation
        for r, c in [(1, 1), (1, 2), (2, 2)]: g[r][c] = 4
        for r, c in [(7, 7), (7, 8), (8, 7)]: g[r][c] = 6
        return g
    if name == "no_objects":
        # marker but no other components → nothing to crop
        g[5][5] = 2
        return g
    if name == "tied_distances":
        # two equidistant objects → ambiguous "nearest"
        g[5][5] = 2
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 4   # NW, dist ~3
        for r, c in [(7, 7), (8, 7), (8, 8)]: g[r][c] = 6   # SE, dist ~3 (tied)
        return g
    return g
