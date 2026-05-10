"""Generator for arc_puzzle_bank_21_set4_d:easy_d03.

Same-color diagonal dominoes complete their enclosing 2x2 blocks.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_dominoes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dominoes, full_2x2, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "01bb2cbe1309"
VERSION = "1.1.0"
TASK_ID = "01bb2cbe1309"

SUMMARY = "Same-color diagonal dominoes complete their enclosing 2x2 blocks."

INVARIANTS = [
    "background is 0",
    "each target is two same-color cells on opposite corners of a 2x2 box",
    "the other two corners of each target box are empty",
    "target boxes are separated to avoid ambiguous overlaps",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dominoes", "full_2x2", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_dominoes":     {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "isolated_diagonal_dominoes",
                       "valid": "isolated_diagonal_dominoes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        count = ctx.draw_int("domino_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        count = ctx.draw_int("domino_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        count = ctx.draw_int("domino_count", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    anchors = []
    for color in rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], count):
        for _attempt in range(300):
            r0 = rng.randint(0, h - 2)
            c0 = rng.randint(0, w - 2)
            if any(abs(r0 - rr) <= 2 and abs(c0 - cc) <= 2 for rr, cc in anchors):
                continue
            if any(g[r0 + dr][c0 + dc] != 0 for dr in (0, 1) for dc in (0, 1)):
                continue
            if rng.random() < 0.5:
                g[r0][c0] = color
                g[r0 + 1][c0 + 1] = color
            else:
                g[r0][c0 + 1] = color
                g[r0 + 1][c0] = color
            anchors.append((r0, c0))
            break
        else:
            raise ValueError("could not place diagonal domino")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "no_dominoes":
        # blank → no diagonal dominoes to complete
        return g
    if name == "full_2x2":
        # 2x2 already solid → no missing corners
        for dr in range(2):
            for dc in range(2):
                g[2 + dr][2 + dc] = 4
        return g
    if name == "single_cell":
        # single cells → not diagonal pairs, rule won't fire
        g[2][2] = 4; g[5][5] = 6
        return g
    return g
