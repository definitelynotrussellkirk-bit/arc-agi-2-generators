"""Generator for arc_puzzle_bank_21_set12_s:S12_H3.

Rule: top-row legend (3 blue + 2 red) selects the component matching
its graph-cluster size and degree.

Combinatorial axes (8): shape, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_target, missing_neighbors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c2c820ee2654"
VERSION = "1.1.0"
TASK_ID = "c2c820ee2654"
SUMMARY = "Use a two-count legend to select the component with matching graph-cluster size and degree."

INVARIANTS = [
    "the top row has three blue cells and two red cells",
    "the target component belongs to a three-component contact cluster",
    "the target component has degree two within that cluster",
    "no other component matches both the cluster-size and degree constraints",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_target", "missing_neighbors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "shape":          {"type": "int", "default": "rng 0..5", "valid": "0..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "legend_top_components_below",
                       "valid": "legend_top_components_below"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_TARGETS = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
]


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        idx = ctx.draw_int("shape", 0, 2)
    elif difficulty == "hard":
        idx = ctx.draw_int("shape", 3, 5)
    else:
        idx = ctx.draw_int("shape", 0, len(_TARGETS) - 1)
    target = _TARGETS[idx]
    colors = rng.sample([3, 4, 5, 6, 7, 8, 9], 5)
    g = full_grid(9, 12, 0)
    for c in range(3):
        g[0][c] = 1
    for c in range(3, 5):
        g[0][c] = 2

    top, left = 4, 5
    _paint(g, top, left, target, colors[1])
    min_col = min(c for _, c in target)
    max_col = max(c for _, c in target)
    left_cell = next((r, c) for r, c in target if c == min_col)
    right_cell = next((r, c) for r, c in target if c == max_col)
    g[top + left_cell[0]][left + left_cell[1] - 1] = colors[0]
    g[top + right_cell[0]][left + right_cell[1] + 1] = colors[2]

    g[2][1] = colors[3]
    g[2][2] = colors[4]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 12, 0)
    if name == "no_legend":
        # Components present but top row is empty — rule has no legend
        # spec to match cluster-size/degree.
        target = _TARGETS[0]
        for r, c in target:
            g[4 + r][5 + c] = 3
        g[4][4] = 4; g[4][7] = 5
        g[2][1] = 6; g[2][2] = 7
        return g
    if name == "no_target":
        # Legend present but no body components — nothing to select.
        for c in range(3): g[0][c] = 1
        for c in range(3, 5): g[0][c] = 2
        return g
    if name == "missing_neighbors":
        # Legend + a center component but the contact cluster lacks the
        # left/right neighbors — degree 0, doesn't match degree-2 spec.
        for c in range(3): g[0][c] = 1
        for c in range(3, 5): g[0][c] = 2
        target = _TARGETS[0]
        for r, c in target:
            g[4 + r][5 + c] = 3
        return g
    return g
