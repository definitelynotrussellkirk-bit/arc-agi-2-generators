"""Generator for e39e9282.

Rule: dots adjacent to pink shapes move to their center; dots
adjacent to gray shapes mark the inner edge.

Combinatorial axes (8): grid_h/w, include_gray, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_shape, no_dots, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "ee6a99e8b7f9"
VERSION = "1.1.0"
TASK_ID = "ee6a99e8b7f9"
SUMMARY = "Dots near pink shapes move to center; near gray shapes mark inner edge."

INVARIANTS = [
    "shape objects are color 6 or color 5 on a zero background",
    "color-9 dots sit immediately outside a shape bbox edge",
    "gray shapes are cleared to color 8 before adjacent edge is marked",
    "shapes sit clear of grid borders",
]

INCLUDE_GRAY = ("yes", "no")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shape", "no_dots", "full_grid")
HELPFUL_TEXTURES = INCLUDE_GRAY

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "include_gray":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(INCLUDE_GRAY)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for include_gray",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    include_gray = (overrides.get("texture") if overrides.get("texture") in INCLUDE_GRAY else None) or \
                   overrides.get("include_gray") or \
                   ctx.draw_choice("include_gray", list(INCLUDE_GRAY))
    g = full_grid(14, 15, 0)
    pr = 2 + rng.randint(0, 2)
    pc = 2 + rng.randint(0, 1)
    ph = 3 + rng.randint(0, 1)
    pw = 3 + rng.randint(0, 1)
    draw_rect(g, pr, pc, ph, pw, 6)
    if rng.randint(0, 1):
        g[pr + ph // 2][pc - 1] = 9
    else:
        g[pr - 1][pc + pw // 2] = 9
    if include_gray == "yes":
        gr = 3 + rng.randint(0, 1)
        gc = 9 + rng.randint(0, 1)
        gh = 3 + rng.randint(0, 1)
        gw = 3
        draw_rect(g, gr, gc, gh, gw, 5)
        if rng.randint(0, 1):
            g[gr - 1][gc + gw // 2] = 9
        else:
            g[gr + gh // 2][gc + gw] = 9
    else:
        sr = 9 + rng.randint(0, 1)
        sc = 7 + rng.randint(0, 1)
        draw_rect(g, sr, sc, 2, 4, 6)
        g[sr + 2][sc + 2] = 9
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 15, 0)
    if name == "no_shape":
        g[5][5] = 9
        return g
    if name == "no_dots":
        draw_rect(g, 3, 3, 3, 3, 6)
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(15):
                g[r][c] = 6
        return g
    return g
