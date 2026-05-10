"""Generator for arc_puzzle_bank_21_set9_s:S9_M6 — rectangle corners only.

Rule: replace each blob with its 4 bbox corners as 8-cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rects, all_2x2, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dca118da8b9f"
VERSION = "1.1.0"
TASK_ID = "dca118da8b9f"
SUMMARY = "2-3 distinct-color solid rect blobs (3x3 or 4x4)."

INVARIANTS = [
    "background is 0",
    "blobs are solid rectangles ≥ 3×3 (so the 4 corners are distinct cells)",
    "blobs don't overlap or 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rects", "all_2x2", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "solid_rects_3x3_4x4",
                       "valid": "solid_rects_3x3_4x4"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    if r1 < 0 or c1 < 0 or r2 >= h or c2 >= w:
        return False
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0:
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
        w = ctx.draw_int("grid_w", 10, 11)
        n = ctx.draw_int("n_rects", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        n = ctx.draw_int("n_rects", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 10, 13)
        n = ctx.draw_int("n_rects", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], n)
    for color in palette:
        for _ in range(40):
            rh = rng.randint(3, 4)
            rw = rng.randint(3, 4)
            r1 = rng.randint(0, h - rh)
            c1 = rng.randint(0, w - rw)
            r2 = r1 + rh - 1
            c2 = c1 + rw - 1
            if _free(g, r1, c1, r2, c2):
                for r in range(r1, r2 + 1):
                    for c in range(c1, c2 + 1):
                        g[r][c] = color
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_rects":
        # blank → no rectangles to extract corners from
        return g
    if name == "all_2x2":
        # 2x2 rects → 4 corners cover the whole rect, "corners only" is identity
        for r in range(2):
            for c in range(2):
                g[1 + r][1 + c] = 4
                g[5 + r][6 + c] = 6
        return g
    if name == "single_cell":
        # 1-cell "rects" → only 1 corner, can't extract 4 distinct corners
        g[2][2] = 4
        g[5][7] = 6
        return g
    return g
