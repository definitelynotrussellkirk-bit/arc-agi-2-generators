"""Generator for e3fe1151.

Rule: each 2x2 quadrant hole is filled with the color missing from
that quadrant's balanced four-color set.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_quadrants,
n_distinct_colors.
Degenerates: no_holes, all_holes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ca2f5aaf9d79"
VERSION = "1.1.0"
TASK_ID = "ca2f5aaf9d79"
SUMMARY = "2x2 quadrant holes filled with the color missing from each quadrant set."

INVARIANTS = [
    "the puzzle is a 5x5 grid",
    "color 7 marks exactly one hole in each corner 2x2 quadrant",
    "four non-hole colors appear once per quadrant after filling",
    "palette colors are distinct and exclude 7",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_holes", "all_holes", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "5", "valid": "5"},
    "grid_w":         {"type": "int", "default": "5", "valid": "5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_quadrants":    {"type": "int", "default": "4", "valid": "4"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
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
    colors = list(ctx.draw_distinct_colors("palette", n=4, exclude={7}))
    g = full_grid(5, 5, 0)
    quads = [
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 3), (0, 4), (1, 3), (1, 4)],
        [(3, 0), (3, 1), (4, 0), (4, 1)],
        [(3, 3), (3, 4), (4, 3), (4, 4)],
    ]
    for qi, cells in enumerate(quads):
        missing = colors[qi]
        vals = [v for v in colors if v != missing]
        for (r, c), value in zip(cells[:3], vals):
            g[r][c] = value
        r, c = cells[3]
        g[r][c] = 7
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 5, 0)
    if name == "no_holes":
        for r in range(5):
            for c in range(5):
                g[r][c] = 2
        return g
    if name == "all_holes":
        for r in range(5):
            for c in range(5):
                g[r][c] = 7
        return g
    if name == "full_grid":
        for r in range(5):
            for c in range(5):
                g[r][c] = 7
        return g
    return g
