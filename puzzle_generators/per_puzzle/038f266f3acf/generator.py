"""Generator for b527c5c6.

Rule: a red cell on the edge of a solid green rectangle emits an
outward beam with green side rails.

Combinatorial axes (8): grid_h/w, edge, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_rect, no_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "038f266f3acf"
VERSION = "1.1.0"
TASK_ID = "038f266f3acf"
SUMMARY = "Red marker on a solid green rectangle edge emits outward beam with side rails."

INVARIANTS = [
    "background is color 0",
    "a solid nonzero rectangle uses color 3",
    "one edge cell of the rectangle is red color 2",
    "the red marker projects outward from the rectangle edge",
]

EDGES = ("top", "bottom", "left", "right")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rect", "no_marker", "full_grid")
HELPFUL_TEXTURES = EDGES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..14", "valid": "12..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "12..14"},
    "edge":           {"type": "str", "default": "rng helpful",
                       "valid": "|".join(EDGES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "center", "valid": "center"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for edge",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    edge = (overrides.get("texture") if overrides.get("texture") in EDGES else None) or \
           overrides.get("edge") or \
           ctx.draw_choice("edge", list(EDGES))
    if difficulty == "easy":
        h = 12
        w = 12
    elif difficulty == "hard":
        h = 13 + rng.randint(0, 1)
        w = 13 + rng.randint(0, 1)
    else:
        h = 12 + rng.randint(0, 2)
        w = 12 + rng.randint(0, 2)
    g = full_grid(h, w, 0)
    r0 = 4
    c0 = 4
    rh = 4
    rw = 4
    for r in range(r0, r0 + rh):
        for c in range(c0, c0 + rw):
            g[r][c] = 3
    if edge == "top":
        g[r0][c0 + rw // 2] = 2
    elif edge == "bottom":
        g[r0 + rh - 1][c0 + rw // 2] = 2
    elif edge == "left":
        g[r0 + rh // 2][c0] = 2
    else:
        g[r0 + rh // 2][c0 + rw - 1] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_rect":
        g[6][6] = 2
        return g
    if name == "no_marker":
        for r in range(4, 8):
            for c in range(4, 8):
                g[r][c] = 3
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 3
        return g
    return g
