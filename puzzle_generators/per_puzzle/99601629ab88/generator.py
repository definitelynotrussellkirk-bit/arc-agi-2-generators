"""Generator for 9f236235.

Rule: divider grid; rule extracts top-left of each cell, then flips
LR.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
divider_count.
Degenerates: no_dividers, all_dividers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "99601629ab88"
VERSION = "1.1.0"
TASK_ID = "99601629ab88"
SUMMARY = "Divider grid; rule extracts top-left of each cell then flips LR."

INVARIANTS = [
    "single divider color forms full rows AND full cols",
    "two row bands and two col bands carved by dividers",
    "each cell paints its top-left with one non-bg non-divider color",
    "divider color is distinct from cell colors",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_dividers", "all_dividers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "divider_count":  {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 11, 12
    elif difficulty == "hard":
        h_lo, h_hi = 14, 17
    else:
        h_lo, h_hi = 11, 15
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette = ctx.draw_distinct_colors("palette", n=4, exclude={0})
    div_color = palette[0]
    cell_colors = palette[1:]
    g = full_grid(h, w, 0)
    div_r1 = rng.randint(2, h // 2)
    div_r2 = rng.randint(div_r1 + 2, h - 2)
    div_c1 = rng.randint(2, w // 2)
    div_c2 = rng.randint(div_c1 + 2, w - 2)
    for c in range(w):
        g[div_r1][c] = div_color
        g[div_r2][c] = div_color
    for r in range(h):
        g[r][div_c1] = div_color
        g[r][div_c2] = div_color
    row_starts = [0, div_r1 + 1, div_r2 + 1]
    col_starts = [0, div_c1 + 1, div_c2 + 1]
    for rs in row_starts:
        for cs in col_starts:
            if rng.random() < 0.7:
                g[rs][cs] = rng.choice(cell_colors)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_dividers":
        g[3][3] = 2
        return g
    if name == "all_dividers":
        for r in range(13):
            for c in range(13):
                g[r][c] = 5
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
