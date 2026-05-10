"""Generator for arc_puzzle_bank_eleventh21:E77.

Rule: fill diagonal segments between matching-color endpoints.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_endpoint, axis_aligned_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2c83e8cd1c07"
VERSION = "1.1.0"
TASK_ID = "2c83e8cd1c07"

SUMMARY = "Fill diagonal segments between matching-color endpoints."

INVARIANTS = [
    "background is 0",
    "each active color appears as two endpoints on a perfect diagonal",
    "interior diagonal cells are initially zero",
    "segments are separated to avoid overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_endpoint", "axis_aligned_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "segments":       {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "diagonal_endpoint_pairs",
                       "valid": "diagonal_endpoint_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _path(r1, c1, r2, c2):
    dr = 1 if r2 > r1 else -1
    dc = 1 if c2 > c1 else -1
    return [(r1 + i * dr, c1 + i * dc) for i in range(abs(r2 - r1) + 1)]


def _free(g, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        for rr in range(max(0, r - 1), min(h, r + 2)):
            for cc in range(max(0, c - 1), min(w, c + 2)):
                if g[rr][cc] != 0:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("segments", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 10, 14)
        target = ctx.draw_int("segments", 3, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("segments", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], target)
    placed = 0
    for color in colors:
        for _ in range(160):
            length = rng.randint(2, min(5, h - 1, w - 1))
            dr = rng.choice([-1, 1])
            dc = rng.choice([-1, 1])
            r1 = rng.randint(0 if dr > 0 else length, h - 1 - length if dr > 0 else h - 1)
            c1 = rng.randint(0 if dc > 0 else length, w - 1 - length if dc > 0 else w - 1)
            r2, c2 = r1 + dr * length, c1 + dc * length
            cells = _path(r1, c1, r2, c2)
            if _free(g, cells):
                g[r1][c1] = color
                g[r2][c2] = color
                placed += 1
                break
    if placed == 0:
        raise ValueError("could not place diagonal segment")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule has no diagonal endpoint pairs.
        return g
    if name == "single_endpoint":
        # Color appears once — rule's "endpoint pair" precondition
        # fails; segment undefined.
        g[2][2] = 4
        return g
    if name == "axis_aligned_pair":
        # Two same-color endpoints on a row (not diagonal) —
        # rule's "perfect diagonal" filter excludes.
        g[3][2] = 4; g[3][6] = 4
        return g
    return g
