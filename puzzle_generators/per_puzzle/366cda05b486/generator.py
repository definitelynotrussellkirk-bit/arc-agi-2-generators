"""Generator for arc_puzzle_bank_21_set12_s:S12_M2 — blue seed marks contact cluster.

Rule: a blue seed marks the touching component cluster to crop and
recolor.

Combinatorial axes (8): grid_h, grid_w, palette_kind, cluster_shape,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seed, no_cluster, all_isolated.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "366cda05b486"
VERSION = "1.1.0"
TASK_ID = "366cda05b486"

SUMMARY = "A blue seed marks the touching component cluster to crop and recolor."

INVARIANTS = [
    "background is 0",
    "there is exactly one blue component",
    "the blue component belongs to a multi-component contact cluster",
    "at least one non-blue distractor cluster is disconnected from the seed cluster",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seed", "no_cluster", "all_isolated")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cluster_shape":  {"type": "str", "default": "rng path|branch", "valid": "path|branch"},
    "palette_size":   {"type": "int", "default": "6", "valid": "6..6"},
    "position_bias":  {"type": "str", "default": "blue_seed_with_distractors",
                       "valid": "blue_seed_with_distractors"},
    "n_distinct_colors": {"type": "int", "default": "6", "valid": "6..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 12, 15)
    shape = ctx.draw_choice("cluster_shape", ["path", "branch"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    r = rng.randint(2, h - 5)
    c = rng.randint(2, w - 6)
    if shape == "path":
        cells = [(r, c, 1), (r, c + 1, 3), (r + 1, c + 1, 4), (r + 1, c + 2, 6)]
    else:
        cells = [(r, c, 1), (r, c + 1, 3), (r - 1, c + 1, 4), (r + 1, c + 1, 6)]
    for rr, cc, color in cells:
        g[rr][cc] = color

    g[h - 2][w - 4] = 7
    g[h - 2][w - 3] = 7
    g[1][w - 2] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_seed":
        # no blue cell → no seed to anchor a cluster
        g[3][3] = 3; g[3][4] = 3
        g[6][6] = 4; g[7][6] = 4
        g[1][w - 2] = 8
        return g
    if name == "no_cluster":
        # blue seed exists but is isolated → cluster has just the seed
        g[3][3] = 1
        g[6][6] = 4; g[7][6] = 6
        g[1][w - 2] = 8
        return g
    if name == "all_isolated":
        # every component is its own island → no contact cluster
        g[3][3] = 1
        g[3][8] = 3
        g[6][3] = 4
        g[6][8] = 6
        g[1][w - 2] = 8
        return g
    return g
