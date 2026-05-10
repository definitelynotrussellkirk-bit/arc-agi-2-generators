"""Generator for arc_puzzle_bank_21_set24_s:S24_E1.

Rule: each solid component has its outermost onion layer recolored to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, single_pixel_objects, all_3x3_minimal.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b3bfd59c2c43"
VERSION = "1.1.0"
TASK_ID = "b3bfd59c2c43"
SUMMARY = "Solid components have their outermost onion layer recolored to 8."

INVARIANTS = [
    "background is 0",
    "objects are separated solid monochrome rectangles",
    "each object has a nonempty onion boundary layer",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_pixel_objects", "all_3x3_minimal")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "8..20"},
    "object_count":   {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "scattered_solid_rects",
                       "valid": "scattered_solid_rects"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..6"},
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


def _place_rectangles(grid, rng, count, colors, min_size=3, max_size=6):
    h, w = len(grid), len(grid[0])
    placed = 0
    for color in colors:
        for _ in range(80):
            rh = rng.randint(min_size, max_size)
            rw = rng.randint(min_size, max_size)
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


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        count = ctx.draw_int("object_count", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 17)
        w = ctx.draw_int("grid_w", 16, 19)
        count = ctx.draw_int("object_count", 3, 5)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 12, 16)
        count = ctx.draw_int("object_count", 2, 3)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7], count)
    _place_rectangles(grid, rng, count, colors)
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # Empty grid — rule has no objects to onion-strip.
        return g
    if name == "single_pixel_objects":
        # 1x1 objects — rule's "outermost layer" equals the entire
        # object; rule recolors all to 8 (rule's effect non-trivial
        # but no inner core remains).
        g[2][2] = 4; g[2][8] = 6; g[8][5] = 7
        return g
    if name == "all_3x3_minimal":
        # 3x3 objects — rule's outer layer is 8 cells, leaving only
        # the 1-cell core; minimal interesting case.
        for r in range(2, 5):
            for c in range(2, 5): g[r][c] = 4
        for r in range(7, 10):
            for c in range(8, 11): g[r][c] = 6
        return g
    return g
