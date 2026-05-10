"""Generator for arc_puzzle_bank_twentieth21:M135 — extract interior of 8-frame.

Rule: there is exactly one 8-color rectangle frame; output is the
strict interior crop (preserving any non-8 markers inside).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, frame_no_interior, multiple_frames.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_frame
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "eee19c538953"
VERSION = "1.1.0"
TASK_ID = "eee19c538953"
SUMMARY = "1 8-color rect frame with 2-3 distinct-color markers in its strict interior."

INVARIANTS = [
    "background is 0",
    "exactly one 8-color rectangle frame (>=5x5 so interior is non-trivial)",
    "2-3 markers in the strict interior in distinct non-0/non-8 colors",
    "no non-bg cells outside the frame",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "frame_no_interior", "multiple_frames")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_markers":      {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "interior", "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..5"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rh = rng.randint(5, h - 1)
    rw = rng.randint(5, w - 1)
    r1 = rng.randint(0, h - rh)
    c1 = rng.randint(0, w - rw)
    r2 = r1 + rh - 1
    c2 = c1 + rw - 1
    draw_frame(g, r1, c1, r2, c2, 8)
    interior = [(r, c) for r in range(r1 + 1, r2) for c in range(c1 + 1, c2)]
    rng.shuffle(interior)
    n_markers = rng.randint(2, min(3, len(interior)))
    palette = list(random_palette(rng, n_markers, exclude={8}))
    for (r, c), color in zip(interior[:n_markers], palette):
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # no 8-frame → rule has no anchor for cropping
        for r, c, v in [(2, 3, 4), (3, 5, 6), (5, 6, 7)]:
            g[r][c] = v
        return g
    if name == "frame_no_interior":
        # frame is 3x3 → strict interior is 1x1, rule still works but trivial
        draw_frame(g, 2, 2, 4, 4, 8)
        return g
    if name == "multiple_frames":
        # two separate 8-frames → ambiguous which one to crop to
        draw_frame(g, 0, 0, 3, 3, 8)
        g[1][1] = 4
        draw_frame(g, 4, 4, 8, 8, 8)
        g[5][5] = 6
        g[6][6] = 7
        return g
    return g
