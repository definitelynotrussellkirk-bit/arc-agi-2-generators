"""Generator for arc_additional_puzzles_21_set10_bundle:M67 — Fill target-color frame interiors.

Rule: target = g[0][0]. Each blob of target color that's a perfect
frame → fill its interior with target.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_target, no_frames, broken_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "d0496e8fd941"
VERSION = "1.1.0"
TASK_ID = "d0496e8fd941"
SUMMARY = "Marker color at (0,0) + 1-2 frame-shapes of same color elsewhere."

INVARIANTS = [
    "(0,0) holds non-bg target color",
    "≥1 hollow rect-frame of target color, ≥3×3, NOT including (0,0)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_target", "no_frames", "broken_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "1", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "marker_at_origin_with_frame",
                       "valid": "marker_at_origin_with_frame"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    target = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    g[0][0] = target
    # Frame
    fr = rng.randint(3, 4); fc = rng.randint(4, 5)
    r0 = rng.randint(2, h - fr - 1); c0 = rng.randint(2, w - fc - 1)
    draw_rect_outline(g, r0, c0, fr, fc, target)
    # Distractor (smaller frame won't fill if not closed)
    g[h - 2][w - 2] = rng.choice([c for c in range(1, 10) if c != target])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_target":
        # (0,0) is 0 → no target color, rule has no scope
        draw_rect_outline(g, 2, 2, 3, 5, 4)
        return g
    if name == "no_frames":
        # target color at (0,0) but no frame of that color → rule has nothing to fill
        g[0][0] = 4
        g[3][3] = 6   # decoy of different color
        return g
    if name == "broken_frame":
        # frame has a missing edge → not closed, "perfect frame" precondition fails
        g[0][0] = 4
        draw_rect_outline(g, 2, 2, 3, 5, 4)
        g[2][4] = 0   # gap in top edge
        return g
    return g
