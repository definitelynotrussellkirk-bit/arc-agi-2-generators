"""Generator for 17b:m114 — fill matching border lines inside frame.

Rule: a 5-rectangular frame has paired non-5 markers on opposite
borders. Each pair draws a colored line through the frame's interior.

Combinatorial axes (8): frame_h, frame_w, palette_kind, n_v, n_h,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_pairs, mismatched_pairs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ffaca7acb482"
VERSION = "1.1.0"
TASK_ID = "ffaca7acb482"
SUMMARY = "5-frame with 1-3 vertical pairs (top+bottom) and 1-3 horizontal pairs (left+right)."

INVARIANTS = [
    "background is 0",
    "outer 5-rectangle frame, hollow",
    "1-3 vertical column-pairs: same non-5 color appears at frame top and bottom of same column",
    "1-3 horizontal row-pairs: same non-5 color appears at frame left and right of same row",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_pairs", "mismatched_pairs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "frame_h":        {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "frame_w":        {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_v":            {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "n_h":            {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "frame_with_paired_borders",
                       "valid": "frame_with_paired_borders"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "2..6"},
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
        fh = ctx.draw_int("frame_h", 7, 7)
        fw = ctx.draw_int("frame_w", 9, 9)
    elif difficulty == "hard":
        fh = ctx.draw_int("frame_h", 9, 11)
        fw = ctx.draw_int("frame_w", 11, 13)
    else:
        fh = ctx.draw_int("frame_h", 7, 9)
        fw = ctx.draw_int("frame_w", 9, 11)
    rng = ctx.draw_rng("layout")
    h = fh + 2; w = fw + 3
    g = full_grid(h, w, 0)
    r1, c1 = 1, 1
    r2, c2 = r1 + fh - 1, c1 + fw - 1
    for c in range(c1, c2 + 1): g[r1][c] = 5; g[r2][c] = 5
    for r in range(r1, r2 + 1): g[r][c1] = 5; g[r][c2] = 5
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 4)
    n_v = rng.randint(1, 3)
    v_cols = rng.sample(range(c1 + 1, c2), n_v)
    for color, c in zip(palette[:n_v], v_cols):
        g[r1][c] = color; g[r2][c] = color
    n_h = rng.randint(1, 3)
    h_rows = rng.sample(range(r1 + 1, r2), n_h)
    for color, r in zip(palette[n_v:], h_rows):
        g[r][c1] = color; g[r][c2] = color
    return g


def _draw_from_degenerate(name, rng):
    fh, fw = 7, 9
    h = fh + 2; w = fw + 3
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # No 5-frame at all — rule has no boundary to identify
        # paired markers on.
        g[2][3] = 4; g[6][7] = 6
        return g
    if name == "no_pairs":
        # Frame present but no markers on the borders — rule has
        # nothing to pair and connect.
        for c in range(1, fw + 1): g[1][c] = 5; g[fh][c] = 5
        for r in range(1, fh + 1): g[r][1] = 5; g[r][fw] = 5
        return g
    if name == "mismatched_pairs":
        # Markers exist but top and bottom (or left/right) are different
        # colors — rule's same-color pair never matches, so no line is drawn.
        for c in range(1, fw + 1): g[1][c] = 5; g[fh][c] = 5
        for r in range(1, fh + 1): g[r][1] = 5; g[r][fw] = 5
        g[1][3] = 4; g[fh][3] = 6
        g[3][1] = 7; g[3][fw] = 8
        return g
    return g
