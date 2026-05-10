"""Generator for arc_additional_puzzle_bank_volume15:E101 — fill missing rect cell.

Rule: each filled green rectangle missing exactly one interior cell has
that cell filled cyan.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rectangles,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rectangles, complete_rect, missing_on_border.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7e9fd4cf84a9"
VERSION = "1.1.0"
TASK_ID = "7e9fd4cf84a9"
SUMMARY = "Filled green rectangles with one missing cell have that cell filled cyan."

INVARIANTS = [
    "background is 0",
    "each green component is a filled rectangle missing exactly one interior cell",
    "missing cells are not on the rectangle border",
    "rectangles are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rectangles", "complete_rect", "missing_on_border")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..14", "valid": "5..22"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "5..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rectangles":   {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1 (green)", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "scattered_holed_rects",
                       "valid": "scattered_holed_rects"},
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
        h = ctx.draw_int("grid_h", 14, 18)
        w = ctx.draw_int("grid_w", 14, 18)
        n_rectangles = ctx.draw_int("n_rectangles", 3, 5)
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
        mr = rng.randint(r + 1, r + rh - 2)
        mc = rng.randint(c + 1, c + rw - 2)
        g[mr][mc] = 0
        boxes.append((r, c, rh, rw))
    if not boxes:
        for rr in range(1, 4):
            for cc in range(1, 4):
                g[rr][cc] = 3
        g[2][2] = 0
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 12
    g = full_grid(h, w, 0)
    if name == "no_rectangles":
        # Empty grid — no rectangle to repair.
        return g
    if name == "complete_rect":
        # Filled rectangle with no missing cell — rule has no hole to fill.
        for r in range(2, 6):
            for c in range(2, 6):
                g[r][c] = 3
        return g
    if name == "missing_on_border":
        # Rectangle missing a cell on its border (not interior) — rule's
        # interior-hole filter never matches it.
        for r in range(2, 6):
            for c in range(2, 6):
                g[r][c] = 3
        g[2][3] = 0
        return g
    return g
