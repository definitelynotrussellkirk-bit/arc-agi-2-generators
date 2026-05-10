"""Generator for arc_puzzle_bank_seventh_21_bundle:easy_48_component_centers.

Rule: same-color components collapse to their bounding-box centers.

Combinatorial axes (8): grid_h, grid_w, palette_kind, components,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_singletons, single_component, components_overlap_centers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "82b36c453029"
VERSION = "1.1.0"
TASK_ID = "82b36c453029"
SUMMARY = "Separated same-color components collapse to their bounding-box centers."

INVARIANTS = [
    "background is 0",
    "components are 4-connected same-color rectangles",
    "components are separated by background",
    "each component has area greater than one",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_singletons", "single_component", "components_overlap_centers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "components":     {"type": "int", "default": "rng 3..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_rects",
                       "valid": "scattered_rects"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r0, c0, rh, rw):
    h, w = len(g), len(g[0])
    for r in range(max(0, r0 - 1), min(h, r0 + rh + 1)):
        for c in range(max(0, c0 - 1), min(w, c0 + rw + 1)):
            if g[r][c] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 11)
        target = ctx.draw_int("components", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        target = ctx.draw_int("components", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 13)
        target = ctx.draw_int("components", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(500):
        if placed >= target:
            break
        rh = rng.randint(1, 3)
        rw = rng.randint(2, 4) if rh == 1 else rng.randint(1, 4)
        if rh * rw <= 1:
            continue
        r0 = rng.randint(0, h - rh)
        c0 = rng.randint(0, w - rw)
        if not _free(g, r0, c0, rh, rw):
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for r in range(r0, r0 + rh):
            for c in range(c0, c0 + rw):
                g[r][c] = color
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "all_singletons":
        # area=1 components → "collapse to bbox center" is identity (already a single cell)
        g[2][3] = 4; g[5][7] = 6; g[7][2] = 3; g[3][9] = 8
        return g
    if name == "single_component":
        # one large rect → output has just one center cell, no comparison across components
        for r in range(2, 5):
            for c in range(3, 7):
                g[r][c] = 6
        return g
    if name == "components_overlap_centers":
        # two rects whose bbox centers happen to collide (different parities) → output drops one
        # rect A at (1..2, 1..3), bbox center (1, 2)
        for r in range(1, 3):
            for c in range(1, 4):
                g[r][c] = 4
        # rect B at (5..7, 1..3), bbox center (6, 2) — distinct, but visually centers stack vertically
        for r in range(5, 8):
            for c in range(1, 4):
                g[r][c] = 6
        return g
    return g
