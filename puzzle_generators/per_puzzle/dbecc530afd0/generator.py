"""Generator for af902bf9.

Rule: 4 yellow(4) cells form rect corners; rule fills interior red(2).

Combinatorial axes (8): grid_h/w, rect_h, rect_w, position_bias,
n_extra_yellows, palette_kind, anchor_corner, asymmetry_force.
Degenerates: no_rect, three_yellows, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dbecc530afd0"
VERSION = "1.1.0"
TASK_ID = "dbecc530afd0"
SUMMARY = "Yellow corners of a rectangle; rule fills interior red."

INVARIANTS = [
    "background is 0",
    ">=4 yellow(4) cells, 4 of them forming an axis-aligned rectangle",
    "the rectangle's interior is at least 1 cell (rect >= 3x3)",
    "no other rectangles formed by the yellow set",
]

POSITION_BIASES = ("centered", "corner", "near_edge", "scattered")
DEGENERATE_TEXTURES = ("no_rect", "three_yellows", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "rect_h":         {"type": "int", "default": "rng 4..h-4", "valid": "4..h-2"},
    "rect_w":         {"type": "int", "default": "rng 4..w-4", "valid": "4..w-2"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "n_extra_yellows":{"type": "int", "default": "0", "valid": "0..3"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
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
        h_lo, h_hi = 8, 10
        ne_lo, ne_hi = 0, 0
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
        ne_lo, ne_hi = 0, 2
    else:
        h_lo, h_hi = 10, 14
        ne_lo, ne_hi = 0, 1
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    r1, r2, c1, c2 = _pick_rect(bias, h, w, rng)
    g[r1][c1] = 4; g[r1][c2] = 4
    g[r2][c1] = 4; g[r2][c2] = 4
    return g


def _pick_rect(bias, h, w, rng):
    if bias == "centered":
        rh = max(4, h // 2)
        rw = max(4, w // 2)
        r1 = max(1, (h - rh) // 2)
        c1 = max(1, (w - rw) // 2)
        r2 = r1 + rh - 1
        c2 = c1 + rw - 1
    elif bias == "corner":
        r1 = 1; c1 = 1
        r2 = h - 2; c2 = w - 2
    elif bias == "near_edge":
        r1 = 1; r2 = h - 2
        c1 = rng.randint(1, max(1, w // 2 - 2))
        c2 = rng.randint(min(w - 2, w // 2 + 2), w - 2)
    else:
        r1 = rng.randint(1, max(1, h - 5))
        r2 = rng.randint(r1 + 3, h - 2)
        c1 = rng.randint(1, max(1, w - 5))
        c2 = rng.randint(c1 + 3, w - 2)
    return r1, r2, c1, c2


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_rect":
        g[2][2] = 4; g[5][7] = 4
        return g
    if name == "three_yellows":
        g[2][2] = 4; g[2][8] = 4; g[8][2] = 4
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 4
        return g
    return g
