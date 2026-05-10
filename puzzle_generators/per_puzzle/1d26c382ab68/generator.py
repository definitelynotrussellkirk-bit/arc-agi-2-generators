"""Generator for 5e687677.

Rule: lower objects matching the top color-1 template shape under
rotation are recolored red.

Combinatorial axes (8): grid_h/w, candidate_color, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_template, no_candidates, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1d26c382ab68"
VERSION = "1.1.0"
TASK_ID = "1d26c382ab68"
SUMMARY = "Lower objects matching the top template shape under rotation are recolored red."

INVARIANTS = [
    "a full color-9 separator row splits template from candidates",
    "the top template is read as the cropped shape of color 1",
    "matching lower objects are recolored to color 2 while non-matching objects are preserved",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_candidates", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "candidate_color":{"type": "color", "default": "rng !{0,1,2,9}",
                       "valid": "3..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint_l(g, r, c, color):
    for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1)]:
        g[r + dr][c + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    color = ctx.draw_color("candidate_color", exclude={0, 1, 2, 9})
    g = full_grid(12, 12, 0)
    _paint_l(g, 1, 2 + (sample_index % 2), 1)
    sep = 5
    for c in range(12):
        g[sep][c] = 9
    _paint_l(g, 7, 2 + ((sample_index // 2) % 2), color)
    g[7][8] = color
    g[8][9] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_template":
        for c in range(12):
            g[5][c] = 9
        g[7][3] = 4
        return g
    if name == "no_candidates":
        for c in range(12):
            g[5][c] = 9
        _paint_l(g, 1, 3, 1)
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 9
        return g
    return g
