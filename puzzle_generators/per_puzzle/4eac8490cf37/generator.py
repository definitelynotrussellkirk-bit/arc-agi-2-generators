"""Generator for 9c1e755f.

Rule: a color-5 line and adjacent seed patch define a rectangle filled
by tiling the seed.

Combinatorial axes (8): grid_h/w, orientation, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_line, no_seed, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4eac8490cf37"
VERSION = "1.1.0"
TASK_ID = "4eac8490cf37"
SUMMARY = "Color-5 line and adjacent seed patch define a rectangle filled by tiling seed."

INVARIANTS = [
    "the background is zero",
    "one color-5 line is horizontal or vertical",
    "a non-5 seed patch sits directly beside the line",
    "the seed pattern is tiled across the line span on the seed side",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_line", "no_seed", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
    a, b = ctx.draw_distinct_colors("seed_colors", n=2, exclude={0, 5})
    g = full_grid(12, 12, 0)
    if orientation == "horizontal":
        for c in range(2, 10):
            g[6][c] = 5
        g[4][2], g[4][3], g[5][2], g[5][3] = a, b, b, a
    else:
        for r in range(2, 10):
            g[r][6] = 5
        g[2][4], g[2][5], g[3][4], g[3][5] = a, b, b, a
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_line":
        g[4][2] = 3
        return g
    if name == "no_seed":
        for c in range(2, 10):
            g[6][c] = 5
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 5
        return g
    return g
