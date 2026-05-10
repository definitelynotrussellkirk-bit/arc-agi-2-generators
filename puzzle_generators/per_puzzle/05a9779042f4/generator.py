"""Generator for arc_puzzle_bank_fifth_21_bundle:easy_35_hollow_solid_rectangles.

Rule: solid rectangles of color 6 are hollowed by erasing their interiors.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rects, hollow_rects, wrong_color_rects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "05a9779042f4"
VERSION = "1.1.0"
TASK_ID = "05a9779042f4"
SUMMARY = "Solid 6-rectangles are hollowed by erasing their interiors."

INVARIANTS = [
    "background is 0",
    "there is at least one solid rectangle of color 6",
    "each 6-rectangle has nonempty interior",
    "optional distractors are not color 6",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rects", "hollow_rects", "wrong_color_rects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "6..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "spaced_solid_rects",
                       "valid": "spaced_solid_rects"},
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
        w = ctx.draw_int("grid_w", 10, 11)
        n_rects = ctx.draw_int("n_rects", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
        n_rects = ctx.draw_int("n_rects", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 10, 14)
        n_rects = ctx.draw_int("n_rects", 2, 3)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    occupied: list[tuple[int, int, int, int]] = []
    for _ in range(n_rects):
        for _try in range(80):
            rh = rng.randint(3, 4)
            rw = rng.randint(3, 5)
            rr = rng.randint(0, h - rh)
            rc = rng.randint(0, w - rw)
            bb = (rr, rc, rr + rh - 1, rc + rw - 1)
            if any(not (bb[2] + 1 < ob[0] or ob[2] + 1 < bb[0]
                        or bb[3] + 1 < ob[1] or ob[3] + 1 < bb[1])
                   for ob in occupied):
                continue
            draw_rect(g, rr, rc, rh, rw, 6)
            occupied.append(bb)
            break
    if occupied:
        g[h - 1][0] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_rects":
        # blank → no rectangles to hollow, rule has no effect
        return g
    if name == "hollow_rects":
        # already hollow → rule's interior-erase is a no-op
        for c in range(3): g[1][1 + c] = 6; g[3][1 + c] = 6
        for r in range(3): g[1 + r][1] = 6; g[1 + r][3] = 6
        return g
    if name == "wrong_color_rects":
        # solid rectangles of color 4, not 6 → rule's color predicate fails
        for r in range(3):
            for c in range(4): g[1 + r][1 + c] = 4
        for r in range(3):
            for c in range(4): g[5 + r][6 + c] = 8
        return g
    return g
