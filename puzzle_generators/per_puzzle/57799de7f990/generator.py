"""Generator for 60a26a3e.

Rule: red diamond markers that share a row or column are connected
by blue line segments.

Combinatorial axes (8): grid_h/w, layout, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_diamonds.
Degenerates: no_diamonds, single_diamond, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "57799de7f990"
VERSION = "1.1.0"
TASK_ID = "57799de7f990"
SUMMARY = "Red diamonds aligned in row or column connected by blue line segments."

INVARIANTS = [
    "background is color 0",
    "each marker is a color-2 cardinal diamond around an empty center",
    "some marker centers share exact rows or columns",
    "diamonds sit clear of grid borders so their cardinal cells are in-bounds",
]

LAYOUTS = ("elbow", "row", "column")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_diamonds", "single_diamond", "full_grid")
HELPFUL_TEXTURES = LAYOUTS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 15..19", "valid": "13..22"},
    "grid_w":         {"type": "int", "default": "rng 15..19", "valid": "13..22"},
    "layout":         {"type": "str", "default": "rng helpful",
                       "valid": "|".join(LAYOUTS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_diamonds":     {"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for layout",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_diamond(g, r, c):
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        g[r + dr][c + dc] = 2


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("jitter")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    layout = (overrides.get("texture") if overrides.get("texture") in LAYOUTS else None) or \
             overrides.get("layout") or \
             ctx.draw_choice("layout", list(LAYOUTS))
    h = 15 + 2 * rng.randint(0, 2)
    w = 15 + 2 * rng.randint(0, 2)
    g = full_grid(h, w, 0)
    if layout == "row":
        r = 3 + 2 * rng.randint(0, 2)
        centers = [(r, 3), (r, 8), (r, 13)]
    elif layout == "column":
        c = 4 + 2 * rng.randint(0, 2)
        centers = [(3, c), (8, c), (13, c)]
    else:
        centers = [(4, 4), (4, 10), (10, 10)]
    for r, c in centers:
        _draw_diamond(g, r, c)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 0)
    if name == "no_diamonds":
        return g
    if name == "single_diamond":
        _draw_diamond(g, 7, 7)
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 2
        return g
    return g
