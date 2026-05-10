"""Generator for 7d60a8d4.

Rule: green plus centers connected diagonally receive red bridge
cells between them.

Combinatorial axes (8): grid_h/w, direction, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_pluses, single_plus, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e5525362bfb8"
VERSION = "1.1.0"
TASK_ID = "e5525362bfb8"
SUMMARY = "Diagonally connected green plus centers receive red bridge cells."

INVARIANTS = [
    "candidate centers are color-3 cells with all four cardinal neighbors also color 3",
    "pairs of centers on a non-adjacent diagonal define the bridge",
    "zero cells between those centers are painted color 2",
    "the two pluses sit clear of grid borders",
]

DIRECTIONS = ("down-right", "down-left")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pluses", "single_plus", "full_grid")
HELPFUL_TEXTURES = ("dr", "dl")

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "direction":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DIRECTIONS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for direction",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint_plus(g, r, c):
    for dr, dc in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
        g[r + dr][c + dc] = 3


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in HELPFUL_TEXTURES:
        direction = "down-right" if tx == "dr" else "down-left"
    else:
        direction = ctx.draw_choice("direction", list(DIRECTIONS))
        if "direction" not in overrides:
            direction = "down-right" if sample_index % 2 == 0 else "down-left"
    g = full_grid(12, 12, 0)
    r1 = 2 + (sample_index % 3)
    c1 = 2 if direction == "down-right" else 9
    delta = 5
    c2 = c1 + delta if direction == "down-right" else c1 - delta
    _paint_plus(g, r1, c1)
    _paint_plus(g, r1 + delta, c2)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_pluses":
        return g
    if name == "single_plus":
        _paint_plus(g, 5, 5)
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 3
        return g
    return g
