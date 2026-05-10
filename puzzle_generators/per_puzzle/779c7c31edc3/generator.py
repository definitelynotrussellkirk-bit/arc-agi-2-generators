"""Generator for arc_puzzle_bank_seventeenth_21_bundle:easy_118_turn_filled_rectangles_into_frames.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rectangles,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rects, all_2x2, already_outline.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "779c7c31edc3"
VERSION = "1.1.0"
TASK_ID = "779c7c31edc3"

SUMMARY = "Separated filled rectangles are reduced to their outer frames."

INVARIANTS = [
    "background is 0",
    "each object is a filled rectangle",
    "every rectangle has an interior cell",
    "rectangles are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rects", "all_2x2", "already_outline")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "6..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rectangles":     {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "filled_rects_to_frames",
                       "valid": "filled_rects_to_frames"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        target = ctx.draw_int("rectangles", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
        target = ctx.draw_int("rectangles", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 13)
        target = ctx.draw_int("rectangles", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(target, 9))
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        rh = rng.randint(3, 4)
        rw = rng.randint(3, 5)
        r0 = rng.randint(0, h - rh)
        c0 = rng.randint(0, w - rw)
        guard = {
            (r, c)
            for r in range(max(0, r0 - 1), min(h, r0 + rh + 1))
            for c in range(max(0, c0 - 1), min(w, c0 + rw + 1))
        }
        if guard & reserved:
            continue
        color = colors[placed % len(colors)]
        for r in range(r0, r0 + rh):
            for c in range(c0, c0 + rw):
                g[r][c] = color
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_rects":
        # blank → no rectangles to frame
        return g
    if name == "all_2x2":
        # 2x2 rects → border IS the entire rect, no interior to clear
        for r in range(2):
            for c in range(2):
                g[1 + r][1 + c] = 4
                g[5 + r][6 + c] = 6
        return g
    if name == "already_outline":
        # rects are already hollow frames → rule is identity
        for c in range(2, 6): g[2][c] = 3; g[5][c] = 3
        for r in range(2, 6): g[r][2] = 3; g[r][5] = 3
        return g
    return g
