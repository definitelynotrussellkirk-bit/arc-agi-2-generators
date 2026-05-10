"""Generator for 11b:m76 — recover rectangle from 3 corners.

Rule: each color has 3 of 4 corner cells of a rectangle. Output draws
the full rect-outline by inferring the 4th corner from the 3 given.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rects, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_corners, complete_rect, mixed_rect.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4b57f748d763"
VERSION = "1.1.0"
TASK_ID = "4b57f748d763"
SUMMARY = "1-2 colors each with 3 of 4 rectangle corners marked."

INVARIANTS = [
    "background is 0",
    "each non-zero color has exactly 3 cells at 3 of 4 axis-aligned rect corners",
    "rectangles don't overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_corners", "complete_rect", "mixed_rect")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "scattered_corners",
                       "valid": "scattered_corners"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..3"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(1, 2)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    reserved: set[tuple[int, int]] = set()
    for color in palette:
        for _ in range(40):
            r1 = rng.randint(0, h - 4)
            c1 = rng.randint(0, w - 4)
            r2 = rng.randint(r1 + 3, min(h - 1, r1 + 5))
            c2 = rng.randint(c1 + 3, min(w - 1, c1 + 5))
            cells = {(r, c) for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)}
            if cells & reserved:
                continue
            corners = [(r1, c1), (r1, c2), (r2, c1), (r2, c2)]
            missing = rng.choice(corners)
            for corner in corners:
                if corner != missing:
                    g[corner[0]][corner[1]] = color
            reserved |= cells
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_corners":
        # Empty grid — no rectangle to recover.
        return g
    if name == "complete_rect":
        # All 4 corners of a rectangle present — rule has nothing to add.
        for r, c in [(1, 1), (1, 5), (5, 1), (5, 5)]:
            g[r][c] = 4
        return g
    if name == "mixed_rect":
        # 3 corners but they're not axis-aligned (form a triangle, not a
        # rectangle) — rule's 4th-corner inference has no consistent answer.
        for r, c in [(1, 1), (3, 5), (5, 2)]:
            g[r][c] = 6
        return g
    return g
