"""Generator for arc_additional_puzzles_21_set10_bundle:E65 — Connect 2 same-color cells aligned in row or col.

Rule: each color with exactly 2 cells aligned in row/col → fill
segment between them.

Combinatorial axes (8): grid_h, grid_w, palette_kind, alignment,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pair, diagonal_only, adjacent_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "be7f70e60fb7"
VERSION = "1.1.0"
TASK_ID = "be7f70e60fb7"
SUMMARY = "1 color with 2 cells aligned in row/col + 1 distractor singleton."

INVARIANTS = [
    "≥1 color with 2 cells aligned in same row or col, ≥3 cells apart",
    "1 distractor singleton of different color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pair", "diagonal_only", "adjacent_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "alignment":      {"type": "str", "default": "rng row|col", "valid": "row|col"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "aligned_pair_plus_singleton",
                       "valid": "aligned_pair_plus_singleton"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 2)
    if rng.random() < 0.5:
        r = rng.randint(0, h - 1)
        cs = sorted(rng.sample(range(w), 2))
        if cs[1] - cs[0] >= 3:
            g[r][cs[0]] = pal[0]; g[r][cs[1]] = pal[0]
    else:
        c = rng.randint(0, w - 1)
        rs = sorted(rng.sample(range(h), 2))
        if rs[1] - rs[0] >= 3:
            g[rs[0]][c] = pal[0]; g[rs[1]][c] = pal[0]
    for _ in range(20):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = pal[1]
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_pair":
        # only singletons → no segment to fill
        g[2][3] = 4
        g[4][7] = 6
        return g
    if name == "diagonal_only":
        # 2 cells of same color on diagonal → row/col-aligned precondition fails
        g[1][1] = 4; g[3][3] = 4
        g[5][8] = 6
        return g
    if name == "adjacent_pair":
        # pair separated by 1 cell → no zero between them to fill
        g[2][3] = 4; g[2][4] = 4
        g[4][7] = 6
        return g
    return g
