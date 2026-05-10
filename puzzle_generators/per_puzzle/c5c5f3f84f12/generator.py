"""Generator for arc_additional_puzzle_bank_volume18:M121.

Rule: a corner blue marker encodes rotation; the red object is rotated and
the result is emitted as a cyan crop.

Combinatorial axes (8): grid_h/w, palette_kind, corner_position,
palette_size, position_bias, n_distinct_colors, blob_size, texture.
Degenerates: no_blue, no_red, blue_not_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c5c5f3f84f12"
VERSION = "1.1.0"
TASK_ID = "c5c5f3f84f12"
SUMMARY = "A corner blue marker encodes rotation of the red object into a cyan crop."

INVARIANTS = [
    "background is 0",
    "there is exactly one blue control marker in a grid corner",
    "there is exactly one red object",
    "the red object is away from the control marker",
]

PALETTE_KINDS = ("default", "tl_corner", "tr_corner", "bl_or_br_corner")
DEGENERATE_TEXTURES = ("no_blue", "no_red", "blue_not_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "5..24"},
    "grid_w":         {"type": "int", "default": "rng 7..12", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "corner_position": {"type": "str", "default": "rng",
                        "valid": "tl|tr|bl|br"},
    "blob_size":      {"type": "int", "default": "4", "valid": "4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "interior",
                       "valid": "interior"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 10, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 7, 12)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    corner = rng.choice([(0, 0), (0, w - 1), (h - 1, w - 1), (h - 1, 0)])
    g[corner[0]][corner[1]] = 1
    r = rng.randint(2, h - 4)
    c = rng.randint(2, w - 4)
    for dr, dc in [(0, 0), (0, 1), (1, 0), (2, 0)]:
        g[r + dr][c + dc] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_blue":
        # red object but no blue marker — rotation encoding undefined
        for dr, dc in [(0, 0), (0, 1), (1, 0), (2, 0)]:
            g[3 + dr][3 + dc] = 2
        return g
    if name == "no_red":
        # blue marker but no red object — rule has nothing to rotate
        g[0][0] = 1
        return g
    if name == "blue_not_at_corner":
        # blue is not at a corner — invariant violated
        g[3][3] = 1
        for dr, dc in [(0, 0), (0, 1), (1, 0), (2, 0)]:
            g[5 + dr][5 + dc] = 2
        return g
    return g
