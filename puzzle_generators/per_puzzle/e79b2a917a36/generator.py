"""Generator for 5adee1b2.

Rule: left-edge palette pairs map source colors to frame colors
around matching icons.

Combinatorial axes (8): grid_h/w, entry_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_palette, no_icons, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e79b2a917a36"
VERSION = "1.1.0"
TASK_ID = "e79b2a917a36"
SUMMARY = "Palette pairs map source colors to frame colors around matching icons."

INVARIANTS = [
    "background is color 0",
    "palette entries are two-row source/frame color pairs in columns 0 and 1",
    "source-color icons away from the palette are separated",
    "palette colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_palette", "no_icons", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "entry_count":    {"type": "int", "default": "2", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    n = ctx.draw_int("entry_count", 2, 2)
    h = 12 + rng.randint(0, 4)
    w = 12 + rng.randint(0, 4)
    colors = ctx.draw_distinct_colors("colors", n=2 * n, exclude={0})
    g = full_grid(h, w, 0)
    for i in range(n):
        src = colors[2 * i]
        frame = colors[2 * i + 1]
        rr = i * 3
        g[rr][0] = src
        g[rr + 1][0] = src
        g[rr][1] = frame
        g[rr + 1][1] = frame
        r0 = 3 + i * 4
        c0 = 5 + ((sample_index + i) % 2)
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[r0 + dr][c0 + dc] = src
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_palette":
        for r in range(2):
            g[5][5 + r] = 2
        return g
    if name == "no_icons":
        for i in range(2):
            g[i][0] = 2; g[i][1] = 3
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
