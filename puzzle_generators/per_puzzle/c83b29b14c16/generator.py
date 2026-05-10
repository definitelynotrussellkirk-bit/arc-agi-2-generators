"""Generator for arc_additional_puzzles_21_set11_bundle:E71 — Connect same-color pairs in row or col.

Rule: for each color with exactly 2 cells, if both are in same row or
col, fill the line between them with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, no_shared_axis, adjacent_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c83b29b14c16"
VERSION = "1.1.0"
TASK_ID = "c83b29b14c16"
SUMMARY = "1-3 colors, each with 2 cells in a shared row OR shared col, ≥3 apart."

INVARIANTS = [
    "1-3 distinct colors",
    "each color: 2 cells in same row OR same col",
    "the 2 cells are ≥3 apart so the connector is non-trivial",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "no_shared_axis", "adjacent_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "shared_axis_pairs",
                       "valid": "shared_axis_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
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
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 10, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_pairs = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_pairs)
    occupied = [[False] * w for _ in range(h)]
    for color in palette:
        for _ in range(40):
            horiz = rng.choice([True, False])
            if horiz:
                r = rng.randint(0, h - 1)
                c0 = rng.randint(0, w - 4)
                c1 = rng.randint(c0 + 3, w - 1)
                cells = [(r, c) for c in range(c0, c1 + 1)]
            else:
                c = rng.randint(0, w - 1)
                r0 = rng.randint(0, h - 4)
                r1 = rng.randint(r0 + 3, h - 1)
                cells = [(r, c) for r in range(r0, r1 + 1)]
            if any(occupied[rr][cc] for rr, cc in cells):
                continue
            for rr, cc in cells:
                occupied[rr][cc] = True
            g[cells[0][0]][cells[0][1]] = color
            g[cells[-1][0]][cells[-1][1]] = color
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule has no pair to bridge.
        return g
    if name == "no_shared_axis":
        # Same color appears twice but on different rows AND cols —
        # rule's "in-row OR in-col" gate doesn't fire.
        g[1][2] = 4; g[5][6] = 4
        return g
    if name == "adjacent_pair":
        # Pair shares an axis but is adjacent — rule's "fill between"
        # produces zero filler cells.
        g[3][2] = 4; g[3][3] = 4
        return g
    return g
