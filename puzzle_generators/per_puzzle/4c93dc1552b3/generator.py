"""Generator for arc_additional_puzzle_bank_volume19:E127.

Corners of filled blue rectangles are recolored red.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rectangles,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rectangles, hollow_rects, length_one_rects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "4c93dc1552b3"
VERSION = "1.1.0"
TASK_ID = "4c93dc1552b3"
SUMMARY = "Corners of filled blue rectangles are recolored red."

INVARIANTS = [
    "background is 0",
    "each blue object is a solid filled rectangle",
    "rectangles are at least 2x2 so corners are well-defined",
    "rectangles are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rectangles", "hollow_rects", "length_one_rects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..14", "valid": "4..22"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "4..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rectangles":   {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "separated_solid_rects",
                       "valid": "separated_solid_rects"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n_rectangles = ctx.draw_int("n_rectangles", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 12, 14)
        n_rectangles = ctx.draw_int("n_rectangles", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 14)
        w = ctx.draw_int("grid_w", 9, 14)
        n_rectangles = ctx.draw_int("n_rectangles", 1, 3)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    boxes: list[tuple[int, int, int, int]] = []
    for _ in range(220):
        if len(boxes) >= n_rectangles:
            break
        rh = rng.randint(2, min(5, h))
        rw = rng.randint(2, min(5, w))
        r = rng.randint(0, h - rh)
        c = rng.randint(0, w - rw)
        if any(not (r + rh < ar - 1 or ar + ah < r - 1 or c + rw < ac - 1 or ac + aw < c - 1)
               for ar, ac, ah, aw in boxes):
            continue
        draw_rect(g, r, c, rh, rw, 1)
        boxes.append((r, c, rh, rw))
    if not boxes:
        draw_rect(g, 1, 1, 3, 3, 1)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_rectangles":
        # blank → no rectangles to recolor corners of
        return g
    if name == "hollow_rects":
        # frame outlines (not solid) → "filled rectangle" precondition fails
        for r, c in [(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2), (3, 3)]:
            g[r][c] = 1
        return g
    if name == "length_one_rects":
        # 1-cell or 1xN/Nx1 rectangles → corners not well-defined (1x1 trivially all corner)
        g[2][2] = 1
        for c in range(5, 9): g[5][c] = 1
        return g
    return g
