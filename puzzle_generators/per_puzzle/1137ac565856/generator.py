"""Generator for additional_bank:H5 — smallest enclosing frame crop.

Rule: nested rectangular frames enclose a red marker; output is cropped
to the smallest enclosing (innermost) frame.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frames, marker_outside, single_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "1137ac565856"
VERSION = "1.1.0"
TASK_ID = "1137ac565856"
SUMMARY = "Nested rectangular frames enclose a red marker; the smallest enclosing frame wins."

INVARIANTS = [
    "background is 0",
    "there are nested rectangular frames in distinct non-red colors",
    "the red marker is strictly inside every frame",
    "the innermost frame is at least 5x5",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "marker_outside", "single_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 15..17", "valid": "15..20"},
    "grid_w":         {"type": "int", "default": "rng 15..18", "valid": "15..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "nested_concentric",
                       "valid": "nested_concentric"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..4"},
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
        h = ctx.draw_int("grid_h", 15, 16)
        w = ctx.draw_int("grid_w", 15, 16)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 16, 17)
        w = ctx.draw_int("grid_w", 17, 18)
    else:
        h = ctx.draw_int("grid_h", 15, 17)
        w = ctx.draw_int("grid_w", 15, 18)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 3, 4, 5, 6, 7, 8, 9], 3)
    boxes = [
        (1, 1, h - 2, w - 2),
        (3, 3, h - 4, w - 4),
        (5, 5, h - 6, w - 6),
    ]
    if boxes[-1][2] - boxes[-1][0] < 4 or boxes[-1][3] - boxes[-1][1] < 4:
        raise ValueError("grid too small for nested frames")
    for color, box in zip(colors, boxes):
        draw_frame(g, *box, color)
    r1, c1, r2, c2 = boxes[-1]
    g[rng.randint(r1 + 2, r2 - 2)][rng.randint(c1 + 2, c2 - 2)] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 16, 16
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # marker exists but no frames → no enclosing frame to find
        g[7][7] = 2
        return g
    if name == "marker_outside":
        # frames present but red marker outside all of them → "smallest enclosing" undefined
        draw_frame(g, 1, 1, h - 2, w - 2, 4)
        draw_frame(g, 3, 3, h - 4, w - 4, 6)
        g[0][0] = 2  # outside even the outer frame
        return g
    if name == "single_frame":
        # only one frame → "smallest enclosing" = the only frame, trivial answer
        draw_frame(g, 2, 2, h - 3, w - 3, 4)
        g[7][7] = 2
        return g
    return g
