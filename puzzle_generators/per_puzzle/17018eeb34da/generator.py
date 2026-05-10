"""Generator for arc_additional_puzzles_21_set2:H9 — two-row color substitution key.

Rule: top two rows give old-to-new color pairs; the body is recolored
and the key is dropped.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_body_use, body_uses_unknown_colors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "17018eeb34da"
VERSION = "1.1.0"
TASK_ID = "17018eeb34da"
SUMMARY = "Top two rows give old-to-new color pairs; the body is recolored and the key is dropped."

INVARIANTS = [
    "legend columns have nonzero top and bottom entries",
    "body cells include at least one old color that changes",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_body_use", "body_uses_unknown_colors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "two_row_legend_with_body",
                       "valid": "two_row_legend_with_body"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        n = min(ctx.draw_int("n_pairs", 3, 3), w)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n = min(ctx.draw_int("n_pairs", 4, 5), w)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        n = min(ctx.draw_int("n_pairs", 3, 5), w)
    rng = ctx.draw_rng("layout")
    colors = list(ctx.draw_distinct_colors("colors", n=n + 2, exclude=[0]))
    old = colors[:n]
    new = colors[1:n + 1]
    g = full_grid(h, w, 0)
    for c, (src, dst) in enumerate(zip(old, new)):
        g[0][c] = src
        g[1][c] = dst
    for r in range(2, h):
        for c in range(w):
            roll = rng.random()
            if roll < 0.55:
                g[r][c] = rng.choice(old)
            elif roll < 0.75:
                g[r][c] = rng.choice(new)
    g[2][0] = old[0]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # body cells but top two rows blank → no recolor mapping
        g[3][3] = 4
        g[5][6] = 6
        return g
    if name == "no_body_use":
        # legend present but body has no old-color cells → rule has nothing
        g[0][0] = 4; g[0][1] = 6; g[0][2] = 7
        g[1][0] = 6; g[1][1] = 7; g[1][2] = 8
        for r in range(2, h):
            for c in range(w): g[r][c] = 9   # body uses 9 only, none in old
        return g
    if name == "body_uses_unknown_colors":
        # body uses colors NOT in the legend → no mapping for those cells
        g[0][0] = 4; g[0][1] = 6
        g[1][0] = 6; g[1][1] = 7
        g[3][3] = 9; g[5][5] = 8   # 9 and 8 not in {4,6}
        return g
    return g
