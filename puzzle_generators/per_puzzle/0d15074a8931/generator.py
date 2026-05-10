"""Generator for arc_puzzle_bank_fourteenth_21_bundle:easy_96_keep_centers_of_odd_rectangles.

Rule: solid odd-sized rectangles → only their geometric centers are
retained.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rectangles,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: even_dims, single_cell_rects, full_grid_rect.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0d15074a8931"
VERSION = "1.1.0"
TASK_ID = "0d15074a8931"
SUMMARY = "Place separated solid odd-sized rectangles whose centers are retained."

INVARIANTS = [
    "background is 0",
    "each object is a solid rectangle",
    "rectangle heights and widths are odd",
    "rectangles are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("even_dims", "single_cell_rects", "full_grid_rect")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rectangles":     {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_rects",
                       "valid": "spaced_rects"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        target = min(ctx.draw_int("rectangles", 2, 2), 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
        target = min(ctx.draw_int("rectangles", 3, 3), 9)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 13)
        target = min(ctx.draw_int("rectangles", 2, 3), 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], target)
    reserved: set[tuple[int, int]] = set()
    placed = 0
    sizes = [3, 5]
    for _ in range(500):
        if placed >= target:
            break
        rh = rng.choice([s for s in sizes if s <= h])
        rw = rng.choice([s for s in sizes if s <= w])
        r0 = rng.randint(0, h - rh)
        c0 = rng.randint(0, w - rw)
        guard = {
            (r, c)
            for r in range(max(0, r0 - 1), min(h, r0 + rh + 1))
            for c in range(max(0, c0 - 1), min(w, c0 + rw + 1))
        }
        if guard & reserved:
            continue
        color = colors[placed]
        for r in range(r0, r0 + rh):
            for c in range(c0, c0 + rw):
                g[r][c] = color
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 12
    g = full_grid(h, w, 0)
    if name == "even_dims":
        # rectangles with even h and even w → center is between cells, ambiguous
        for r in range(1, 5):
            for c in range(1, 5): g[r][c] = 4   # 4x4 (even)
        for r in range(7, 9):
            for c in range(7, 11): g[r][c] = 6   # 2x4 (both even)
        return g
    if name == "single_cell_rects":
        # 1x1 rects → "center" is the cell itself, rule is identity (no shrink visible)
        g[2][3] = 4; g[5][7] = 6; g[8][2] = 3
        return g
    if name == "full_grid_rect":
        # rectangle = entire grid → after rule, only center cell remains; rest blanked
        for r in range(h):
            for c in range(w):
                g[r][c] = 4
        return g
    return g
