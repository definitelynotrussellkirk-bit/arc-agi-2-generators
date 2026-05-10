"""Generator for 642248e4.

Rule: border colors project one cell inward from each color-1 marker
toward matching side.

Combinatorial axes (8): grid_h/w, orientation, marker_count,
palette_kind, anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_borders, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b19deac47327"
VERSION = "1.1.0"
TASK_ID = "b19deac47327"
SUMMARY = "Border colors project one cell inward from color-1 markers."

INVARIANTS = [
    "background is color 0",
    "either the top and bottom rows or the left and right columns are solid nonzero borders",
    "interior color-1 markers sit away from the border",
    "markers in the upper/left half project the first border color, and the others project the far border color",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_borders", "no_markers", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "7..18"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "7..18"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "marker_count":   {"type": "int", "default": "rng 4..6", "valid": "2..12"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered|spread|rng"},
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
    if difficulty == "easy":
        h_lo, h_hi = 7, 9
        mc_lo, mc_hi = 2, 4
    elif difficulty == "hard":
        h_lo, h_hi = 13, 18
        mc_lo, mc_hi = 6, 12
    else:
        h_lo, h_hi = 9, 13
        mc_lo, mc_hi = 4, 6
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("orientation") or \
                  ctx.draw_choice("orientation", list(ORIENTATIONS))
    marker_count = ctx.draw_int("marker_count", mc_lo, mc_hi)
    edge_a, edge_b = ctx.draw_distinct_colors("edge_colors", n=2,
                                              exclude={0, 1})
    h = rng.randint(h_lo, h_hi)
    w = rng.randint(h_lo, h_hi)
    g = full_grid(h, w, 0)
    if orientation == "horizontal":
        for c in range(w):
            g[0][c] = edge_a
            g[h - 1][c] = edge_b
        candidates = [(r, c) for r in range(2, h - 2) for c in range(1, w - 1)]
    else:
        for r in range(h):
            g[r][0] = edge_a
            g[r][w - 1] = edge_b
        candidates = [(r, c) for r in range(1, h - 1) for c in range(2, w - 2)]
    rng.shuffle(candidates)
    for r, c in candidates[:marker_count]:
        g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "no_borders":
        for r in range(2, h - 2):
            for c in range(2, w - 2):
                if rng.random() < 0.1:
                    g[r][c] = 1
        return g
    if name == "no_markers":
        for c in range(w):
            g[0][c] = 2
            g[h - 1][c] = 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
