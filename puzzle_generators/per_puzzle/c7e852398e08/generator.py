"""Generator for arc_additional_puzzles_21_set8:E55.

Rule: a colored motif is placed away from the outer border; output is
the motif cropped to its bounding box.

Combinatorial axes (8): grid_h/w, palette_kind, motif_position,
palette_size, position_bias, n_distinct_colors, motif_density, texture.
Degenerates: motif_at_border, motif_fills_grid, no_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c7e852398e08"
VERSION = "1.1.0"
TASK_ID = "c7e852398e08"
SUMMARY = "A colored motif is placed away from the outer border and then cropped to content."

INVARIANTS = [
    "zero padding surrounds the motif on every side",
    "the motif's bounding box is smaller than the input grid",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("motif_at_border", "motif_fills_grid", "no_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_position": {"type": "str", "default": "interior",
                       "valid": "interior"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "interior",
                       "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "motif_density":  {"type": "str", "default": "fixed", "valid": "fixed"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    colors = list(ctx.draw_distinct_colors("colors", n=3, exclude=[0]))
    g = full_grid(h, w, 0)
    top = ctx.draw_int("top", 1, h - 4)
    left = ctx.draw_int("left", 1, w - 6)
    for dr, dc, color in [
        (0, 0, colors[0]),
        (0, 1, colors[0]),
        (1, 1, colors[1]),
        (2, 1, colors[1]),
        (2, 3, colors[2]),
    ]:
        g[top + dr][left + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "motif_at_border":
        # motif touches the top-left corner — zero-padding invariant violated
        for dr, dc, color in [(0, 0, 2), (0, 1, 2), (1, 1, 3), (2, 1, 3), (2, 3, 4)]:
            g[dr][dc] = color
        return g
    if name == "motif_fills_grid":
        # motif fills entire grid — crop equals input (rule trivial)
        for r in range(h):
            for c in range(w):
                g[r][c] = ((r + c) % 3) + 2
        return g
    if name == "no_motif":
        # empty grid — nothing to crop
        return g
    return g
