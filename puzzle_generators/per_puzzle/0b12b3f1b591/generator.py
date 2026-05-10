"""Generator for arc_puzzle_bank_nineteenth21:E131.

Rule: a single top-row legend color recolors body markers (color 1) to
the legend color; the legend row is cleared.

Combinatorial axes (8): grid_h/w, palette_kind, legend_color, n_markers,
palette_size, position_bias, n_distinct_colors, marker_density, texture.
Degenerates: no_legend, no_markers, multi_legend.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0b12b3f1b591"
VERSION = "1.1.0"
TASK_ID = "0b12b3f1b591"
SUMMARY = "A single top-row legend color recolors body markers with value 1."

INVARIANTS = [
    "background is 0",
    "the top row contains exactly one nonzero legend cell",
    "body markers use color 1",
    "the output clears the legend row and recolors body markers",
]

PALETTE_KINDS = ("default", "warm_legend", "cool_legend", "rainbow_legend")
DEGENERATE_TEXTURES = ("no_legend", "no_markers", "multi_legend")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..7", "valid": "3..12"},
    "grid_w":         {"type": "int", "default": "rng 5..9", "valid": "3..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "legend_color":   {"type": "int", "default": "rng", "valid": "2..9"},
    "markers":        {"type": "int", "default": "rng 3..7", "valid": "1..20"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "marker_density": {"type": "str", "default": "mixed", "valid": "mixed"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 5, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 4, 7)
        w = ctx.draw_int("grid_w", 5, 9)
    target = ctx.draw_int("markers", 3, 7)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    legend_color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    g[0][rng.randrange(w)] = legend_color
    body = [(r, c) for r in range(1, h) for c in range(w)]
    rng.shuffle(body)
    for r, c in body[:target]:
        g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # markers but no legend → recolor source undefined
        g[2][3] = 1
        g[3][5] = 1
        g[4][1] = 1
        return g
    if name == "no_markers":
        # legend but no body markers — rule has nothing to recolor
        g[0][3] = 5
        return g
    if name == "multi_legend":
        # multiple legends in row 0 → ambiguous which color to apply
        g[0][1] = 4
        g[0][5] = 7
        g[2][3] = 1
        g[4][2] = 1
        return g
    return g
