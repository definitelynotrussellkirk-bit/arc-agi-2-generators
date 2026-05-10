"""Generator for arc_puzzle_bank_seventh_21_bundle:easy_46_crop_frame_contents.

Combinatorial axes (8): grid_h, grid_w, palette_kind, density,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, empty_interior, multiple_frames.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f69240d923b2"
VERSION = "1.1.0"
TASK_ID = "f69240d923b2"

SUMMARY = "A unique cyan frame contains the crop that should be returned."

INVARIANTS = [
    "background is 0",
    "frame color is 8",
    "there is exactly one rectangular 8 frame",
    "interior cells use non-8 colors or background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "empty_interior", "multiple_frames")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "5..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "density_pct":    {"type": "int", "default": "rng 35..60", "valid": "5..95"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8..8"},
    "position_bias":  {"type": "str", "default": "single_8frame_with_interior",
                       "valid": "single_8frame_with_interior"},
    "n_distinct_colors": {"type": "int", "default": "8", "valid": "8..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 10)
        density = ctx.draw_int("density", 35, 45)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
        density = ctx.draw_int("density", 50, 60)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 13)
        density = ctx.draw_int("density", 35, 60)
    ih = min(ctx.draw_int("inner_h", 3, 6), h - 2)
    iw = min(ctx.draw_int("inner_w", 3, 6), w - 2)
    rng = ctx.draw_rng("layout")
    fh = ih + 2
    fw = iw + 2
    r0 = rng.randint(0, h - fh)
    c0 = rng.randint(0, w - fw)
    r1 = r0 + fh - 1
    c1 = c0 + fw - 1
    g = full_grid(h, w, 0)
    for c in range(c0, c1 + 1):
        g[r0][c] = 8
        g[r1][c] = 8
    for r in range(r0, r1 + 1):
        g[r][c0] = 8
        g[r][c1] = 8
    colors = [1, 2, 3, 4, 5, 6, 7, 9]
    for r in range(r0 + 1, r1):
        for c in range(c0 + 1, c1):
            if rng.randrange(100) < density:
                g[r][c] = rng.choice(colors)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # interior content but no 8-frame → no cyan frame to crop
        for r in range(2, 5):
            for c in range(2, 6):
                g[r][c] = 4
        return g
    if name == "empty_interior":
        # 8-frame but empty interior → trivial crop, no contrast
        for c in range(2, 8): g[2][c] = 8; g[7][c] = 8
        for r in range(2, 8): g[r][2] = 8; g[r][7] = 8
        return g
    if name == "multiple_frames":
        # 2 separate 8-frames → "exactly one" precondition fails
        for c in range(1, 5): g[1][c] = 8; g[4][c] = 8
        for r in range(1, 5): g[r][1] = 8; g[r][4] = 8
        for c in range(6, 10): g[1][c] = 8; g[4][c] = 8
        for r in range(1, 5): g[r][6] = 8; g[r][9] = 8
        return g
    return g
