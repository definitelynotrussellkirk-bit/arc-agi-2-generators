"""Generator for arc_puzzle_bank_21_set9_e:hard_i15.

Combinatorial axes (8): variant, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, no_inserts, equal_interiors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "cdb5c49033cd"
VERSION = "1.1.0"
TASK_ID = "cdb5c49033cd"
SUMMARY = "Match each detached insert to the hollow frame with the same interior size."

INVARIANTS = [
    "all hollow frames are color 8 and have distinct interior dimensions",
    "each detached insert has a bounding box matching exactly one frame interior",
    "insert components are connected non-frame shapes",
    "the output keeps the frames and moves each insert into its matching interior",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_inserts", "equal_interiors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "variant":        {"type": "int", "default": "rng 0..5", "valid": "0..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "two_frames_two_inserts",
                       "valid": "two_frames_two_inserts"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_VARIANTS = [
    (((3, 3), [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
     ((4, 2), [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)])),
    (((2, 4), [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3)]),
     ((4, 3), [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1), (3, 2)])),
    (((3, 2), [(0, 0), (1, 0), (1, 1), (2, 1)]),
     ((2, 3), [(0, 0), (0, 1), (1, 1), (1, 2)])),
    (((4, 4), [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1), (3, 2), (3, 3)]),
     ((3, 3), [(0, 2), (1, 0), (1, 1), (1, 2), (2, 0)])),
    (((2, 2), [(0, 0), (1, 0), (1, 1)]),
     ((3, 4), [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (2, 3)])),
    (((4, 2), [(0, 1), (1, 1), (2, 0), (2, 1), (3, 0)]),
     ((2, 4), [(0, 0), (1, 0), (1, 1), (1, 2), (1, 3)])),
]


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        variant = ctx.draw_int("variant", 0, 1)
    elif difficulty == "hard":
        variant = ctx.draw_int("variant", 3, 5)
    else:
        variant = ctx.draw_int("variant", 0, len(_VARIANTS) - 1)
    first, second = _VARIANTS[variant]
    colors = rng.sample([2, 3, 4, 5, 6, 7, 9], 2)
    g = full_grid(12, 16, 0)

    for (top, left), ((ih, iw), cells), color in [
        ((1, 1), first, colors[0]),
        ((1, 9), second, colors[1]),
    ]:
        draw_frame(g, top, left, top + ih + 1, left + iw + 1, 8)
        _paint(g, 8 if ih <= 3 else 7, 1 if left == 1 else 9, cells, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 16, 0)
    if name == "no_frames":
        # Inserts present but no frames — rule has nowhere to place inserts.
        for r, c in [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]: g[8 + r][1 + c] = 4
        return g
    if name == "no_inserts":
        # Frames present but no detached inserts — rule has nothing to match.
        draw_frame(g, 1, 1, 5, 5, 8)
        draw_frame(g, 1, 9, 6, 12, 8)
        return g
    if name == "equal_interiors":
        # Both frames have the same interior size — match is ambiguous.
        draw_frame(g, 1, 1, 4, 4, 8)
        draw_frame(g, 1, 9, 4, 12, 8)
        for r, c in [(0, 0), (1, 0), (1, 1)]: g[8 + r][1 + c] = 4
        for r, c in [(0, 0), (1, 0), (1, 1)]: g[8 + r][9 + c] = 5
        return g
    return g
