"""Generator for arc_additional_puzzle_bank_volume14:E94 — Blue rings get cyan centers.

Rule: hollow blue 3×3 frames have their center cells filled cyan.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, solid_squares, centers_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect_outline, full_grid

GENERATOR_ID = "db2bc2b4fec6"
VERSION = "1.1.0"
TASK_ID = "db2bc2b4fec6"
SUMMARY = "Hollow blue 3x3 frames have their center cells filled cyan."

INVARIANTS = [
    "background is 0",
    "targets are exact hollow 3x3 blue frames",
    "center cells are empty before the rule runs",
    "frames are separated so their 3x3 windows do not overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "solid_squares", "centers_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "5..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "spaced_3x3_blue_rings",
                       "valid": "spaced_3x3_blue_rings"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_frames = ctx.draw_int("n_frames", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
        n_frames = ctx.draw_int("n_frames", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
        n_frames = ctx.draw_int("n_frames", 2, 4)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    anchors: list[tuple[int, int]] = []
    for _ in range(200):
        if len(anchors) >= n_frames:
            break
        r = rng.randint(0, h - 3)
        c = rng.randint(0, w - 3)
        if any(abs(r - rr) < 4 and abs(c - cc) < 4 for rr, cc in anchors):
            continue
        draw_rect_outline(g, r, c, 3, 3, 1)
        anchors.append((r, c))
    if not anchors:
        draw_rect_outline(g, 1, 1, 3, 3, 1)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # blank → no frames to fill
        return g
    if name == "solid_squares":
        # solid 3x3 blue squares → no center to fill
        for r in range(3):
            for c in range(3): g[1 + r][1 + c] = 1
        for r in range(3):
            for c in range(3): g[5 + r][5 + c] = 1
        return g
    if name == "centers_already_filled":
        # 3x3 blue ring with center already non-bg → fill precondition fails
        draw_rect_outline(g, 1, 1, 3, 3, 1)
        g[2][2] = 8
        draw_rect_outline(g, 5, 5, 3, 3, 1)
        g[6][6] = 6
        return g
    return g
