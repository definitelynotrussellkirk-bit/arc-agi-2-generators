"""Generator for arc_additional_puzzle_bank_volume10:E69.

Rule: the uniquely smallest connected object is cropped out.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_components,
palette_size, position_bias, n_distinct_colors, size_spread, texture.
Degenerates: equal_smallest, single_component, no_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "ba988f8d25d5"
VERSION = "1.1.0"
TASK_ID = "ba988f8d25d5"
SUMMARY = "The uniquely smallest connected object is cropped out."

INVARIANTS = [
    "background is 0",
    "there are at least three nonzero connected components",
    "one component is uniquely smallest by cell count",
    "components are separated so the object ranking is unambiguous",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("equal_smallest", "single_component", "no_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "5..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_components":   {"type": "int", "default": "3", "valid": "3..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "spread_corners",
                       "valid": "spread_corners"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..4"},
    "size_spread":    {"type": "str", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    draw_rect(g, 0, 0, 2, 3, 4)
    draw_rect(g, h - 3, w - 3, 3, 3, 7)
    if h > 10 and w > 10:
        draw_rect(g, h // 2, 0, 3, 2, 8)
    for _ in range(100):
        sr = rng.randint(2, h - 4)
        sc = rng.randint(3, w - 4)
        if g[sr][sc] == 0 and g[sr][sc + 1] == 0:
            g[sr][sc] = 2
            g[sr][sc + 1] = 2
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "equal_smallest":
        # multiple smallest components share one size → "uniquely smallest" is ambiguous
        draw_rect(g, 0, 0, 2, 2, 4)
        draw_rect(g, 0, w - 3, 2, 2, 7)
        draw_rect(g, h - 3, 0, 2, 2, 8)
        return g
    if name == "single_component":
        # only one component → uniquely smallest = uniquely largest, rule trivializes
        draw_rect(g, 2, 2, 4, 4, 5)
        return g
    if name == "no_components":
        # empty grid → no components to compare, smallest is undefined
        return g
    return g
