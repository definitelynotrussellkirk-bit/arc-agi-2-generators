"""Generator for arc_additional_puzzle_bank_volume12:H80 — stamp prototype copies via control codes.

Rule: gray anchors with control cells above stamp transformed copies of
a maroon prototype.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_anchors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_prototype, no_anchors, missing_control.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "274345a1792c"
VERSION = "1.1.0"
TASK_ID = "274345a1792c"
SUMMARY = "Gray anchors with control cells above stamp transformed copies of a maroon prototype."

INVARIANTS = [
    "the maroon prototype has more than one cell",
    "each gray anchor has a control value 1 through 4 directly above",
    "all transformed prototype stamps fit in-bounds",
    "anchor stamps do not overlap the prototype",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_prototype", "no_anchors", "missing_control")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 13..17", "valid": "9..24"},
    "grid_w":         {"type": "int", "default": "rng 15..20", "valid": "12..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_anchors":      {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "5", "valid": "4..6"},
    "position_bias":  {"type": "str", "default": "prototype_with_anchors_and_codes",
                       "valid": "prototype_with_anchors_and_codes"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "4..6"},
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
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 15, 16)
        n_anchors = ctx.draw_int("n_anchors", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 15, 17)
        w = ctx.draw_int("grid_w", 18, 20)
        n_anchors = ctx.draw_int("n_anchors", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 13, 17)
        w = ctx.draw_int("grid_w", 15, 20)
        n_anchors = ctx.draw_int("n_anchors", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1)]:
        g[1 + dr][1 + dc] = 9
    spots = [(5, 7), (5, 11), (9, 7), (9, 11), (h - 5, w - 5)]
    rng.shuffle(spots)
    codes = [1, 2, 3, 4]
    rng.shuffle(codes)
    for i, (r, c) in enumerate(spots[:n_anchors]):
        g[r - 1][c] = codes[i % len(codes)]
        g[r][c] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 16
    g = full_grid(h, w, 0)
    if name == "no_prototype":
        # anchors but no maroon prototype → no shape to stamp
        for (r, c) in [(5, 7), (5, 11), (9, 7)]:
            g[r - 1][c] = 1; g[r][c] = 6
        return g
    if name == "no_anchors":
        # prototype only, no anchors → nothing to stamp at
        for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1)]:
            g[1 + dr][1 + dc] = 9
        return g
    if name == "missing_control":
        # anchor without control cell above → transform code undefined
        for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1)]:
            g[1 + dr][1 + dc] = 9
        g[5][7] = 6   # anchor with no control cell at (4,7)
        return g
    return g
