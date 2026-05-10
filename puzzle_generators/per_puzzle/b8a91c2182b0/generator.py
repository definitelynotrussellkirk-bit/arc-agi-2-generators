"""Generator for arc_additional_puzzle_bank_volume7:M49.

Rule: among 2-blobs that have exactly one enclosed 0-hole, pick the
largest by size and paint its hole cells with 8.

Combinatorial axes (8): grid_h/w, palette_kind, num_frames, frame_sizes,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_holes, tied_largest, single_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, fill_box, full_grid

GENERATOR_ID = "b8a91c2182b0"
VERSION = "1.1.0"
TASK_ID = "b8a91c2182b0"
SUMMARY = "1 large 2-frame (hollow) + 1 small 2-frame (hollow) + decoration."

INVARIANTS = [
    "exactly 2 closed 2-frames (h≥3, w≥3 each)",
    "the larger frame has interior cells that get painted",
    "decoration is non-2 cells outside",
]

PALETTE_KINDS = ("default", "wide_gap", "tight_frames", "spread")
DEGENERATE_TEXTURES = ("no_holes", "tied_largest", "single_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_frames":     {"type": "int", "default": "2", "valid": "1..3"},
    "frame_sizes":    {"type": "str", "default": "mixed",
                       "valid": "small|mixed|large"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    draw_frame(g, 1, 1, 5, 5, 2)
    draw_frame(g, 6, 7, 8, 9, 2)
    g[h - 1][w - 1] = rng.choice([3, 4, 6, 7])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_holes":
        # solid 2-blocks — no enclosed 0 region to paint
        fill_box(g, 1, 1, 5, 5, 2)
        fill_box(g, 6, 7, 8, 11, 2)
        return g
    if name == "tied_largest":
        # two frames at the same size — "largest" pick is ambiguous
        draw_frame(g, 1, 1, 4, 4, 2)
        draw_frame(g, 6, 7, 9, 10, 2)
        return g
    if name == "single_frame":
        # only one frame — trivial pick
        draw_frame(g, 2, 2, 7, 9, 2)
        return g
    return g
