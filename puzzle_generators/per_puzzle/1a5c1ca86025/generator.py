"""Generator for v2_meta_puzzles:E5 — fill bbox interior of each object.

Rule: for each connected component, fill the interior of its bbox
(cells strictly inside the rectangle) with the object's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: solid_rects, single_cells, line_rects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "1a5c1ca86025"
VERSION = "1.1.0"
TASK_ID = "1a5c1ca86025"
SUMMARY = "1-2 hollow rectangles in distinct colors."

INVARIANTS = [
    "background is 0",
    "1-2 hollow rectangles in distinct colors (≥4×4 each)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("solid_rects", "single_cells", "line_rects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "hollow_rects",
                       "valid": "hollow_rects"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w: return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0: return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        n = 1
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        n = 2
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
        n = ctx.draw_int("n_rects", 1, 2)
    rng = ctx.draw_rng("layout")

    for outer in range(40):
        g = full_grid(h, w, 0)
        colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
        ok = True
        for color in colors:
            placed = False
            for _ in range(80):
                fh = rng.choice([4, 5]); fw = rng.choice([4, 5])
                r0 = rng.randint(0, h - fh); c0 = rng.randint(0, w - fw)
                if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
                draw_frame(g, r0, c0, r0 + fh - 1, c0 + fw - 1, color)
                placed = True; break
            if not placed:
                ok = False; break
        if ok:
            return g
    raise ValueError("could not realize E5 layout")


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "solid_rects":
        # already-solid rectangles → bbox interior is already filled, rule is identity
        for r in range(1, 5):
            for c in range(1, 5):
                g[r][c] = 4
        return g
    if name == "single_cells":
        # objects are 1x1 → bbox has no interior, rule fills nothing
        g[2][2] = 4; g[5][7] = 6; g[7][3] = 3
        return g
    if name == "line_rects":
        # objects are 1×N or N×1 lines → bbox is degenerate (no interior strictly inside)
        for c in range(1, 6): g[2][c] = 4   # 1x5
        for r in range(4, 8): g[r][7] = 6   # 4x1
        return g
    return g
