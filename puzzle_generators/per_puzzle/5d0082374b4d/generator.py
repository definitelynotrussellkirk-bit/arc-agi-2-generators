"""Generator for arc_additional_puzzles_21_set13_bundle:M87 — alternating-column fill of 1-frame interiors.

Rule: each 1-color rectangle frame has 2 marker cells at the top-row
interior corners (r1+1, c1+1) = a and (r1+1, c2-1) = b. Output keeps
the frames and fills each frame's interior with alternating columns:
columns offset 0, 2, 4, ... = a; offset 1, 3, ... = b.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_frames, texture.
Degenerates: no_frames, no_markers, single_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_frame
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "5d0082374b4d"
VERSION = "1.1.0"
TASK_ID = "5d0082374b4d"
SUMMARY = "2 1-color rectangle frames with 2 distinct marker colors at top-interior corners."

INVARIANTS = [
    "background is 0",
    "exactly 2 full-perimeter 1-color rectangle frames (≥4×4 each)",
    "each frame has 2 distinct non-1 marker colors at (r1+1, c1+1) and (r1+1, c2-1)",
    "frames don't touch each other (bbox padding ≥1)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frames", "no_markers", "single_marker")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "two_frames_with_corner_markers",
                       "valid": "two_frames_with_corner_markers"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 12, 12)
        n_frames = ctx.draw_int("n_frames", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 16, 19)
        n_frames = ctx.draw_int("n_frames", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 12, 16)
        n_frames = ctx.draw_int("n_frames", 2, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed: list[tuple[int, int, int, int]] = []
    for _ in range(80):
        if len(placed) >= n_frames: break
        rh = rng.randint(4, 6)
        rw = rng.randint(4, 6)
        r1 = rng.randint(0, h - rh)
        c1 = rng.randint(0, w - rw)
        r2 = r1 + rh - 1
        c2 = c1 + rw - 1
        bb_pad = (r1 - 1, c1 - 1, r2 + 1, c2 + 1)
        if any(bbox_overlaps(bb_pad, (p[0]-1, p[1]-1, p[2]+1, p[3]+1)) for p in placed):
            continue
        placed.append((r1, c1, r2, c2))
    for r1, c1, r2, c2 in placed:
        draw_frame(g, r1, c1, r2, c2, 1)
        a, b = rng.sample(list(random_palette(rng, 4, exclude={1})), 2)
        g[r1 + 1][c1 + 1] = a
        g[r1 + 1][c2 - 1] = b
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 14
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # Markers floating without frames — rule's frame-finder finds
        # no rectangles to fill.
        g[2][2] = 4; g[2][8] = 6
        return g
    if name == "no_markers":
        # 1-frame present but interior corners are empty — rule has
        # no a/b colors to alternate; interior fill is undefined.
        draw_frame(g, 1, 1, 6, 8, 1)
        return g
    if name == "single_marker":
        # 1-frame with only one corner marker — rule's a/b alternation
        # has only one column color; rule's effect collapses to solid
        # fill.
        draw_frame(g, 1, 1, 6, 8, 1)
        g[2][2] = 4
        return g
    return g
