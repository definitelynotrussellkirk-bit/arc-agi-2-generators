"""Generator for 1efba499.

Rule: colored dots on opposite sides of a dominant barrier move to
the nearest barrier edge.

Combinatorial axes (8): grid_h/w, orientation, pair_count,
palette_kind, anchor_corner, asymmetry_force, palette_size, barrier.
Degenerates: no_barrier, no_dots, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a2ad2da63297"
VERSION = "1.1.0"
TASK_ID = "a2ad2da63297"
SUMMARY = "Dots on opposite sides of barrier move to nearest barrier edge."

INVARIANTS = [
    "the barrier color is the most frequent nonzero color",
    "the barrier is either a horizontal or vertical straight segment",
    "selected barrier rows or columns have one colored dot on each side",
    "barrier color is non-zero and distinct from dot colors",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_barrier", "no_dots", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "pair_count":     {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "barrier":        {"type": "color", "default": "rng !0", "valid": "1..9"},
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
    pair_count = ctx.draw_int("pair_count", 2, 4)
    barrier = ctx.draw_color("barrier", exclude={0})
    dot_colors = ctx.draw_distinct_colors("dot_colors", n=4, exclude={0, barrier})
    h = rng.randint(10, 13)
    w = rng.randint(10, 13)
    g = full_grid(h, w, 0)
    if orientation == "horizontal":
        row = rng.randint(4, h - 5)
        c0 = rng.randint(1, 2)
        length = min(w - c0 - 1, rng.randint(6, 8))
        for c in range(c0, c0 + length):
            g[row][c] = barrier
        cols = list(range(c0 + 1, c0 + length - 1))
        rng.shuffle(cols)
        for i, c in enumerate(cols[:pair_count]):
            g[row - 2][c] = dot_colors[i % len(dot_colors)]
            g[row + 2][c] = dot_colors[(i + 1) % len(dot_colors)]
    else:
        col = rng.randint(4, w - 5)
        r0 = rng.randint(1, 2)
        length = min(h - r0 - 1, rng.randint(6, 8))
        for r in range(r0, r0 + length):
            g[r][col] = barrier
        rows = list(range(r0 + 1, r0 + length - 1))
        rng.shuffle(rows)
        for i, r in enumerate(rows[:pair_count]):
            g[r][col - 2] = dot_colors[i % len(dot_colors)]
            g[r][col + 2] = dot_colors[(i + 1) % len(dot_colors)]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_barrier":
        g[3][3] = 2; g[7][7] = 3
        return g
    if name == "no_dots":
        for c in range(11):
            g[5][c] = 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 2
        return g
    return g
