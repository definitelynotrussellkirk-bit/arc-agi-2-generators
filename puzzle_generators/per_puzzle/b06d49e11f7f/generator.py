"""Generator for arc_puzzle_bank_21_set10_s:S10_H5.

The top two rows define source-to-target colors. Each color-5 room contains
one source-color seed; the rule fills that room with the mapped target color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rooms,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_seed, seed_not_in_legend.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "b06d49e11f7f"
VERSION = "1.1.0"
TASK_ID = "b06d49e11f7f"
SUMMARY = "A two-row legend maps room seed colors to fill colors."

INVARIANTS = [
    "legend pairs occupy matching columns in rows 0 and 1",
    "body frames are color 5 rectangular outlines",
    "each room contains exactly one non-0/non-5 seed color from the legend",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_seed", "seed_not_in_legend")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "15", "valid": "15..15"},
    "grid_w":         {"type": "int", "default": "19", "valid": "19..19"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rooms":        {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "3..7"},
    "position_bias":  {"type": "str", "default": "legend_with_5_frame_rooms",
                       "valid": "legend_with_5_frame_rooms"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "3..7"},
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
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        n_rooms = ctx.draw_int("n_rooms", 1, 1)
    elif difficulty == "hard":
        n_rooms = ctx.draw_int("n_rooms", 2, 3)
    else:
        n_rooms = ctx.draw_int("n_rooms", 1, 3)
    sources = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_rooms)
    targets = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_rooms)
    g = full_grid(15, 19, 0)
    for i, (src, dst) in enumerate(zip(sources, targets)):
        c = 1 + i * 3
        g[0][c] = src
        g[1][c] = dst
    origins = [(3, 1), (3, 8), (9, 5)]
    for i in range(n_rooms):
        r0, c0 = origins[i]
        draw_frame(g, r0, c0, r0 + 4, c0 + 5, 5)
        g[r0 + 2][c0 + 2] = sources[i]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 19, 0)
    if name == "no_legend":
        # rooms with seeds but no top-row legend → no source→target map
        draw_frame(g, 3, 1, 7, 6, 5)
        g[5][3] = 4
        return g
    if name == "no_seed":
        # legend present + room frame, but room is empty → no seed to fill from
        g[0][1] = 4; g[1][1] = 6
        draw_frame(g, 3, 1, 7, 6, 5)
        return g
    if name == "seed_not_in_legend":
        # seed color not in legend → no mapping for that seed, lookup fails
        g[0][1] = 4; g[1][1] = 6
        draw_frame(g, 3, 1, 7, 6, 5)
        g[5][3] = 7   # 7 is not in legend
        return g
    return g
