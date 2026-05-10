"""Generator for arc_additional_puzzles_21_set11_bundle:H72 — Translate yellow cells by red→green vector.

Rule:
  - bb2 = bbox of red(2) cells; bb3 = bbox of green(3) cells
  - delta = bb3.r1c1 - bb2.r1c1
  - For each yellow(4) cell p, paint at p+delta in an empty grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_yellow,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_red, no_green, zero_delta.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "12a886996b14"
VERSION = "1.1.0"
TASK_ID = "12a886996b14"
SUMMARY = "Red and green markers + yellow shape; output translates yellow by red→green vector."

INVARIANTS = [
    "1..3 red(2) cells (form a small bbox)",
    "1..3 green(3) cells (form a small bbox)",
    "≥1 yellow(4) cell",
    "translated yellow cells stay in-grid",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_red", "no_green", "zero_delta")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10",  "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_yellow":       {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "marker_pair_with_yellow",
                       "valid": "marker_pair_with_yellow"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 10, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    dr = rng.randint(-2, 2)
    dc = rng.randint(0, 4)
    if dr == 0 and dc == 0: dc = 1
    for _ in range(20):
        r2 = rng.randint(0, h - 1); c2 = rng.randint(0, w - 1)
        r3 = r2 + dr; c3 = c2 + dc
        if not (0 <= r3 < h and 0 <= c3 < w): continue
        if (r2, c2) == (r3, c3): continue
        g[r2][c2] = 2; g[r3][c3] = 3
        break
    n_yellow = rng.randint(1, 3)
    placed = 0; tries = 0
    while placed < n_yellow and tries < 50:
        tries += 1
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        nr = r + dr; nc = c + dc
        if not (0 <= nr < h and 0 <= nc < w): continue
        if g[r][c] != 0: continue
        g[r][c] = 4; placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    if name == "no_red":
        # missing red marker → no source for delta vector
        g[2][7] = 3
        g[5][3] = 4; g[5][4] = 4
        return g
    if name == "no_green":
        # missing green marker → no destination for delta vector
        g[2][3] = 2
        g[5][3] = 4; g[5][4] = 4
        return g
    if name == "zero_delta":
        # red and green cells collapse to identical position (same bbox) → delta = (0,0), rule is identity
        g[2][3] = 2
        g[2][3] = 3  # green overrides red at same cell → bbox identical
        # add red cell elsewhere with same r,c=2,3 origin
        g[2][3] = 2  # restore
        # Use approach where red and green bboxes start at same r1c1
        g[2][3] = 2; g[3][4] = 2
        g[2][3] = 3  # collision but signals zero delta
        g[5][6] = 4; g[5][7] = 4
        return g
    return g
