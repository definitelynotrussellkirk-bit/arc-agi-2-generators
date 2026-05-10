"""Generator for arc_puzzle_bank_21_set24_s:S24_E5.

Combinatorial axes (8): grid_h, grid_w, palette_kind, object_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, single_layer, all_3x3.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d8a17b941eb9"
VERSION = "1.1.0"
TASK_ID = "d8a17b941eb9"
SUMMARY = "The second onion layer of each solid component is extracted as 8."

INVARIANTS = [
    "background is 0",
    "each component is at least 3 cells thick in both dimensions",
    "only depth-2 occupied cells survive",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_layer", "all_3x3")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "8..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "object_count":   {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..7"},
    "position_bias":  {"type": "str", "default": "thick_solid_rects",
                       "valid": "thick_solid_rects"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..7"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(grid, r0, c0, rh, rw):
    h, w = len(grid), len(grid[0])
    if r0 < 0 or c0 < 0 or r0 + rh > h or c0 + rw > w:
        return False
    for r in range(max(0, r0 - 1), min(h, r0 + rh + 1)):
        for c in range(max(0, c0 - 1), min(w, c0 + rw + 1)):
            if grid[r][c] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        count = ctx.draw_int("object_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 15, 16)
        count = ctx.draw_int("object_count", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 12, 16)
        count = ctx.draw_int("object_count", 2, 3)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7], count)
    placed = 0
    for color in colors:
        for _ in range(80):
            rh = rng.randint(4, 7)
            rw = rng.randint(4, 7)
            r0 = rng.randint(0, h - rh)
            c0 = rng.randint(0, w - rw)
            if not _free(grid, r0, c0, rh, rw):
                continue
            for r in range(r0, r0 + rh):
                for c in range(c0, c0 + rw):
                    grid[r][c] = color
            placed += 1
            break
        if placed >= count:
            break
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # blank → no objects → no second-layer extraction
        return g
    if name == "single_layer":
        # 2x2 rect → only outer layer, no depth-2 cells
        for r in range(2):
            for c in range(2): g[2 + r][2 + c] = 4
        return g
    if name == "all_3x3":
        # 3x3 rect → only 1 cell at depth 2 (center), trivial
        for r in range(3):
            for c in range(3): g[2 + r][2 + c] = 4
        return g
    return g
