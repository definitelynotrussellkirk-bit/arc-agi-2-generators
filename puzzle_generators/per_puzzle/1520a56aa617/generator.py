"""Generator for 19b:hard_130 — fill chambers by legend priority.

Rule: top row holds a priority legend of colors (excluding 0 and 8).
Body has 8-walls forming chambers; each chamber may contain seed cells
in legend colors. For each chamber, find seeds present and fill with
the highest-priority (earliest in legend) seed color.

Combinatorial axes (8): ch_h, ch_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_seeds, no_walls.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1520a56aa617"
VERSION = "1.1.0"
TASK_ID = "1520a56aa617"

SUMMARY = "Top legend (3-color priority) + 8-walled body with seeds inside chambers."

INVARIANTS = [
    "background is 0",
    "row 0 holds a 3-color priority legend at distinct columns (no 0 or 8)",
    "8-walls form chambers in rows 2+ (outer 8-frame + 1-2 internal vertical walls)",
    "each chamber holds 1-2 seed cells using legend colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_seeds", "no_walls")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "ch_h":           {"type": "int", "default": "rng 4..5", "valid": "3..7"},
    "ch_w":           {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "legend_top_chambers_below",
                       "valid": "legend_top_chambers_below"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
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
        ch = ctx.draw_int("ch_h", 4, 4)
        cw = ctx.draw_int("ch_w", 4, 4)
    elif difficulty == "hard":
        ch = ctx.draw_int("ch_h", 5, 6)
        cw = ctx.draw_int("ch_w", 5, 6)
    else:
        ch = ctx.draw_int("ch_h", 4, 5)
        cw = ctx.draw_int("ch_w", 4, 5)
    rng = ctx.draw_rng("layout")
    h = ch + 4
    w = 2 * cw + 3
    g = full_grid(h, w, 0)
    legend = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], 3)
    for j, v in enumerate(legend): g[0][j + 1] = v
    walls_c = [0, cw + 1, w - 1]
    for c in range(w):
        g[2][c] = 8; g[h - 1][c] = 8
    for r in range(2, h):
        for wc in walls_c: g[r][wc] = 8
    chamber_cols = [(walls_c[i] + 1, walls_c[i + 1] - 1) for i in range(2)]
    for c_lo, c_hi in chamber_cols:
        n_seeds = rng.randint(1, 2)
        cells = [(r, c) for r in range(3, h - 1) for c in range(c_lo, c_hi + 1)]
        slots = rng.sample(cells, n_seeds)
        seed_colors = rng.sample(legend, n_seeds)
        for (r, c), color in zip(slots, seed_colors):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    ch, cw = 4, 4
    h = ch + 4
    w = 2 * cw + 3
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # Walls + seeds present but row 0 has no legend — rule has
        # no priority order to consult.
        for c in range(w):
            g[2][c] = 8; g[h - 1][c] = 8
        for r in range(2, h):
            for wc in [0, cw + 1, w - 1]: g[r][wc] = 8
        g[3][2] = 3; g[5][cw + 3] = 7
        return g
    if name == "no_seeds":
        # Legend + walls present but chambers are empty — rule has no
        # seeds to rank.
        for j, v in enumerate([3, 7, 2]): g[0][j + 1] = v
        for c in range(w):
            g[2][c] = 8; g[h - 1][c] = 8
        for r in range(2, h):
            for wc in [0, cw + 1, w - 1]: g[r][wc] = 8
        return g
    if name == "no_walls":
        # Legend + seeds but body has no 8-walls — chamber regions are
        # undefined, rule has nothing to fill.
        for j, v in enumerate([3, 7, 2]): g[0][j + 1] = v
        g[3][2] = 3; g[5][cw + 3] = 7
        return g
    return g
