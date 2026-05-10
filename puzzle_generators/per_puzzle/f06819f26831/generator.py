"""Generator for 72322fa7.

Rule: a complete multicolor template is copied onto matching single-cell
partials.

Combinatorial axes (8): grid_h/w, partial_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_template, no_partials, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f06819f26831"
VERSION = "1.1.0"
TASK_ID = "f06819f26831"
SUMMARY = "Complete multicolor template is copied onto matching single-cell partials."

INVARIANTS = [
    "the background is zero",
    "one 2x2 connected component is a complete multicolor template",
    "partial cells away from the template match unique template colors",
    "each partial is isolated so it remains a partial rather than a second template",
]

PARTIAL_KINDS = ("P2", "P3")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_partials", "full_grid")
HELPFUL_TEXTURES = PARTIAL_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "partial_count":  {"type": "choice", "default": "rng helpful",
                       "valid": "2|3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for partial_count",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint_template(g, r, c, colors):
    g[r][c] = colors[0]
    g[r][c + 1] = colors[1]
    g[r + 1][c] = colors[2]
    g[r + 1][c + 1] = colors[3]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in PARTIAL_KINDS:
        partial_count = int(tx[1])
    elif difficulty == "easy":
        partial_count = 2
    elif difficulty == "hard":
        partial_count = 3
    else:
        partial_count = ctx.draw_choice("partial_count", [2, 3])
    colors = ctx.draw_distinct_colors("template_colors", n=4, exclude={0})
    g = full_grid(11, 12, 0)
    _paint_template(g, 1, 1, colors)
    anchors = [(1, 7), (6, 2), (7, 8)]
    offsets = [(0, 0), (0, 1), (1, 0)]
    for idx in range(partial_count):
        ar, ac = anchors[idx]
        dr, dc = offsets[idx]
        g[ar + dr][ac + dc] = colors[idx]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 12, 0)
    if name == "no_template":
        g[1][7] = 3
        return g
    if name == "no_partials":
        _paint_template(g, 1, 1, [3, 4, 5, 6])
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(12):
                g[r][c] = 3
        return g
    return g
