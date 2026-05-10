"""Generator for arc_puzzle_bank_twentysecond21:E151 — keep first-found color.

Rule: scan the grid in row-major order; the first non-zero color found is
the 'key'. Output keeps only cells of the key color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: blank, single_color, key_appears_once.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "341758fa9de1"
VERSION = "1.1.0"
TASK_ID = "341758fa9de1"

SUMMARY = "Multiple non-zero cells in 2-3 colors; the first (top-left-most) defines the key."

INVARIANTS = [
    "background is 0",
    "2-3 non-zero colors used",
    "the topmost non-zero cell appears multiple times (so the rule's effect is visible)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("blank", "single_color", "key_appears_once")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..6", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 5..6", "valid": "4..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_multicolor",
                       "valid": "scattered_multicolor"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 5, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 6, 6)
    else:
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 5, 6)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        n_colors = rng.randint(2, 3)
        colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n_colors)
        for color in colors:
            for _ in range(rng.randint(2, 3)):
                for _t in range(40):
                    r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
                    if g[r][c] != 0: continue
                    g[r][c] = color
                    break
        first = None
        for r in range(h):
            for c in range(w):
                if g[r][c] != 0:
                    first = g[r][c]; break
            if first: break
        if first and sum(1 for row in g for v in row if v == first) >= 2:
            return g
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 6
    g = full_grid(h, w, 0)
    if name == "blank":
        # blank → no first color, rule has no effect
        return g
    if name == "single_color":
        # only one color → key is trivially that color, output identical (rule is identity)
        g[1][1] = 4; g[2][3] = 4; g[4][2] = 4
        return g
    if name == "key_appears_once":
        # the topmost color appears only once → output has just one cell
        g[0][2] = 4
        g[2][1] = 6; g[3][3] = 6
        g[4][4] = 3; g[5][1] = 3
        return g
    return g
