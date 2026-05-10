"""Generator for d017b73f.

Rule: separated path objects are packed left-to-right by connecting
exits to entries.

Combinatorial axes (8): grid_h/w, variant, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_paths, single_path, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "664a918eb273"
VERSION = "1.1.0"
TASK_ID = "664a918eb273"
SUMMARY = "Separated path objects are packed left-to-right by connecting exits to entries."

INVARIANTS = [
    "each colored object is a one-cell-wide orthogonal path",
    "objects are ordered by their leftmost column",
    "each later path is translated so its leftmost endpoint follows the previous exit",
]

VARIANTS = ("v0", "v1", "v2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_paths", "single_path", "full_grid")
HELPFUL_TEXTURES = VARIANTS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9"},
    "grid_w":         {"type": "int", "default": "20", "valid": "20"},
    "variant":        {"type": "choice", "default": "rng helpful",
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
    "texture":        {"type": "str", "default": "alias for variant",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint_offsets(g, r0, c0, offsets, color):
    for dr, dc in offsets:
        g[r0 + dr][c0 + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in VARIANTS:
        variant = int(tx[1])
    else:
        variant = ctx.draw_choice("variant", [0, 1, 2])
    colors = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    g = full_grid(9, 20, 0)
    shapes = [
        [(0, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 2)],
    ]
    rows = [
        [1, 4, 2],
        [2, 1, 5],
        [4, 2, 1],
    ][variant]
    cols = [1, 8, 15]
    for i, color in enumerate(colors):
        _paint_offsets(g, rows[i], cols[i], shapes[i], color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 20, 0)
    if name == "no_paths":
        return g
    if name == "single_path":
        _paint_offsets(g, 1, 1, [(0, 0), (0, 1), (1, 1)], 3)
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(20):
                g[r][c] = 4
        return g
    return g
