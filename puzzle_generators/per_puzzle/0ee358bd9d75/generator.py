"""Generator for 780d0b14.

Rule: 0-row + 0-col separators carve sections; rule outputs each
section's dominant color.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
divider_count.
Degenerates: no_dividers, single_section, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0ee358bd9d75"
VERSION = "1.1.0"
TASK_ID = "0ee358bd9d75"
SUMMARY = "0-row + 0-col separators carve sections; output each section's dominant color."

INVARIANTS = [
    "background is 0",
    "at least one full-bg row AND at least one full-bg col",
    "each section has at least one non-bg cell with unambiguous mode",
    "section colors are drawn from a non-zero palette",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_dividers", "single_section", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "9..18"},
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
    div_r1 = rng.randint(2, h // 2)
    div_r2 = rng.randint(div_r1 + 2, h - 2)
    div_c1 = rng.randint(2, w // 2)
    div_c2 = rng.randint(div_c1 + 2, w - 2)
    g = full_grid(h, w, 0)
    row_starts = [0, div_r1 + 1, div_r2 + 1]
    row_ends = [div_r1, div_r2, h]
    col_starts = [0, div_c1 + 1, div_c2 + 1]
    col_ends = [div_c1, div_c2, w]
    for ri in range(3):
        for ci in range(3):
            color = rng.choice(palette)
            for r in range(row_starts[ri], row_ends[ri]):
                for c in range(col_starts[ci], col_ends[ci]):
                    if rng.random() < 0.6:
                        g[r][c] = color
            ar = rng.randint(row_starts[ri], row_ends[ri] - 1)
            ac = rng.randint(col_starts[ci], col_ends[ci] - 1)
            g[ar][ac] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_dividers":
        for r in range(13):
            for c in range(13):
                if rng.random() < 0.4:
                    g[r][c] = 2
        return g
    if name == "single_section":
        g[5][5] = 2
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
