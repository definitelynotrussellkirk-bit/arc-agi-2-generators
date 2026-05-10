"""Generator for arc_puzzle_bank_21_set12_bundle:easy_l04.

Rule: for each filled (solid) rectangle with both dims odd, paint
output cross: middle row of bbox + middle col of bbox in the obj's
color (on a fresh empty grid).

Combinatorial axes (8): grid_h, grid_w, palette_kind, rect_dims,
palette_size, position_bias, n_distinct_colors, n_rects, texture.
Degenerates: even_dim_rect, no_rects, hollow_rect.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "e4cb0224ca42"
VERSION = "1.1.0"
TASK_ID = "e4cb0224ca42"
SUMMARY = "1-2 solid rects with both dims odd (≥3) in distinct colors."

INVARIANTS = [
    "1-2 solid rectangles, each with odd width AND odd height ≥3",
    "rectangles don't touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("even_dim_rect", "no_rects", "hollow_rect")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rect_dims":      {"type": "str", "default": "odd_3_or_5", "valid": "odd_3_or_5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "interior", "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "n_rects":        {"type": "int", "default": "1", "valid": "1..2"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 2)
    rh = rng.choice([3, 5]); rw = rng.choice([3, 5])
    r0 = rng.randint(0, h - rh); c0 = rng.randint(0, w - rw)
    draw_rect(g, r0, c0, rh, rw, pal[0])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "even_dim_rect":
        # solid rect with an even dimension → "middle" cell is undefined
        draw_rect(g, 1, 1, 4, 4, 4)
        return g
    if name == "no_rects":
        # empty grid — no rectangles to project crosses from
        return g
    if name == "hollow_rect":
        # outline only — predicate "solid rect" fails
        for c in range(1, 6):
            g[1][c] = 4; g[3][c] = 4
        for r in range(1, 4):
            g[r][1] = 4; g[r][5] = 4
        return g
    return g
