"""Generator for arc_additional_puzzle_bank_volume9:E62.

Rule: solid blue 2x3 or 3x2 rectangles are recolored red.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rectangles,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rectangles, wrong_size, hollow_rects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "079abfdee401"
VERSION = "1.1.0"
TASK_ID = "079abfdee401"
SUMMARY = "Solid blue 2x3 or 3x2 rectangles are recolored red."

INVARIANTS = [
    "background is 0",
    "target blue components are solid rectangles with dimensions 2x3 or 3x2",
    "blue components are separated by background",
    "non-target blue distractors are not solid 2x3 or 3x2 rectangles",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rectangles", "wrong_size", "hollow_rects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "5..24"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rectangles":   {"type": "int", "default": "rng 2..4", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "spaced_2x3_rects",
                       "valid": "spaced_2x3_rects"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear(g, cells):
    h = len(g)
    w = len(g[0])
    for r, c in cells:
        if not (0 <= r < h and 0 <= c < w) or g[r][c] != 0:
            return False
        for rr in range(max(0, r - 1), min(h, r + 2)):
            for cc in range(max(0, c - 1), min(w, c + 2)):
                if g[rr][cc] == 1:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_rectangles = ctx.draw_int("n_rectangles", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
        n_rectangles = ctx.draw_int("n_rectangles", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_rectangles = ctx.draw_int("n_rectangles", 2, 4)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(300):
        if placed >= n_rectangles:
            break
        rh, rw = rng.choice([(2, 3), (3, 2)])
        r = rng.randint(0, h - rh)
        c = rng.randint(0, w - rw)
        cells = [(rr, cc) for rr in range(r, r + rh) for cc in range(c, c + rw)]
        if _clear(g, cells):
            for rr, cc in cells:
                g[rr][cc] = 1
            placed += 1
    if placed == 0:
        for r in range(1, 3):
            for c in range(1, 4):
                g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_rectangles":
        # blank → no rectangles to recolor
        return g
    if name == "wrong_size":
        # 2x2 and 2x4 rectangles → predicate "exact 2x3" fails
        for r in range(2):
            for c in range(2): g[1 + r][1 + c] = 1
        for r in range(2):
            for c in range(4): g[5 + r][4 + c] = 1
        return g
    if name == "hollow_rects":
        # 2x3 outline only (interior 0) → predicate "solid filled" fails
        for c in range(3): g[1][1 + c] = 1; g[3][1 + c] = 1
        for r in range(3): g[1 + r][1] = 1; g[1 + r][3] = 1
        return g
    return g
