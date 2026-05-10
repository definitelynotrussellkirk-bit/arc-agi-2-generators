"""Generator for arc_additional_puzzles_21_set5:H29.

Rule: convert the nonzero mask into connected components, ranked by
descending bbox area.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_components,
palette_size, position_bias, n_distinct_colors, size_spread, texture.
Degenerates: equal_bboxes, single_component, no_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "2d5acf84dd20"
VERSION = "1.1.0"
TASK_ID = "2d5acf84dd20"
SUMMARY = "Convert the nonzero mask into connected components, ranked by descending bbox area."

INVARIANTS = [
    "nonzero components are separated by background",
    "largest bounding boxes are visually distinct",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("equal_bboxes", "single_component", "no_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_components":   {"type": "int", "default": "3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
    "size_spread":    {"type": "str", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


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
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    draw_rect_outline(g, 1, 1, 4, 5, rng.choice([2, 4, 6]))
    for r in range(1, 5):
        g[r][3] = rng.choice([2, 4, 6])
    draw_rect_outline(g, h - 5, w - 5, 4, 4, rng.choice([3, 5, 7]))
    for dr, dc in [(0, 0), (0, 1), (1, 0)]:
        g[h - 3 + dr][1 + dc] = rng.choice([8, 9])
    if w > 12:
        g[1][w - 2] = rng.choice([3, 4, 5])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "equal_bboxes":
        # all components share the same bbox area → ranking by area is ambiguous
        draw_rect_outline(g, 1, 1, 3, 3, 2)
        draw_rect_outline(g, 1, 7, 3, 3, 4)
        draw_rect_outline(g, 7, 1, 3, 3, 6)
        draw_rect_outline(g, 7, 7, 3, 3, 8)
        return g
    if name == "single_component":
        # only one component → ranking has one entry, ordering trivial
        draw_rect_outline(g, 3, 3, 5, 5, 5)
        return g
    if name == "no_components":
        # empty grid → nothing to rank
        return g
    return g
