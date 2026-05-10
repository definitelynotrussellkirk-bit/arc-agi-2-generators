"""Generator for puzzle `arc_puzzle_bank_21_next:easy_c03` — within
each row, slide non-zero cells to the right, preserving their L-to-R
order (gravity-right).

Combinatorial axes (8): grid_h, grid_w, palette_kind, fg_palette,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: already_right_packed, no_active_rows, fully_packed_rows.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1ec277b81469"
VERSION = "1.1.0"
TASK_ID = "1ec277b81469"
SUMMARY = "Sparse non-bg cells in rows; rule slides each row's non-bg cells to the right."

INVARIANTS = [
    "background is 0",
    ">=2 rows contain multiple non-bg cells separated by bg",
    "non-bg cells use 2-4 distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("already_right_packed", "no_active_rows", "fully_packed_rows")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "fg_palette":     {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "left_biased",
                       "valid": "left_biased"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 8, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 8, 14)
    palette_n = ctx.draw_int("fg_palette", 2, 4)
    palette = ctx.draw_distinct_colors("palette", n=palette_n, exclude={0})
    rng_ratio = ctx.draw_rng("fill_ratio")
    ratio = rng_ratio.uniform(0.25, 0.5)

    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("cells")

    for r in range(h):
        n_paint = max(0, int(w * ratio))
        if n_paint == 0: continue
        positions = list(range(w * 2 // 3))
        rng.shuffle(positions)
        for i, c in enumerate(positions[:n_paint]):
            g[r][c] = palette[i % len(palette)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "already_right_packed":
        # rows already right-aligned → rule is identity, no movement visible
        for r, vs in [(1, [3, 4, 5]), (3, [6, 7]), (5, [8, 9, 2, 3])]:
            for i, v in enumerate(vs):
                g[r][w - len(vs) + i] = v
        return g
    if name == "no_active_rows":
        # empty grid → no rows to slide
        return g
    if name == "fully_packed_rows":
        # rows entirely nonzero → no gaps to close, identity output
        for r in range(h):
            for c in range(w):
                g[r][c] = 1 + ((r + c) % 7)
        return g
    return g
