"""Generator for arc_puzzle_bank_21_set24_s:S24_M3.

Rule: a connected solid shape produces a one-row histogram of onion
depths.

Combinatorial axes (8): grid_h, grid_w, palette_kind, radius,
palette_size, position_bias, n_distinct_colors, shape_kind, texture.
Degenerates: empty_grid, two_shapes, hollow_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "12ace26107fd"
VERSION = "1.1.0"
TASK_ID = "12ace26107fd"
SUMMARY = "A connected solid shape produces a one-row histogram of onion depths."

INVARIANTS = [
    "the input contains one nonzero connected shape",
    "background is zero",
    "the output is a one-row count per erosion layer",
]

PALETTE_KINDS = ("default", "small", "medium", "large")
DEGENERATE_TEXTURES = ("empty_grid", "two_shapes", "hollow_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "radius":         {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "interior", "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "shape_kind":     {"type": "str", "default": "diamond", "valid": "diamond"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        radius = ctx.draw_int("radius", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
        radius = ctx.draw_int("radius", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 7, 11)
        radius = ctx.draw_int("radius", 1, 2)
    g = full_grid(h, w, 0)
    cr = rng.randint(radius, h - radius - 1)
    cc = rng.randint(radius, w - radius - 1)
    for r in range(h):
        for c in range(w):
            if abs(r - cr) + abs(c - cc) <= radius:
                g[r][c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        # no shape — onion depth histogram is empty
        return g
    if name == "two_shapes":
        # two separate components → predicate "one connected shape" fails
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 2
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][5 + dc] = 2
        return g
    if name == "hollow_shape":
        # shape with a hole → erosion layer counts mis-represent "solid" depth
        for r, c in [(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)]:
            g[r][c] = 2
        return g
    return g
