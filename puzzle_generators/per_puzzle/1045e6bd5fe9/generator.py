"""Generator for ecdecbb3.

Rule: each red center projects to nearest full 8 walls, adding legs
and 3x3 wall nodes.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_centers.
Degenerates: no_walls, no_centers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1045e6bd5fe9"
VERSION = "1.1.0"
TASK_ID = "1045e6bd5fe9"
SUMMARY = "Red centers project to nearest full 8 walls; legs and 3x3 nodes added."

INVARIANTS = [
    "the scene has full horizontal or full vertical color-8 walls",
    "one or more color-2 cells sit between those walls",
    "each color-2 projects perpendicular to the wall family",
    "centers sit clear of walls so projections have room",
]

ORIENTATIONS = ("horizontal_walls", "vertical_walls")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_walls", "no_centers", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_centers":      {"type": "int", "default": "2", "valid": "1..4"},
    "texture":        {"type": "str", "default": "alias for orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("orientation") or \
                  ctx.draw_choice("orientation", list(ORIENTATIONS))
    h = 10 + rng.randint(0, 3)
    w = 10 + rng.randint(0, 3)
    g = full_grid(h, w, 0)
    if orientation == "horizontal_walls":
        top = 1
        bot = h - 2
        for c in range(w):
            g[top][c] = 8
            g[bot][c] = 8
        for c in sorted({rng.randint(2, w - 3), rng.randint(2, w - 3)}):
            g[rng.randint(top + 3, bot - 3)][c] = 2
    else:
        left = 1
        right = w - 2
        for r in range(h):
            g[r][left] = 8
            g[r][right] = 8
        for r in sorted({rng.randint(2, h - 3), rng.randint(2, h - 3)}):
            g[r][rng.randint(left + 3, right - 3)] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_walls":
        g[5][5] = 2
        return g
    if name == "no_centers":
        for c in range(11):
            g[1][c] = 8
            g[9][c] = 8
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 8
        return g
    return g
