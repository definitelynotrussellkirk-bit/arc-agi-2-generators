"""Generator for arc_puzzle_bank_21_set18_s:S18_M1 — component-wise horizontal closure.

Rule: each blob → fill its bbox (every cell in [r1..r2]×[c1..c2])
with 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, single_cell_blob, all_solid_rects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "28c998e193d9"
VERSION = "1.1.0"
TASK_ID = "28c998e193d9"
SUMMARY = "2-3 hollow rect-frames in same color (color 2) — output fills each bbox to 8s."

INVARIANTS = [
    "background is 0",
    "each blob is a hollow rect-frame in color 2",
    "frames don't 4-touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "single_cell_blob", "all_solid_rects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "hollow_color2_frames",
                       "valid": "hollow_color2_frames"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 11, 12)
        n = ctx.draw_int("n_frames", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 13, 14)
        n = ctx.draw_int("n_frames", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 11, 14)
        n = ctx.draw_int("n_frames", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for _ in range(n):
        for _ in range(40):
            fh = rng.randint(3, 4); fw = rng.randint(3, 4)
            r1 = rng.randint(0, h - fh)
            c1 = rng.randint(0, w - fw)
            r2 = r1 + fh - 1; c2 = c1 + fw - 1
            if _free(g, r1, c1, r2, c2):
                for c in range(c1, c2 + 1):
                    g[r1][c] = 2; g[r2][c] = 2
                for r in range(r1, r2 + 1):
                    g[r][c1] = 2; g[r][c2] = 2
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # blank → no bboxes to fill, identity
        return g
    if name == "single_cell_blob":
        # single cells → bbox is 1x1, "fill" is identity-recolor
        g[2][2] = 2
        g[5][7] = 2
        return g
    if name == "all_solid_rects":
        # solid rects (no hollow interior) → bbox-fill is identity recolor of color
        for r in range(1, 4):
            for c in range(1, 4):
                g[r][c] = 2
        for r in range(4, 7):
            for c in range(7, 11):
                g[r][c] = 2
        return g
    return g
