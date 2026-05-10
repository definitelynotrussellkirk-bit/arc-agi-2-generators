"""Generator for arc_puzzle_bank_21_more:medium_b06 — Crop quadrant by corner marker.

Rule: body = grid[1..h-2, 1..w-2]. Find which corner of grid has a
non-zero cell. Crop body's matching quadrant (TL/TR/BL/BR).

Combinatorial axes (8): grid_h, grid_w, palette_kind, corner,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, multiple_corners, blank_body.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6d86d867b40b"
VERSION = "1.1.0"
TASK_ID = "6d86d867b40b"
SUMMARY = "Frame-padded grid: corner marker at one of 4 corners + multicolor body inside."

INVARIANTS = [
    "exactly one corner cell (h corner) is non-zero",
    "border (rows/cols 0 and h-1, w-1) is zero except corner",
    "body has even h and w (so quadrants are equal)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "multiple_corners", "blank_body")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "corner":         {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8..8"},
    "position_bias":  {"type": "str", "default": "frame_with_corner",
                       "valid": "frame_with_corner"},
    "n_distinct_colors": {"type": "int", "default": "8", "valid": "8..8"},
    "density":        {"type": "str", "default": "dense", "valid": "dense"},
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
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 6, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 6, 8)
    if h % 2 != 0: h += 1
    if w % 2 != 0: w += 1
    corner_idx = ctx.draw_int("corner", 0, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    corners = [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]
    cr, cc = corners[corner_idx]
    g[cr][cc] = 9
    bh = h - 2; bw = w - 2
    counter = 1
    for r in range(bh):
        for c in range(bw):
            g[1 + r][1 + c] = (counter % 8) + 1
            counter += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 6
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # body present but no corner marker → rule can't pick a quadrant
        for r in range(h - 2):
            for c in range(w - 2):
                g[1 + r][1 + c] = ((r * (w - 2) + c) % 8) + 1
        return g
    if name == "multiple_corners":
        # multiple corner markers → ambiguous quadrant choice
        g[0][0] = 9
        g[h - 1][w - 1] = 9
        for r in range(h - 2):
            for c in range(w - 2):
                g[1 + r][1 + c] = ((r * (w - 2) + c) % 8) + 1
        return g
    if name == "blank_body":
        # marker but body is all zeros → cropped quadrant is blank
        g[0][0] = 9
        return g
    return g
