"""Generator for arc_puzzle_bank_21_set4:S4_H2 — corner marker rotates template.

A top-left color-2 template is rotated into each color-5 frame according
to which interior corner contains a color-8 marker.

Combinatorial axes (8): n_frames, template, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_frames, no_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "641011d9dcfc"
VERSION = "1.1.0"
TASK_ID = "641011d9dcfc"
SUMMARY = "Color-5 frames contain corner color-8 markers that rotate a color-2 template."

INVARIANTS = [
    "one color-2 template object appears before the frames in reading order",
    "all target frames are color-5 rectangular outlines",
    "each frame has one color-8 marker in an interior corner",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_frames", "no_marker")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "n_frames":       {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "template":       {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "template_topleft_frames_below",
                       "valid": "template_topleft_frames_below"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TEMPLATES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
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
    _paint(g, 1, 1, template, 2)
    frame_origins = [(6, 1), (6, 10), (12, 5)]
    corners = ["tl", "tr", "br", "bl"]
    rng.shuffle(corners)
    for i in range(n_frames):
        r0, c0 = frame_origins[i]
        r2, c2 = r0 + 5, c0 + 5
        draw_frame(g, r0, c0, r2, c2, 5)
        corner = corners[i % len(corners)]
        if corner == "tl":
            mr, mc = r0 + 1, c0 + 1
        elif corner == "tr":
            mr, mc = r0 + 1, c2 - 1
        elif corner == "br":
            mr, mc = r2 - 1, c2 - 1
        else:
            mr, mc = r2 - 1, c0 + 1
        g[mr][mc] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(18, 18, 0)
    if name == "no_template":
        # Frames + markers but no color-2 template — rule has no shape
        # to rotate into the frames.
        draw_frame(g, 6, 1, 11, 6, 5)
        g[7][2] = 8
        return g
    if name == "no_frames":
        # Template present but no color-5 frames — rule has no
        # destination to place the rotated template into.
        _paint(g, 1, 1, _TEMPLATES[0], 2)
        return g
    if name == "no_marker":
        # Template + frame present but no corner color-8 marker — rule
        # has no rotation cue, can't determine orientation.
        _paint(g, 1, 1, _TEMPLATES[0], 2)
        draw_frame(g, 6, 1, 11, 6, 5)
        return g
    return g
