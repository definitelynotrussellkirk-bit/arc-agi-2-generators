"""Generator for arc_puzzle_bank_21_set6:medium_f05.

Rule: keep innermost frame from a stack of nested rectangular frames.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, frame_gap, texture.
Degenerates: single_frame, touching_frames, no_innermost.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "a88fd33fba06"
VERSION = "1.1.0"
TASK_ID = "a88fd33fba06"
SUMMARY = "Nested rectangular frames where the deepest frame is unique."

INVARIANTS = [
    "background is 0",
    "all nonzero objects are rectangular outline frames",
    "frames are strictly nested with at least one blank gap",
    "the innermost frame is uniquely enclosed by all others",
]

PALETTE_KINDS = ("default", "warm_nest", "cool_nest", "varied_nest")
DEGENERATE_TEXTURES = ("single_frame", "touching_frames", "no_innermost")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 17..20", "valid": "17..22"},
    "grid_w":         {"type": "int", "default": "rng 17..21", "valid": "17..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "concentric", "valid": "concentric"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "frame_gap":      {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 17, 18)
        w = ctx.draw_int("grid_w", 17, 18)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 19, 20)
        w = ctx.draw_int("grid_w", 19, 21)
    else:
        h = ctx.draw_int("grid_h", 17, 20)
        w = ctx.draw_int("grid_w", 17, 21)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    for color, box in zip(colors, [(1, 1, h - 2, w - 2), (4, 4, h - 5, w - 5), (7, 7, h - 8, w - 8)]):
        if box[2] - box[0] < 2 or box[3] - box[1] < 2:
            raise ValueError("frame too small")
        draw_frame(g, *box, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 18, 18
    g = full_grid(h, w, 0)
    if name == "single_frame":
        # only one frame → "innermost" is trivial, no nesting structure
        draw_frame(g, 1, 1, h - 2, w - 2, 4)
        return g
    if name == "touching_frames":
        # frames share a row of cells → no blank gap, nesting predicate fails
        draw_frame(g, 1, 1, h - 2, w - 2, 4)
        draw_frame(g, 2, 2, h - 4, w - 4, 6)
        draw_frame(g, 3, 3, h - 6, w - 6, 7)
        return g
    if name == "no_innermost":
        # two side-by-side frames at same nesting depth → no unique innermost
        draw_frame(g, 1, 1, h - 2, w // 2 - 1, 4)
        draw_frame(g, 1, w // 2 + 1, h - 2, w // 2 - 2, 6)
        return g
    return g
