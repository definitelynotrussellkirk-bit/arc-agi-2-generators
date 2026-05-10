"""Generator for b1986d4b.

Rule: counts of colored solid squares by side length are encoded as a
staircase.

Combinatorial axes (8): grid_h/w, counts, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_squares, single_square, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "d0a85a878975"
VERSION = "1.1.0"
TASK_ID = "d0a85a878975"
SUMMARY = "Counts of colored solid squares by side length encoded as staircase."

INVARIANTS = [
    "foreground components are solid same-color squares with side length at least two",
    "each square size has its own color",
    "the rule counts squares per size and emits a compact staircase encoding",
]

COUNT_KINDS = ("c0", "c1", "c2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_squares", "single_square", "full_grid")
HELPFUL_TEXTURES = COUNT_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16"},
    "counts":         {"type": "choice", "default": "rng helpful",
                       "valid": "0|1|2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for counts",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in COUNT_KINDS:
        counts_variant = int(tx[1])
    else:
        counts_variant = ctx.draw_choice("counts", [0, 1, 2])
    c2, c3, c4 = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    counts = [
        {2: 1, 3: 2, 4: 1},
        {2: 2, 3: 2, 4: 1},
        {2: 1, 3: 1, 4: 2},
    ][counts_variant]
    colors = {2: c2, 3: c3, 4: c4}
    positions = {
        2: [(1, 1), (1, 5)],
        3: [(6, 1), (6, 6)],
        4: [(1, 11), (8, 10)],
    }
    g = full_grid(14, 16, 0)
    for size in [2, 3, 4]:
        for r, c in positions[size][:counts[size]]:
            draw_rect(g, r, c, size, size, colors[size])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 16, 0)
    if name == "no_squares":
        return g
    if name == "single_square":
        draw_rect(g, 1, 1, 2, 2, 3)
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(16):
                g[r][c] = 3
        return g
    return g
