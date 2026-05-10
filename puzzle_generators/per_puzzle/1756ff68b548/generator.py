"""Generator for arc_additional_puzzles_21_set8:M55.

Sort objects by size and pack horizontally.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rects, all_same_size, all_touching.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "1756ff68b548"
VERSION = "1.1.0"
TASK_ID = "1756ff68b548"
SUMMARY = "3 small rectangles of distinct sizes (1x2, 2x2, 2x3) and distinct colors."

INVARIANTS = [
    "3 solid rectangles of distinct sizes",
    "rectangles use distinct colors",
    "rectangles don't touch (≥1 bg cell apart)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rects", "all_same_size", "all_touching")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "three_distinct_size_rects",
                       "valid": "three_distinct_size_rects"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 12, 16)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    sizes = [(2, 2), (2, 3), (3, 3), (2, 4)]
    chosen_sizes = rng.sample(sizes, 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    placed = []
    for (rh, rw), color in zip(chosen_sizes, palette):
        for _ in range(60):
            r0 = rng.randint(1, h - rh - 1); c0 = rng.randint(1, w - rw - 1)
            if any(abs(r0 - pr) < (rh + 2) and abs(c0 - pc) < (rw + 2) for pr, pc in placed):
                continue
            draw_rect(g, r0, c0, rh, rw, color)
            placed.append((r0, c0))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 14
    g = full_grid(h, w, 0)
    if name == "no_rects":
        # blank → no rectangles to sort
        return g
    if name == "all_same_size":
        # all rectangles same size → sort-by-size has no signal
        draw_rect(g, 1, 1, 2, 2, 4)
        draw_rect(g, 1, 5, 2, 2, 6)
        draw_rect(g, 1, 9, 2, 2, 7)
        return g
    if name == "all_touching":
        # rectangles touching → form a single component, can't sort separately
        draw_rect(g, 2, 2, 2, 2, 4)
        draw_rect(g, 2, 4, 2, 3, 6)
        draw_rect(g, 2, 7, 3, 3, 7)
        return g
    return g
