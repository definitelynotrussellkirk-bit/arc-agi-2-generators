"""Generator for arc_puzzle_bank_21_set13_bundle:medium_m06 — keep contents matching frame.

Rule: each rect-frame has interior cells. If any interior cell's color
differs from the frame color, all interior cells are erased to 0. If
all interior cells equal the frame color, they stay.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames (no rect-frames → rule has nothing to apply
the keep/erase decision to), all_match (every frame's interior == frame
color → rule keeps everything, no erase contrast), all_mismatch
(every frame has off-color interior → rule erases everything, no
keep contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4dd02f124024"
VERSION = "1.1.0"
TASK_ID = "4dd02f124024"
SUMMARY = "Two 5x5 rect-frames: one with same-color interior, one with off-color interior."

INVARIANTS = [
    "background is 0",
    "exactly two rect-frames in distinct colors",
    "one frame has interior cells in its OWN color (kept); the other has interior cells in a third color (erased)",
    "frames don't overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "all_match", "all_mismatch")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":            {"type": "int", "default": "rng 13..16", "valid": "10..18"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "two_frames_match_mismatch",
                          "valid": "two_frames_match_mismatch"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
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


def _stamp_frame(g, r1, c1, r2, c2, frame_color, inner_color, rng):
    for c in range(c1, c2 + 1):
        g[r1][c] = frame_color; g[r2][c] = frame_color
    for r in range(r1, r2 + 1):
        g[r][c1] = frame_color; g[r][c2] = frame_color
    inner = [(r, c) for r in range(r1 + 1, r2) for c in range(c1 + 1, c2)]
    n = rng.randint(1, max(1, len(inner) // 2))
    for r, c in rng.sample(inner, n):
        g[r][c] = inner_color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 15, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 13, 16)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    fc1, fc2, foreign = palette
    placed = []
    for _ in range(40):
        if len(placed) >= 2: break
        fh = rng.randint(4, 5)
        fw = rng.randint(4, 5)
        r1 = rng.randint(0, h - fh)
        c1 = rng.randint(0, w - fw)
        r2 = r1 + fh - 1
        c2 = c1 + fw - 1
        if _free(g, r1, c1, r2, c2):
            placed.append((r1, c1, r2, c2))
            if len(placed) == 1:
                _stamp_frame(g, r1, c1, r2, c2, fc1, fc1, rng)
            else:
                _stamp_frame(g, r1, c1, r2, c2, fc2, foreign, rng)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 14
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # No rect-frames — rule has nothing to apply keep/erase to.
        g[4][4] = 4
        g[5][5] = 6
        return g
    if name == "all_match":
        # Both frames have own-color interior — rule keeps both;
        # no erase contrast.
        for c in range(1, 5): g[1][c] = 4; g[4][c] = 4
        for r in range(1, 5): g[r][1] = 4; g[r][4] = 4
        g[2][2] = 4; g[3][3] = 4
        for c in range(8, 12): g[5][c] = 6; g[8][c] = 6
        for r in range(5, 9): g[r][8] = 6; g[r][11] = 6
        g[6][9] = 6; g[7][10] = 6
        return g
    if name == "all_mismatch":
        # Both frames have off-color interior — rule erases both;
        # no keep contrast.
        for c in range(1, 5): g[1][c] = 4; g[4][c] = 4
        for r in range(1, 5): g[r][1] = 4; g[r][4] = 4
        g[2][2] = 8; g[3][3] = 8
        for c in range(8, 12): g[5][c] = 6; g[8][c] = 6
        for r in range(5, 9): g[r][8] = 6; g[r][11] = 6
        g[6][9] = 8; g[7][10] = 8
        return g
    return g
