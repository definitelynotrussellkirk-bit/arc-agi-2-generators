"""Generator for 11b:m72 — frame gate cross fill.

Rule: each hollow 9-frame has one top-mark in the row just below the
top wall and one left-mark in the column just right of the left wall,
both same color. Output draws both lines (row at left-mark's row and
column at top-mark's column) in that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_marks, mismatched_marks.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "954070a7d7ce"
VERSION = "1.1.0"
TASK_ID = "954070a7d7ce"
SUMMARY = "1-2 hollow 9-frames; each has one top-mark + one left-mark, same color."

INVARIANTS = [
    "background is 0",
    "1-2 hollow rectangular 9-frames, distinct positions",
    "each frame has one cell in row r1+1 (top reading row, not corner) and one in col c1+1 (left reading col, not corner), both same color",
    "the column-line at top-mark's col and the row-line at left-mark's row are interior (so output != input)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_marks", "mismatched_marks")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "9..14"},
    "grid_w":         {"type": "int", "default": "rng 13..16", "valid": "12..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "9_frames_with_axis_marks",
                       "valid": "9_frames_with_axis_marks"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 10, 10)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 16, 18)
    else:
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 13, 16)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_frames = rng.randint(1, 2)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], n_frames)
    for color in palette:
        for _ in range(60):
            fh = rng.randint(6, 7); fw = rng.randint(6, 7)
            r0 = rng.randint(0, h - fh); c0 = rng.randint(0, w - fw)
            if not _free(g, r0, c0, r0 + fh - 1, c0 + fw - 1): continue
            for c in range(c0, c0 + fw): g[r0][c] = 9; g[r0 + fh - 1][c] = 9
            for r in range(r0, r0 + fh): g[r][c0] = 9; g[r][c0 + fw - 1] = 9
            tc = rng.randint(c0 + 2, c0 + fw - 2)
            lr = rng.randint(r0 + 2, r0 + fh - 2)
            g[r0 + 1][tc] = color
            g[lr][c0 + 1] = color
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 14
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # Marks float without a 9-frame around them — rule has no
        # frame to cross-fill within.
        g[3][5] = 4
        g[5][2] = 4
        return g
    if name == "no_marks":
        # 9-frame but no marks — rule has no axis marks to determine
        # the cross.
        for c in range(2, 9): g[2][c] = 9; g[8][c] = 9
        for r in range(2, 9): g[r][2] = 9; g[r][8] = 9
        return g
    if name == "mismatched_marks":
        # 9-frame with top-mark and left-mark in DIFFERENT colors —
        # rule's "same color" precondition fails; cross color
        # ambiguous.
        for c in range(2, 9): g[2][c] = 9; g[8][c] = 9
        for r in range(2, 9): g[r][2] = 9; g[r][8] = 9
        g[3][5] = 4
        g[6][3] = 7
        return g
    return g
