"""Generator for arc_puzzle_bank_fourth_21_bundle:easy_27_recolor_exact_2x3_rectangles.

Rule: each exact solid 2x3 or 3x2 color-2 rectangle is recolored to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_exact_rects, wrong_size_rects, hollow_rects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "4e7a80731133"
VERSION = "1.1.0"
TASK_ID = "4e7a80731133"
SUMMARY = "Exact solid 2x3 or 3x2 color-2 rectangles are recolored to 8."

INVARIANTS = [
    "background is 0",
    "at least one color-2 object is an exact 2x3 or 3x2 rectangle",
    "rectangles do not touch",
    "some optional color-2 distractors are not exact 2x3 rectangles",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_exact_rects", "wrong_size_rects", "hollow_rects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "spaced_2x3_rects",
                       "valid": "spaced_2x3_rects"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
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
        w = ctx.draw_int("grid_w", 9, 10)
        n_rects = ctx.draw_int("n_rects", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
        n_rects = ctx.draw_int("n_rects", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 13)
        n_rects = ctx.draw_int("n_rects", 2, 3)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    occupied: list[tuple[int, int, int, int]] = []
    for _ in range(n_rects):
        for _try in range(100):
            rh, rw = rng.choice([(2, 3), (3, 2)])
            rr = rng.randint(0, h - rh)
            rc = rng.randint(0, w - rw)
            bb = (rr, rc, rr + rh - 1, rc + rw - 1)
            if any(not (bb[2] + 1 < ob[0] or ob[2] + 1 < bb[0]
                        or bb[3] + 1 < ob[1] or ob[3] + 1 < bb[1])
                   for ob in occupied):
                continue
            draw_rect(g, rr, rc, rh, rw, 2)
            occupied.append(bb)
            break
    if occupied and h > 1:
        g[h - 1][0] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_exact_rects":
        # only color-2 distractors, no exact rectangles → rule fires zero times
        g[1][1] = 2; g[2][3] = 2; g[5][6] = 2
        return g
    if name == "wrong_size_rects":
        # 2x2 and 2x4 rectangles → predicate "exact 2x3" fails
        for r in range(2):
            for c in range(2): g[1 + r][1 + c] = 2
        for r in range(2):
            for c in range(4): g[5 + r][4 + c] = 2
        return g
    if name == "hollow_rects":
        # 2x3 outline only (interior 0) → predicate "solid filled" fails
        for c in range(3): g[1][1 + c] = 2; g[3][1 + c] = 2
        for r in range(3): g[1 + r][1] = 2; g[1 + r][3] = 2
        return g
    return g
