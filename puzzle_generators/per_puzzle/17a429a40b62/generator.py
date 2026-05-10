"""Generator for arc_puzzle_bank_tenth21:M66 — two-row legend remap.

Rule: top 2 rows hold (src, dst) pairs at the same columns. Below row
1, every cell whose value matches a src is remapped to its dst.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_src_below, src_collision_with_dst.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "17a429a40b62"
VERSION = "1.1.0"
TASK_ID = "17a429a40b62"
SUMMARY = "2-row legend (src/dst) at distinct cols + scattered src cells below."

INVARIANTS = [
    "background is 0",
    "row 0 has 3 distinct src colors at 3 distinct cols",
    "row 1 has dst colors at the same cols",
    "below row 1: scattered src cells (so remap is non-trivial)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_src_below", "src_collision_with_dst")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "6", "valid": "4..6"},
    "position_bias":  {"type": "str", "default": "row01_legend_with_src_below",
                       "valid": "row01_legend_with_src_below"},
    "n_distinct_colors": {"type": "int", "default": "6", "valid": "4..6"},
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
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cols = sorted(rng.sample(range(w), 3))
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 6)
    srcs = pal[:3]
    dsts = pal[3:]
    for c, s, d in zip(cols, srcs, dsts):
        g[0][c] = s
        g[1][c] = d
    for r in range(2, h):
        for c in range(w):
            if rng.random() < 0.3:
                g[r][c] = rng.choice(srcs)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # rows 0/1 empty → no remap dictionary
        for r in range(2, h):
            for c in range(w):
                if (r + c) % 3 == 0: g[r][c] = 4
        return g
    if name == "no_src_below":
        # legend present but no src cells below → remap has nothing to operate on
        cols = [1, 3, 5]
        for c, s, d in zip(cols, [2, 3, 4], [6, 7, 8]):
            g[0][c] = s; g[1][c] = d
        return g
    if name == "src_collision_with_dst":
        # src and dst share a value → remap is partially identity, iteration semantics ambiguous
        cols = [1, 3, 5]
        srcs = [2, 3, 4]
        dsts = [3, 4, 5]   # 3 is both src and dst
        for c, s, d in zip(cols, srcs, dsts):
            g[0][c] = s; g[1][c] = d
        for c in range(w):
            if c % 2 == 0: g[3][c] = 2
        return g
    return g
