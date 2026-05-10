"""Generator for arc_puzzle_bank_21_more:hard_b05.

Inside each rectangular frame, a singleton seed color recolors the larger
enclosed object.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, no_seed, no_target_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "61090a45e458"
VERSION = "1.1.0"
TASK_ID = "61090a45e458"
SUMMARY = "Frames contain one singleton seed and one larger object to be recolored."

INVARIANTS = [
    "all frames are rectangular outlines",
    "each frame interior contains exactly one singleton seed color",
    "each frame interior contains one larger object in another color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_seed", "no_target_object")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "auto", "valid": "auto"},
    "grid_w":         {"type": "int", "default": "auto", "valid": "auto"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "frame_h":        {"type": "int", "default": "rng 5..6", "valid": "5..8"},
    "frame_w":        {"type": "int", "default": "rng 5..7", "valid": "5..8"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "3..9"},
    "position_bias":  {"type": "str", "default": "frames_with_seed_and_target",
                       "valid": "frames_with_seed_and_target"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "3..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_OBJECTS = [
    [(0, 0), (0, 1), (1, 0), (2, 0)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
]


def _paint_object(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        n_frames = ctx.draw_int("n_frames", 1, 1)
        fh = ctx.draw_int("frame_h", 5, 5)
        fw = ctx.draw_int("frame_w", 5, 5)
    elif difficulty == "hard":
        n_frames = ctx.draw_int("n_frames", 2, 2)
        fh = ctx.draw_int("frame_h", 6, 6)
        fw = ctx.draw_int("frame_w", 6, 7)
    else:
        n_frames = ctx.draw_int("n_frames", 1, 2)
        fh = ctx.draw_int("frame_h", 5, 6)
        fw = ctx.draw_int("frame_w", 5, 7)
    h = fh + 4
    w = n_frames * fw + (n_frames + 1) * 2
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n_frames * 3)

    for i in range(n_frames):
        r0 = 2
        c0 = 2 + i * (fw + 2)
        frame_color, seed_color, object_color = colors[i * 3:i * 3 + 3]
        draw_frame(g, r0, c0, r0 + fh - 1, c0 + fw - 1, frame_color)
        g[r0 + 1][c0 + fw - 2] = seed_color
        obj = rng.choice(_OBJECTS)
        _paint_object(g, r0 + 1, c0 + 1, obj, object_color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # seed + object but no frame → no enclosure for the rule
        g[3][3] = 4
        for dr, dc in _OBJECTS[0]: g[2 + dr][1 + dc] = 6
        return g
    if name == "no_seed":
        # frame + object but no singleton seed → no recolor color defined
        draw_frame(g, 2, 2, 6, 6, 7)
        for dr, dc in _OBJECTS[0]: g[3 + dr][3 + dc] = 6
        return g
    if name == "no_target_object":
        # frame + seed but no larger enclosed object → nothing to recolor
        draw_frame(g, 2, 2, 6, 6, 7)
        g[3][5] = 4
        return g
    return g
