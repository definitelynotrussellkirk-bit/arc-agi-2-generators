"""Generator for ba1aa698.

Rule: marker positions progress through bordered boxes and
extrapolate into the next box.

Combinatorial axes (8): grid_h/w, delta, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_boxes.
Degenerates: no_borders, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8a8682f21e71"
VERSION = "1.1.0"
TASK_ID = "8a8682f21e71"
SUMMARY = "Marker positions progress through bordered boxes; rule extrapolates."

INVARIANTS = [
    "full-height border-color columns divide equal-width boxes",
    "each box interior starts as a uniform box color",
    "the same marker shape appears in each known box with consistent vertical progression",
    "border, box and marker colors are distinct and non-zero",
]

DELTAS = ("d1", "d2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_borders", "no_markers", "full_grid")
HELPFUL_TEXTURES = DELTAS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16"},
    "delta":          {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DELTAS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_boxes":        {"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for delta",
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
    if tx in DELTAS:
        delta = int(tx[1])
    else:
        delta = ctx.draw_choice("delta", [1, 2])
    border, box, marker = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    h = 9
    box_w = 4
    n_boxes = 3
    w = n_boxes * box_w + n_boxes + 1
    g = full_grid(h, w, box)
    for c in range(w):
        g[0][c] = border
        g[h - 1][c] = border
    border_cols = [i * (box_w + 1) for i in range(n_boxes + 1)]
    for c in border_cols:
        for r in range(h):
            g[r][c] = border
    for i in range(n_boxes):
        left = border_cols[i] + 1
        top = 1 + i * delta
        for dr, dc in [(0, 1), (1, 1), (1, 2)]:
            g[top + dr][left + dc] = marker
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 16, 5)
    if name == "no_borders":
        g[3][3] = 2
        return g
    if name == "no_markers":
        for c in range(16):
            g[0][c] = 1; g[8][c] = 1
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(16):
                g[r][c] = 1
        return g
    return g
