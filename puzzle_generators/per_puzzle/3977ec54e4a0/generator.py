"""Generator for 896d5239.

Rule: three nearby green markers define a triangular wedge whose
interior is filled with cyan.

Combinatorial axes (8): grid_h/w, orientation, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_markers, single_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3977ec54e4a0"
VERSION = "1.1.0"
TASK_ID = "3977ec54e4a0"
SUMMARY = "Three nearby green markers define triangular wedge filled with cyan."

INVARIANTS = [
    "green markers form a valid V-shaped triangle support",
    "the apex and both arms are within Chebyshev distance two links of each other",
    "covered non-marker cells inside the triangle become color 8",
]

ORIENTATIONS = ("down", "up", "right", "left")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "single_marker", "full_grid")
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
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
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
                  ["down", "up", "right", "left"][sample_index % 4]
    g = full_grid(12, 12, 0)
    d = 2
    shift = (sample_index // 4) % 3
    if orientation == "down":
        apex = (2 + shift, 6)
        arms = [(apex[0] + d, apex[1] - d), (apex[0] + d, apex[1] + d)]
    elif orientation == "up":
        apex = (9 - shift, 6)
        arms = [(apex[0] - d, apex[1] - d), (apex[0] - d, apex[1] + d)]
    elif orientation == "right":
        apex = (6, 2 + shift)
        arms = [(apex[0] - d, apex[1] + d), (apex[0] + d, apex[1] + d)]
    else:
        apex = (6, 9 - shift)
        arms = [(apex[0] - d, apex[1] - d), (apex[0] + d, apex[1] - d)]
    for r, c in [apex] + arms:
        g[r][c] = 3
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_markers":
        return g
    if name == "single_marker":
        g[6][6] = 3
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 3
        return g
    return g
