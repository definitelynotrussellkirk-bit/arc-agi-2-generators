"""Generator for arc_puzzle_bank_21_set12_s:S12_E1 — anchor recolors all touching neighbors to 4.

Rule: a color-1 anchor touches several components; exactly those
neighbors are recolored to 4.

Combinatorial axes (8): grid_h, grid_w, palette_kind, neighbor_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, no_neighbors, all_isolated.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a4fb12580b3f"
VERSION = "1.1.0"
TASK_ID = "a4fb12580b3f"
SUMMARY = "A color-1 anchor touches several components; exactly those neighbors are recolored to 4."

INVARIANTS = [
    "background is 0",
    "there is exactly one color-1 anchor component",
    "the anchor has two or three edge-touching neighbor components",
    "at least one non-neighbor distractor component is isolated from the anchor",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "no_neighbors", "all_isolated")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..15"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "neighbor_count": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "anchor_with_neighbors_and_distractor",
                       "valid": "anchor_with_neighbors_and_distractor"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint(g, cells, color):
    for r, c in cells:
        g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        n = ctx.draw_int("neighbor_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
        n = ctx.draw_int("neighbor_count", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 13)
        n = ctx.draw_int("neighbor_count", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    r = rng.randint(2, h - 4)
    c = rng.randint(2, w - 7)
    g[r][c] = 1
    neighbor_specs = [
        (3, [(r, c + 1), (r, c + 2)]),
        (6, [(r + 1, c), (r + 2, c)]),
        (8, [(r, c - 1)]),
    ]
    for color, cells in neighbor_specs[:n]:
        _paint(g, cells, color)
    _paint(g, [(h - 2, w - 3), (h - 2, w - 2)], 7)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # no color-1 component → no anchor to identify neighbors
        _paint(g, [(2, 2), (2, 3)], 3)
        _paint(g, [(5, 5), (6, 5)], 6)
        _paint(g, [(h - 2, w - 3), (h - 2, w - 2)], 7)
        return g
    if name == "no_neighbors":
        # anchor exists but is isolated → no neighbors to recolor
        g[3][3] = 1
        _paint(g, [(7, 8), (7, 9)], 7)
        return g
    if name == "all_isolated":
        # every component is isolated from the anchor → rule recolors nothing
        g[3][3] = 1
        _paint(g, [(7, 7), (7, 8)], 3)
        _paint(g, [(2, 8), (2, 9)], 6)
        return g
    return g
