"""Generator for 7c008303.

Rule: cross splits grid; 2x2 key in one corner, 3-pattern opposite;
rule maps 3s through key.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
density.
Degenerates: no_cross, no_pattern, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1180c5a8d3c2"
VERSION = "1.1.0"
TASK_ID = "1180c5a8d3c2"
SUMMARY = "Cross splits grid; 2x2 key + opposite 3-pattern; rule maps 3s through key."

INVARIANTS = [
    "row cross_r and col cross_c are uniformly 8",
    "2x2 key uses 4 distinct non-{0,3,8} colors",
    "main quadrant uses only 0 and 3; the two non-key quadrants are all 0",
    "main quadrant has at least 2x2 size",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_cross", "no_pattern", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "density":        {"type": "float", "default": "0.4", "valid": "0.3..0.5"},
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
        h_lo, h_hi = 12, 13
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
    else:
        h_lo, h_hi = 12, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    palette = ctx.draw_distinct_colors("palette", n=4, exclude={0, 3, 8})
    cross_r = rng.randint(3, h - 5)
    cross_c = rng.randint(3, w - 5)
    corner = rng.choice(["tl", "tr", "bl", "br"])
    g = full_grid(h, w, 0)
    for c in range(w):
        g[cross_r][c] = 8
    for r in range(h):
        g[r][cross_c] = 8
    if corner == "tl":
        kr1, kc1 = 0, 0
        gr1, gc1, gr2, gc2 = cross_r + 1, cross_c + 1, h, w
    elif corner == "tr":
        kr1, kc1 = 0, cross_c + 1
        gr1, gc1, gr2, gc2 = cross_r + 1, 0, h, cross_c
    elif corner == "bl":
        kr1, kc1 = cross_r + 1, 0
        gr1, gc1, gr2, gc2 = 0, cross_c + 1, cross_r, w
    else:
        kr1, kc1 = cross_r + 1, cross_c + 1
        gr1, gc1, gr2, gc2 = 0, 0, cross_r, cross_c
    g[kr1][kc1] = palette[0]
    g[kr1][kc1 + 1] = palette[1]
    g[kr1 + 1][kc1] = palette[2]
    g[kr1 + 1][kc1 + 1] = palette[3]
    placed = False
    for r in range(gr1, gr2):
        for c in range(gc1, gc2):
            if rng.random() < 0.4:
                g[r][c] = 3
                placed = True
    if not placed:
        g[gr1][gc1] = 3
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_cross":
        g[5][5] = 3
        return g
    if name == "no_pattern":
        for c in range(13):
            g[5][c] = 8
        for r in range(13):
            g[r][5] = 8
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 8
        return g
    return g
