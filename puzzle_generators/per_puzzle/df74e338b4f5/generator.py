"""Generator for arc_additional_puzzles_21_set12_bundle:H81 — recolor by nesting depth.

Rule: detect rectangular color-9 frames; for each non-{0,9} marker cell, count
how many frame interiors contain it and replace the marker with that depth.
Frames are unchanged.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "df74e338b4f5"
VERSION = "1.1.0"
TASK_ID = "df74e338b4f5"

SUMMARY = "Several nested rectangular 9-frames; marker cells at various depths get recolored to depth."

INVARIANTS = [
    "background is 0",
    "3-5 concentric/nested rectangular color-9 frames; each is a hollow border",
    "every frame has interior strictly inside the previous; gap between frames is 1 cell",
    "at least one non-{0,9} marker cell with a non-trivial depth count",
    "markers are placed in valid 0-cells (not on a frame)",
]

AXES = {
    "grid_h": {"type": "int", "default": "rng 11..14", "valid": "10..18"},
    "grid_w": {"type": "int", "default": "rng 13..16", "valid": "11..18"},
    "n_frames": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    h = ctx.draw_int("grid_h", 11, 14)
    w = ctx.draw_int("grid_w", 13, 16)
    n_frames = ctx.draw_int("n_frames", 3, 4)
    rng = ctx.draw_rng("layout")
    # cap n_frames to fit available space
    max_frames = (min(h, w) - 3) // 2 + 1
    n_frames = min(n_frames, max_frames)

    for outer in range(40):
        g = full_grid(h, w, 0)
        r1, c1, r2, c2 = 0, 0, h - 1, w - 1
        drawn = 0
        for fi in range(n_frames):
            if r2 - r1 < 2 or c2 - c1 < 2:
                break
            draw_frame(g, r1, c1, r2, c2, 9)
            drawn += 1
            r1 += 2; c1 += 2; r2 -= 2; c2 -= 2
        if drawn < 2:
            continue

        # place markers at random in 0-cells; choose 3-6 markers in non-frame, non-9 positions
        marker_color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
        n_markers = rng.randint(3, 6)
        zero_positions = [(r, c) for r in range(h) for c in range(w) if g[r][c] == 0]
        if len(zero_positions) < n_markers:
            continue
        chosen = rng.sample(zero_positions, n_markers)
        for r, c in chosen:
            g[r][c] = marker_color
        return g
    raise ValueError("could not realize nested-frame layout in 40 attempts")
