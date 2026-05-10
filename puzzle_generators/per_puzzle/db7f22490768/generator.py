"""Generator for arc_puzzle_bank_eleventh_21_bundle:easy_75_fill_hollow_rectangles.

Rule: each hollow rectangle has its interior filled with the frame color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_rectangles, only_2x2, open_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "db7f22490768"
VERSION = "1.1.0"
TASK_ID = "db7f22490768"

SUMMARY = "Draw separated hollow monochrome rectangles whose interiors get filled."

INVARIANTS = [
    "background is 0",
    "objects are hollow rectangular frames",
    "frame interiors are initially zero",
    "frames are separated from each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rectangles", "only_2x2", "open_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..18"},
    "rectangles":     {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "scattered_hollow_rects",
                       "valid": "scattered_hollow_rects"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
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


def _draw_frame(g, r1, c1, r2, c2, color):
    for r in range(r1, r2 + 1):
        g[r][c1] = color
        g[r][c2] = color
    for c in range(c1, c2 + 1):
        g[r1][c] = color
        g[r2][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("rectangles", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 15)
        w = ctx.draw_int("grid_w", 13, 17)
        target = ctx.draw_int("rectangles", 3, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 13)
        target = ctx.draw_int("rectangles", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(400):
        if placed >= target:
            break
        rh = rng.randint(3, min(5, h))
        rw = rng.randint(3, min(6, w))
        r1 = rng.randint(0, h - rh)
        c1 = rng.randint(0, w - rw)
        r2 = r1 + rh - 1
        c2 = c1 + rw - 1
        if not _free(g, r1, c1, r2, c2):
            continue
        _draw_frame(g, r1, c1, r2, c2, rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]))
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_rectangles":
        # Empty grid — rule has no frames to fill.
        return g
    if name == "only_2x2":
        # 2x2 frames — rule's "interior" is empty (zero cells);
        # rule's fill branch never paints anything.
        for r in range(2, 4):
            for c in range(2, 4): g[r][c] = 4
        for r in range(6, 8):
            for c in range(7, 9): g[r][c] = 6
        return g
    if name == "open_frame":
        # Three sides of a rectangle (one wall missing) — rule's
        # "hollow rectangle" filter excludes; output equals input.
        for c in range(2, 7): g[2][c] = 4
        for r in range(2, 6): g[r][2] = 4
        for r in range(2, 6): g[r][6] = 4
        return g
    return g
