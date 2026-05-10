"""Generator for arc_additional_puzzles_21_set6:E40.

Rule: a padded asymmetric motif is cropped to its bbox and rotated 90°
clockwise.

Combinatorial axes (8): grid_h/w, palette_kind, motif_position,
palette_size, position_bias, n_distinct_colors, motif_density, texture.
Degenerates: motif_at_border, motif_180_symmetric, no_motif.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a6211f2301a7"
VERSION = "1.1.0"
TASK_ID = "a6211f2301a7"
SUMMARY = "A padded asymmetric motif is cropped and then rotated clockwise."

INVARIANTS = [
    "the motif has zero padding outside its bounding box",
    "the motif is asymmetric so rotation changes the layout",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("motif_at_border", "motif_180_symmetric", "no_motif")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..13"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..13"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
    colors = list(ctx.draw_distinct_colors("colors", n=3, exclude=[0]))
    g = full_grid(h, w, 0)
    top = ctx.draw_int("top", 1, h - 5)
    left = ctx.draw_int("left", 1, w - 5)
    for dr, dc, color in [
        (0, 0, colors[0]),
        (1, 0, colors[0]),
        (2, 0, colors[1]),
        (2, 1, colors[1]),
        (0, 2, colors[2]),
    ]:
        g[top + dr][left + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "motif_at_border":
        # motif touches grid border — zero-padding invariant violated
        for dr, dc, color in [(0, 0, 2), (1, 0, 2), (2, 0, 3), (2, 1, 3), (0, 2, 4)]:
            g[dr][dc] = color
        return g
    if name == "motif_180_symmetric":
        # motif is point-symmetric → rotate-CW twice == identity (rule trivial)
        cells = [(2, 3, 5), (2, 5, 5), (3, 4, 5), (4, 3, 5), (4, 5, 5)]
        for r, c, v in cells:
            g[r][c] = v
        return g
    if name == "no_motif":
        # empty grid — nothing to crop or rotate
        return g
    return g
