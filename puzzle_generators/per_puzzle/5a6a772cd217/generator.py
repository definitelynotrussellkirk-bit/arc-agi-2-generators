"""Generator for arc_puzzle_bank_21_set18_bundle:medium_p07 — frame interior gallery.

Rule: extract the interior of each 5-rect-outline frame; place
interiors side-by-side in their grid order with separators, padded to
common height.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, empty_interior, single_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5a6a772cd217"
VERSION = "1.1.0"
TASK_ID = "5a6a772cd217"
SUMMARY = "Two 5-frames side-by-side (different sizes), each with its own non-5 interior pattern."

INVARIANTS = [
    "background is 0",
    "two 5-rect-outlines, both at least 4x4 with non-empty interiors",
    "each interior contains a small distinct-color blob",
    "frames don't overlap (1-cell padding)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "empty_interior", "single_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "12..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "two_5frames_with_dots",
                       "valid": "two_5frames_with_dots"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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


def _stamp_frame_with_dot(g, r1, c1, r2, c2, frame_color, dot_color, rng):
    for c in range(c1, c2 + 1):
        g[r1][c] = frame_color; g[r2][c] = frame_color
    for r in range(r1, r2 + 1):
        g[r][c1] = frame_color; g[r][c2] = frame_color
    inner = [(r, c) for r in range(r1 + 1, r2) for c in range(c1 + 1, c2)]
    n = rng.randint(1, max(1, len(inner) // 2))
    for r, c in rng.sample(inner, n):
        g[r][c] = dot_color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 14, 15)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 17, 21)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 14, 18)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 2)
    for color in palette:
        for _ in range(40):
            fh = rng.randint(4, 5); fw = rng.randint(4, 5)
            r1 = rng.randint(0, h - fh)
            c1 = rng.randint(0, w - fw)
            r2 = r1 + fh - 1; c2 = c1 + fw - 1
            if _free(g, r1, c1, r2, c2):
                _stamp_frame_with_dot(g, r1, c1, r2, c2, 5, color, rng)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 16
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # Loose dots but no 5-frames — rule's "extract interior"
        # has no frames; output is empty gallery.
        g[3][4] = 4; g[5][10] = 6
        return g
    if name == "empty_interior":
        # Two 5-frames with no interior dots — interiors are
        # all-zero; rule's gallery has no content to display.
        for c in range(1, 6): g[1][c] = 5; g[5][c] = 5
        for r in range(1, 6): g[r][1] = 5; g[r][5] = 5
        for c in range(8, 13): g[1][c] = 5; g[5][c] = 5
        for r in range(1, 6): g[r][8] = 5; g[r][12] = 5
        return g
    if name == "single_frame":
        # Only one 5-frame — rule's "side-by-side" gallery
        # collapses to a single panel; padding never applies.
        for c in range(1, 6): g[1][c] = 5; g[5][c] = 5
        for r in range(1, 6): g[r][1] = 5; g[r][5] = 5
        g[3][3] = 4
        return g
    return g
