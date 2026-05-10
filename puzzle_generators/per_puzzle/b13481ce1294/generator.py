"""Generator for arc_puzzle_bank_twentysecond21:M153.

Rule: two panels separated by a vertical 8-col. Output: cell-wise XOR
(non-zero in left only OR right only → keep that value; both or neither
→ 0).

Combinatorial axes (8): grid_h, grid_w, palette_kind, panel_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_separator, panels_identical, single_panel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b13481ce1294"
VERSION = "1.1.0"
TASK_ID = "b13481ce1294"
SUMMARY = "Two equal-width panels separated by full vertical 8-col."

INVARIANTS = [
    "background is 0",
    "exactly one full vertical 8-col separator",
    "left and right panels have different sparse non-zero patterns",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separator", "panels_identical", "single_panel")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "panel_w":        {"type": "int", "default": "rng 3..5", "valid": "2..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "fill_prob":      {"type": "float", "default": "0.4", "valid": "0.0..1.0"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "two_panel_sep",
                       "valid": "two_panel_sep"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
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
        h = ctx.draw_int("grid_h", 4, 4)
        pw = ctx.draw_int("panel_w", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        pw = ctx.draw_int("panel_w", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        pw = ctx.draw_int("panel_w", 3, 5)
    w = pw * 2 + 1
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    sep = pw
    for r in range(h):
        g[r][sep] = 8
    for r in range(h):
        for c in range(pw):
            if rng.random() < 0.4:
                g[r][c] = rng.choice([2, 3, 4, 5, 6])
        for c in range(sep + 1, w):
            if rng.random() < 0.4:
                g[r][c] = rng.choice([2, 3, 4, 5, 6])
    return g


def _draw_from_degenerate(name, rng):
    h, pw = 5, 4
    w = pw * 2 + 1
    g = full_grid(h, w, 0)
    if name == "no_separator":
        # no 8-col → panel boundary undefined
        for r in range(h):
            for c in range(w):
                if (r + c) % 3 == 0: g[r][c] = 4
        return g
    if name == "panels_identical":
        # left and right panels identical → XOR is all 0, output empty
        for r in range(h): g[r][pw] = 8
        for r in range(h):
            for c in range(pw):
                if (r + c) % 2: g[r][c] = 4
        for r in range(h):
            for c in range(pw):
                if (r + c) % 2: g[r][pw + 1 + c] = 4
        return g
    if name == "single_panel":
        # only left panel populated; right panel empty → XOR = left (rule trivial)
        for r in range(h): g[r][pw] = 8
        for r in range(h):
            for c in range(pw):
                if (r + c) % 2: g[r][c] = 4
        return g
    return g
