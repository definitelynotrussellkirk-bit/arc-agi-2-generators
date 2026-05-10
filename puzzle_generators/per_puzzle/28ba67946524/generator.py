"""Generator for arc_puzzle_bank_21_set12_s:S12_M7.

Rule: components exactly two contact-graph steps from the blue seed
are marked in cyan.

Combinatorial axes (8): grid_h, grid_w, palette_kind, branch,
palette_size, position_bias, n_distinct_colors, chain_kind, texture.
Degenerates: no_seed, no_distance_2_node, isolated_seed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "28ba67946524"
VERSION = "1.1.0"
TASK_ID = "28ba67946524"
SUMMARY = "Components exactly two contact-graph steps from the blue seed are marked in cyan."

INVARIANTS = [
    "background is 0",
    "there is exactly one blue seed component",
    "the seed cluster contains at least one component at graph distance two",
    "distractor components outside the seed cluster are ignored",
]

PALETTE_KINDS = ("default", "linear_chain", "branched_chain", "varied")
DEGENERATE_TEXTURES = ("no_seed", "no_distance_2_node", "isolated_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..15"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "branch":         {"type": "bool", "default": "rng", "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "chain", "valid": "chain"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
    "chain_kind":     {"type": "str", "default": "1_3_4_6", "valid": "1_3_4_6"},
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
        h = ctx.draw_int("height", 9, 10)
        w = ctx.draw_int("width", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 11, 12)
        w = ctx.draw_int("width", 14, 15)
    else:
        h = ctx.draw_int("height", 9, 12)
        w = ctx.draw_int("width", 11, 15)
    branch = ctx.draw_choice("branch", [False, True])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    r = rng.randint(3, h - 4)
    c = rng.randint(2, w - 6)
    g[r][c] = 1
    g[r][c + 1] = 3
    g[r][c + 2] = 4
    g[r][c + 3] = 6
    if branch:
        g[r + 1][c + 1] = 5

    g[h - 2][w - 3] = 7
    g[h - 2][w - 2] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_seed":
        # chain present but no blue seed → graph-distance source undefined
        g[3][2] = 3; g[3][3] = 4; g[3][4] = 6
        g[h - 2][w - 3] = 7
        return g
    if name == "no_distance_2_node":
        # seed plus only direct neighbor → no node at exactly distance 2
        g[3][2] = 1; g[3][3] = 3
        g[h - 2][w - 3] = 7
        return g
    if name == "isolated_seed":
        # blue seed with no contacts at all → graph cluster is just the seed
        g[3][3] = 1
        g[h - 2][w - 3] = 7
        g[h - 2][w - 2] = 7
        return g
    return g
