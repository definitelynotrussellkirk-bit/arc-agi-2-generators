"""Generator for arc_additional_puzzle_bank_volume14:M93 — Fill 4-frame interior with (5 + count_of_2s_inside).

Rule: each closed 4-rect frame ≥4×4. Count cells of color 2 strictly
inside the frame; fill ALL interior cells (including the 2s) with
(5 + count): 6 for one 2, 7 for two, 8 for three.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, frame_no_markers, open_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "d68b3843203e"
VERSION = "1.1.0"
TASK_ID = "d68b3843203e"
SUMMARY = "2-3 closed 4-frames each holding 1..3 cells of color 2."

INVARIANTS = [
    "2-3 closed 4-frames, each ≥4×4",
    "each frame has 1..3 interior cells of color 2",
    "frames don't overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "frame_no_markers", "open_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..12"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "two_4frames_with_markers",
                       "valid": "two_4frames_with_markers"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    fr = 4; fc = 4
    draw_rect_outline(g, 1, 1, fr, fc, 4)
    cnt1 = rng.randint(1, 3)
    interior1 = [(r, c) for r in range(2, 1 + fr - 1) for c in range(2, 1 + fc - 1)]
    rng.shuffle(interior1)
    for (r, c) in interior1[:cnt1]:
        g[r][c] = 2
    fr2 = 4; fc2 = 4
    r0 = h - fr2 - 1; c0 = w - fc2 - 1
    draw_rect_outline(g, r0, c0, fr2, fc2, 4)
    cnt2 = rng.randint(1, 3)
    while cnt2 == cnt1:
        cnt2 = rng.randint(1, 3)
    interior2 = [(r, c) for r in range(r0 + 1, r0 + fr2 - 1) for c in range(c0 + 1, c0 + fc2 - 1)]
    rng.shuffle(interior2)
    for (r, c) in interior2[:cnt2]:
        g[r][c] = 2
    g[0][w - 1] = rng.choice([5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # color-2 markers but no enclosing 4-frame → no count region defined
        g[2][2] = 2; g[5][7] = 2; g[3][8] = 2
        g[0][w - 1] = 5
        return g
    if name == "frame_no_markers":
        # frames present but interior has no color-2 → count=0, undefined fill (5+0)
        draw_rect_outline(g, 1, 1, 4, 4, 4)
        draw_rect_outline(g, 4, 6, 4, 4, 4)
        g[0][w - 1] = 5
        return g
    if name == "open_frame":
        # broken frame (missing one side) → not closed, no interior to fill
        for c in range(1, 5): g[1][c] = 4
        for r in range(1, 5): g[r][1] = 4
        for c in range(1, 5): g[4][c] = 4
        # right side intentionally missing
        g[2][2] = 2; g[3][3] = 2
        g[0][w - 1] = 5
        return g
    return g
