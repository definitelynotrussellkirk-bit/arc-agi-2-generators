"""Generator for arc_puzzle_bank_21_set13_s:S13_H6 — pick by blue holes + red symmetry.

Rule: the blue object supplies the hole count and the red object
supplies the symmetry class. The target is the non-blue/non-red object
with both features.

Combinatorial axes (8): grid_h, grid_w, palette_kind, target_size,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_blue, no_red, no_matching_target.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "643fb1ca2780"
VERSION = "1.1.0"
TASK_ID = "643fb1ca2780"
SUMMARY = "Select the object matching blue's hole count and red's symmetry class."

INVARIANTS = [
    "one color-1 object has exactly one enclosed hole",
    "one color-2 object is symmetric both horizontally and vertically",
    "exactly one other object has one hole and the same symmetry class",
    "the selected object is cropped and recolored to 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_blue", "no_red", "no_matching_target")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11..11"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "target_size":    {"type": "int", "default": "rng 4..5", "valid": "4..5"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "blue_red_with_target",
                       "valid": "blue_red_with_target"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint(g, top, left, cells, color):
    for dr, dc in cells:
        g[top + dr][left + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        target_size = ctx.draw_int("target_size", 4, 4)
    elif difficulty == "hard":
        target_size = ctx.draw_int("target_size", 5, 5)
    else:
        target_size = ctx.draw_int("target_size", 4, 5)
    target_color = rng.choice([3, 4, 5, 6, 7, 9])
    g = full_grid(11, 14, 0)

    draw_frame(g, 1, 1, 4, 4, 1)
    _paint(g, 1, 8, [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)], 2)
    draw_frame(g, 6, 6, 6 + target_size - 1, 6 + target_size - 1, target_color)
    _paint(g, 6, 1, [(0, 0), (1, 0), (1, 1), (2, 1)], rng.choice([3, 4, 5, 6, 7, 9]))
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 14, 0)
    if name == "no_blue":
        # no color-1 object → no hole-count anchor specified
        _paint(g, 1, 8, [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)], 2)
        draw_frame(g, 6, 6, 9, 9, 4)
        _paint(g, 6, 1, [(0, 0), (1, 0), (1, 1), (2, 1)], 7)
        return g
    if name == "no_red":
        # no color-2 object → no symmetry-class anchor specified
        draw_frame(g, 1, 1, 4, 4, 1)
        draw_frame(g, 6, 6, 9, 9, 4)
        _paint(g, 6, 1, [(0, 0), (1, 0), (1, 1), (2, 1)], 7)
        return g
    if name == "no_matching_target":
        # blue + red anchors present but no target object matches both features
        draw_frame(g, 1, 1, 4, 4, 1)
        _paint(g, 1, 8, [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)], 2)
        # only solid (no holes) candidates
        _paint(g, 6, 1, [(0, 0), (0, 1), (1, 0), (1, 1)], 4)
        _paint(g, 7, 8, [(0, 0), (1, 0), (1, 1)], 7)
        return g
    return g
