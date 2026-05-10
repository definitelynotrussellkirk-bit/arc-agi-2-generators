"""Generator for arc_additional_puzzles_21_set15_bundle:H103 — Rotation-equivalent shape relation matrix.

Rule: components are compared by rotation-equivalent shape, producing
a 7/0 relation matrix.

Combinatorial axes (8): grid_h, grid_w, palette_kind, third_shape,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_same_shape, all_distinct_shapes, single_component.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2ed2f53ebb44"
VERSION = "1.1.0"
TASK_ID = "2ed2f53ebb44"
SUMMARY = "Components are compared by rotation-equivalent shape, producing a 7/0 relation matrix."

INVARIANTS = [
    "nonzero components are sorted by their left edge",
    "component shape equality is tested under 0/90/180/270 degree rotations",
    "the output relation matrix uses 7 for rotation matches and 0 otherwise",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_same_shape", "all_distinct_shapes", "single_component")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8..8"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "third_shape":    {"type": "choice", "default": "line", "valid": "line|corner"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "three_components_lined_up",
                       "valid": "three_components_lined_up"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    third_shape = ctx.draw_choice("third_shape", ["line", "corner"])
    if "third_shape" not in overrides:
        third_shape = "line" if sample_index % 2 == 0 else "corner"
    color = ctx.draw_color("color", exclude={0})
    g = full_grid(8, 14, 0)
    for dr, dc in [(0, 0), (1, 0), (1, 1)]:
        g[1 + dr][1 + dc] = color
    for dr, dc in [(0, 0), (0, 1), (1, 0)]:
        g[2 + dr][6 + dc] = color
    if third_shape == "line":
        for dc in range(3):
            g[5][10 + dc] = color
    else:
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[5 + dr][10 + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 14, 0)
    color = 4
    if name == "all_same_shape":
        # all 3 components are rotation-equivalent corners → output is all-7 matrix
        for dr, dc in [(0, 0), (1, 0), (1, 1)]: g[1 + dr][1 + dc] = color
        for dr, dc in [(0, 0), (0, 1), (1, 0)]: g[2 + dr][6 + dc] = color
        for dr, dc in [(0, 0), (1, 0), (1, 1)]: g[5 + dr][10 + dc] = color
        return g
    if name == "all_distinct_shapes":
        # all 3 are rotation-distinct → output relation matrix mostly 0 (only diagonal 7)
        for dr, dc in [(0, 0), (0, 1), (0, 2)]: g[1 + dr][1 + dc] = color   # line
        for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 1)]: g[1 + dr][5 + dc] = color  # S-shape
        for dr, dc in [(0, 0), (0, 1), (1, 1), (2, 0)]: g[3 + dr][10 + dc] = color  # Z-shape
        return g
    if name == "single_component":
        # only 1 component → trivial 1x1 relation matrix [[7]]
        for dr, dc in [(0, 0), (1, 0), (1, 1)]: g[3 + dr][6 + dc] = color
        return g
    return g
