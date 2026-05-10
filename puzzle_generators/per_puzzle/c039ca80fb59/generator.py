"""Generator for arc_puzzle_bank_21_set9_s:S9_H5.

A color-2 template and a hollow color-4 frame are given. The rule stamps the
template plus its horizontal, vertical, and 180-degree variants into the four
interior corners of the frame.

Combinatorial axes (8): grid_h, grid_w, palette_kind, template_variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_template, no_frame, frame_too_small.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "c039ca80fb59"
VERSION = "1.1.0"
TASK_ID = "c039ca80fb59"
SUMMARY = "Stamp a template and its mirrored/rotated variants into a 4-frame."

INVARIANTS = [
    "there is exactly one hollow rectangular frame of color 4",
    "there is exactly one connected template object of color 2",
    "the frame interior is large enough for all four variants",
    "the input template is outside the frame",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "no_frame", "frame_too_small")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13..13"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "template_variant": {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "template_plus_frame",
                       "valid": "template_plus_frame"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TEMPLATES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
]


def _paint(g, top, left, cells, color):
    for dr, dc in cells:
        g[top + dr][left + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed, sample_index=sample_index, version=VERSION,
        task_id=TASK_ID, difficulty=difficulty, overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        variant_idx = ctx.draw_int("template_variant", 0, 0)
    elif difficulty == "hard":
        variant_idx = ctx.draw_int("template_variant", 1, 2)
    else:
        variant_idx = ctx.draw_int("template_variant", 0, len(_TEMPLATES) - 1)
    template = _TEMPLATES[variant_idx]
    g = full_grid(13, 16, 0)
    _paint(g, 1 + rng.randint(0, 1), 1 + rng.randint(0, 1), template, 2)
    top = 2 + rng.randint(0, 1)
    left = 7 + rng.randint(0, 1)
    draw_frame(g, top, left, top + 8, left + 7, 4)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 16, 0)
    if name == "no_template":
        # frame without template → no stencil to stamp into corners
        draw_frame(g, 2, 7, 10, 14, 4)
        return g
    if name == "no_frame":
        # template without frame → no stamping target
        _paint(g, 1, 1, _TEMPLATES[0], 2)
        return g
    if name == "frame_too_small":
        # frame interior too small to fit all 4 template variants
        _paint(g, 1, 1, _TEMPLATES[0], 2)
        draw_frame(g, 2, 7, 6, 11, 4)
        return g
    return g
