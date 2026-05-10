"""Generator for v3_rich_schema:medium_01_connect_matching_endpoints — connect same-color row/col pairs.

Rule: each non-bg color has 2 markers in a shared row or column;
fill the segment (inclusive) between them with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_colors, texture.
Degenerates: no_pairs, no_shared_axis, adjacent_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "f44596002946"
VERSION = "1.1.0"
TASK_ID = "f44596002946"
SUMMARY = "2-3 distinct colors, each with 2 markers in a shared row or column."

INVARIANTS = [
    "background is 0",
    "2-3 distinct colors, each with exactly 2 markers",
    "every pair shares a row or column with ≥1 0-cell strictly between",
    "pairs use distinct rows and distinct cols",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "no_shared_axis", "adjacent_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "= n_colors", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "shared_axis_pairs",
                       "valid": "shared_axis_pairs"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        n_colors = ctx.draw_int("n_colors", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 11, 13)
        n_colors = ctx.draw_int("n_colors", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
        n_colors = ctx.draw_int("n_colors", 2, 3)
    rng = ctx.draw_rng("layout")
    colors = list(random_palette(rng, n_colors))
    g = full_grid(h, w, 0)
    busy_rows: set[int] = set()
    busy_cols: set[int] = set()
    for color in colors:
        for _ in range(60):
            if rng.random() < 0.5:
                r = rng.randint(0, h - 1)
                if r in busy_rows: continue
                cs = sorted(rng.sample(range(w), 2))
                if cs[1] - cs[0] < 2: continue
                if cs[0] in busy_cols or cs[1] in busy_cols: continue
                g[r][cs[0]] = color; g[r][cs[1]] = color
                busy_rows.add(r)
                break
            else:
                c = rng.randint(0, w - 1)
                if c in busy_cols: continue
                rs = sorted(rng.sample(range(h), 2))
                if rs[1] - rs[0] < 2: continue
                if rs[0] in busy_rows or rs[1] in busy_rows: continue
                g[rs[0]][c] = color; g[rs[1]][c] = color
                busy_cols.add(c)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule has no pairs to connect.
        return g
    if name == "no_shared_axis":
        # Pair has same color but different rows AND cols — rule's
        # "in-row OR in-col" precondition fails.
        g[1][2] = 4; g[5][6] = 4
        return g
    if name == "adjacent_pair":
        # Pair shares a row but is adjacent — rule's "fill between"
        # produces zero cells.
        g[3][2] = 4; g[3][3] = 4
        return g
    return g
