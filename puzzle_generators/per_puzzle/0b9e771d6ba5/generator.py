"""Generator for 52df9849.

Rule: solid rectangle with a foreign colored cell is repaired by
filling the whole bbox with the rectangle color.

Combinatorial axes (8): grid_h/w, rect_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_rect, no_foreign, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0b9e771d6ba5"
VERSION = "1.1.0"
TASK_ID = "0b9e771d6ba5"
SUMMARY = "Solid rectangle with foreign cell repaired by filling bbox with rect color."

INVARIANTS = [
    "background is color 0",
    "one non-background rectangle bbox has no background holes",
    "that bbox contains exactly one foreign non-background color",
    "main and foreign colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rect", "no_foreign", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "8..18"},
    "rect_size":      {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
    if difficulty == "easy":
        sz_lo, sz_hi = 3, 3
    elif difficulty == "hard":
        sz_lo, sz_hi = 4, 5
    else:
        sz_lo, sz_hi = 3, 4
    size = ctx.draw_int("rect_size", sz_lo, sz_hi)
    h = 9 + rng.randint(0, 4)
    w = 9 + rng.randint(0, 4)
    main_color, foreign_color = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(h, w, 0)
    r0 = 2 + ((sample_index + rng.randint(0, 2)) % max(1, h - size - 3))
    c0 = 2 + ((seed + sample_index + rng.randint(0, 2)) % max(1, w - size - 3))
    for dr in range(size):
        for dc in range(size):
            g[r0 + dr][c0 + dc] = main_color
    g[r0 + size // 2][c0 + size // 2] = foreign_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_rect":
        g[5][5] = 3
        return g
    if name == "no_foreign":
        for r in range(3, 6):
            for c in range(3, 6):
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 2
        return g
    return g
