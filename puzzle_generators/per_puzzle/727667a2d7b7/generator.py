"""Generator for arc_additional_puzzle_bank_volume6:M40.

Rule: each blue object rotates inside its local box according to the
marker value above it (1=identity, 2=cw90, 3=180, 4=ccw90).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, marker_zero, marker_misaligned.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "727667a2d7b7"
VERSION = "1.1.0"
TASK_ID = "727667a2d7b7"
SUMMARY = "Each blue object rotates inside its local box according to the marker above it."

INVARIANTS = [
    "background is 0",
    "blue objects are separated and have square local boxes",
    "each blue object has a control value immediately above its bbox top-left",
    "controls use values 1 through 4",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "marker_zero", "marker_misaligned")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "2", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "spread_corners",
                       "valid": "spread_corners"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..5"},
    "density":        {"type": "str", "default": "low", "valid": "low"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 10, 14)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    anchors = [(2, 1), (2, w - 5), (h - 4, 1)]
    rng.shuffle(anchors)
    codes = [rng.choice([2, 3, 4]), rng.choice([1, 2, 3, 4])]
    for i, (r0, c0) in enumerate(anchors[:2]):
        g[r0 - 1][c0] = codes[i]
        for dr, dc in [(0, 0), (0, 1), (1, 0), (2, 0)]:
            g[r0 + dr][c0 + dc] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # blue object with no control value above → rotation undefined
        for dr, dc in [(0, 0), (0, 1), (1, 0), (2, 0)]:
            g[3 + dr][2 + dc] = 6
        for dr, dc in [(0, 0), (0, 1), (1, 0), (2, 0)]:
            g[3 + dr][8 + dc] = 6
        return g
    if name == "marker_zero":
        # marker value of 0 (background) → not a valid control code
        g[2][2] = 0
        for dr, dc in [(0, 0), (0, 1), (1, 0), (2, 0)]:
            g[3 + dr][2 + dc] = 6
        return g
    if name == "marker_misaligned":
        # marker not directly above the object's bbox top-left → matching fails
        g[2][5] = 3
        for dr, dc in [(0, 0), (0, 1), (1, 0), (2, 0)]:
            g[3 + dr][2 + dc] = 6
        return g
    return g
