"""Generator for arc_puzzle_bank_fourteenth21:H94.

A color-9 anchor defines the rotation center. The surrounding colored shape is
stamped at all four quarter-turn rotations around that anchor.

Combinatorial axes (8): grid_size, palette_kind, motif, n_motif_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, no_payload, anchor_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "df0b89714b4f"
VERSION = "1.1.0"
TASK_ID = "df0b89714b4f"
SUMMARY = "A 9-anchored colored shape is completed across four rotations."

INVARIANTS = [
    "there is exactly one color-9 anchor",
    "payload cells are nonzero and not 9",
    "all four rotations of every payload cell remain in bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_payload", "anchor_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 13..17 odd", "valid": "11..19"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif":          {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "n_motif_cells":  {"type": "int", "default": "rng 3..5", "valid": "3..5"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "anchor_with_motif",
                       "valid": "anchor_with_motif"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "3..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_OFFSETS = [
    [(-2, 0), (-1, 0), (-1, 1)],
    [(-2, -1), (-1, -1), (-1, 0), (0, 0)],
    [(-3, 0), (-2, 0), (-1, 0), (-1, 1)],
    [(-2, 1), (-1, 0), (-1, 1), (0, 1)],
    [(-3, -1), (-2, -1), (-2, 0), (-1, 0), (-1, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        motif = _OFFSETS[ctx.draw_int("motif", 0, 1)]
        size = ctx.draw_int("grid_size", 13, 13)
    elif difficulty == "hard":
        motif = _OFFSETS[ctx.draw_int("motif", 2, 4)]
        size = ctx.draw_int("grid_size", 15, 17)
    else:
        motif = _OFFSETS[ctx.draw_int("motif", 0, len(_OFFSETS) - 1)]
        size = ctx.draw_int("grid_size", 13, 17)
    if size % 2 == 0:
        size += 1
    g = full_grid(size, size, 0)
    margin = 4
    ar = rng.randint(margin, size - margin - 1)
    ac = rng.randint(margin, size - margin - 1)
    g[ar][ac] = 9
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], len(motif))
    for (dr, dc), color in zip(motif, colors):
        g[ar + dr][ac + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    size = 13
    g = full_grid(size, size, 0)
    if name == "no_anchor":
        # payload cells without 9-anchor → no rotation pivot defined
        for (dr, dc), color in zip(_OFFSETS[0], [4, 6, 7]):
            g[6 + dr][6 + dc] = color
        return g
    if name == "no_payload":
        # anchor alone → nothing to rotate
        g[6][6] = 9
        return g
    if name == "anchor_at_corner":
        # anchor at corner (0,0) → rotations of payload land out of bounds
        g[0][0] = 9
        # tiny payload near corner
        g[1][1] = 4
        return g
    return g
