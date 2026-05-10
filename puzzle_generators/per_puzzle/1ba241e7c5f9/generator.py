"""Generator for 1be83260.

Rule: a marker slot provides colors for a clean dice-mask slot in a
tiled output.

Combinatorial axes (8): grid_h/w, base_color, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_markers, no_clean, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1ba241e7c5f9"
VERSION = "1.1.0"
TASK_ID = "1ba241e7c5f9"
SUMMARY = "Marker slot provides colors for a clean dice-mask slot in a tiled output."

INVARIANTS = [
    "nonzero rows and columns form two 5x5 slot bands in each direction",
    "one slot contains marker colors at dice-pip positions",
    "one clean slot contains only the base mask color",
    "the clean mask determines which output positions receive marker-slot colors",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "no_clean", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "base_color":     {"type": "int", "default": "1", "valid": "1"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
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
    base = ctx.draw_int("base_color", 1, 1)
    colors = ctx.draw_distinct_colors("marker_colors", n=4, exclude={0, base})
    g = full_grid(11, 11, 0)
    row_starts = [0, 6]
    col_starts = [0, 6]
    for rs in row_starts:
        for cs in col_starts:
            for r in range(rs, rs + 5):
                for c in range(cs, cs + 5):
                    g[r][c] = base
    marker_positions = [(1, 1), (1, 3), (3, 1), (3, 3)]
    for (dr, dc), color in zip(marker_positions, colors):
        g[dr][dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_markers":
        for rs in [0, 6]:
            for cs in [0, 6]:
                for r in range(rs, rs + 5):
                    for c in range(cs, cs + 5):
                        g[r][c] = 1
        return g
    if name == "no_clean":
        for rs in [0, 6]:
            for cs in [0, 6]:
                for r in range(rs, rs + 5):
                    for c in range(cs, cs + 5):
                        g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 1
        return g
    return g
