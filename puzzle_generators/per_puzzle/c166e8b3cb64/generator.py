"""Generator for arc_additional_puzzles_21_set18_bundle:E125.

Rule: crop the largest non-zero connected component (ties broken by
earliest bbox position).

Combinatorial axes (8): grid_h/w, palette_kind, large_size, small_size,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: tied_largest, only_one_component, all_same_size.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "c166e8b3cb64"
VERSION = "1.1.0"
TASK_ID = "c166e8b3cb64"
SUMMARY = "The largest nonzero connected component is cropped from the grid."

INVARIANTS = [
    "nonzero cells form several 4-connected components",
    "the chosen component is largest, then earliest by bounding-box position",
    "the output is the tight crop around that component",
]

PALETTE_KINDS = ("wide", "tall", "warm", "cool")
DEGENERATE_TEXTURES = ("tied_largest", "only_one_component", "all_same_size")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "large_size":     {"type": "choice", "default": "wide",
                       "valid": "wide|tall"},
    "small_size":     {"type": "int", "default": "4", "valid": "4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
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
    large_size = ctx.draw_choice("large_size", ["wide", "tall"])
    if "large_size" not in overrides:
        large_size = "wide" if sample_index % 2 == 0 else "tall"
    a, b = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(10, 12, 0)
    if large_size == "wide":
        draw_rect(g, 5, 3, 2, 4, a)
    else:
        draw_rect(g, 3, 5, 4, 2, a)
    draw_rect(g, 1, 1, 2, 2, b)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "tied_largest":
        # two components tied for largest — pick is ambiguous
        draw_rect(g, 1, 1, 2, 3, 4)
        draw_rect(g, 6, 6, 2, 3, 7)
        return g
    if name == "only_one_component":
        draw_rect(g, 3, 3, 3, 4, 5)
        return g
    if name == "all_same_size":
        # all 3 components same size — no unique largest
        draw_rect(g, 1, 1, 2, 2, 3)
        draw_rect(g, 1, 8, 2, 2, 4)
        draw_rect(g, 7, 4, 2, 2, 6)
        return g
    return g
