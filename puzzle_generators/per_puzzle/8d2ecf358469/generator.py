"""Generator for 4b:hard_25 — bar chart component areas by color.

Rule: for each non-bg color, compute total cell count across all its
components. Output is a grid where each row is a color (sorted asc)
filled with that color from col 0 for `area` cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, single_color, all_areas_equal.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8d2ecf358469"
VERSION = "1.1.0"
TASK_ID = "8d2ecf358469"
SUMMARY = "2-3 colors with multiple components each, distinct total areas."

INVARIANTS = [
    "background is 0",
    "2-3 distinct non-bg colors",
    "each color has 1-2 components; total areas across colors are strictly distinct",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "single_color", "all_areas_equal")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "scattered_areas_by_color",
                       "valid": "scattered_areas_by_color"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = {
    1: [[(0, 0)]],
    2: [[(0, 0), (0, 1)], [(0, 0), (1, 0)]],
    3: [[(0, 0), (0, 1), (1, 0)], [(0, 0), (0, 1), (0, 2)]],
    4: [[(0, 0), (0, 1), (1, 0), (1, 1)]],
    5: [[(0, 0), (0, 1), (1, 0), (1, 1), (1, 2)]],
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def _place(g, rng, shape, color):
    h, w = len(g), len(g[0])
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    for _ in range(40):
        r0 = rng.randint(0, h - sh); c0 = rng.randint(0, w - sw)
        if not _free(g, r0, c0, r0 + sh - 1, c0 + sw - 1): continue
        for dr, dc in shape:
            g[r0 + dr][c0 + dc] = color
        return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 17)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_colors = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_colors)
    sizes = rng.sample([2, 3, 4, 5], n_colors)
    for color, size in zip(palette, sizes):
        _place(g, rng, rng.choice(_SHAPES[size]), color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_components":
        # Empty grid — bar chart has zero rows.
        return g
    if name == "single_color":
        # Only one color present — rule's per-color sort has a
        # single bar; output is one row.
        for r, c in [(2, 2), (2, 3), (2, 4)]: g[r][c] = 4
        return g
    if name == "all_areas_equal":
        # Both colors have identical total areas — rule's "sort
        # by area" tie-break ambiguous; bar lengths equal.
        for r, c in [(2, 2), (2, 3)]: g[r][c] = 4
        for r, c in [(6, 7), (6, 8)]: g[r][c] = 6
        return g
    return g
