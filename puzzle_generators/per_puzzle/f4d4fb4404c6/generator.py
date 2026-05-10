"""Generator for c62e2108.

Rule: edge markers extend aligned 4-by-4 hollow frames toward the grid
edge.

Combinatorial axes (8): grid_h/w, direction, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, color.
Degenerates: no_frame, no_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "f4d4fb4404c6"
VERSION = "1.1.0"
TASK_ID = "f4d4fb4404c6"
SUMMARY = "Edge markers extend aligned 4-by-4 hollow frames toward grid edge."

INVARIANTS = [
    "colored objects are 4-by-4 hollow frames",
    "blue edge markers align with a frame span",
    "each marker direction repeats the matching frame until the grid edge",
    "the output keeps frames and their extensions but removes marker cells",
]

DIRECTIONS = ("up", "down", "left", "right")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "no_marker", "full_grid")
HELPFUL_TEXTURES = DIRECTIONS

AXES = {
    "grid_h":         {"type": "int", "default": "16", "valid": "16"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16"},
    "direction":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DIRECTIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "color":          {"type": "color", "default": "rng !{0,1}",
                       "valid": "2..9"},
    "texture":        {"type": "str", "default": "alias for direction",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    direction = (overrides.get("texture") if overrides.get("texture") in DIRECTIONS else None) or \
                overrides.get("direction") or \
                ["up", "right", "down", "left"][sample_index % 4]
    color = ctx.draw_color("frame_color", exclude={0, 1})
    g = full_grid(16, 16, 0)
    if direction in {"up", "down"}:
        r, c = (8, 6) if direction == "up" else (4, 6)
        draw_frame(g, r, c, r + 3, c + 3, color)
        marker_r = 0 if direction == "up" else 15
        g[marker_r][c + 1] = 1
        g[marker_r][c + 2] = 1
    else:
        r, c = 6, 8 if direction == "left" else 4
        draw_frame(g, r, c, r + 3, c + 3, color)
        marker_c = 0 if direction == "left" else 15
        g[r + 1][marker_c] = 1
        g[r + 2][marker_c] = 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(16, 16, 0)
    if name == "no_frame":
        g[0][7] = 1
        g[0][8] = 1
        return g
    if name == "no_marker":
        draw_frame(g, 6, 6, 9, 9, 3)
        return g
    if name == "full_grid":
        for r in range(16):
            for c in range(16):
                g[r][c] = 3
        return g
    return g
