"""Generator for arc_puzzle_bank_21_set2:S2_M2 — frame filled by inner dot.

Rule: each 5-rect-outline frame has exactly one non-bg cell inside it
(the dot). Output: fill the frame's interior with the dot's color
(the dot itself stays its color, frame stays 5).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_dot, multiple_dots.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f5d85347c2fe"
VERSION = "1.1.0"
TASK_ID = "f5d85347c2fe"
SUMMARY = "1-2 5-rect-outline frames, each with one non-5 inner dot."

INVARIANTS = [
    "background is 0",
    "frames are color-5 rectangle outlines (≥4×4)",
    "each frame's interior has exactly one non-5 cell (the dot)",
    "frames don't overlap each other (with 1-cell padding)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_dot", "multiple_dots")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "frames_with_inner_dot",
                       "valid": "frames_with_inner_dot"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _frame_free(g, r1, c1, r2, c2):
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
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 16)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 11, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(1, 2)
    dot_palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n)
    for color in dot_palette:
        for _ in range(40):
            fh = rng.randint(4, 5)
            fw = rng.randint(4, 5)
            r1 = rng.randint(0, h - fh)
            c1 = rng.randint(0, w - fw)
            r2 = r1 + fh - 1
            c2 = c1 + fw - 1
            if not _frame_free(g, r1, c1, r2, c2):
                continue
            for c in range(c1, c2 + 1):
                g[r1][c] = 5; g[r2][c] = 5
            for r in range(r1, r2 + 1):
                g[r][c1] = 5; g[r][c2] = 5
            dot_r = rng.randint(r1 + 1, r2 - 1)
            dot_c = rng.randint(c1 + 1, c2 - 1)
            g[dot_r][dot_c] = color
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # Loose dots but no 5-frame — rule's "fill frame interior"
        # has no frame to fill.
        g[3][3] = 4; g[7][7] = 6
        return g
    if name == "no_dot":
        # 5-frame but no inner dot — rule's "dot color → fill"
        # source is undefined.
        for c in range(2, 7): g[2][c] = 5; g[6][c] = 5
        for r in range(2, 7): g[r][2] = 5; g[r][6] = 5
        return g
    if name == "multiple_dots":
        # Two distinct-color dots inside one frame — rule's
        # "exactly one inner dot" precondition fails; fill color
        # ambiguous.
        for c in range(2, 7): g[2][c] = 5; g[6][c] = 5
        for r in range(2, 7): g[r][2] = 5; g[r][6] = 5
        g[3][4] = 6; g[5][5] = 7
        return g
    return g
