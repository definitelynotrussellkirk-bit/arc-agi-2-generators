"""Generator for arc_additional_puzzles_21_set16_bundle:M106 — A:B::C:? transform analogy.

Rule: split input by blank columns into 3 framed panels (5-frame).
Find the transform code that maps A's interior to B's interior, then
apply it to C's interior. Output is C transformed.

Combinatorial axes (8): interior_size, n_marks, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_panels, identity_transform, mismatched_transform.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import (
    full_grid, fill_box, transpose, rot90_cw, rot180, flip_lr, flip_ud, cmirror,
)

GENERATOR_ID = "85782e8a5dc9"
VERSION = "1.1.0"
TASK_ID = "85782e8a5dc9"
SUMMARY = "3 5-framed panels separated by blank cols: A, B=T(A), C, where T is one of 8 transforms."

INVARIANTS = [
    "exactly 3 panels separated by blank columns",
    "each panel is a full 5-color rectangle frame with a small interior pattern",
    "panel B's interior = some transform T applied to A's interior",
    "panel C's interior is unrelated; output is C transformed by the same T",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_panels", "identity_transform", "mismatched_transform")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "interior_size":  {"type": "int", "default": "rng 3..4", "valid": "3..6"},
    "n_marks":        {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "5", "valid": "4..6"},
    "position_bias":  {"type": "str", "default": "three_panels_blankcol_sep",
                       "valid": "three_panels_blankcol_sep"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "4..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_CODES = [1, 2, 3, 4, 5, 6, 8]


def _apply(grid, code):
    if code == 1: return [row[:] for row in grid]
    if code == 2: return rot90_cw(grid)
    if code == 3: return rot180(grid)
    if code == 4: return transpose(grid)
    if code == 5: return flip_lr(grid)
    if code == 6: return flip_ud(grid)
    if code == 8: return cmirror(grid)
    return [row[:] for row in grid]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        isize = ctx.draw_int("interior_size", 3, 3)
        n_marks = ctx.draw_int("n_marks", 3, 4)
    elif difficulty == "hard":
        isize = ctx.draw_int("interior_size", 4, 5)
        n_marks = ctx.draw_int("n_marks", 6, 9)
    else:
        isize = ctx.draw_int("interior_size", 3, 4)
        n_marks = ctx.draw_int("n_marks", 4, 6)
    rng = ctx.draw_rng("layout")
    panel_size = isize + 2
    h = panel_size
    w = panel_size * 3 + 2
    g = full_grid(h, w, 0)
    code = rng.choice(_CODES)

    def _make_pattern():
        pat = [[0] * isize for _ in range(isize)]
        cells = [(r, c) for r in range(isize) for c in range(isize)]
        rng.shuffle(cells)
        for r, c in cells[:n_marks]:
            pat[r][c] = rng.choice([1, 2, 3, 4])
        return pat

    pattern_a = _make_pattern()
    pattern_b = _apply(pattern_a, code)
    pattern_c = _make_pattern()

    for idx, pat in enumerate([pattern_a, pattern_b, pattern_c]):
        c0 = idx * (panel_size + 1)
        c1 = c0 + panel_size - 1
        for c in range(c0, c1 + 1):
            g[0][c] = 5
            g[panel_size - 1][c] = 5
        for r in range(panel_size):
            g[r][c0] = 5
            g[r][c1] = 5
        for ir in range(isize):
            for ic in range(isize):
                g[1 + ir][c0 + 1 + ic] = pat[ir][ic]
    return g


def _draw_from_degenerate(name, rng):
    isize = 3
    panel_size = isize + 2
    w = panel_size * 3 + 2
    h = panel_size
    g = full_grid(h, w, 0)
    if name == "no_panels":
        # No panels at all — rule has nothing to read.
        return g
    if name == "identity_transform":
        # B = A, C = anything — rule applies identity, output = C unchanged.
        for idx in range(3):
            c0 = idx * (panel_size + 1); c1 = c0 + panel_size - 1
            for c in range(c0, c1 + 1):
                g[0][c] = 5; g[panel_size - 1][c] = 5
            for r in range(panel_size):
                g[r][c0] = 5; g[r][c1] = 5
        # A and B identical, C different
        g[1][1] = 1; g[1][2] = 2; g[2][1] = 3
        g[1][6] = 1; g[1][7] = 2; g[2][6] = 3
        g[1][11] = 4; g[2][12] = 1
        return g
    if name == "mismatched_transform":
        # B is not any pure transform of A — rule cannot infer T uniquely.
        for idx in range(3):
            c0 = idx * (panel_size + 1); c1 = c0 + panel_size - 1
            for c in range(c0, c1 + 1):
                g[0][c] = 5; g[panel_size - 1][c] = 5
            for r in range(panel_size):
                g[r][c0] = 5; g[r][c1] = 5
        g[1][1] = 1; g[2][2] = 2
        g[1][7] = 3; g[2][6] = 4
        g[1][11] = 1
        return g
    return g
