"""Generator for arc_additional_puzzle_bank_volume19:M133 — Fill 5-frame interior with single marker color.

Rule: each closed 5-rect frame contains exactly one non-{0,5} marker
color inside; fill all 0-cells inside with that marker color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, empty_interior, multiple_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.grid import draw_rect_outline

GENERATOR_ID = "b07ab22c1245"
VERSION = "1.1.0"
TASK_ID = "b07ab22c1245"
SUMMARY = "2 closed 5-frames each containing one marker cell of a different color."

INVARIANTS = [
    "exactly 2 closed 5-frames, ≥4×4 each",
    "each frame's interior has exactly one marker cell of distinct non-{0,5} color",
    "frames don't overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "empty_interior", "multiple_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..12"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "two_5frames_with_marker",
                       "valid": "two_5frames_with_marker"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    fr = rng.randint(4, 5); fc = rng.randint(4, 5)
    draw_rect_outline(g, 1, 1, fr, fc, 5)
    palette = rng.sample([2, 3, 4, 6, 7, 8], 2)
    g[1 + rng.randint(1, fr - 2)][1 + rng.randint(1, fc - 2)] = palette[0]
    fr2 = rng.randint(4, 5); fc2 = rng.randint(4, 5)
    draw_rect_outline(g, h - fr2 - 1, w - fc2 - 1, fr2, fc2, 5)
    g[h - fr2 - 1 + rng.randint(1, fr2 - 2)][w - fc2 - 1 + rng.randint(1, fc2 - 2)] = palette[1]
    g[0][w - 1] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # markers without 5-frames → no boundary to fill within
        g[3][3] = 4
        g[6][9] = 6
        return g
    if name == "empty_interior":
        # 5-frames with no marker → "exactly one marker" precondition fails
        draw_rect_outline(g, 1, 1, 4, 4, 5)
        draw_rect_outline(g, 5, 7, 4, 4, 5)
        return g
    if name == "multiple_markers":
        # frame interior contains 2+ different colors → ambiguous fill color
        draw_rect_outline(g, 1, 1, 4, 4, 5)
        g[2][2] = 4
        g[3][3] = 6  # both inside same frame
        draw_rect_outline(g, 5, 7, 4, 4, 5)
        g[6][8] = 7
        return g
    return g
