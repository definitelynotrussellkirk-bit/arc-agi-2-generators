"""Generator for additional_bank:M5 — fill 0-gaps between same-color markers in shared row/col.

Rule: for each non-bg color (in input-cell order), find pairs of
markers sharing a row or column; fill 0-cells strictly between them
with that color. First-color-wins on overlap.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_colors, texture.
Degenerates: no_pairs, adjacent_pair, no_shared_axis.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "9349fabc466a"
VERSION = "1.1.0"
TASK_ID = "9349fabc466a"
SUMMARY = "Pairs of same-color markers sharing a row or column with a 0-gap between."

INVARIANTS = [
    "background is 0",
    "1-3 distinct non-bg colors, each with exactly 2 markers",
    "every pair shares a row or column with at least 1 0-cell strictly between them",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "adjacent_pair", "no_shared_axis")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..9", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 5..9", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "= n_colors", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "scattered_axis_pairs",
                       "valid": "scattered_axis_pairs"},
    "n_distinct_colors": {"type": "int", "default": "= n_colors", "valid": "1..4"},
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
        w = ctx.draw_int("grid_w", 5, 6)
        n_colors = ctx.draw_int("n_colors", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
        n_colors = ctx.draw_int("n_colors", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 5, 9)
        w = ctx.draw_int("grid_w", 5, 9)
        n_colors = ctx.draw_int("n_colors", 1, 3)
    rng = ctx.draw_rng("layout")
    colors = list(random_palette(rng, n_colors))
    g = full_grid(h, w, 0)
    for color in colors:
        for _ in range(40):
            if rng.random() < 0.5:
                r = rng.randint(0, h - 1)
                cs = sorted(rng.sample(range(w), 2))
                if cs[1] - cs[0] < 2: continue
                if g[r][cs[0]] != 0 or g[r][cs[1]] != 0: continue
                g[r][cs[0]] = color; g[r][cs[1]] = color
                break
            else:
                c = rng.randint(0, w - 1)
                rs = sorted(rng.sample(range(h), 2))
                if rs[1] - rs[0] < 2: continue
                if g[rs[0]][c] != 0 or g[rs[1]][c] != 0: continue
                g[rs[0]][c] = color; g[rs[1]][c] = color
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Single markers (no second of any color) — rule's pair-finder
        # has no input.
        g[2][2] = 3; g[5][6] = 7
        return g
    if name == "adjacent_pair":
        # Pair shares an axis but is adjacent (no 0-gap) — rule's
        # "fill 0-cells between" produces no fill cells.
        g[2][2] = 3; g[2][3] = 3
        return g
    if name == "no_shared_axis":
        # Pair has same color but different rows AND different columns
        # — rule's row-or-col pairing condition fails.
        g[1][2] = 3; g[5][6] = 3
        return g
    return g
