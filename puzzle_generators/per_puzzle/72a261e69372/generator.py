"""Generator for arc_puzzle_bank_21_set3:S3_H5.

Rule: color-1 marker dots sit inside nested rectangular frames. Each
dot is recolored to the smallest frame that encloses it.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_groups,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, marker_outside, single_frame_only.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "72a261e69372"
VERSION = "1.1.0"
TASK_ID = "72a261e69372"
SUMMARY = "Nested colored frames enclose color-1 markers."

INVARIANTS = [
    "frames are rectangular outlines",
    "marker dots are color 1",
    "each marker is strictly inside at least one frame",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "marker_outside", "single_frame_only")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14..14"},
    "grid_w":         {"type": "int", "default": "18", "valid": "18..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_groups":       {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "nested":         {"type": "bool", "default": "rng", "valid": "true/false"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "3..7"},
    "position_bias":  {"type": "str", "default": "nested_frames_with_markers",
                       "valid": "nested_frames_with_markers"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "3..7"},
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
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        n_groups = ctx.draw_int("n_groups", 1, 1)
        nested = bool(ctx.draw_int("nested", 0, 0))
    elif difficulty == "hard":
        n_groups = ctx.draw_int("n_groups", 2, 2)
        nested = bool(ctx.draw_int("nested", 1, 1))
    else:
        n_groups = ctx.draw_int("n_groups", 1, 2)
        nested = bool(ctx.draw_int("nested", 0, 1))
    g = full_grid(14, 18, 0)
    colors = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], n_groups * 2)
    anchors = [(1, 1), (1, 10)]

    for i in range(n_groups):
        r0, c0 = anchors[i]
        outer = colors[2 * i]
        inner = colors[2 * i + 1]
        draw_frame(g, r0, c0, r0 + 10, c0 + 6, outer)
        if nested:
            draw_frame(g, r0 + 2, c0 + 2, r0 + 7, c0 + 5, inner)
            g[r0 + 4][c0 + 3] = 1
        else:
            g[r0 + 5][c0 + 3] = 1
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 18, 0)
    if name == "no_frames":
        # marker but no frames → no enclosing frame for the dot
        g[5][8] = 1
        return g
    if name == "marker_outside":
        # frame present but marker is outside → not inside any frame
        draw_frame(g, 2, 2, 8, 8, 4)
        g[10][12] = 1   # outside the frame
        return g
    if name == "single_frame_only":
        # only one frame (no nesting) → "smallest enclosing frame" is trivially the only frame
        draw_frame(g, 2, 2, 11, 8, 4)
        g[6][5] = 1
        return g
    return g
