"""Generator for arc_puzzle_bank_21_set15:S15_M1.

Rule: a multicolor template is copied to the single blue marker anchor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_template, multiple_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b24eadbaf79d"
VERSION = "1.1.0"
TASK_ID = "b24eadbaf79d"
SUMMARY = "A multicolor template is copied to the single blue marker anchor."

INVARIANTS = [
    "background is 0",
    "there is exactly one color-1 marker",
    "all nonzero non-marker cells form one multicolor template",
    "the marker anchor has room for the whole template footprint",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_template", "multiple_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

TEMPLATE_A = [(0, 0, 2), (0, 1, 3), (1, 0, 4), (2, 1, 3)]
TEMPLATE_B = [(0, 1, 2), (1, 0, 4), (1, 1, 3), (1, 2, 4), (2, 0, 2)]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 13..16", "valid": "11..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "variant":        {"type": "enum", "default": "rng a|b", "valid": "a|b"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "template_top_marker_bottom",
                       "valid": "template_top_marker_bottom"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint_entries(g, r0, c0, entries):
    for dr, dc, color in entries:
        g[r0 + dr][c0 + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 11, 12)
        w = ctx.draw_int("width", 13, 14)
        variant = ctx.draw_choice("variant", ["a"])
    elif difficulty == "hard":
        h = ctx.draw_int("height", 13, 14)
        w = ctx.draw_int("width", 15, 16)
        variant = ctx.draw_choice("variant", ["b"])
    else:
        h = ctx.draw_int("height", 11, 14)
        w = ctx.draw_int("width", 13, 16)
        variant = ctx.draw_choice("variant", ["a", "b"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    entries = TEMPLATE_A if variant == "a" else TEMPLATE_B
    _paint_entries(g, rng.randint(1, 2), 1, entries)
    g[h - 5][w - 5] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # template without color-1 marker → no anchor to copy to
        _paint_entries(g, 1, 1, TEMPLATE_A)
        return g
    if name == "no_template":
        # marker without template → nothing to copy
        g[h - 5][w - 5] = 1
        return g
    if name == "multiple_markers":
        # 2 color-1 markers → which to copy to is ambiguous
        _paint_entries(g, 1, 1, TEMPLATE_A)
        g[h - 5][w - 5] = 1
        g[h - 5][w - 9] = 1
        return g
    return g
