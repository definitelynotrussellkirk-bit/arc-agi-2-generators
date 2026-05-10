"""Generator for arc_additional_puzzle_bank_volume16:E108.

Solid green rectangles have only their perimeters recolored cyan.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rectangles,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rects, all_2x2, hollow_outline.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "34f8510e39d0"
VERSION = "1.1.0"
TASK_ID = "34f8510e39d0"
SUMMARY = "Solid green rectangles have only their perimeters recolored cyan."

INVARIANTS = [
    "background is 0",
    "each green object is a solid axis-aligned rectangle",
    "rectangles are at least 3x3 so interiors remain green",
    "rectangles are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rects", "all_2x2", "hollow_outline")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..14", "valid": "5..22"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "5..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rectangles":   {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "solid_green_rectangles",
                       "valid": "solid_green_rectangles"},
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
        rh = rng.randint(3, min(5, h))
        rw = rng.randint(3, min(5, w))
        r = rng.randint(0, h - rh)
        c = rng.randint(0, w - rw)
        if any(not (r + rh < ar - 1 or ar + ah < r - 1 or c + rw < ac - 1 or ac + aw < c - 1)
               for ar, ac, ah, aw in boxes):
            continue
        for rr in range(r, r + rh):
            for cc in range(c, c + rw):
                g[rr][cc] = 3
        boxes.append((r, c, rh, rw))
    if not boxes:
        for rr in range(1, 4):
            for cc in range(1, 4):
                g[rr][cc] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_rects":
        # blank → no rectangles to outline
        return g
    if name == "all_2x2":
        # 2x2 rect → no interior, all cells are border, rule is identity
        for r in range(2):
            for c in range(2):
                g[2 + r][2 + c] = 3
        return g
    if name == "hollow_outline":
        # already-hollow outline → not solid, "solid" precondition fails
        for c in range(2, 7): g[2][c] = 3; g[6][c] = 3
        for r in range(2, 7): g[r][2] = 3; g[r][6] = 3
        return g
    return g
