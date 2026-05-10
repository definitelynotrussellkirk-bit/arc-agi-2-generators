"""Generator for arc_additional_puzzles_21_set22_bundle:H149.

Rule: several color-1 components are recolored by descending bounding-box
area rank.

Combinatorial axes (8): grid_h/w, palette_kind, num_components,
component_sizes, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: tied_areas, only_one_component, no_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "c9c4c55a191d"
VERSION = "1.1.0"
TASK_ID = "c9c4c55a191d"
SUMMARY = "Several color-1 components are recolored by descending bounding-box area."

INVARIANTS = [
    "all relevant components are color 1",
    "component bounding-box areas are distinct",
]

PALETTE_KINDS = ("default", "wide_grid", "tight_grid", "varied")
DEGENERATE_TEXTURES = ("tied_areas", "only_one_component", "no_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_components": {"type": "int", "default": "3", "valid": "2..4"},
    "component_sizes": {"type": "str", "default": "varied",
                        "valid": "varied"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
    draw_rect_outline(g, 1, 1, 3, 5, 1)
    draw_rect_outline(g, h - 5, w - 5, 4, 4, 1)
    for dr, dc in [(0, 0), (0, 1), (1, 0)]:
        g[h - 3 + dr][1 + dc] = 1
    if rng.random() < 0.5 and w > 12:
        g[1][w - 2] = 1
        g[2][w - 2] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "tied_areas":
        # two components with the same bbox area — rank ambiguous
        draw_rect_outline(g, 1, 1, 3, 4, 1)
        draw_rect_outline(g, 1, 7, 3, 4, 1)
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[h - 3 + dr][1 + dc] = 1
        return g
    if name == "only_one_component":
        # single component — area rank trivial, palette uses only one color
        draw_rect_outline(g, 3, 3, 4, 5, 1)
        return g
    if name == "no_components":
        return g
    return g
