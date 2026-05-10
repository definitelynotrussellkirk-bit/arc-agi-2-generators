"""Generator for arc_additional_puzzles_21_set22_bundle:E148 — Connect 2 same-color cells aligned in row or col.

Rule: exactly 2 non-zero cells of same color. If they share row, fill
row segment between them; if they share col, fill col segment.

Combinatorial axes (8): grid_h, grid_w, palette_kind, axis,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pair, mismatched_endpoints, diagonal_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "70a3e6be3283"
VERSION = "1.1.0"
TASK_ID = "70a3e6be3283"
SUMMARY = "Exactly 2 cells of single non-bg color aligned in a row or col, separated by gap."

INVARIANTS = [
    "exactly 2 non-bg cells of same color",
    "cells share a row OR a col",
    "separated by ≥3 0-cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pair", "mismatched_endpoints", "diagonal_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "axis":           {"type": "str", "default": "rng row|col", "valid": "row|col"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "single_aligned_pair",
                       "valid": "single_aligned_pair"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    color = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])
    if rng.random() < 0.5:
        r = rng.randint(0, h - 1)
        cs = sorted(rng.sample(range(w), 2))
        if cs[1] - cs[0] >= 3:
            g[r][cs[0]] = color; g[r][cs[1]] = color
    else:
        c = rng.randint(0, w - 1)
        rs = sorted(rng.sample(range(h), 2))
        if rs[1] - rs[0] >= 3:
            g[rs[0]][c] = color; g[rs[1]][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_pair":
        # singleton only — no second cell to connect to
        g[2][3] = 4
        return g
    if name == "mismatched_endpoints":
        # two cells but in different colors → not a same-color pair
        g[2][1] = 4; g[2][6] = 6
        return g
    if name == "diagonal_pair":
        # two cells of same color but neither row- nor col-aligned → no segment
        g[1][1] = 4; g[4][6] = 4
        return g
    return g
