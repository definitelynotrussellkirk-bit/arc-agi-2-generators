"""Generator for arc_additional_puzzle_bank_volume10:E65.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, full_2x2_filled, single_diagonal.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f12f18b44388"
VERSION = "1.1.0"
TASK_ID = "f12f18b44388"
SUMMARY = "Diagonal blue pairs inside 2x2 windows become solid cyan 2x2 blocks."

INVARIANTS = [
    "background is 0",
    "each active 2x2 window has blue cells on exactly one diagonal",
    "active windows are separated so no two diagonal-pair windows overlap",
    "both diagonal orientations can appear",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "full_2x2_filled", "single_diagonal")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 7..12", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "separated_diagonal_blue_pairs",
                       "valid": "separated_diagonal_blue_pairs"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        n_pairs = ctx.draw_int("n_pairs", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 10, 12)
        n_pairs = ctx.draw_int("n_pairs", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 7, 12)
        n_pairs = ctx.draw_int("n_pairs", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    anchors: list[tuple[int, int]] = []
    for _ in range(200):
        if len(anchors) >= n_pairs:
            break
        r = rng.randint(0, h - 2)
        c = rng.randint(0, w - 2)
        if any(abs(r - rr) < 3 and abs(c - cc) < 3 for rr, cc in anchors):
            continue
        if rng.choice([False, True]):
            g[r][c] = 1
            g[r + 1][c + 1] = 1
        else:
            g[r][c + 1] = 1
            g[r + 1][c] = 1
        anchors.append((r, c))
    if not anchors:
        g[1][1] = 1
        g[2][2] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no diagonal pairs to expand into solid blocks
        return g
    if name == "full_2x2_filled":
        # 2x2 already solid blue → "exactly one diagonal" precondition fails
        for dr in range(2):
            for dc in range(2):
                g[1 + dr][1 + dc] = 1
        return g
    if name == "single_diagonal":
        # only one cell of pair → "diagonal pair" precondition fails
        g[1][1] = 1  # missing (2,2)
        g[4][5] = 1
        return g
    return g
