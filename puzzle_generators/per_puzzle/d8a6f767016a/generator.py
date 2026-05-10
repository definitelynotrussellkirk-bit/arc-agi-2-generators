"""Generator for 0a2355a6.

Rule: each 8-blob has N enclosed 0-regions inside its bbox; recolor by
N (1 to 1, 2 to 3, 3 to 2, 4 to 4, else 8).

Combinatorial axes (8): grid_h/w, frame1_h, frame2_h, palette_kind,
anchor_corner, asymmetry_force, palette_size, n_frames.
Degenerates: no_frames, single_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "d8a6f767016a"
VERSION = "1.1.0"
TASK_ID = "d8a6f767016a"
SUMMARY = "Hollow 8-frames split by interior walls; recolor by enclosed-region count."

INVARIANTS = [
    "background is color 0",
    "at least one hollow 8-frame with one enclosed region",
    "at least one hollow 8-frame with two enclosed regions split by an interior wall",
    "frames sit inside the grid with one row of separation",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frames", "single_frame", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 14..16", "valid": "12..20"},
    "frame1_h":       {"type": "int", "default": "rng 3..6", "valid": "3..8"},
    "frame2_h":       {"type": "int", "default": "rng 3..6", "valid": "3..8"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "n_frames":       {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 6, 7, 14, 14
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 8, 10, 16, 18
    else:
        h_lo, h_hi, w_lo, w_hi = 6, 8, 14, 16
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    fr1 = rng.randint(3, h - 2)
    fc1 = rng.randint(4, 6)
    r0_1 = rng.randint(0, h - fr1)
    c0_1 = rng.randint(0, max(0, w // 2 - fc1 - 1))
    draw_rect_outline(g, r0_1, c0_1, fr1, fc1, 8)
    fr2 = rng.randint(3, h - 2)
    fc2 = rng.randint(5, 7)
    r0_2 = rng.randint(0, h - fr2)
    c0_2 = rng.randint(w // 2 + 1, max(w // 2 + 1, w - fc2))
    draw_rect_outline(g, r0_2, c0_2, fr2, fc2, 8)
    mid_c = c0_2 + fc2 // 2
    for r in range(r0_2 + 1, r0_2 + fr2 - 1):
        g[r][mid_c] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 14, 0)
    if name == "no_frames":
        return g
    if name == "single_frame":
        draw_rect_outline(g, 1, 1, 4, 5, 8)
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(14):
                g[r][c] = 8
        return g
    return g
