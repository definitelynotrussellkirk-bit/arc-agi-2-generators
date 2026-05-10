"""Generator for arc_puzzle_bank_21_set4:S4_H6.

A neutral color-1 template is copied into each color-5 frame and recolored to
the frame's interior marker color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_frames, no_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "cdb0009458df"
VERSION = "1.1.0"
TASK_ID = "cdb0009458df"
SUMMARY = "Color-5 frames contain single colored markers that recolor a color-1 template copy."

INVARIANTS = [
    "one color-1 template object appears before the frames in reading order",
    "all target frames are color-5 rectangular outlines",
    "each frame has exactly one non-0/non-5 interior marker",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_frames", "no_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "18", "valid": "18..18"},
    "grid_w":         {"type": "int", "default": "18", "valid": "18..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "color1_template_with_5frames",
                       "valid": "color1_template_with_5frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TEMPLATES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
]


def _paint(g, top, left, cells, color):
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
    elif difficulty == "hard":
        n_frames = ctx.draw_int("n_frames", 3, 3)
    else:
        n_frames = ctx.draw_int("n_frames", 1, 3)
    template = _TEMPLATES[ctx.draw_int("template", 0, len(_TEMPLATES) - 1)]
    g = full_grid(18, 18, 0)
    _paint(g, 1, 1, template, 1)
    frame_origins = [(6, 1), (6, 10), (12, 5)]
    marker_colors = rng.sample([2, 3, 4, 6, 7, 8, 9], n_frames)
    marker_offsets = [(1, 1), (2, 3), (3, 2)]
    for i in range(n_frames):
        r0, c0 = frame_origins[i]
        r2, c2 = r0 + 5, c0 + 5
        draw_frame(g, r0, c0, r2, c2, 5)
        dr, dc = marker_offsets[i]
        g[r0 + dr][c0 + dc] = marker_colors[i]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(18, 18, 0)
    if name == "no_template":
        # frames without color-1 template → nothing to copy from
        draw_frame(g, 6, 1, 11, 6, 5)
        g[7][2] = 4
        return g
    if name == "no_frames":
        # template only, no frames → nowhere to copy template into
        _paint(g, 1, 1, _TEMPLATES[0], 1)
        return g
    if name == "no_markers":
        # template + frames but no interior markers → no recolor target
        _paint(g, 1, 1, _TEMPLATES[0], 1)
        draw_frame(g, 6, 1, 11, 6, 5)
        return g
    return g
