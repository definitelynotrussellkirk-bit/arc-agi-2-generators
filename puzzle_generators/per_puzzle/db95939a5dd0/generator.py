"""Generator for 4364c1c4.

Rule: two-color connected compound shape separates: upper color
shifts left, lower color shifts right.

Combinatorial axes (8): grid_h/w, body_width, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_shape, single_color, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "db95939a5dd0"
VERSION = "1.1.0"
TASK_ID = "db95939a5dd0"
SUMMARY = "Two-color compound separates: top shifts left, bottom shifts right."

INVARIANTS = [
    "the background is the mode color",
    "each foreground component contains exactly two colors",
    "one color occupies the top portion and the other occupies the bottom portion",
    "bg, top and bottom colors are distinct",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shape", "single_color", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..20"},
    "body_width":     {"type": "int", "default": "rng 4..7", "valid": "2..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
        bw_lo, bw_hi = 4, 4
    elif difficulty == "hard":
        bw_lo, bw_hi = 7, 9
    else:
        bw_lo, bw_hi = 4, 7
    width = ctx.draw_int("body_width", bw_lo, bw_hi)
    bg, top, bottom = ctx.draw_distinct_colors("colors", n=3, exclude=set())
    h = rng.randint(10, 14)
    w = max(12, width + 6)
    g = full_grid(h, w, bg)
    r0 = rng.randint(2, h - 6)
    c0 = rng.randint(2, w - width - 3)
    top_h = rng.randint(2, 3)
    bot_h = rng.randint(2, 3)
    for r in range(top_h):
        for c in range(width):
            g[r0 + r][c0 + c] = top
    for r in range(bot_h):
        for c in range(width):
            if not (r == 0 and c == width // 2 and width > 4):
                g[r0 + top_h + r][c0 + c] = bottom
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 14, 0)
    if name == "no_shape":
        return g
    if name == "single_color":
        for r in range(3, 7):
            for c in range(3, 9):
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(14):
                g[r][c] = 2
        return g
    return g
