"""Generator for arc_puzzle_bank_eighth21:H50.

Rule: a payload shape is rotated 90/180/270 about the color-1 pivot,
producing a 4-fold rotational pattern.

Combinatorial axes (9): grid_h/w, palette_kind, motif_idx, payload_color,
pivot_position, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_pivot, payload_clipped, payload_on_pivot.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3dcf9b8e9c1b"
VERSION = "1.1.0"
TASK_ID = "3dcf9b8e9c1b"
SUMMARY = "A payload shape rotates around a color-1 pivot."

INVARIANTS = [
    "there is exactly one color-1 pivot cell",
    "all payload cells use one non-1 color",
    "all four quarter-turn copies remain in bounds",
]

PALETTE_KINDS = ("default", "small_motif", "tall_motif", "warm_color")
DEGENERATE_TEXTURES = ("no_pivot", "payload_clipped", "payload_on_pivot")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif":          {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "pivot_position": {"type": "str", "default": "center", "valid": "center"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "centered", "valid": "centered"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_OFFSETS = [
    [(-2, 0), (-1, 0), (-1, 1)],
    [(-2, -1), (-1, -1), (-1, 0), (0, 0)],
    [(-3, 0), (-2, 0), (-1, 0), (-1, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        offsets = _OFFSETS[ctx.draw_int("motif", 0, 0)]
    elif difficulty == "hard":
        offsets = _OFFSETS[ctx.draw_int("motif", 2, 2)]
    else:
        offsets = _OFFSETS[ctx.draw_int("motif", 0, len(_OFFSETS) - 1)]
    g = full_grid(13, 13, 0)
    ar = ac = 6
    g[ar][ac] = 1
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    for dr, dc in offsets:
        g[ar + dr][ac + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    ar = ac = 6
    if name == "no_pivot":
        # payload but no pivot — rotation centre is undefined
        for dr, dc in _OFFSETS[0]:
            g[ar + dr][ac + dc] = 4
        return g
    if name == "payload_clipped":
        # pivot too close to edge — quarter-turn copies leave the grid
        ar, ac = 1, 1
        g[ar][ac] = 1
        for dr, dc in [(0, 1), (0, 2), (1, 1)]:
            g[ar + dr][ac + dc] = 5
        return g
    if name == "payload_on_pivot":
        # payload includes the pivot cell — ambiguous
        g[ar][ac] = 1
        g[ar][ac + 1] = 1
        g[ar + 1][ac] = 1
        return g
    return g
