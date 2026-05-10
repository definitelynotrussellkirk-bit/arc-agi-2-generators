"""Generator for additional_scaffolded:E4.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_bars,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_bars, length_one_bars, all_bars_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1bc09b475319"
VERSION = "1.1.0"
TASK_ID = "1bc09b475319"
SUMMARY = "Horizontal color-6 bars receive color-8 caps on open ends."

INVARIANTS = [
    "background is 0",
    "all active objects are horizontal runs of color 6 with length at least 2",
    "bars are separated so cap cells are empty",
    "some bars may touch a grid edge and receive only one cap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_bars", "length_one_bars", "all_bars_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "3..18"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "4..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_bars":         {"type": "int", "default": "rng 3..6", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "horizontal_6_bars",
                       "valid": "horizontal_6_bars"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 10)
        n_bars = ctx.draw_int("n_bars", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 12, 14)
        n_bars = ctx.draw_int("n_bars", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 8, 14)
        n_bars = ctx.draw_int("n_bars", 3, 6)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    rows_used: set[int] = set()
    for _ in range(160):
        if len(rows_used) >= min(n_bars, h):
            break
        r = rng.randint(0, h - 1)
        if r in rows_used:
            continue
        length = rng.randint(2, min(5, w - 1))
        c = rng.randint(0, w - length)
        if c > 0 and rng.random() < 0.2:
            c = 0
        elif c + length < w and rng.random() < 0.2:
            c = w - length
        for dc in range(length):
            g[r][c + dc] = 6
        rows_used.add(r)
    if not rows_used:
        g[1][2] = 6
        g[1][3] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_bars":
        # blank → no bars to cap
        return g
    if name == "length_one_bars":
        # length-1 "bars" → not actual bars, "length ≥ 2" precondition fails
        g[1][3] = 6
        g[3][7] = 6
        g[5][2] = 6
        return g
    if name == "all_bars_at_edge":
        # every bar abuts both edges (full-width row) → no open ends to cap
        for c in range(w):
            g[1][c] = 6
        for c in range(w):
            g[5][c] = 6
        return g
    return g
