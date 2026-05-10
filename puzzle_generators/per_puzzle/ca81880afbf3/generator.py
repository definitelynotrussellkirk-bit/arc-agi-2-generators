"""Generator for puzzle 44d8ac46.

Rule: for each 5-blob, check its bbox-interior 0-cells form a square.
If yes, fill those 0s with 2.

Combinatorial axes (8): grid_h/w, n_square, n_rect, square_size,
rect_h, rect_w, position_bias, anchor_corner.
Degenerates: only_squares, only_rects, no_frames.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "ca81880afbf3"
VERSION = "1.1.0"
TASK_ID = "ca81880afbf3"
SUMMARY = "5-frames; rule fills square holes with 2."

INVARIANTS = [
    "background is 0",
    ">=1 5-frame with square interior (gets filled with 2)",
    ">=1 5-frame with rectangular (non-square) interior (no fill)",
    "frames don't overlap",
]

POSITION_BIASES = ("scattered", "row_aligned", "col_aligned", "diagonal")
DEGENERATE_TEXTURES = ("only_squares", "only_rects", "no_frames")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..18"},
    "n_square":       {"type": "int", "default": "1", "valid": "1..2"},
    "n_rect":         {"type": "int", "default": "1", "valid": "1..2"},
    "square_size":    {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "rect_h":         {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "rect_w":         {"type": "int", "default": "rng 5..6", "valid": "4..7"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 8
    elif difficulty == "hard":
        h_lo, h_hi = 12, 16
    else:
        h_lo, h_hi = 7, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 4, h_hi + 4)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    n_square = int(overrides.get("n_square", 1))
    n_rect = int(overrides.get("n_rect", 1))
    n_square = max(1, min(2, n_square))
    n_rect = max(1, min(2, n_rect))
    side = int(overrides.get("square_size",
                             ctx.draw_int("square_size", 4, 5)))
    rh2 = int(overrides.get("rect_h",
                            ctx.draw_int("rect_h", 3, 4)))
    rw2 = int(overrides.get("rect_w",
                            ctx.draw_int("rect_w", 5, 6)))
    side = max(3, min(min(h - 1, w // 2 - 1), side))
    rh2 = max(3, min(h - 1, rh2))
    rw2 = max(rh2 + 1, min(w // 2, rw2))
    g = full_grid(h, w, 0)
    placed = []
    # Place squares first
    for _ in range(n_square):
        for _try in range(20):
            r0 = rng.randint(0, h - side - 1)
            c0 = rng.randint(0, w // 2 - side - 1)
            if any(_overlaps(r0, c0, side, side, p) for p in placed):
                continue
            draw_rect_outline(g, r0, c0, side, side, 5)
            placed.append((r0, c0, side, side))
            break
    # Place rects
    for _ in range(n_rect):
        for _try in range(20):
            r0 = rng.randint(0, h - rh2 - 1)
            c0 = rng.randint(w // 2 + 1, max(w // 2 + 1, w - rw2))
            if any(_overlaps(r0, c0, rh2, rw2, p) for p in placed):
                continue
            draw_rect_outline(g, r0, c0, rh2, rw2, 5)
            placed.append((r0, c0, rh2, rw2))
            break
    return g


def _overlaps(r0, c0, h, w, other):
    or0, oc0, oh, ow = other
    return not (r0 + h + 1 <= or0 or or0 + oh + 1 <= r0
                or c0 + w + 1 <= oc0 or oc0 + ow + 1 <= c0)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "only_squares":
        for r0, c0 in [(1, 1), (1, w - 6)]:
            if r0 + 4 <= h and c0 + 4 <= w:
                draw_rect_outline(g, r0, c0, 4, 4, 5)
        return g
    if name == "only_rects":
        for r0, c0 in [(1, 1), (1, w // 2 + 1)]:
            if r0 + 4 <= h and c0 + 5 <= w:
                draw_rect_outline(g, r0, c0, 3, 5, 5)
        return g
    if name == "no_frames":
        return g
    return g
