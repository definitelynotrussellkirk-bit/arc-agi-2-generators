"""Generator for arc_puzzle_bank_21_set7:easy_g02.

Rule: separated nonzero components of small sizes are recolored
according to size.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_components,
palette_size, position_bias, n_distinct_colors, size_spread, texture.
Degenerates: equal_sizes, single_component, no_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.blobs import grow_blob
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3e7bc7e83316"
VERSION = "1.1.0"
TASK_ID = "3e7bc7e83316"
SUMMARY = "Separated nonzero components of small sizes are recolored according to size."

INVARIANTS = [
    "components are separated",
    "component sizes are in the rule's small-size range",
    "background is zero",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("equal_sizes", "single_component", "no_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_components":   {"type": "int", "default": "rng 3..5", "valid": "1..7"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..7"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..7"},
    "size_spread":    {"type": "str", "default": "1_to_5", "valid": "1_to_5"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        n = ctx.draw_int("n_components", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n = ctx.draw_int("n_components", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        n = ctx.draw_int("n_components", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    used = set()
    for i, size in enumerate([1, 2, 3, 4, 5][:n]):
        cells = grow_blob(rng, h, w, used, size)
        if cells is None:
            continue
        used |= cells
        color = (i % 8) + 1
        for r, c in cells:
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    import random
    rng = random.Random(0)
    h, w = 9, 9
    g = full_grid(h, w, 0)
    used = set()
    if name == "equal_sizes":
        # all components share one size → size-based recolor signal vanishes
        for i, color in enumerate([3, 5, 7]):
            cells = grow_blob(rng, h, w, used, 2)
            if cells is None:
                continue
            used |= cells
            for r, c in cells:
                g[r][c] = color
        return g
    if name == "single_component":
        # only one component → ranking by size has no second element
        cells = grow_blob(rng, h, w, used, 3)
        if cells:
            for r, c in cells:
                g[r][c] = 4
        return g
    if name == "no_components":
        # empty grid → nothing to recolor
        return g
    return g
