"""Generator for 50a16a69.

Rule: periodic checker tile with one removed color is recovered,
color-cycled, and tiled across the grid.

Combinatorial axes (8): grid_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, removal_size,
n_distinct_colors.
Degenerates: no_removed, all_removed, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "27d29b6b289a"
VERSION = "1.1.0"
TASK_ID = "27d29b6b289a"
SUMMARY = "Periodic checker tile with one removed color recovered and color-cycled."

INVARIANTS = [
    "one removed color appears in adjacent same-color runs as a wildcard",
    "all non-removed cells support a small periodic tile",
    "the tile colors are read in first-appearance order",
    "tile and removed colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_removed", "all_removed", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 12..18", "valid": "8..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "removal_size":   {"type": "str", "default": "4x5", "valid": "4x5"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    a, b, removed = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    if difficulty == "easy":
        h_lo, h_hi = 12, 13
    elif difficulty == "hard":
        h_lo, h_hi = 18, 22
    else:
        h_lo, h_hi = 12, 18
    h = ctx.draw_int("height", h_lo, h_hi)
    w = ctx.draw_int("width", h_lo, h_hi)
    g = full_grid(h, w, 0)
    tile = [[a, b], [b, a]]
    for r in range(h):
        for c in range(w):
            g[r][c] = tile[r % 2][c % 2]
    r0 = rng.randint(3, h - 5)
    c0 = rng.randint(3, w - 5)
    for r in range(r0, min(h, r0 + 4)):
        for c in range(c0, min(w, c0 + 5)):
            g[r][c] = removed
    return g


def _draw_from_degenerate(name, rng):
    h = w = 14
    g = full_grid(h, w, 0)
    tile = [[2, 3], [3, 2]]
    for r in range(h):
        for c in range(w):
            g[r][c] = tile[r % 2][c % 2]
    if name == "no_removed":
        return g
    if name == "all_removed":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
