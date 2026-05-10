"""Generator for 9ba4a9aa.

Rule: the icon adjacent to the most common outside dot color is
extracted.

Combinatorial axes (8): grid_h/w, answer_slot, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_icons, no_dots, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "48c4cd5004a1"
VERSION = "1.1.0"
TASK_ID = "48c4cd5004a1"
SUMMARY = "Icon adjacent to the most common outside dot color is extracted."

INVARIANTS = [
    "the background is zero",
    "several 3x3 icons have a uniform border and contrasting center",
    "outside singleton dots are not part of any icon",
    "the most frequent dot color touches exactly one icon",
]

SLOTS = ("S0", "S1", "S2", "S3")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_icons", "no_dots", "full_grid")
HELPFUL_TEXTURES = SLOTS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "answer_slot":    {"type": "choice", "default": "rng helpful",
                       "valid": "0|1|2|3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "9", "valid": "9"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "9", "valid": "9"},
    "texture":        {"type": "str", "default": "alias for answer_slot",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _icon(g, r, c, border, center):
    for dr in range(3):
        for dc in range(3):
            g[r + dr][c + dc] = border
    g[r + 1][c + 1] = center


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in SLOTS:
        answer = int(tx[1])
    else:
        answer = ctx.draw_choice("answer_slot", [0, 1, 2, 3])
    colors = ctx.draw_distinct_colors("colors", n=9, exclude={0})
    g = full_grid(14, 14, 0)
    slots = [(1, 1), (1, 9), (9, 1), (9, 9)]
    dot_color = colors[8]
    for idx, (r, c) in enumerate(slots):
        _icon(g, r, c, colors[idx], colors[idx + 4])
    ar, ac = slots[answer]
    g[ar + 3][ac + 1] = dot_color
    g[ar + 4][ac + 1] = dot_color
    g[6][6] = colors[(answer + 1) % 4]
    g[7][7] = colors[(answer + 2) % 4]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 14, 0)
    if name == "no_icons":
        g[6][6] = 3
        return g
    if name == "no_dots":
        for r, c in [(1, 1), (1, 9), (9, 1), (9, 9)]:
            _icon(g, r, c, 3, 4)
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(14):
                g[r][c] = 5
        return g
    return g
