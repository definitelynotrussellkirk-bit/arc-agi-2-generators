"""Generator for arc_puzzle_bank_twentieth_21_bundle:easy_139_fill_hollow_rectangles.

Rule: hollow rectangular borders are filled into solid rectangles.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, frames, texture.
Degenerates: no_frames, all_solid, frame_open.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "43a7d8f7ab6c"
VERSION = "1.1.0"
TASK_ID = "43a7d8f7ab6c"

SUMMARY = "Hollow rectangular borders are filled into solid rectangles."

INVARIANTS = [
    "background is 0",
    "each component is a one-cell-thick rectangular frame",
    "frames have nonempty interiors",
    "frames are separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "all_solid", "frame_open")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "5..22"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "frames":         {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "= frames", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_frames",
                       "valid": "scattered_frames"},
    "n_distinct_colors": {"type": "int", "default": "= frames", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r0, c0, r1, c1):
    h, w = len(g), len(g[0])
    if r0 < 0 or c0 < 0 or r1 >= h or c1 >= w:
        return False
    for r in range(max(0, r0 - 1), min(h, r1 + 2)):
        for c in range(max(0, c0 - 1), min(w, c1 + 2)):
            if g[r][c] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("frames", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 16)
        w = ctx.draw_int("grid_w", 14, 18)
        target = ctx.draw_int("frames", 3, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 14)
        target = ctx.draw_int("frames", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(160):
        if placed >= target:
            break
        rh = rng.randint(3, min(5, h))
        rw = rng.randint(3, min(6, w))
        r0 = rng.randint(0, h - rh)
        c0 = rng.randint(0, w - rw)
        r1, c1 = r0 + rh - 1, c0 + rw - 1
        if not _free(g, r0, c0, r1, c1):
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for c in range(c0, c1 + 1):
            g[r0][c] = color
            g[r1][c] = color
        for r in range(r0, r1 + 1):
            g[r][c0] = color
            g[r][c1] = color
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # Empty grid — rule has no frames to fill.
        return g
    if name == "all_solid":
        # Shapes are already solid rectangles, not hollow frames —
        # rule's "fill the interior" is no-op.
        for r in range(2, 6):
            for c in range(3, 8): g[r][c] = 4
        return g
    if name == "frame_open":
        # Frame is broken (one side missing) — rule's "rectangular
        # frame" precondition fails; bbox interior is undefined.
        for c in range(2, 8): g[2][c] = 4
        for r in range(2, 6): g[r][2] = 4; g[r][7] = 4
        return g
    return g
